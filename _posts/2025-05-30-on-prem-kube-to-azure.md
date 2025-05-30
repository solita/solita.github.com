---
layout: post
title: Authenticate on-prem Kubernetes workload to Azure without secrets
author: mattipulkkinen
excerpt: Inspired by the Azure Kubernetes Service way of authenticating workloads to Azure to access other resources without secrets, I configured my on-premises Kubernetes cluster to do the same.
tags:
  - Azure
  - Secrets
  - Managed identity
  - Role-based access control
  - Kubernetes
  - OIDC
---

I've been learning Kubernetes, starting with an on-premises single-node cluster and later moving on to Azure Kubernetes Service (AKS). While configuring secretless workload identity-based authentication for a pod in AKS, I began to wonder: could I use a similar approach with other Kubernetes clusters - e.g., my on-premises Kubernetes cluster?

Identity-based authentication has several advantages:

- No need to manage secrets (reducing the risk of leaking an access key)
- Access tokens have a much shorter lifetime (a leaked token expires sooner)
- Enables granting granular access rights

[_Use Microsoft Entra Workload ID with AKS_ page](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview) states that _Microsoft Entra Workload ID uses [Service Account Token Volume Projection](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#serviceaccount-token-volume-projection)..., to enable pods to use a Kubernetes identity._ Could I configure that on my on-premises cluster as well, and would Entra ID allow me to use those tokens to authenticate the workload? Curious whether the same approach could work outside of AKS, I set out to replicate it in my on-premises cluster — and here’s how it went.

## Getting started

I decided to start by searching the Internet for similar implementations because I had limited Kubernetes skills. The odds are, I'm not the first to think of this.

I used keywords _Kubernetes_, _OIDC_, _provider_, _issuer_, etc. Initially, I didn't find anything related, as all the results were about how to use Entra ID or other identity providers as login providers in your cluster. After a while, I found [a blog post](https://medium.com/in-the-weeds/service-to-service-authentication-on-kubernetes-94dcb8216cdc) describing a similar thing that I had in mind.

The blog post also discussed Kubernetes service account token volume projection and listed [AWS EKS pod identity webhook self-hosted Kubernetes setup](https://github.com/aws/amazon-eks-pod-identity-webhook/blob/master/SELF_HOSTED_SETUP.md) as a source. The blog post and the AWS instructions should make an excellent starting point and provide me with plenty of tips moving forward.

## Configuring cluster

I used a single-node [k0s](https://docs.k0sproject.io/) cluster for an on-premises cluster. Cluster configuration instructions are focused on that setup.

I started by getting a pod running with a projected service account token, to see the actual contents of a token, not the examples from the Internet. The Kubernetes [service account token projection page](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#launch-a-pod-using-service-account-token-projection) has an almost-ready YAML, I just needed to create the service account too. YAML for the service account was available on the same page.

The token (decoded token payload below, irrelevant properties removed) looked the same as in the examples. So, from a cluster configuration point of view, all I need to change is the _issuer_ (_iss_). According to the OpenID Connect (OIDC) [spec](https://openid.net/specs/openid-connect-discovery-1_0.html#IssuerDiscovery), the value can be any URL address, as long as it meets the following requirements:

- It uses the https scheme
- It doesn't have a query or fragment part in it
- You're able to host content under that

The address may contain a path component, e.g., _https://domain.tld/tenant1_ is allowed. The **cluster doesn't need to be hosted in that address**! In the AWS instructions, they set the _issuer_ to be an S3 bucket, as that's one easy way to host relevant documents.

```json
{
  "aud": ["vault"],
  "iss": "https://kubernetes.default.svc",
  "sub": "system:serviceaccount:default:build-robot"
}
```

In the blog post, it's mentioned that the _issuer_ can be changed by setting `--service-account-issuer` kube-apiserver flag. But how do I set that with k0s? Or in general? I didn't need to do any configuration when setting up the k0s. The [k0s configuration file reference](https://docs.k0sproject.io/stable/configuration/#configuration-file-reference) had nothing related to it. Maybe k0s doesn't support setting that? After some searching, I checked the k0s project GitHub issues. Search for _issuers_ yielded [one result](https://github.com/k0sproject/k0s/issues/3978), which shows that the configuration file reference might not have all the options listed. That's annoying, but fortunately, that issue showed me how it might be done. I gave it a try and modified my k0s configuration file.

```json
{
  "aud": ["vault"],
  "iss": "https://k.mydomain.tld",
  "sub": "system:serviceaccount:default:build-robot"
}
```

That worked, nice! That should be enough for the cluster-level configuration.

## Kubernetes deployment changes

Next up were Kubernetes deployment changes. There were a couple of things that needed to be done related to Kubernetes resources:

I created a service account for the application. You could use the default service account, but I prefer having application-specific service accounts. The service account needs to be in the same namespace as the deployment.

Creating a service account can be done with simple YAML:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: application1-sa
  namespace: application1
```

I set the deployment to use the created service account when deploying pods. That's done by setting the `.spec.template.spec.serviceAccountName` value.

I added the service account token volume projection and mounted it. When using token volume projection, you can specify the token expiration time (optional, one hour by default) and the audience. By default, Azure/Entra ID expects the audience to be _api://AzureADTokenExchange_, so I used that.

Finally, I added _AZURE_TENANT_ID_, _AZURE_CLIENT_ID_, and _AZURE_FEDERATED_TOKEN_FILE_ environment variables to the pod template. Those are later used by Microsoft's identity library. You can get _AZURE_TENANT_ID_ and _AZURE_CLIENT_ID_ values with the following Azure CLI command:

`az identity show --resource-group {resource-group-name} --name {user-assigned-managed-identity-name} --query "{clientId:clientId,tenantId:tenantId}"`.

_AZURE_FEDERATED_TOKEN_FILE_ needs to be set `{volumeMount.mountPath}/{serviceAccountToken.path}`. The identity library will try to find the token file from that path.

After everything, my Kubernetes deployment looked something like this:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
  namespace: application1
spec:
  # ...
  template:
    # ...
    spec:
      containers:
        - name: application1
          # ...
          env:
            - name: AZURE_CLIENT_ID
              value: aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa
            - name: AZURE_FEDERATED_TOKEN_FILE
              value: /var/run/secrets/kubernetes.io/tokens/application1-token
            - name: AZURE_TENANT_ID
              value: bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb
          volumeMounts:
            - name: application1-token
              mountPath: /var/run/secrets/kubernetes.io/tokens
      serviceAccountName: application1-sa
      volumes:
        - name: application1-token
          projected:
            sources:
              - serviceAccountToken:
                  path: application1-token
                  audience: api://AzureADTokenExchange
```

## Configure Azure user-assigned managed identity

To grant access to Cosmos DB, you need an identity that can be authorized. On the Azure side, I created and configured a workload identity. This workload identity can either be a user-assigned managed identity or an app registration with a service principal. I chose to use a managed identity, which can be created as any other Azure resource.

Then, I assigned my Cosmos DB instance-scoped _Cosmos DB Built-in Data Contributor_ role to the managed identity. Microsoft has [instructions](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-grant-data-plane-access) for that. Unfortunately, you still can't list or assign Cosmos DB data plane roles from the Azure portal, but you need to use either CLI or IaC.

Finally, I configured a _Federated credential_ for the user-assigned managed identity. This allows any system to authenticate as that identity, as long as it provides a valid token with the right _issuer_, _subject_, and _audience_. Federated credentials can be added from the user-assigned managed identity resource, there's a _Federated credentials_ item under _Settings_, and then click _Add Credential_. From the dropdown menu, you can select from a couple of options, one of which is _Kubernetes accessing Azure resources_. I used that because it forms the _subject_ automatically from my _(Kubernetes) Namespace_ and _Service Account (name)_ inputs.

![Kubernetes accessing Azure resources form](/img/2025-on-prem-kube-to-azure/add-federated-credential-kube.png)

## Necessary code changes

There's only one thing you need to change in the code. Instead of providing a key for the `CosmosClient`, you provide credentials that can be used to get an authentication token. In practice, the changes should look like something like this:

```javascript
// old
const client = new CosmosClient({
  endpoint: process.env.COSMOS_ENDPOINT,
  key: process.env.COSMOS_KEY,
});
```

```javascript
// new
const credential = new DefaultAzureCredential();
const client = new CosmosClient({
  aadCredentials: credential,
  endpoint: process.env.COSMOS_ENDPOINT,
});
```

[`DefaultAzureCredential`](https://learn.microsoft.com/en-us/dotnet/azure/sdk/authentication/credential-chains#defaultazurecredential-overview) tries a combination of different authentication mechanisms until it finds a working one. One of the tried mechanisms is `WorkloadIdentityCredential`, which requires _AZURE_TENANT_ID_, _AZURE_CLIENT_ID_, and _AZURE_FEDERATED_TOKEN_FILE_ environment variables. You can use the `WorkloadIdentityCredential` directly, instead of `DefaultAzureCredential`, and pass the values to the constructor. To make sure I was using the `WorkloadIdentityCredential`, I changed my application to use it instead of `DefaultAzureCredential`.

When startup speed is important, you may want to use [ChainedTokenCredential](https://learn.microsoft.com/en-gb/dotnet/azure/sdk/authentication/credential-chains#chainedtokencredential-overview). It allows you to list the authentication mechanisms yourself. That way, you can omit irrelevant authentication mechanisms but still have multiple ways of authenticating, e.g., one for hosted workloads and one for local development.

## Preparing OIDC discovery document and public keys

To validate the token, there needs to be an OpenID discovery document at `{issuer}/.well-known/openid-configuration`, and the discovery document must have a link to JSON Web Key Sets (JWKS), which lists the public keys that can be used to validate the token signature. The blog post listed a sample discovery document. The blog post and AKS used different addresses for the JWKS. `{issuer}/keys.json` JWKS address was used in the sample document, but AKS uses `{issuer}/openid/v1/jwks` address for the JWKS. I decided to use the AKS preferred address just to be safe. Based on [OpenID discovery spec](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata), it doesn't matter what you use, as long as the discovery document has a link to the JWKS document.

Next was preparing the JWKS file content. The AWS instructions suggested creating a new key pair and then converting it twice. First from _OpenSSH public key_ format to _PKCS #8_ and then from _PKCS #8_ to JWKS suitable format ([RFC7517](https://www.rfc-editor.org/rfc/rfc7517)). However, I wanted to use the existing key pair, so I skipped the generating part. By checking `k0scontroller.service` status on my cluster host, I found the location of the current public key.

The next step was to convert the key to _PKCS #8_ format. When trying to convert the existing key, I got _Load key ".../sa.pub": error in libcrypto_ error. To make sure the instructions were right, I decided to generate a new key pair and try again. That time the conversion worked. I then compared the converted key to the public key file I was trying to convert. They looked almost identical, so I figured the key was already in _PKCS #8_ format. I just had to hope that it wouldn't come and bite me later on...

Then I needed to run the public key through the second conversion. [The conversion tool](https://github.com/aws/amazon-eks-pod-identity-webhook/blob/master/hack/self-hosted/main.go) was provided in the AWS pod identity webhook repository. The conversion tool was written in Go, but I didn't have Go installed, and I didn't want to install it for a single run. So, I used the _golang_ Docker image, cloned the repository there (git was pre-installed), and ran the code in the container. The hardest part was getting the existing public key to the container, as the _golang_ image didn't have `nano` or `vim` installed. So, I did some searching and found `cat <<EOF> filename` trickery (apparently it's called [_here document_](https://en.wikipedia.org/wiki/Here_document)). I had seen it before but hadn't used it, except for some individual copy-pastes from tutorials.

Now I have the discovery and the keys document contents prepared.

## Hosting OIDC discovery document and keys

Next up is hosting those two documents under the URL address set as the issuer. I created a new subdomain for my domain, let's call it _k.mydomain.tld_. As this was about learning Kubernetes, I hosted the contents in the same cluster. I created a simple nginx deployment and configured a listener for the subdomain. Cert-manager handled acquiring the TLS certificate automatically. I put the file contents into a ConfigMap and mounted those as files under the nginx default content hosting folder.

At this point, I had the entire setup ready, but it didn't work. The error I received was `AADSTS90061: Request to External OIDC endpoint failed`. For whatever reason, that's not listed in the [Entra authentication and authorization error codes list](https://learn.microsoft.com/en-us/entra/identity-platform/reference-error-codes). I found a [GitHub pull request](https://github.com/Azure/azure-workload-identity/pull/608) about adding related documentation and checked the file changes. By glancing through the changes, I figured they wouldn't help. So, I went back to the [OpenID spec](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig) and noticed that both files needed to have _application/json_ content type, which my files didn't have. Let's fix that.

I looked up how to configure nginx static files content type and found the [default_type configuration](https://nginx.org/en/docs/http/ngx_http_core_module.html#default_type). Setting the default type is a bit overkill, but I just wanted a quick fix, and I'm not hosting any other files in the same deployment. I read the current configuration file contents, added the default_type, added another ConfigMap with customized configuration, and mounted that as well. Now my documents were returned with the right content type.

But I'm still getting the same error. What could be the issue? Have I made a mistake? After banging my head against the wall, I noticed the URL where I'm hosting the discovery document, _/.well-known/oidc-configuration_. I immediately realized my error, it should be _/.well-known/**openid**-configuration_. I manually wrote the addresses when I hosted them, which is when the error happened. The GitHub pull request actually had curl commands to verify that the discovery file and JWKS addresses respond. Had I tried the commands, I would have noticed this. Well, maybe next time.

## Closing words

After fixing the path, it all started to work. So, you can use any token provider with Azure Workload identities. Of course, it's stated on the [Microsoft Workload identity federation page](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation), but it feels more concrete when you implement it and get it to work.

I expected this to be harder. Sure, it took me a couple of days to get this whole thing working, but it was mostly due to my lack of skills and stupid errors. Initially, I thought I would have to install a third-party plugin to generate the tokens, but Kubernetes had that capability built in!

Implementing this was also really fun; I got to solve problems and learn new stuff along the way. I will definitely take this into use in my personal projects, as I don't like managing secrets, and this is a good solution for handling authentication, not some dirty hack.
