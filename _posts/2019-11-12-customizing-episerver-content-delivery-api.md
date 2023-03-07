---
layout: post
title: Customizing Episerver content delivery API.
author: demonru
excerpt: It was my first project with the use of Episerver as a Headless CMS. Episerver CMS supports such mode but requires some customization for the exact needs. 
categories: 
- EPiServer
tags:
- EPiServer
- API
- CMS
- DOTNET
---

## Episerver as Headless CMS
Episerver is a well known Content Management System (CMS). It officially supports working in a "headless CMS" mode. There is a bunch of [articles](https://world.episerver.com/documentation/developer-guides/content-delivery-api/) how to get started with it in this mode. In this article, I will be talking only about Content delivery API part of the CMS usage. Default Alloy template allows you to quickly get content API up and running, but the default output result is far from being perfect for real case usage and usually requires customization.

To demonstrate the problem I'll start by adding `EPiServer.ContentDeliveryApi.Cms` dependency to default [Alloy site](https://world.episerver.com/documentation/developer-guides/CMS/getting-started/install-a-sample-site/). With the default configuration you get predefined API endpoints and extensive output models. The endpoints support querying and searching content, authorization and works with friendly URLs. 

ProductPage class from the Alloy template site:
```csharp
namespace EpiAlloy.Models.Pages
{
    /// <summary>
    /// Used to present a single product
    /// </summary>
    [SiteContentType(
        GUID = "17583DCD-3C11-49DD-A66D-0DEF0DD601FC",
        GroupName = Global.GroupNames.Products)]
    [SiteImageUrl(Global.StaticGraphicsFolderPath + "page-type-thumbnail-product.png")]
    [AvailableContentTypes(
        Availability = Availability.Specific,
        IncludeOn = new[] { typeof(StartPage) })]
    public class ProductPage : StandardPage, IHasRelatedContent
    {
        [Required]
        [Display(Order = 305)]
        [UIHint(Global.SiteUIHints.StringsCollection)]
        [CultureSpecific]
        public virtual IList<string> UniqueSellingPoints { get; set; }

        [Display(
            GroupName = SystemTabNames.Content,
            Order = 330)]
        [CultureSpecific]
        [AllowedTypes(new[] { typeof(IContentData) },new[] { typeof(JumbotronBlock) })]
        public virtual ContentArea RelatedContentArea { get; set; }
    }
}
```

Once I retrieve it via content delivery API by calling for example `https://example.com/api/episerver/v2.0/content/6`, I get the following result:
```json
{
	"contentLink": {
		"id": 6,
		"workId": 0,
		"guidValue": "567a6012-5af2-4f26-a198-593326b80722",
		"providerName": null,
		"url": "/en/alloy-plan/"
	},
	"name": "Alloy Plan",
	"language": {
		"link": "/en/alloy-plan/",
		"displayName": "English",
		"name": "en"
	},
	"existingLanguages": [
		{
			"link": "/en/alloy-plan/",
			"displayName": "English",
			"name": "en"
		}
	],
	"masterLanguage": {
		"link": "/en/alloy-plan/",
		"displayName": "English",
		"name": "en"
	},
	"contentType": [
		"Page",
		"ProductPage"
	],
	"parentLink": {
		"id": 5,
		"workId": 0,
		"guidValue": "0b9c1a6e-129a-456b-ac3c-5a1b108362e0",
		"providerName": null,
		"url": "/en/"
	},
	"routeSegment": "alloy-plan",
	"url": "/en/alloy-plan/",
	"changed": "2019-10-28T14:26:13Z",
	"created": "2012-08-22T15:15:48Z",
	"startPublish": "2012-08-22T15:15:48Z",
	"stopPublish": null,
	"saved": "2019-10-28T14:26:13Z",
	"status": "Published",
	"category": {
		"value": [
			{
				"id": 3,
				"name": "Plan",
				"description": "Alloy Plan"
			}
		],
		"propertyDataType": "PropertyCategory"
	},
	"metaTitle": {
		"value": "Alloy Plan, online project management",
		"propertyDataType": "PropertyLongString"
	},
	"pageImage": {
		"value": {
			"id": 43,
			"workId": 0,
			"guidValue": "c04c11c5-4314-4fdc-b1b8-c3bfb9fdb9d8",
			"providerName": null,
			"url": null
		},
		"propertyDataType": "PropertyContentReference"
	},
	"teaserText": {
		"value": "Project management has never been easier!",
		"propertyDataType": "PropertyLongString"
	},
	"hideSiteHeader": {
		"value": null,
		"propertyDataType": "PropertyBoolean"
	},
	"metaDescription": {
		"value": "Project management has never been easier! Use Alloy Meet with Alloy Plan to get the whole team involved in the creation of project plans and see how this commitment translates into finite and achievable goals.",
		"propertyDataType": "PropertyLongString"
	},
	"hideSiteFooter": {
		"value": null,
		"propertyDataType": "PropertyBoolean"
	},
	"uniqueSellingPoints": {
		"value": [
			"Project planning",
			"Reporting and statistics",
			"Email handling of tasks",
			"Risk calculations",
			"Direct communication to members"
		],
		"propertyDataType": "PropertyStringList"
	},
	"mainBody": {
		"value": "<p><img style=\"float: left;\" src=\"/contentassets/89bccbae16d14665b08fac3525c9a999/alloyplanscreen.png\" alt=\"Alloy Plan - Efficient project planning\" /></p>\n<p>Planning is crucial to the success of any project. Alloy Plan takes into consideration all aspects of project planning; from well-defined objectives to staffing, capital investments and management support. Nothing is left to chance.</p>\n<p>Alloy Plan supports all project methodologies efficiently as the system is totally flexible in terms of setup and use.</p>\n<p>Realize the benefits of using Alloy Plan. Our customers see on average  an 80% increase in delivery of their projects on time, on budget and  with minimal risk involved.</p>\n<p>Work with an Alloy Technology partner to define the scale of your organization's needs and find the best fit with Alloy Plan.</p>",
		"propertyDataType": "PropertyXhtmlString"
	},
	"mainContentArea": {
		"value": [
			{
				"displayOption": "wide",
				"tag": null,
				"contentLink": {
					"id": 46,
					"workId": 0,
					"guidValue": "7026878a-a6e3-4916-811d-40bf3fd9b50b",
					"providerName": null,
					"url": null
				}
			},
			{
				"displayOption": "narrow",
				"tag": null,
				"contentLink": {
					"id": 28,
					"workId": 0,
					"guidValue": "2e90d62d-4abe-4c75-b87e-27817edad095",
					"providerName": null,
					"url": null
				}
			},
			{
				"displayOption": "narrow",
				"tag": null,
				"contentLink": {
					"id": 31,
					"workId": 0,
					"guidValue": "da738746-4912-4603-953c-d727f744fa91",
					"providerName": null,
					"url": null
				}
			}
		],
		"propertyDataType": "PropertyContentArea"
	},
	"relatedContentArea": {
		"value": [
			{
				"displayOption": "",
				"tag": null,
				"contentLink": {
					"id": 47,
					"workId": 0,
					"guidValue": "2dfadba3-31f8-45ac-9d80-6c8ff3a51b5e",
					"providerName": null,
					"url": null
				}
			},
			{
				"displayOption": "",
				"tag": null,
				"contentLink": {
					"id": 48,
					"workId": 0,
					"guidValue": "87d2fa31-712a-4dac-b57c-a369d28f149b",
					"providerName": null,
					"url": null
				}
			}
		],
		"propertyDataType": "PropertyContentArea"
	},
	"disableIndexing": {
		"value": null,
		"propertyDataType": "PropertyBoolean"
	}
}
```
The default output shows a lot of data. Fields like "existingLanguages", "masterLanguage", "changed", "created", "startPublish", "stopPublish" are probably not needed for the frontend. Other fields like "contentLink", "parentLink" are too intense in data and would be preferred as integer ids. At the same time, "mainContentArea" lists only content links but not its content. Also, if I would use `enum` somewhere as `propertyDataType`, it will be serialized as a number, while I would like it to be rendered as a string name. Most of the fields have value and `propertyDataType` options which is in most cases useless. For a boolean field, I would like to have only `fieldname : value`.

In a real project I would like to get something like this:
```json
{
  "ContentType": "ProductPage",
  "Url": "https://example.com/en/alloy-plan/",
  "MetaTitle": "Alloy Plan, online project management",
  "PageImage": {
    "ContentType": "ImageFile",
    "Url": "https://example.com/contentassets/89bccbae16d14665b08fac3525c9a999/alloyplan.png"
  },
  "TeaserText": "Project management has never been easier!",
  "HideSiteHeader": 1,
  "MetaDescription": "Project management has never been easier! Use Alloy Meet with Alloy Plan to get the whole team involved in the creation of project plans and see how this commitment translates into finite and achievable goals.",
  "HideSiteFooter": 0,
  "UniqueSellingPoints": [
    "Project planning",
    "Reporting and statistics",
    "Email handling of tasks",
    "Risk calculations",
    "Direct communication to members"
  ],
  "MainBody": "<p><img style=\"float: left;\" src=\"https://example.com/contentassets/89bccbae16d14665b08fac3525c9a999/alloyplanscreen.png\" alt=\"Alloy Plan - Efficient project planning\" /></p>\n<p>Planning is crucial to the success of any project. Alloy Plan takes into consideration all aspects of project planning; from well-defined objectives to staffing, capital investments and management support. Nothing is left to chance.</p>\n<p>Alloy Plan supports all project methodologies efficiently as the system is totally flexible in terms of setup and use.</p>\n<p>Realize the benefits of using Alloy Plan. Our customers see on average an 80% increase in delivery of their projects on time, on budget and with minimal risk involved.</p>\n<p>Work with an Alloy Technology partner to define the scale of your organization's needs and find the best fit with Alloy Plan.</p>",
  "MainContentArea": [
    {
      "ContentType": "TeaserBlock",
      "Heading": "Streamlined planning",
      "Text": "“Using Alloy Plan has saved time and money for our organization - but most importantly, has increased customer satisfaction greatly!” - Susan Peters, Trek Cyclery ",
      "Image": {
        "ContentType": "ImageFile",
        "Url": "https://example.com/contentassets/c427705fd91b4f62977f99ddbf55651f/susanpeters.jpg"
      }
    },
    {
      "ContentType": "StandardPage",
      "Url": "https://example.com/en/about-us/contact-us/",
      "MetaTitle": "Online demo, Alloy Track, Alloy Plan, Alloy Meet",
      "PageImage": {
        "ContentType": "ImageFile",
        "Url": "https://example.com/contentassets/5df93cf8473c426cbdf3c09c3668d57e/teaser_contactus.png"
      },
      "TeaserText": "Are you interested in our products?",
      "HideSiteHeader": -1,
      "MetaDescription": "Are you interested in our products and want to have more detailed information or perhaps an online demo?",
      "HideSiteFooter": -1,
      "MainBody": "<p>Please contact Todd Slayton, our VP Sales at: +46 8 123 457.</p>"
    },
    {
      "ContentType": "StandardPage",
      "Url": "https://example.com/en/how-to-buy/find-a-reseller/",
      "MetaTitle": "Alloy partner network, highly skilled project management concultancy companies worldwide",
      "PageImage": {
        "ContentType": "ImageFile",
        "Url": "https://example.com/contentassets/515c926b51da4862bc25041a4b18a049/teaser_findreseller.png"
      },
      "TeaserText": "Buy the Alloy Product suite now.",
      "HideSiteHeader": -1,
      "MetaDescription": "The Alloy product suite is implemented by our partner network. Our partners are  highly skilled project management consultancy companies with offices worldwide.",
      "HideSiteFooter": -1,
      "MainBody": "<p><img src=\"https://example.com/contentassets/515c926b51da4862bc25041a4b18a049/findreseller.png\" alt=\"Our worldwide partner network\" width=\"770\" height=\"429\" /></p>"
    },
    {
      "ContentType": "ImageFile",
      "Url": "https://example.com/contentassets/89bccbae16d14665b08fac3525c9a999/alloyplan.png"
    }
  ],
  "RelatedContentArea": [
    {
      "ContentType": "PageListBlock",
      "Heading": "Events",
      "IncludePublishDate": -1,
      "IncludeIntroduction": 1,
      "Root": {
        "ContentType": "NewsPage",
        "Url": "https://example.com/en/about-us/news-events/events/",
        "MetaTitle": "Alloy Events",
        "HideSiteHeader": -1,
        "MetaDescription": "Become more productive in your projects. Alloy offers numerous courses and seminars to help get you started or improve your proficiency.",
        "HideSiteFooter": -1,
        "MainContentArea": [
          {
            "ContentType": "StandardPage",
            "Url": "https://example.com/en/about-us/news-events/events/risk-management-in-complex-projects/",
            "MetaTitle": "Seminar on Risk Management in Complex Projects",
            "PageImage": {
              "ContentType": "ImageFile",
              "Url": "https://example.com/contentassets/3ddf25ae230748ebb831daddd741fd8c/patrickjones.png"
            },
            "TeaserText": "The theory behind risk management calculations.  ",
            "HideSiteHeader": -1,
            "MetaDescription": "The theory behind risk management calculations. ",
            "HideSiteFooter": -1,
            "MainBody": "<p>On completion of this seminar, you will be prepared to measure, assess and manage risk in your projects using Alloy Plan.</p>\n<hr />\n<p><img style=\"float: left;\" src=\"https://example.com/globalassets/events/patrick-jane_keynote.png\" alt=\"Patrick Jane, Risk Management Specialist\" />Key Note:</p>\n<h2>Patrick Jones</h2>\n<p>Risk Management Specialist</p>\n<p>Mr Jones has twenty years of experience in risk management. He has  been the leader of numerous large-scale, high-risk projects in various  industries.</p>\n<p>Don't miss this opportunity to learn from Patrick's expansive knowledge and wealth of experience.</p>",
            "MainContentArea": [
              {
                "ContentType": "EditorialBlock",
                "MainBody": "<hr />\n<h3>When and where?</h3>\n<p>Start: 09/10/2012 3:00:00 PM<br />End: 09/11/2012 3:30:00 PM<br />Address: Mandalay Bay Las Vegas</p>"
              }
            ]
          },
          {
            "ContentType": "StandardPage",
            "Url": "https://example.com/en/about-us/news-events/events/reporting-made-simple/",
            "MetaTitle": "Configure Alloy Track for all team members and define the reporting parameters, layout, and frequency of updates",
            "PageImage": {
              "ContentType": "ImageFile",
              "Url": "https://example.com/contentassets/b141002e0c5449cf942080e4b60d6ed0/reports.png"
            },
            "TeaserText": "No one likes writing reports, but everyone wants them. ",
            "HideSiteHeader": -1,
            "MetaDescription": "Alloy takes the pain out of writing reports and enables the delivery of key statistics to stakeholders and decision-makers. ",
            "HideSiteFooter": -1,
            "MainContentArea": [
              {
                "ContentType": "EditorialBlock",
                "MainBody": "<hr />\n<h3>When and where?</h3>\n<p>Start: 11/01/2012 1:00:00 PM<br />End: 11/01/2012 3:30:00 PM<br />Address: Mandalay Bay Las Vegas</p>"
              }
            ]
          }
        ]
      },
      "PageTypeFilter": "StandardPage"
    },
    {
      "ContentType": "PageListBlock",
      "Heading": "News",
      "IncludePublishDate": 1,
      "IncludeIntroduction": 1,
      "Root": {
        "ContentType": "NewsPage",
        "Url": "https://example.com/en/about-us/news-events/press-releases/",
        "MetaTitle": "Alloy Inc Press Releases",
        "HideSiteHeader": -1,
        "MetaDescription": "Alloy is a leading manufacturer of project management software. Read about our success stories, future plans and accolades here. ",
        "HideSiteFooter": -1,
        "MainContentArea": [
          {
            "ContentType": "ArticlePage",
            "Url": "https://example.com/en/about-us/news-events/press-releases/newworld-wildlife-fund-chooses-alloy/",
            "MetaTitle": "Alloy saves polar bears",
            "PageImage": {
              "ContentType": "ImageFile",
              "Url": "https://example.com/contentassets/34b56b481f1946f889915e1294316a6f/polarbearonice.png"
            },
            "TeaserText": "Alloy products to save endangered species.",
            "HideSiteHeader": -1,
            "MetaDescription": "Alloy products have contributed to higher success rates of complex projects to save endangered species. World Wildlife Fund chooses Alloy to help save polar bears.",
            "HideSiteFooter": -1,
            "MainBody": "<p><strong>Huntsville AL – February 8, 2012</strong></p>\n<p>Alloy Technologies, the leader in collaborative project management, today announced that the World Wildlife Fund has used Alloy Technologies to improve the success rate of complex five nation resource efforts. The use of Alloy Meet, Alloy Plan, and Alloy Track has helped save over 200 polar bears in the project spanning Canada, Norway, Sweden, Finland and Russia.</p>\n<p><img src=\"https://example.com/contentassets/34b56b481f1946f889915e1294316a6f/polarbearonice.png\" alt=\"World Wildlife Fund chooses Alloy to save polar bears\" /></p>"
          }
        ]
      },
      "PageTypeFilter": "ArticlePage"
    },
    {
      "ContentType": "ImageFile",
      "Url": "https://example.com/contentassets/89bccbae16d14665b08fac3525c9a999/alloyplanscreen.png"
    }
  ],
  "AnotherColumnsNumber": "Two",
  "Rows": "Three",
  "Breadcrumb": [
    "Top",
    "Sub",
    "Bottom"
  ]
}
```
All URLs are absolute, only needed fields listed, data follows key-value principle wherever possible without data type attributes, extra field added. So, it's obvious that some customization is needed.

### Content data flow
Before I dive into different ways of customizing results, let me quickly show how `PageData` gets transformed into the JSON seen above in Episerver:

![Content delivery API flow](/img/customizing-episerver-content-delivery-API/ContentDeliveryAPI_flow.png)

Detailed description of the [serialization](https://world.episerver.com/documentation/developer-guides/content-delivery-api/serialization/) is available on the Episerver site. At the same time, it's not clear how to use this info to tune the resulting model, so I'll elaborate it.

So far I've found the following ways to customize content delivery API results:
* Customize content model serialization within content delivery API flow
	* Attributes
	* Property Model mappers
	* Custom `IContentModelMapper` implementation
	* Output model filtering
* Create custom controller

### JSON attributes
The first and simplest way to modify the final model is to hide some of ContentData properties. It can be easily done with `[JsonIgnore]` attribute. Just decorate a property with it and would be ignored in the resulting model. `ContentModelMapperBase` checks properties via reflection for the attribute during ContentApiModel building and ignores if it's present. 

```csharp
	[JsonIgnore]
	[Display(
		GroupName = SystemTabNames.Content,
		Order = 330)]
	[CultureSpecific]
	[AllowedTypes(new[] { typeof(IContentData) },new[] { typeof(JumbotronBlock) })]
	public virtual ContentArea RelatedContentArea { get; set; }
```
And that's it. That's the only attribute that is checked by `ContentModelMapperBase`. So I couldn't get anything more useful out of it. 

### Property Model mappers
The second way to wedge into the model building process is to implement and register custom property models. That is a fine-tuning mechanism that changes how a property type is serialized. As one can get it from the name it applies only to custom properties of the page data and does not have any influence on the internal properties of the IContent object. It does not affect the visibility of the property in the final model either.

Create an implementation of `IPropertyModel` interface or derive an existing one. As an example, I've changed rendering for Boolean values from "null, true, false" to "-1, 1, 0":
```csharp
    public class CustomBooleanPropertyModel : PropertyModel<int, PropertyBoolean>
    {
        public CustomBooleanPropertyModel(PropertyBoolean propertyBoolean)
            : base(propertyBoolean)
        {
            this.Value = propertyBoolean.Boolean.HasValue ? Convert.ToInt32(propertyBoolean.Boolean.Value) : -1;
        }
    }
```
This customization will be auto-magically picked up by Episerver. There is no need to register this model anywhere else. 

#### Making URLs absolute in XHtmlString properties
Make image and file URLs absolute in texts. Not the best way, but so far, the most elegant that I was able to find. 
```csharp
    public class CustomXHtmlPropertyModel : XHtmlPropertyModel
    {
        private const string GlobalAssetsPath = "/globalassets/";
        private const string ContentPath = "/contentassets/";
        private static readonly string AbsoluteGlobalUrl = UriSupport.AbsoluteUrlBySettings(GlobalAssetsPath);
        private static readonly string AbsoluteContentUrl = UriSupport.AbsoluteUrlBySettings(ContentPath);

        public CustomXHtmlPropertyModel(PropertyXhtmlString propertyXhtmlString, bool excludePersonalizedContent) 
            : base(propertyXhtmlString, excludePersonalizedContent)
        {
            this.Value = ParseUrlsToMakeAbsolute( _xHtmlStringPropertyRenderer.Service.Render(propertyXhtmlString, excludePersonalizedContent));
        }

        private string ParseUrlsToMakeAbsolute(string content)
        {
            // replace relative part of the path with absolute part.
            return content.Replace(GlobalAssetsPath, AbsoluteGlobalUrl)
                .Replace(ContentPath, AbsoluteContentUrl);
        }
    }
```
As a result, XHtmlProperties will contain absolute URLs in its value:
```json
	"mainBody": {
		"value": "<p><img style=\"float: left;\" src=\"https://example.com/contentassets/89bccbae16d14665b08fac3525c9a999/alloyplanscreen.png\" alt=\"Alloy Plan - Efficient project planning\" /></p>\n<p>Planning is crucial to the success of any project. Alloy Plan takes into consideration all aspects of project planning; from well-defined objectives to staffing, capital investments and management support. Nothing is left to chance.</p>\n<p>Alloy Plan supports all project methodologies efficiently as the system is totally flexible in terms of setup and use.</p>\n<p>Realize the benefits of using Alloy Plan. Our customers see on average  an 80% increase in delivery of their projects on time, on budget and  with minimal risk involved.</p>\n<p>Work with an Alloy Technology partner to define the scale of your organization's needs and find the best fit with Alloy Plan.</p>",
		"propertyDataType": "PropertyXhtmlString"
	},
```
This can be very helpful if the frontend is hosted on a different domain.

#### Expanding ContentAreaPropertyModel
A very useful case is where a model expands content areas. 
```csharp
    public class CustomContentAreaPropertyModel: ContentAreaPropertyModel
    {
        public CustomContentAreaPropertyModel(PropertyContentArea propertyContentArea, bool excludePersonalizedContent)
            : base(propertyContentArea, excludePersonalizedContent)
        {
        }
        /// <summary>
        /// Here we override Expand behaviour of this model and expands all level 
        /// </summary>
        protected override IEnumerable<ContentApiModel> ExtractExpandedValue(CultureInfo language)
        {
            var expandedValue = new List<ContentApiModel>();
            var contentReferences = Value.Where(x => x.ContentLink != null).Select(x => new ContentReference(x.ContentLink.Id.Value));
            var content = _contentLoaderService.GetItems(contentReferences, language).ToList();
            var principal = ExcludePersonalizedContent ? _principalAccessor.GetAnonymousPrincipal() : _principalAccessor.GetCurrentPrincipal();
            var filteredContent = content.Where(x => _accessEvaluator.HasAccess(x, principal, AccessLevel.Read)).ToList();
            filteredContent.ForEach(x => expandedValue.Add(_contentModelMapper.TransformContent(x, ExcludePersonalizedContent, "*")));
            return expandedValue;
        }
    }
```
To make it work I would need to register this `CustomContentAreaPropertyModel` in a `CustomPropertyModelConverter`, though `PropertyContentArea` is a known type for Episerver. There is also one more gotcha - the `ConvertToPropertyModel` will always get incoming parameter `expand` with value `false` unless I would specify it in the API request. I wanted it to expand always for the ContentAreas. Without messing with invocations of the method, I've decided to ignore the `expand` input and to expand in all cases in the overridden version of the `ConvertToPropertyModel` method.
<a name="ConvertToPropertyModel"></a>
```csharp
    [ServiceConfiguration(typeof(IPropertyModelConverter), Lifecycle = ServiceInstanceScope.Singleton)]
    public class CustomPropertyModelConverter2 : DefaultPropertyModelConverter
    {
        public override int SortOrder { get; } = 200;

        protected override IEnumerable<TypeModel> InitializeModelTypes()
        {
            var typeList = new List<TypeModel>
            {
                new TypeModel
                {
                    PropertyType = typeof(PropertyContentArea),
                    ModelType = typeof(CustomContentAreaPropertyModel),
                    ModelTypeString = typeof(CustomContentAreaPropertyModel).FullName
                },
            };
            return typeList;
        }
        
        public override IPropertyModel ConvertToPropertyModel(
            PropertyData propertyData,
            CultureInfo language,
            bool excludePersonalizedContent,
            bool expand = false)
        {
            if (propertyData == null)
                return (IPropertyModel)null;
            TypeModel typeModel = this.ModelTypes.FirstOrDefault<TypeModel>((Func<TypeModel, bool>)(x => x.PropertyType == propertyData.GetType()));
            if (typeModel == null)
                return (IPropertyModel)null;
            IPropertyModel instance;
            if (typeof(IPersonalizableProperty).IsAssignableFrom(typeModel.ModelType))
                instance = (IPropertyModel)this._reflectionService.CreateInstance(typeModel.ModelType, (object)propertyData, (object)excludePersonalizedContent);
            else
                instance = (IPropertyModel)this._reflectionService.CreateInstance(typeModel.ModelType, (object)propertyData);
            // if (expand) - I want it to expand always 
                (instance as IExpandableProperty)?.Expand(language);
            return instance;
        }
    }
```
As a result, all ContentArea properties will be expanded and all content of the referenced blocks and pages will be listed. 

#### Enum property model 1
Customizing rendering for enum values, i.e. as strings. I've found at least two ways to do it. First is a "quick and dirty" option. 
For a property of enum type in IContent of type ProductPage:
```csharp
        [Display(
            GroupName = SystemTabNames.Content,
            Name = "RowsEnum number",
            Order = 340)]
        public virtual RowsEnum RowsEnum { get; set; }
```
The default rendering format is number:
```json		
	"rows": {
		"value": "3",
		"propertyDataType": "PropertyNumber"
	}
```
This property model gives me fine control over the value:
```csharp
    public class EnumNumberPropertyModel : PropertyModel<string, PropertyNumber>
    {
        public EnumNumberPropertyModel(PropertyNumber propertyEnumNumber) : base(propertyEnumNumber)
        {
            if (propertyEnumNumber.IsNull) return;

            switch (propertyEnumNumber.Name)
            {
                case nameof(ProductPage.RowsEnum):
                    if (Enum.TryParse<RowsEnum>(PropertyDataProperty.Value.ToString(), out var result))
                    {
                        Value = result.ToString();
                    }
                    break;
                default:
                    Value = PropertyDataProperty.Value.ToString();
                    break;
            }
        }
    }
```
Result:
```json
	...
	"rows": {
		"value": "Three",
		"propertyDataType": "PropertyNumber"
	},
	...
```
The drawback of this method is that it would try to convert all numbers, and I had to limit it by checking the name of the property.

#### Enum property model 2
A better way to do it is to use custom property types. That requires more effort but gives a more reliable implementation. 
Property in class:
```csharp
        [Display(
            GroupName = SystemTabNames.Content,
            Name = "Column Number",
            Order = 350)]
        [BackingType(typeof(EnumProperty))]        
        public virtual Columns AnotherColumnsNumber { get; set; }
```  
Custom property type:
```csharp
    [PropertyDefinitionTypePlugIn]
    public class EnumProperty : PropertyNumber
    {
        public override object Value {
            get => Number.HasValue ?(Columns)Number.Value : Columns.One;
            set => this.Number = (int)Enum.Parse(typeof(Columns), value.ToString());
        }

        public override Type PropertyValueType => typeof(Columns);

        public override object SaveData(PropertyDataCollection properties)
        {
            return base.Number;
        }
    }
```
By default, custom property types do not have any matching propertyModels, so as a result there the value will be missing in the response.
Property model:
```csharp
    public class EnumPropertyModel : PropertyModel<string, EnumProperty>
    {
        public EnumPropertyModel(EnumProperty propertyEnum) : base(propertyEnum)
        {
            if (propertyEnum.IsNull) return;

            Value = PropertyDataProperty.Value.ToString();
        }
    }
```

The model for custom property type requires additionally a registration: 
```csharp
    [ServiceConfiguration(typeof(IPropertyModelConverter), Lifecycle = ServiceInstanceScope.Singleton)]
    public class CustomPropertyModelConverter : DefaultPropertyModelConverter
    {
        public CustomPropertyModelConverter()
        {
            ModelTypes = new List<TypeModel>
            {
                new TypeModel
                {
                    ModelType = typeof(EnumPropertyModel), ModelTypeString = nameof(EnumPropertyModel), PropertyType = typeof(EnumProperty)
                }
            };
        }
        public override int SortOrder { get; } = 100;
    }
```
The result value is like the first method, but coding implementation is solid and strongly typed. 
```json
	...
	"anotherColumnsNumber": {
		"value": "Two",
		"propertyDataType": "EnumProperty"
	},
	...
```
The only sad limitation with the PropertyModels is that it works only for custom properties. The built-in properties of the `PageData` are not affected by these customizations. So, "we need to go deeper".

### Working with ContentModelMapper 
`IContentModelMapper` implementation is the key place to tweak built-in `PageData` properties. It gives full control over the way `ContentApiModel` is built and its properties are converted and mapped. 
The easiest way is to derive from `DefaultContentModelMapper` and override one or several virtual methods of `ContentModelMapperBase`. I did override `ResolveUrl` method in my `CustomContentModelMapper` to make URLs absolute:
```csharp
    [ServiceConfiguration(typeof(IContentModelMapper), Lifecycle = ServiceInstanceScope.Singleton)]
    public class CustomContentModelMapper : DefaultContentModelMapper
    {
        public CustomContentModelMapper(
            IContentTypeRepository contentTypeRepository,
            ReflectionService reflectionService,
            IContentModelReferenceConverter contentModelService,
            IEnumerable<IPropertyModelConverter> propertyModelConverters,
            IContentVersionRepository contentVersionRepository,
            ContentLoaderService contentLoaderService,
            UrlResolverService urlResolverService
        ) : base(
            contentTypeRepository,
            reflectionService,
            contentModelService,
            propertyModelConverters,
            contentVersionRepository,
            contentLoaderService,
            urlResolverService)
        {
        }

        public override int Order => 200; // Any number larger than default which equals to 100.

        protected override string ResolveUrl(ContentReference contentLink, string language)
        {
            string resolvedUrl;
            if (this._urlResolver == null)
            {
                resolvedUrl = this._urlResolverService.ResolveUrl(contentLink, language);
            }
            else
            {
                resolvedUrl = this._urlResolver.GetUrl(contentLink, language, new UrlResolverArguments()
                {
                    ContextMode = ContextMode.Default,
                    ForceCanonical = true
                });
            }
            return string.IsNullOrEmpty(resolvedUrl) ? null : UriSupport.AbsoluteUrlBySettings(resolvedUrl);
        }
    }
```
This makes URLs in built-in properties absolute:
```json
	...
	"url": "https://example.com/en/alloy-plan/",
	...
``` 
Another option can be to tweak `AddToPropertyMap` where converted properties are added to the dictionary of the resulting model. `ExtractPropertyDataCollection` contains the invocation of the [ConvertToPropertyModel](#ConvertToPropertyModel) method, so instead of tweaking the method, I could have changed the invocation parameters here.

And it's also always possible to create your custom implementation of `IContentModelMapper` where it's possible to do everything in the way you want it to be. A good [example](https://github.com/episerver/musicfestival-vue-template/blob/master/src/MusicFestival.Vue.Template/Models/ExtendedContentModelMapper.cs) is available in another Episerver site template. It has a nice implementation of model flattening. 

The only limitation which all IContentModelMapper implementations have is that the resulting object will be of type `ContentApiModel`. So, all extra fields that I wanted to hide will stay in the result anyway. That is a place where model filtering customization comes into action.

### Output model filtering
Model filtering is a way to remove properties from the data returned by the Content Delivery API. It is done by filtering out properties in a custom `ContentResultService` as [recommended by Episerver](https://world.episerver.com/documentation/developer-guides/content-delivery-api/how-to-customize-data-returned-to-clients/). That is a very powerful way to shrink your model because you can decide yourself which fields will stay. 
Before the discovery of `ContentModelMapperBase` capabilities, I was using model filtering as my main model formatting tool. I used Episerver's sample a base and changed it quite heavily to go recursively over the expanded fields. 
```scharp
    [ServiceConfiguration(typeof(ContentResultService))]
    public class CustomContentResultService : ContentResultService
    {
        public CustomContentResultService(IContentApiSerializer contentApiSerializer) : base(contentApiSerializer)
        {
        }
        /// <summary>
        /// Build string content from object use given serializer
        /// (1) Only return needed fields to clients (2) Only applied for content api not search api
        /// </summary>
        public override StringContent BuildContent(object value)
        {
            if (!(value is ContentApiModel))
            {
                return base.BuildContent(value);
            }

            var convertedObj = ReduceFields(value);
            return base.BuildContent(convertedObj);
        }


        private readonly string[] _excludedProperties =
		{
            "Id", "Name", "WorkId","GuidValue","ProviderName","ContentLink","Language",
            "ExistingLanguages","MasterLanguage","ParentLink","Changed","Created",
            "StartPublish","StopPublish","Saved","Status","Category","ExcludeFromSearch",
            "NavigationTitle","PropertyDataType", "PropertyDataProperty", "DisplayOption",
            "ExcludePersonalizedContent", "RouteSegment", "disableIndexing", "recursive", 
            "count", "sortOrder", "categoryFilter"
        };

        private bool ShouldIncludeProperty(string property)
        {
            return !_excludedProperties.Any(prop => string.Equals(prop, property, StringComparison.InvariantCultureIgnoreCase));
        }

        public IDictionary<string, Object> ReduceFields(object model)
        {
            var convertedObj = new ExpandoObject() as IDictionary<string, Object>;
            foreach (var prop in model.GetType().GetProperties())
            {
                var propertyType = prop.PropertyType;
                // expand generic dictionary
                if (propertyType.IsGenericType && propertyType.GetGenericTypeDefinition() == typeof(IDictionary<,>))
                {
                    var propertyDataDict = prop.GetValue(model, null);
                    foreach (KeyValuePair<string, object> item in propertyDataDict as IDictionary<string, object>)
                    {
                        var dictReducedResult = GetFieldValue(item.Key, item.Value, item.Value.GetType());
                        if (dictReducedResult.HasValue)
                        {
                            convertedObj.Add(dictReducedResult.Value);
                        }
                    }
                    continue;
                }

                // expand IEnumerable
                if (!propertyType.IsString() && propertyType.GetInterfaces().Contains(typeof(IEnumerable)))
                {
                    var resultArray = new List<object>();

                    var propertyValue = prop.GetValue(model, null);
                    if (propertyValue == null)
                    {
                        continue;
                    }

                    foreach (object item in (IEnumerable)propertyValue)
                    {
                        var dictReducedResult = GetFieldValue(prop.Name, item, item.GetType());
                        if (dictReducedResult.HasValue)
                        {
                            if (dictReducedResult.Value.Value is IDictionary<string, object> reducedValue && reducedValue.Count == 0)
                            {
                                continue;
                            }

                            resultArray.Add(dictReducedResult.Value.Value);
                        }
                    }

                    if (resultArray.Count > 0)
                    {
                        convertedObj.Add(prop.Name, prop.Name == "ContentType" ? resultArray.Last() : resultArray);
                    }
                    continue;
                }

                var reducedResult = GetFieldValue(prop.Name, prop.GetValue(model, null), propertyType);
                if (reducedResult.HasValue)
                {

                    convertedObj.Add(reducedResult.Value);
                }
            }

            return convertedObj;
        }

        private KeyValuePair<string, object>? GetFieldValue(string fieldName, object value, Type propertyType)
        {
            if (!ShouldIncludeProperty(fieldName)
                || value == null
                || (value is PropertyData propertyValue && propertyValue.IsNull)
                || (value is string stringValue) && string.IsNullOrEmpty(stringValue))
            {
                return null;
            }

            if (!propertyType.IsValueType && !propertyType.IsString())
            {
                var subResult = ReduceFields(value);
                if (subResult.Count == 0)
                {
                    return null;
                }
                if (IsFlatteningRequired(subResult))
                {
                    return new KeyValuePair<string, object>(fieldName, subResult.First().Value);
                }
                return new KeyValuePair<string, object>(fieldName, subResult);
            }
            else if (propertyType.IsEnum)
            {
                return new KeyValuePair<string, object>(fieldName, value.ToString());
            }
            else
            {
                return new KeyValuePair<string, object>(fieldName, value);
            }
        }

        private bool IsFlatteningRequired(IDictionary<string, object> subResult)
        {
            var fieldsToFlatten = new[] { "Value", "ExpandedValue" };
            return subResult.Count == 1 &&
                   fieldsToFlatten.Any(fieldName => string.Equals(fieldName, subResult.Keys.First(), StringComparison.InvariantCultureIgnoreCase));
        }
    }
```
This service should be registered in Initialization module in order to be picked up instead of the default one. This way I ended up having a nicer model with only those fields that I found valuable for the frontend app.


### Custom controller 
In my case, I had some special requirements regarding the request URLs, authorization, output model and model properties serialization. So, I decided to create my controller. Thanks to the guys from Episerver with the use of the IoC principle it's easy to reuse the Content Delivery components whenever you need them. Here is a quick sample just to illustrate that it's easily doable. The actual implementation is more complicated:
```csharp
    [RoutePrefix("api/v1/page")]
    public class CustomContentController : ApiController
    {
        private readonly IUrlResolver _urlResolver;
        private readonly IContentModelMapper _mapper;
        private readonly CustomContentResultService _contentResultService;

        public CustomContentController(IUrlResolver urlResolver, IContentModelMapper mapper, CustomContentResultService contentResultService)
        {
            _urlResolver = urlResolver;
            _mapper = mapper;
            _contentResultService = contentResultService;
        }

        [HttpGet]
        [Route]
        public IHttpActionResult Get([FromUri]string pageName)
        {
            // get the page content someway
            UrlBuilder urlBuilder = new UrlBuilder($"https://example.com/en/{pageName}");
            IContent content = _urlResolver.Route(urlBuilder, ContextMode.Default);

            // Transform IContent to ContentApiModel
            ContentApiModel model = _mapper.TransformContent(content, false, "*");

            // Filter out fields that are not needed
            IDictionary<string, object> reducedModel = _contentResultService.ReduceFields(model);

            // Add a custom field
            reducedModel.Add("Breadcrumb", new []{ "Top", "Sub", "Bottom"});

            return Ok(reducedModel);
        }
    }
```
It also gave me an ability to add a custom breadcrumb field to the final model.
The drawback is that you are now on your own, and need to worry yourself about request model validation, authorization, and some epi services that might not be invoked anymore.
If you decide to go for your controller, do not forget to disable the original Episerver's content delivery endpoints.
```csharp
    [ModuleDependency(typeof(ContentApiCmsInitialization))]
    public class ExtendedContentApiCmsInitialization : IConfigurableModule
    {
        public void Initialize(InitializationEngine context)
        {
        }
        public void Uninitialize(InitializationEngine context)
        {
        }
        public void ConfigureContainer(ServiceConfigurationContext context)
        {
            context.Services.Configure<ContentApiConfiguration>(config =>
            {
                config.Default()
                    .SetSiteDefinitionApiEnabled(false)
                    .SetMultiSiteFilteringEnabled(false);
            });
        }
    }
```
## Sum 
Now when I've written all this, the whole process looks very straightforward and easy. It was not that obvious when I started with it. For a long period, I was considering dropping the use of Episerver's content delivery API classes and do everything myself. It might have even taken less time. Anyway, now I feel quite comfortable with the level of control that I have over the models. I hope this article might save some time for others.