---
layout: post
author: riipah
title: Active directory integration with Episerver
excerpt: TODO
tags:
- programming
- Episerver
- Active Directory
- LDAP
---

## The problem

Recently I was tasked with enabling our customer to log in to Episerver (version 8) using their Windows Active Directory credentials. 
During the implementation I encountered multiple issues that aren't mentioned in the official documentation.
In the end, I ended up rewriting large parts of both the [ActiveDirectoryMembershipProvider](https://msdn.microsoft.com/en-us/library/system.web.security.activedirectorymembershipprovider) (built-in to .NET SDK) 
and [ActiveDirectoryRoleProvider](http://world.episerver.com/documentation/Class-library/?documentId=cms/8/49807A1D) (provided by Episerver).

In general, the documentation regarding AD integration seems to be spread in different blogs, so I decided to write about my experiences here, 
and hopefully it will be useful to someone else in the same situation

Now, about the issues encountered:

## Firewall ports

[The official documentation](http://world.episerver.com/documentation/Items/Developers-Guide/EPiServer-CMS/8/Security/Configuring-Active-Directory-membership-provider/) 
says that ports 389 and 445 both need to be opened. 
This was somewhat confusing. Port 389 is the main port for LDAP communication so that one is to be expected, but 445 is the port for SMB file transfer, 
usually only needed in LAN environments, and opening it could possibly be a security issue, so IT departments are generally very reluctant about opening that port. 
However, as expected, for one reason or another, that port really needs to be opened. 

First we tried with just the port 389, but this led to an error message "Workstation service is not started". Opening port 445 in the firewall fixed that.

## Searching users

Next, we noticed that searching users by name or email doesn't work at all. 

After some debugging it turned out that Episerver surrounds the keyword with SQL wildcards '%', which obviously doesn't work. 
In LDAP you need to use '** instead. You need to override the query methods in ActiveDirectoryMembershipProvider, 
replacing the '%' in the query with '*'.

```
public override MembershipUserCollection FindUsersByName(string usernameToMatch, int pageIndex, int pageSize, out int totalRecords)
{
    return base.FindUsersByName(usernameToMatch.Replace("%", "*"), pageIndex, pageSize, out totalRecords);
}
```

## Limits for the number of groups

LDAP (at least the Active Directory implementation) has a limit of 1000 entries per query. 
We hit that limit with groups, which led to Episerver not listing all groups in the AD, because ActiveDirectoryRoleProvider tries to load all groups 
and do the searching/pagination client side. 
I solved this by tweaking the LDAP query so that only specific groups are loaded, which also made it faster since a smaller number of entries is returned.

In general, searching for users and groups can be very slow if your AD has a large number of users and groups. 
At least the groups are cached after the first query, which unfortunately leads to...

## Caching problems with multiple active directories

As mentioned, Episerver caches results of AD queries, in a class called [AdsiDataFactory](http://world.episerver.com/documentation/Class-library/?documentId=cms/8/EEDB98B2).

Looking in decompiler, the cache key looks like this:
```
string cacheKey = "EPiServer:DirectoryServiceFindAll:" + filter + scope.ToString();
```
where *scope* is an enum value. It uses the query itself as the cache key, which works fine if you have just one AD.
But in our case, we had two ADs, which means two providers, and since the same queries are issued to both ADs, the results get cached only for the first one.

My solution was to override GetAllRoles in ActiveDirectoryRoleProvider.

```
public override string[] GetAllRoles()
{
    // For example (sAMAccountName=externals)(sAMAccountName=others)
    var groupsToGet = string.Join("", (ConfigurationManager.AppSettings["AD.GroupsToGet"] ?? string.Empty)
        .Split(new [] { "," }, StringSplitOptions.RemoveEmptyEntries)
        .Select(g => string.Format("({0}={1})", roleNameAttribute, g)));

    // AdsiDataFactory (DirectoryDataFactory) caches by query key. 
    // The extraCacheKey={1} part is needed to add provider name as part of the query to support multiple providers.
    var query = string.Format("(&(objectClass=group)(|{0}(extraCacheKey={1})))", groupsToGet, Name);

    // The rest is copied from the base class
}
```
where *groupsToGet* is a list of AD group names to be loaded. We're generating a custom LDAP query that filters by group names, and also appends the
provider name to the LDAP query so that it gets cached **per provider**.

## Group names with special characters

The last problem I encountered was about commas in AD group names, for example a group called "Cats, dogs and sheep" would not be identified.

I pinpointed the problem to how the names are encoded. In ActiveDirectoryRoleProvider there's this code:
```
private void GetRolesForUserRecursive(DirectoryData entry, List<string> roles, HashSet<string> visitedDirectoryEntry)
{
    string[] propertyValue1;
    if (!entry.TryGetValue("memberOf", out propertyValue1))
        return;
    foreach (string distinguishedName in propertyValue1)
    {
        DirectoryData entry1 = this.DirectoryDataFactory.GetEntry(distinguishedName);
        /* removed unnecessary code */
    }
}
```

The problem is that *DirectoryDataFactory.GetEntry* encodes the distinguishedName parameter, but the  distinguished name (DN)
returned by *entry.TryGetValue* is already encoded, so it gets encoded twice! This means the DN of the "Cats, Dogs and Sheep" group becomes
*CN=Cats\\\\, dogs and sheep,CN=Users,DC=dev,DC=ad* (notice the double backslash before the comma).

You need to override this method as well and somehow make it not double encode the DNs.

## Alternatives

Others told me they have implemented the integration using Active Directory Federation Services (ADFS) with better luck, so I'd look into that if possible. 
In our case the customer wasn't ready for ADFS quite yet, so we had to do the integration with LDAP. 
It's also possible to integrate with the AD using [WindowsMembershipProvider](http://world.episerver.com/documentation/Class-library/?documentId=cms/8/C3725E6D), 
if your frontend server is a member of the AD, which wasn't true in our case. I heard this is even more simple, but I have no first hand experience.