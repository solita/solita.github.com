---
layout: post
title: Keycloak and Suomi.fi from scratch
author: timomantyvaara
excerpt: Simple step-by-step instructions on how to configure Suomi.fi e-Identification as an identity broker on Keycloak.
tags:
  - Keycloak
  - SAML
  - suomi.fi

---

## Preface
[Suomi.fi e-Identification](https://www.suomi.fi/instructions-and-support/identification/what-is-suomifi-e-identification) is a shared strong identification service of public administration e-services.
[Keycloak](https://www.keycloak.org/) is a popular open-source identity and access management solution.

They are commonly used together for authentication in services developed for authorities, public agencies, health care, municipalities etc.
Usually in a project the authentication is set up once quite early and the details might get lost in time. This guide aims to provide simple step-by-step instructions on how to configure everything from scratch.

### Prerequisites
- Keycloak
- Access to the Keycloak admin console
- Access to Suomi.fi Palveluhallinta (directly or by proxy)

### What this guide does not cover
- How to configure Keycloak for your application
- How to integrate with AWS Cognito (a common combination)

### Good to know
We use Suomi.fi test environment for this guide, but the steps should be more or less the same for production as well. You can use any existing realm in Keycloak or create your own, depending on your configuration.

## Certificates

Let's start by generating self-signed certificates (Suomi.fi test environment accepts self-signed).
We'll be using separate certificates for signing and encryption.

For example, using `openssl`:
```bash
openssl req -newkey rsa:2048 -nodes -keyout sig.key -x509 -days 365 -out sig.crt -subj "/C=FI/O=Solita/CN=example.com"
openssl req -newkey rsa:2048 -nodes -keyout enc.key -x509 -days 365 -out enc.crt -subj "/C=FI/O=Solita/CN=example.com"
```

Obviously, real certificates should be used in production, but we'll leave them as homework.

### Add the certificates to Keycloak

Open the Keycloak admin console, choose your realm and go to **Realm settings** > **Keys** > **Add providers**.

First, remove providers `rsa-generated` and `rsa-enc-generated` so that they don't interfere with our configuration.
After they're gone, let's add our generated certificates to our realm.

Add new provider of type `rsa`:
- Name: `suomi.fi sig cert`
- Priority: `0`
- Enabled: `true`
- Active: `true`
- Private RSA Key: upload `sig.key` created earlier
- X509 Certificate: upload `sig.crt` created earlier
- Algorithm: `RS256`

![Signing certificate](/img/2024-keycloak-suomifi-from-scratch/sig-cert.png)

Add new provider of type `rsa-enc`:
- Name: `suomi.fi enc cert`
- Priority: `0`
- Enabled: `true`
- Active: `true`
- Private RSA Key: upload `enc.key` created earlier
- X509 Certificate: upload `enc.crt` created earlier
- Algorithm: `RSA-OAEP`

![Encryption certificate](/img/2024-keycloak-suomifi-from-scratch/enc-cert.png)

## SAML v2.0 identity provider

Now that we have our certificates in order, we can add Suomi.fi as an identity provider. Keycloak is already the identity provider (IDP) for your application, but in this case, it also is the service provider (SP) for Suomi.fi. And respectively, Suomi.fi is the identity provider for Keycloak.

Open the Keycloak admin console, choose your realm and go to **Identity providers**.

Add new identity provider of type `SAML v2.0`:
- Alias: `suomi.fi`
- Display name: `Suomi.fi`
- Display order: `1`
- Service provider entity ID: usually the URL of your environment, e.g. http://keycloak-demo-application<br> 
  _(Must be an URL, but it does not need to actually exist. This will identify the service in Suomi.fi and must be globally unique.)_
- Use entity descriptor: `true`
- SAML entity descriptor: `https://static.apro.tunnistus.fi/static/metadata/idp-metadata.xml`

_(Don't save yet, we want to tweak the settings first a bit)_

![SAML v2.0 identity provider config](/img/2024-keycloak-suomifi-from-scratch/suomifi-idp.png)

We'll configure the identity provider to use social security number (SSN) to identify external users. 

Switch **Use entity descriptor** off and edit the following values:

- Principal type: `Attribute [Name]`
- Principal attribute: `urn:oid:1.2.246.21`
- Want Assertions signed: `true`
- Want Assertions encrypted: `true`
- Encryption Algorithm: `RSA-OAEP` _(matches the configured encryption key)_

![SAML v2.0 extra settings](/img/2024-keycloak-suomifi-from-scratch/suomifi-idp-saml-settings.png)

### Attribute mappers

We can extract user information from the identity provided by Suomi.fi with attribute mappers. Let's add a few.

Open the Keycloak admin console, choose your realm and go to **Identity providers** > **Suomi.fi** > **Mappers**.

Add new mapper:
- Name: `ssn`
- Sync mode override: `inherit`
- Mapper type: `Attribute Importer`
- Attribute Name: `urn:oid:1.2.246.21`
- Friendly Name: `<empty>`
- Name Format: `ATTRIBUTE_FORMAT_URI`
- User Attribute Name: `username`

![Attribute mappers](/img/2024-keycloak-suomifi-from-scratch/ssn-mapper.png)

Add new mapper:
- Name: `first names`
- Sync mode override: `inherit`
- Mapper type: `Attribute Importer`
- Attribute Name: `http://eidas.europa.eu/attributes/naturalperson/CurrentGivenName`
- Friendly Name: `<empty>`
- Name Format: `ATTRIBUTE_FORMAT_URI`
- User Attribute Name: `firstName`

![Attribute mappers](/img/2024-keycloak-suomifi-from-scratch/first-names-mapper.png)

Add new mapper:
- Name: `last name`
- Sync mode override: `inherit`
- Mapper type: `Attribute Importer`
- Attribute Name: `urn:oid:2.5.4.4`
- Friendly Name: `<empty>`
- Name Format: `ATTRIBUTE_FORMAT_URI`
- User Attribute Name: `lastName`

![Attribute mappers](/img/2024-keycloak-suomifi-from-scratch/last-name-mapper.png)

Relevant Suomi.fi support articles:
- [IDP metadata addresses](https://palveluhallinta.suomi.fi/fi/tuki/artikkelit/5eaab63f85880b00f6428e84) (at the bottom of the page)
- [Attributes of the identified user](https://palveluhallinta.suomi.fi/fi/tuki/artikkelit/590ad07b14bbb10001966f50)

## Service provider metadata
Keycloak generates a service provider metadata but Suomi.fi has its own special requirements for the metadata.
I've found that it's usually easiest to just create the metadata manually based on the Suomi.fi example metadata.

There are a few things in the metadata we'll need to customize:
- `EntityDescriptor` element's `entityID` attribute uniquely identifies the application. Must equal **Service provider entity ID** in Keycloak IDP settings.
- `UIInfo` element contains a description of the environment. These are visible to the end user.
- `SPSSODescriptor`element contains certificates as `KeyDescriptor`elements. We use separate certificates for `use="signing"` and `use="encryption"` but it's also possible to use one certificate for both purposes.
- `SingleLogoutService` and `AssertionConsumerService` elements' `Location` attribute is the redirect address of the service provider (Keycloak). Must equal **Redirect URI** in Keycloak IDP settings.
- `AttributeConsumingService` element contains the service provider name (which be different from the one in `UIInfo` element) and the attributes of the identified user that we want to request.
- `Organization` element contains organization info.
- `ContactPerson` elements contain contact information. At least technical contact information is mandatory.

### Example metadata 

A minimal example of a working metadata (using the "suppea tietosisältö" set of user attributes). Things to customize are marked with `CHANGE_ME`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" entityID="CHANGE_ME">
  <md:Extensions>
    <mdattr:EntityAttributes xmlns:mdattr="urn:oasis:names:tc:SAML:metadata:attribute">
      <saml:Attribute xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" Name="FinnishAuthMethod" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">http://ftn.ficora.fi/2017/loa3</saml:AttributeValue>
        <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">http://ftn.ficora.fi/2017/loa2</saml:AttributeValue>
        <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">http://eidas.europa.eu/LoA/high</saml:AttributeValue>
        <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">http://eidas.europa.eu/LoA/substantial</saml:AttributeValue>
        <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">urn:oid:1.2.246.517.3002.110.999</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" FriendlyName="VtjVerificationRequired" Name="urn:oid:1.2.246.517.3003.111.3" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">true</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" FriendlyName="SkipEndpointValidationWhenSigned" Name="urn:oid:1.2.246.517.3003.111.4" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">false</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" FriendlyName="CipherName" Name="urn:oid:1.2.246.517.3003.111.26" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">AES-GCM</saml:AttributeValue>
      </saml:Attribute>
    </mdattr:EntityAttributes>
  </md:Extensions>
  <md:SPSSODescriptor AuthnRequestsSigned="true" WantAssertionsSigned="true" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:Extensions>
      <mdui:UIInfo xmlns:mdui="urn:oasis:names:tc:SAML:metadata:ui">
        <mdui:DisplayName xml:lang="fi">CHANGE_ME</mdui:DisplayName>
        <mdui:DisplayName xml:lang="sv">CHANGE_ME</mdui:DisplayName>
        <mdui:DisplayName xml:lang="en">CHANGE_ME</mdui:DisplayName>
        <mdui:Description xml:lang="fi">CHANGE_ME</mdui:Description>
        <mdui:Description xml:lang="sv">CHANGE_ME</mdui:Description>
        <mdui:Description xml:lang="en">CHANGE_ME</mdui:Description>
        <mdui:PrivacyStatementURL xml:lang="fi">CHANGE_ME</mdui:PrivacyStatementURL>
        <mdui:PrivacyStatementURL xml:lang="sv">CHANGE_ME</mdui:PrivacyStatementURL>
        <mdui:PrivacyStatementURL xml:lang="en">CHANGE_ME</mdui:PrivacyStatementURL>
      </mdui:UIInfo>
    </md:Extensions>
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        <ds:X509Data>
          <ds:X509Certificate>CHANGE_ME</ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
    </md:KeyDescriptor>
    <md:KeyDescriptor use="encryption">
      <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        <ds:X509Data>
          <ds:X509Certificate>CHANGE_ME</ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
      <md:EncryptionMethod Algorithm="http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p"/>
      <md:EncryptionMethod Algorithm="http://www.w3.org/2009/xmlenc11#rsa-oaep"/>
    </md:KeyDescriptor>
    <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="CHANGE_ME"/>
    <md:NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:transient</md:NameIDFormat>
    <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="CHANGE_ME" isDefault="true" index="1"/>
    <md:AttributeConsumingService index="1" isDefault="true">
      <md:ServiceName xml:lang="fi">CHANGE_ME</md:ServiceName>
      <md:ServiceName xml:lang="sv">CHANGE_ME</md:ServiceName>
      <md:ServiceName xml:lang="en">CHANGE_ME</md:ServiceName>
      <md:RequestedAttribute FriendlyName="FamilyName" Name="http://eidas.europa.eu/attributes/naturalperson/CurrentFamilyName" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
      <md:RequestedAttribute FriendlyName="FirstName" Name="http://eidas.europa.eu/attributes/naturalperson/CurrentGivenName" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
      <md:RequestedAttribute FriendlyName="DateOfBirth" Name="http://eidas.europa.eu/attributes/naturalperson/DateOfBirth" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
      <md:RequestedAttribute FriendlyName="PersonIdentifier" Name="http://eidas.europa.eu/attributes/naturalperson/PersonIdentifier" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
      <md:RequestedAttribute FriendlyName="nationalIdentificationNumber" Name="urn:oid:1.2.246.21" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
      <md:RequestedAttribute FriendlyName="displayName" Name="urn:oid:2.16.840.1.113730.3.1.241" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
      <md:RequestedAttribute FriendlyName="cn" Name="urn:oid:2.5.4.3" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
      <md:RequestedAttribute FriendlyName="sn" Name="urn:oid:2.5.4.4" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
      <md:RequestedAttribute FriendlyName="givenName" Name="urn:oid:2.5.4.42" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri"/>
    </md:AttributeConsumingService>
  </md:SPSSODescriptor>
  <md:Organization>
    <md:OrganizationName xml:lang="fi">CHANGE_ME</md:OrganizationName>
    <md:OrganizationName xml:lang="sv">CHANGE_ME</md:OrganizationName>
    <md:OrganizationName xml:lang="en">CHANGE_ME</md:OrganizationName>
    <md:OrganizationDisplayName xml:lang="fi">CHANGE_ME</md:OrganizationDisplayName>
    <md:OrganizationDisplayName xml:lang="sv">CHANGE_ME</md:OrganizationDisplayName>
    <md:OrganizationDisplayName xml:lang="en">CHANGE_ME</md:OrganizationDisplayName>
    <md:OrganizationURL xml:lang="fi">CHANGE_ME</md:OrganizationURL>
    <md:OrganizationURL xml:lang="sv">CHANGE_ME</md:OrganizationURL>
    <md:OrganizationURL xml:lang="en">CHANGE_ME</md:OrganizationURL>
  </md:Organization>
  <md:ContactPerson contactType="technical">
    <md:GivenName>CHANGE_ME</md:GivenName>
    <md:SurName>CHANGE_ME</md:SurName>
    <md:EmailAddress>mailto:CHANGE_ME</md:EmailAddress>
  </md:ContactPerson>
</md:EntityDescriptor>
```

Relevant Suomi.fi support articles:
- [Suomi.fi example metadata](https://palveluhallinta.suomi.fi/fi/tuki/artikkelit/5a814d109ea47311bfd599a3)
- [Metadata contents explained](https://palveluhallinta.suomi.fi/fi/tuki/artikkelit/590adae814bbb10001966f53)
- [Attributes of identified user](https://palveluhallinta.suomi.fi/fi/tuki/artikkelit/590ad07b14bbb10001966f50)

### Upload metadata 
The prepared metadata must be uploaded to [Suomi.fi Palveluhallinta](https://palveluhallinta.suomi.fi). Do it through your proxy (usually the client) or do it yourself, if you've been authorized.

After the metadata has been approved and published, we should be good to go for testing.

![Published metadata](/img/2024-keycloak-suomifi-from-scratch/published-metadata.png)

Relevant Suomi.fi support article: [Instructions for using Palveluhallinta](https://palveluhallinta.suomi.fi/fi/tuki/artikkelit/59ddf073002aa00072b71d0b)

## Testing

With "basic" settings in Keycloak, Suomi.fi will appear as an alternative way to log in.

![Keycloak login with Suomi.fi](/img/2024-keycloak-suomifi-from-scratch/suomifi-option-login.png)

We left the user's email address out of the attributes and in this case, Keycloak will ask for it when the user logs in for the first time.

![Keycloak wants your email](/img/2024-keycloak-suomifi-from-scratch/keycloak-email.png)

You'll probably want to configure this (and many other things) differently but that is a story for another time.