---
layout: post
title: Using Azure without secrets, Part 1
author: mattipulkkinen
excerpt: Managing secrets properly is hard and that's why you should avoid it whenever possible. Here's how to login to Azure CLI in GitHub Actions without secrets.
tags:
 - Azure
 - Secrets
 - OIDC
 - CI/CD
---

Often in software development we need to access other resources, be it database server, blob storage or something else. This naturally requires authentication, which usually involves a client secret, a password or a certificate. But managing secrets and certificates properly is hard and mistakes could lead into catastrophic situation.

But there's another way! Azure and many of its resources can be used without secrets. In this blog I'll tell you how to login to Azure CLI in GitHub Actions workflow without secrets. The focus of this post is on providing an example and less on the explanation part, however, that can't be completely avoided.

Before we get into the actual content it's good to make a distinction here; when I talk about secrets, I mean passwords, client secrets and certificates. Not subscription IDs, application IDs, database server addresses or such. Though we usually keep database server addresses etc. safe, they themselves shouldn't provide malicious user access to the resource without a secret. So, we still need database server addresses etc. to identify target resources, but we can get rid of passwords and client secrets.

## Before getting started
Azure CLI login in workflow run without secrets is done quite similarly as with secrets; app registration and service principal are needed but a token is passed instead of a client secret.

The token is a regular JSON Web Token (JWT), where subject (sub) claim plays key role. Azure will only accept the token if issuer, subject and audience values match. However, the subject claim value is the only one that might change when using GitHub Actions. Depending on what triggered the workflow and whether an environment is referenced, GitHub issues token with different subjects. Different scenarios are described [here](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#example-subject-claims). In this post **I've referenced *Development* environment in GitHub Actions workflow, so I need to configure the subject accordingly**.

## 1. Create app registration and assign roles
This can be done in different ways, for example, in [Azure Portal](https://portal.azure.com/) by using Azure CLI. But I've prepared a bash script that will do all of the steps listed below. The script can be found further down. You just need to set the SUBJECT value. Also, you should check whether APP_NAME, ROLE and SCOPE make sense in your scenario. You might want to limit the scope to a resource group, for example.

1. [Create an app registration](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-service-principal-portal#register-an-application-with-microsoft-entra-id-and-create-a-service-principal) with some name, which represents your CI/CD pipeline in this case. Leave other settings default.
2. Create a service principal for the app registration (if you create app registration in Azure Portal or Entra admin center, this is done for you automatically). Service principal is required because role assignments can only be assigned to identities and app registration doesn't have an *identity*. Service principal acts an identity for the app registration.
3. [Configure *Federated credentials*](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust?pivots=identity-wif-apps-methods-azp#github-actions) for the app registration. You can find *Federated credentials* tab next to *Certificates* and *Client secrets* tabs when you open the app registration.
4. [Assign role(s) to service principal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal?tabs=delegate-condition#step-1-identify-the-needed-scope). If you're unsure, *Contributor* role is a good starting point.

Script requirements:
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) needs to be installed
- You're logged in to Azure CLI
- You have rights to create app registrations (you have e.g. Application Developer Entra role)
- You have rights to assign Azure roles (you have e.g. Role Based Access Control Administrator Azure role)
- [jq](https://jqlang.github.io/jq/download/) needs to be installed (for handling JSON)

```bash
#!/usr/bin/env bash

# CONFIGURATION
# Use currently active subscription or you can set the subscription ID here manually
SUBSCRIPTION_ID=$(az account show --query "id" --output tsv)

# Change this
SUBJECT=repo:my-org/my-repo:environment:Development

# Check whether these make sense in your scenario
APP_NAME=github-actions
ROLE=Contributor
SCOPE=/subscriptions/$SUBSCRIPTION_ID

# ACTUAL SCRIPT
# Create app registration
APPLICATION_ID=$(az ad app create --display-name $APP_NAME --query "appId" --output tsv)

# Create service principal for the app
OBJECT_ID=$(az ad sp create --id $APPLICATION_ID --query "id" --output tsv)

# Prepare federated identity request object
# jq will create a JSON like this: {"name":"github-actions","issuer":"https://token.actions.githubusercontent.com","subject":"repo:my-org/my-repo:environment:Development","audiences":["api://AzureADTokenExchange"]}
FEDERATED_CREDENTIAL=$(jq --null-input \
    --compact-output \
    --arg name $APP_NAME \
    --arg issuer "https://token.actions.githubusercontent.com" \
    --arg subject $SUBJECT \
    --arg audience "api://AzureADTokenExchange" \
    '{"name":$name,"issuer":$issuer,"subject":$subject,"audiences":[$audience]}')

# Create federated identity
az ad app federated-credential create --id $APPLICATION_ID --parameters $FEDERATED_CREDENTIAL

# Assign role
az role assignment create --role $ROLE --assignee-object-id $OBJECT_ID --assignee-principal-type "ServicePrincipal" --scope $SCOPE

# Print relevant values
echo TenantID $(az account show --query "tenantId" --output tsv)
echo SubscriptiontID $SUBSCRIPTION_ID
echo ApplicationtID $APPLICATION_ID
```

## 2. Set GitHub Actions (non-)secrets
I know I said we're getting rid of secrets, but let's keep subscription IDs etc. safe anyway.

1. Find tenant ID, subscription ID and client ID (application ID) values. You can find the values in the last three lines printed by the script.
2. Store those values as [GitHub Actions secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) with names *AZURE_TENANT_ID*, *AZURE_SUBSCRIPTION_ID* and *AZURE_CLIENT_ID*.

## 3. Configure GitHub Actions workflow
Here we're going to use [Azure Login](https://github.com/marketplace/actions/azure-login) Action. After the login step you can use az commands or other actions which require Azure CLI login, like [Deploy ARM Template](https://github.com/marketplace/actions/deploy-azure-resource-manager-arm-template) or [Deploy Azure Web App](https://github.com/marketplace/actions/azure-webapp).

Important parts here are:
- Permissions: id-token needs write permission, otherwise you won't be able to request the JWT. Permissions can also be assigned on workflow level if you need them on multiple jobs.
- Add *azure/login@v1* step
- Set the environment if you configured the federated credential subject to contain it.

```yaml
...

jobs:
  login:
    runs-on: ubuntu-latest
    environment:
      name: Development
    permissions:
      id-token: write
    steps:
      - name: Login
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      - name: Show current account
        run: az account show
```

And that's it.

## Tip
Entra admin center and Azure Portal both have nice tool for forming subjects based on given parameter values. You can use that to make sure you get the subject in the right format.

![Screenshot of Entra admin center federated credential creation form](/img/azure-without-secrets-part-1/entra-federated-credential-subject.png)

## It's not just Azure and GitHub
GitHub also has well documented examples (e.g. [AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) and [GCP](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-google-cloud-platform)) of using OIDC in other services as well, not just Azure. And even better, you can [fetch the JWT manually](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#updating-your-actions-for-oidc), enabling you to use it on any service because you're not limited to GitHub Actions available in the marketplace.

And turning this the other way around, you can also do this in, for example, [GitLab](https://docs.gitlab.com/ee/ci/yaml/index.html#id_tokens). It provides similar mechanism for fetching JWT for OIDC authentication.

## What's next
When using Azure, you can also get rid of many other secrets as well. You can for example authenticate to Azure Blob Storage or Cosmos DB without secrets using managed identities and role-based access control. More on that in [part 2](https://dev.solita.fi/2024/01/31/azure-without-secrets-part-2.html).

## Sources
- [Workload identity federation by Microsoft](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation)
- [GitHub OIDC documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [GitHub OIDC in Azure](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-azure)
