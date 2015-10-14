---
layout: post
title: Writing automated tests for EPiServer websites
author: riipah
excerpt: What to test on the server side and how to test code interacting with the content repository
---

I'm a big fan of automated testing, having had good experiences with keeping complex pieces of software maintainable by having a comprehensive automated test suite. 
When developing websites based on a CMS platform such as [EPiServer CMS](http://www.episerver.com/), or another similarly complex platform, I often hear opinions saying it's too difficult and not worth the effort. 
However, almost all CMS-based sites have some custom business logic, some more than others, and whenever there's custom logic, there's code that can break when changes are made, 
so regression tests are needed.

Note: if you already know enough about automated testing and EPiServer you can skip straight to the last chapter.

## What to test?

The point of this post is not to explain why automated testing should be done, or how to write tests in general. 
I'm also not going to talk about the technical differences between various types of testing, such as unit vs. integration testing. 

That said, I will start by saying that there's a lot of code that doesn't need to be tested directly:
Anything that can be considered trivial or boilerplate code, such as class constructors, accessors and loops in views for example.
On a CMS website this includes the content type definitions. This code is unlikely to contain bugs by itself, 
and it will get tested indirectly together with other tests.

On a typical CMS website, some examples of good candidates for automated tests on the server side are:

* Algorithms, such as calculating store opening hours based on a set of rules.
* Systems integration code, such as XML/JSON/CSV parsing and processing.
* Database queries and mappings.
* Any sufficiently complex code that deals with the site structure, such as crawling and listing pages.

## Testing EPiServer-specific code

When working with EPiServer websites, large parts of the code tend to be involved with the EPiServer database, 
which is managed through the content repository. Usually this consists of creating and saving content, or traversing the content tree. 
Testing against the full CMS, as with any system that contains a database, is slow and fragile - there's simply too much initialization and too many moving parts.
For majority of your tests, you need to break dependencies to that database and any other external interfaces such as web APIs.

The content repository (*IContentRepository*), as well as most of the core types in EPiServer, are nowadays provided as interfaces.
They are injected to wherever they are needed, so they can be mocked, either by hand or by using a mock framework such as [Moq](https://github.com/Moq/moq4).
However, I dislike mocking such low-level general purpose interfaces, because as the code is refactored and new features added, 
it tends to be those low level details that change the most frequently, making such tests fragile. 
Mocking more complex interfaces such as EPiServer Find or Entity Framework is even worse.

For example, consider code that loads content with *Get<T>(ContentReference)* and you mock that method to return a fixed value. 
That call in code could easily be changed to *TryGet* or even *GetItems*, breaking your test setups. Even worse, the code might make multiple calls to that *Get* method
with different parameters so you'd have multiple setups returning different values based on the parameter, which easily becomes complicated.

In order to make such code more testable, I've used two different strategies:

* Creating another layer of abstraction between the code and the content repository.
* Using a simplified in-memory implementation of the content repository that mimics the behavior of the original EPiServer content repository. This is also called a "fake".

## Writing an abstraction layer

For example, let's say you have code that deals with product pages on an EPiServer website. 
You can make that code manage product pages through an interface called *IProductPageRepository*, with methods for listing, loading and saving those pages. 
This interface should be easier to mock since it contains a limited number of higher level methods. Additionally, since the actual method of persisting the pages is now abstracted,
the implementation of this page repository could be changed to use EPiServer Find or a custom SQL database instead of the EPiServer content repository.

The main drawback of course is that writing such abstraction layers is additional work, it might complicate your overall architecture, 
and you're going to need a lot of them if you have plenty of content types. Additionally, you're still tied to how the interface is
being called (such as whether the code requests a single item or a list), even if it's higher abstraction level with less options. 

The earlier EPiServer testing libraries I've seen ([EPiAbstractions](https://github.com/MikeHook/EPiAbstractions) 
and [EPiServer-FakeMaker](https://github.com/DavidVujic/EPiServer-FakeMaker)) are mainly based on mocking and abstractions, 
so to overcome the limitations mentioned above I decided to try faking the content repository instead.

## Faking the content repository (finally some code)

Majority of the methods provided by the *IContentRepository* interface are pretty straightforward CRUD (Create, Read, Update, Delete) operations.
I decided to write a fake implementation of that interface which persists the saved content in memory and attempts to mimic the behavior of EPiServer's content repository as
closely as needed, without actually requiring the EPiServer context to be initialized.

The contents in my *FakeContentRepository* are saved in a dictionary, where the key is the content ID. 

```
public class FakeContentRepository : IContentRepository
{
    private readonly Dictionary<ContentReference, IContent> contents 
        = new Dictionary<ContentReference, IContent>();    
    ...
}
```

When saving content using the the save method, it checks if the content to be saved already has an ID, and if not, a new ID is assigned.

```
public ContentReference Save(IContent content, SaveAction action, AccessLevel access)
{            
    if (ContentReference.IsNullOrEmpty(content.ContentLink))
    {
        content.ContentLink = new ContentReference(id++);
    }

    if (contents.ContainsKey(content.ContentLink)) {
        contents[content.ContentLink] = content;
    } else
    {
        contents.Add(content.ContentLink, content);
    }

    return content.ContentLink;
}
```

Obviously this is skipping things like content events and versioning, but you can easily extend the method if your code depends on those features.

Implementing (simplified versions) of GetItems, Delete and GetChildren methods was very straightforward.

```
public void Delete(ContentReference contentLink, bool forceDelete, AccessLevel access)
{
    if (contents.ContainsKey(contentLink))
        contents.Remove(contentLink);
}  
    
public IEnumerable<T> GetChildren<T>(ContentReference contentLink) where T : IContentData
{
    return contents.Values.Where(c => c.ParentLink == contentLink).OfType<T>();
}

public IEnumerable<IContent> GetItems(IEnumerable<ContentReference> contentLinks, CultureInfo language)
{
    var items = contents.Values.Where(c => contentLinks.Contains(c.ContentLink));
    return items;
}      
```

Creating new content with the GetDefault method is a bit more interesting. 
For that I took inspiration from the [CreatePage class](https://github.com/MikeHook/EPiAbstractions/blob/master/EPiAbstractions.FixtureSupport/CreatePage.cs) 
in [EPiAbstractions](https://github.com/MikeHook/EPiAbstractions). 
Additionally, I implemented a similar CreateSharedBlock class for creating instances of shared blocks using EPiServer's 
[SharedBlockFactory](http://world.episerver.com/documentation/Class-library/?documentId=cms/9/B79494A8).

With these methods you have a sufficiently working implementation of EPiServer's content repository which is able to create, save, load and delete
pages and shared blocks. You can then inject this fake implementation into your code under test, possibly through that abstraction layer mentioned earlier.
Compared to simply mocking the content repository, you can now use the standard Save method for providing your test data, and it doesn't matter whether the
code under tests loads that data using the *Get*, *GetItems* or *TryGet* methods. Or if the code first adds items and then deletes those items, the results are updated correctly. 
Then after test, instead of recording which method was called, you can simply
check the contents of the repository, because that's what we're really interested in: the end result. Everything happening in between is just implementation details.

For example, consider testing article import that saves the articles as ArticlePages in the content repository:

```
[TestMethod]
public void TestArticleImport()
{            
    var contentRepository = new FakeContentRepository();
    var importer = new ArticleImporter(contentRepository, ...);
    importer.Import(fileStream);

    var articles = contentRepository.Contents.OfType<ArticlePage>();
    Assert.AreEqual(2, articles.Count(), "Number of articles imported");
}    
```