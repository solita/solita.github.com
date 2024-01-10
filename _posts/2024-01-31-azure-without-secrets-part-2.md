---
layout: post
title: Using Azure without secrets, Part 2
author: mattipulkkinen
excerpt: Utilizing managed identities when authenticating to a resource in Azure instead of a secret value.
tags:
 - Azure
 - Secrets
 - Managed identity
 - Role-based access control
---

In the [first part](https://dev.solita.fi/2024/01/12/azure-without-secrets-part-1.html) I described how to use Azure CLI in GitHub Actions workflow runs or more generally in CI/CD pipeline runs. However, that leaves us with plenty of secrets (passwords, client secrets and certificates) because we still need to authenticate to database servers, to blob storages and such. Authenticating to those without secrets requires different approach, namely managed identities and role-based access control (RBAC).

In this post I'll demonstrate how to enable system-assigned managed identity for Azure App Service and then utilize it in three different examples. The examples demonstrate reading blob data from Azure Storage account, accessing Azure SQL Database and authenticating Azure Functions to Service Bus for queue trigger. In the samples I'll be using .NET 8 (C#), [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview?tabs=bicep) and [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/what-is-azure-cli).

The necessary steps for each of the examples are quite similar; enable managed identity, grant access rights and change the code to utilize identity-based connection. As an additional step, I will also show how to disable key-based authentication, because identity-based authentication/authorization is more secure and recommended by Microsoft (sources: [Storage account](https://learn.microsoft.com/en-us/azure/storage/blobs/authorize-access-azure-active-directory#access-data-with-a-microsoft-entra-account), [Azure SQL](https://learn.microsoft.com/en-us/azure/azure-sql/database/security-best-practice?view=azuresql#minimize-the-use-of-password-based-authentication-for-users) and [Service Bus](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-authentication-and-authorization#microsoft-entra-id)).

## Why do we need managed identity
Let's take an example; we have an application hosted in Azure App Service which needs to read blobs from a storage account. In Azure, there are multiple ways to grant access to read blobs: shared key, shared access signature and RBAC. Since we want to get rid of managing secrets, that leaves us with just the RBAC.

RBAC works by assigning roles to identities. There are three required values when assigning a role: who (identity), what rights (role) and to which resources (scope). By selecting these values carefully, we can grant just the right level of access to resources and follow the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege). The problem with RBAC is that roles can only be assigned to identities. And App Service is a compute resource, it doesn't have an identity by default.

That's where [managed identity](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview) comes in. It enables us to give an Azure resource an identity and thus, the ability to grant access through role assignments. There are two types of managed identities; system-assigned and user-assigned. In this post we'll focus only system-assigned managed identities.

## Enable managed identity
Before going into the examples, let's enable system-assigned managed identity. This is common for all scenarios and it works the same way for Azure App Service and Azure Functions. This can be done in Bicep by setting `type` *SystemAssigned*  under `identity` or in Azure Portal [by switching `System assigned Status` *On*](https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Chttp#add-a-system-assigned-identity) in the App Service's `Identity` settings.

```bicep
resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: appServiceName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  // ...
}
```

## App Service to Storage account
In this example I'll show you how to use identity-based authentication to list and read blobs in Azure Storage account.

### Grant access rights
After enabling the system-assigned managed identity we need to grant access to the storage account. Access can be granted on different levels; subscription (access to all storage accounts in the subscription), resource group, storage account or container level. I'll grant the application read access ([Storage Blob Data Reader role](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#storage-blob-data-reader)) to all blobs in a single storage account.

Create the storage account and container
```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  // ...
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2022-09-01' = {
  name: '${storageAccount.name}/default/data'
}
```

Grant read access to the storage account. Notice the *existing* keyword; *Storage Blob Data Reader* is one of the Microsoft's built-in roles, so we don't need to create it.
```bicep
resource blobDataReaderRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1' // Storage Blob Data Reader role id
}

resource blobDataContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(appService.id, blobDataReaderRole.id, storageAccount.id)
  properties: {
    roleDefinitionId: blobDataReaderRole.id
    principalId: appService.identity.principalId
  }
  scope: storageAccount
}
```

Role assignment name must be unique, a guid and should be deterministic to avoid being created multiple times. To achieve that we can use [guid function](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/bicep-functions-string#guid). Using that we can easily fulfill the requirements by passing role, principal and scope as parameters.

Role assignment can also be done in Azure Portal, [here](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal?tabs=delegate-condition#step-1-identify-the-needed-scope) are instructions for that.

It's also good to note that **you need to grant yourself rights as well**. Even if you are the owner of the subscription, **by default, you don't have access to data plane operations**.

### Code changes

#### Add blob storage endpoint to configuration
First we need to store the blob storage endpoint address somewhere. I put it in two places; for localhost development I put it in the `appsettings.Development.json` and for the app service, I put it in the app settings using Bicep.
```json
{
  "BlobEndpoint": "https://storageaccountnamehere.blob.core.windows.net/",
  // ...
}
```

```bicep
resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: appServiceName
  location: location
  properties: {
    siteConfig: {
      appSettings: [
        {
          name: 'BlobEndpoint'
          value: storageAccount.properties.primaryEndpoints.blob
        }
      ]
      // ...
    }
    // ...
  }
}
```

#### Add NuGet packages
We need two packages; `Azure.Storage.Blobs` and `Azure.Identity`. `Azure.Storage.Blobs` provides the Azure storage blob client implementations. `Azure.Identity` allows us to create `DefaultAzureCredential` object, which inherits `TokenCredential` class. Different Azure client classes accept `TokenCredential` object as parameter, which is then used as a token provider.

`DefaultAzureCredential` checks different options, whether you've logged in to Azure CLI, Visual Studio or some other supported application and then utilizes that identity. It also checks whether the host has managed identity enabled and that's what makes this work in Azure. Complete list of credentials it tries can be found [here](https://learn.microsoft.com/en-us/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet#definition). **Remember to login to at least one of the listed applications to for localhost development to work!**

```shell
dotnet add package Azure.Identity
dotnet add package Azure.Storage.Blobs
```

#### Inject client and access blob storage
The only thing left is to inject the client through dependency injection in `Program.cs` and then utilize it. Since we already have created a container (`data`) and we want to list and read blobs in that container, we're going to inject `BlobContainerClient`. `BlobContainerClient` has different constructors, but we'll use the one which accepts container `Uri` and `TokenCredential`.

```csharp
var builder = WebApplication.CreateBuilder(args);

var containerAddress = string.Join('/', builder.Configuration["BlobEndpoint"].TrimEnd('/'), "data");
builder.Services.AddSingleton(new BlobContainerClient(new Uri(containerAddress), new DefaultAzureCredential()));

var app = builder.Build();
```

In .NET minimal API we can access the injected `BlobContainerClient` by adding it to handler parameters with `FromServices` attribute.
```csharp
app.MapGet("/", async ([FromServices] BlobContainerClient containerClient) =>
{
    // do something with containerClient here
});
```

### Disable key-based auth (optional)
You can disable key-based access to storage account by setting `allowSharedKeyAccess` *false* in storage account's `properties` in Bicep.

```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  properties: {
    allowSharedKeyAccess: false
    // ...
  }
}
```

## App Service to Azure SQL Database
In this example I'll show you how to use identity-based authentication to access data in Azure SQL Database. Granting access to SQL database is a bit different compared to other examples. We can't use RBAC, because there are no data plane roles for SQL databases. Instead, we need to create a database user for the managed identity and grant database access to that user.

### Set Entra ID authenticated admin
First we need to add an Entra ID authenticated database admin. We need this because only Entra ID logged in admins are able to create database users that utilize Entra ID authentication. It can be done by adding a separate adminstrators resource in Bicep. I added az commands for getting values for current Azure CLI logged in user.

```bicep
resource sqlServerAdminstrators 'Microsoft.Sql/servers/administrators@2021-11-01' = {
  name: 'ActiveDirectory'
  parent: sqlServer
  properties: {
    administratorType: 'ActiveDirectory'
    login: 'sampleuser@company.tld' // az ad signed-in-user show --query userPrincipalName
    sid: 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa' // az ad signed-in-user show --query id
    tenantId: 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb' // ad account show --query tenantId
  }
}
```

### Create SQL user and grant access rights
Next we need to create the database user and grant it access rights. Here are the steps to do that:

1. Connect to the SQL database (not master) with the Entra ID authenticated admin.
2. Create user for the managed identity's service principal using following command (notice that the brackets are required): `CREATE USER [app-service-name] FROM EXTERNAL PROVIDER`
3. Grants access rights to the newly created user. For example, to grant read and write access, run rollowing commands: `ALTER ROLE db_datareader ADD MEMBER [app-service-name]` and `ALTER ROLE db_datawriter ADD MEMBER [app-service-name]`

More detailed instructions can be found [here](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/tutorial-windows-vm-access-sql?source=recommendations#create-contained-user).

### Code changes
#### Add NuGet package
Entity Framework Core requires database engine specific client library, with Azure SQL Database we need `Microsoft.EntityFrameworkCore.SqlServer`. Despite the name, it also supports Azure SQL.
```shell
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
```

#### Add connection strings to configuration
Similar to storage account case, we need to store the database connection string somewhere. Once again, I put it in two places; `ConnectionStrings` in `appsettings.Development.json` for localhost development and for the App Service, I put it in the App Service's connection strings using Bicep.

The key part of these connection strings is that they have `Authentication=Active Directory Default`. This means that under the hood, it will utilize the same `AzureDefaultCredential` we passed to the `BlobContainerClient`. In order for us to use that `Active Directory Default` we [need version 3.0.0+ of `Microsoft.Data.SqlClient`](https://learn.microsoft.com/en-us/sql/connect/ado-net/sql/azure-active-directory-authentication?view=sql-server-ver16#setting-microsoft-entra-authentication). However, if you're using `Microsoft.EntityFrameworkCore.SqlServer` NuGet version `7.0.0+` then there's nothing to worry about, as there's recent enough dependency on the `Microsoft.Data.SqlClient`.

```json
{
  // ...
  "ConnectionStrings": {
    "SQL": "Server=tcp:sql-server-name.database.windows.net,1433;Initial Catalog=database-name;Encrypt=True;TrustServerCertificate=False;Authentication=Active Directory Default;",
  // ...
  }
}
```

```bicep
resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: appName
  location: location
  properties: {
    siteConfig: {
      connectionStrings: [
        {
          name: 'SQL'
          connectionString: 'Server=tcp:${sqlServer.properties.fullyQualifiedDomainName},1433;Initial Catalog=${sqlDatabase.name};Encrypt=True;TrustServerCertificate=False;Authentication=Active Directory Default;'
          type: 'SQLAzure'
        }
      ]
      // ...
    }
    // ...
  }
}
```


#### Create database model and apply database changes
When creating material for this blog post I created a sample database model for a phonebook application. It had only one table with three columns; ID, person's name and phone number. I left it out of this post in addition to applying the database changes, as there are no differences compared to password-based authentication. However, here are links on how to do those things: [create database model](https://learn.microsoft.com/en-us/ef/core/get-started/overview/first-app?tabs=netcore-cli#create-the-model) and [install tools for database update and apply changes](https://learn.microsoft.com/en-us/ef/core/get-started/overview/first-app?tabs=netcore-cli#create-the-database).

#### Inject data context and access database
Configure data context to use right database client and connection string
```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<ApplicationDataContext>(options => options.UseSqlServer(builder.Configuration.GetConnectionString("SQL")));

var app = builder.Build();
```

Access the database through the injected data context
```csharp
app.MapGet("/", async ([FromServices] ApplicationDataContext dataContext) =>
{
    // do something with dataContext here
});
```

### Disable key-based auth (optional)
You can disable password-based authentication by setting `azureADOnlyAuthentication` *true* in a separate `azureADOnlyAuthentications` resource in Bicep.

```bicep
resource sqlServerADOnlyAuth 'Microsoft.Sql/servers/azureADOnlyAuthentications@2021-11-01' = {
  name: 'Default'
  parent: sqlServer
  properties: {
    azureADOnlyAuthentication: true
  }
}
```

## Azure Functions and Service Bus queue trigger
In this example I'll show you how to use identity-based authentication in Azure Functions Service Bus queue trigger. Since I'm using .NET 8 in this example, I'm using isolated worker process model. For in-process model, at least the NuGet package is different.

### Grant access rights
Similar to storage account example, we grant the access through role assignment. Once again, access can be granted on different levels. We'll grant receive messages access rights to a single queue. [Service Bus Data Receiver](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#azure-service-bus-data-receiver) is the right role for that.

Create Service Bus namespace and queue resources
```bicep
resource serviceBus 'Microsoft.ServiceBus/namespaces@2021-11-01' = {
  name: serviceBusNamespaceName
  location: location
  // ...
}

resource serviceBusQueue 'Microsoft.ServiceBus/namespaces/queues@2021-11-01' = {
  name: serviceBusQueueName
  parent: serviceBus
}
```

Grant access to the queue using role assignments
```bicep
resource serviceBusDataReceiverRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '4f6d3b9b-027b-4f4c-9142-0e5a2a2247e0' // Service Bus Data Receiver role id
}

resource serviceBusDataReceiverRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(functionApp.id, serviceBusDataReceiverRole.id, serviceBusQueue.id)
  properties: {
    roleDefinitionId: serviceBusDataReceiverRole.id
    principalId: functionApp.identity.principalId
  }
  scope: serviceBusQueue
}
```

### Code changes
#### Add NuGet package
Each of the Azure Functions [trigger types](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings?tabs=isolated-process%2Cpython-v2&pivots=programming-language-csharp#supported-bindings) requires a specific NuGet package that provides trigger implementation. For (isolated worker process) Service Bus triggers, we need `Microsoft.Azure.Functions.Worker.Extensions.ServiceBus`.

```shell
dotnet add Microsoft.Azure.Functions.Worker.Extensions.ServiceBus
```

#### Declare ServiceBus queue trigger
When declaring the trigger, we need to pass `ServiceBusTrigger` two parameters; queue name and connection string setting name. The runtime will then read the actual connection string from configuration with the given name.

```csharp
[Function(nameof(ServiceBusQueueTrigger))]
public void Run([ServiceBusTrigger("queue-name-here", Connection = "ServiceBusConnection")] ServiceBusReceivedMessage message)
{
    // do something with message here
}
```

#### Add ServiceBusConnection to configuration
When using key-based authentication, the connection string would contain service bus namespace endpoint address, access key etc. With identity-based access we'll have to do this a bit differently, instead of setting `ServiceBusConnection`, we'll set `ServiceBusConnection__fullyQualifiedNamespace`. The value must contain only the fully qualified namespace (e.g. *myservicebusnamespace.servicebus.windows.net*). Using this notation changes the library to use identity-based authentication.

Once again, I put the configuration to two places; `Values` in `local.settings.json` for localhost development and for the Azure Functions resource, I put it in the app settings using Bicep.

More detailed instructions for the Service Bus queue trigger can be found [here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial-2).

```json
{
    "IsEncrypted": false,
    "Values": {
        "ServiceBusConnection__fullyQualifiedNamespace": "my-servicebus-namespace.servicebus.windows.net",
        // ...
    }
}
```

```bicep
resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: functionAppName
  location: location
  properties: {
    siteConfig: {
      appSettings: [
        {
          name: 'ServiceBusConnection__fullyQualifiedNamespace'
          value: '${serviceBus.name}.servicebus.windows.net'
        }
      ]
      // ...
    }
    // ...
  }
}
```

### Disable key-based auth (optional)
You can disable key-based authentication by setting `disableLocalAuth` *true* in the service bus namespace resource under `properties` in Bicep.

```bicep
resource serviceBus 'Microsoft.ServiceBus/namespaces@2021-11-01' = {
  name: serviceBusNamespaceName
  location: location
  properties: {
    disableLocalAuth: true
  }
  // ...
}
```

## The list doesn't end here
In the examples I showed how to access blobs, SQL database and Service Bus queue with managed identity and RBAC. However, many other services are supported, too. You can find the complete list [here](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/services-id-authentication-support). That list doesn't cover services that are in preview. For example, Azure Cache for Redis [is in preview](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-azure-active-directory-for-authentication).

In addition to that, even more resources support managed identities. You can, for example, assign Azure API Management managed identity and [access Key Vault using that](https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-use-managed-service-identity).

But wait, there's more! C# isn't the only supported language, Azure Identity library is available for at least Java, JavaScript, Python and Go as well.

## Closing words
In this post I demonstrated how to use system-assigned managed identity to access Azure resources. As you noticed, even though the basic structure of utilizing managed identity and RBAC is the same, each of the services have their own little quirks. In order to get to know these quirks, you need to read the documentation carefully and do some digging. And some scenarios are just not supported (yet). But even if it takes a little more time, I think it's worth it. When you don't have manage secrets, there's one less place to make mistakes. Especially, when mistakes can be extremely costly.

## Further reading
- [What are managed identities for Azure resources?](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
- [What is Azure role-based access control](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview)
- [Azure built-in roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles)
- [Understand scope for Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview)
