layout: post
title: I challenged low-code with code
author: hnybom
excerpt: >

tags:
 - Low code
 - OutSystems
 - Spring
 - Vaadin
 - Kotlin

# Low-codecalypse

Low-code platforms will account for 65% of application development by 2024 says Gartner 

> https://venturebeat.com/2021/02/14/no-code-low-code-why-you-should-be-paying-attention/

Development with the low-code platforms is stated to be 5 to 7 times faster than traditional development. Time to apply for early retirement I guess, so long and thanks for all the fishes!

Well...maybe, just maybe there is still a chance for us traditional devs as well. There are fast catalog of open source components that do similar things that low code does. In this blog I'm going to write a simple web application with productivity boosting OS components. The application will be a web application for game high scores. Basically it will have a list of games and their high scores.

## Quick word about low-code

In this blog I'm going to use OutSystems as the representation for low-code platforms. OutSystems is a platform I've used and I also have a OutSystems developer certificate. So I do know something about it. The intention of this blog is not to undersell low-code in any way. On the contrary I feel that OutSystems at least can do many things very well, not all, but many.

If the subject matter is not familiar, low-code platforms are usually graphical based programming where many common features come out of the box. Following picture depicts the what low-code logic programming looks like with OutSystems

![Outsystems code flow](../img/i-challenged-low-code-with-code/low-code-flow.jpg)

***OutSystems logic diagram***

From these graphical presentations OutSystems creates C# code and jQuery / React web application. If you're interested to learn more, OutSystems provides a free developer environment to test out the platform and in my opinion one of the best practice materials I've come across:

>  https://www.outsystems.com/training/paths/

The aspects of OutSystems that I'm going to focus on are the following

- **Data layer**
  - Automatic creation of CRUD database calls, OutSystems creates these operations automatically for all DB entities
- **UI layer**
  - Fast visual UI creation using components and scaffolding
- **Logic layer**
  - Graphical logic implementation
- **Deployment** 
  - pipeline with environments out of the box

I'll try to challenge each of these with my code based solution.

## A challenger appears

To challenge the the speed of low-code I'm going to need some help. So I'm going to use the following stack to develop at speed.comparison

* **Vaadin** **flow** for UI 
* **Spring boot** for backend server
* **Spring data JDBC** for DB access
* **Kotlin** as the programming language

To get started I need to do some work to be even able to code anything. I'm already lacking behind OutSystems' out of the box development.

**Creating project skeleton**

To save some time I'm going to use spring initializr web app (https://start.spring.io/) to generate the needed skeleton for the project. 

![Spring initilzr](../img/i-challenged-low-code-with-code/spring-init.png)

***Spring initializr UI***

In the initilizr you just fill in the information about the project and select languages and dependencies you want to use. After that you just download the skeleton as a zip-file and of you go. 

**Development environment**

In OutSystems the development is always done in the cloud environment. This has multiple implications

* No need to setup anything 
* The environment is shared with all the developers
* Internet connection is needed for the development

For my application development I really do want a local dev environment that can be easily debugged and tested. Spring boot is pretty self contained but what is needed is a database. For this I'll use docker compose to quickly get a local testing portgresql database.

```
version: "3.7"
services:
  low-code-postgres:
    container_name: low-code-postgres
    restart: always
    image: postgres:latest
    volumes:
      - ./database:/var/lib/postgresql/data
      - ./shared:/shared
    ports:
      - "127.0.0.1:5432:5432"
    environment:
      POSTGRES_USER: lowcode
      POSTGRES_PASSWORD: vscode
      POSTGRES_DB: lowcodedb
```

To start the db I just need to issue docker-compose up command.

Now at last I'm ready to start coding. Well in reality that really didn't take too much time but still more than 0.
## Data layer 

One of the aspects to compare is data handling. It consists of two parts, data mapping to code objects and accessing data from the database. OutSystems provides these functionalities in a standard way that is built into the platform. On the code side we have a fast spectrum of libraries and I've chosen spring data JDBC. Spring data JDBC is not as comprehensive or fast as a full ORM. My rational against ORMs like JPA is the complexity. It wouldn't be a problem in a simple app as this but in a large scale application it can be very confusing. Spring data JDBC gives some rational why to use it

>If you load an entity, SQL statements get run. Once this is done, you have a completely loaded entity. No lazy loading or caching is done.

> If you save an entity, it gets saved. If you do not, it does not. There is no dirty tracking and no session.

> There is a simple model of how to map entities to tables. It probably only works for rather simple cases. If you do not like that, you should code your own strategy. Spring Data JDBC offers only very limited support for customizing the strategy with annotations.

I like the opinionated simple approach where you know what you get and there is not much magic behind the scenes.

### Mapping the data to entities

OutSystems uses ORM technology as its data access. It also generates the DB schema based on the created entities same way as hibernate does when hbm2ddl.auto is set to update the DB. As you know use of hbm2ddl is discouraged in production as it can lead to unforeseen consequences in the DB schema. In my experience this is also the case with OutSystems. If you e.g. drop a property from an entity the column will stay in the DB it's just hidden. The same is true if you delete an entity the table will still be there. This will not break the system but will lead to a bloated DB. This is undoubtedly fast but also little risky.

The modeling with OutSystems is done  by a graphical interface where you create the entities. This combines the entity models and the DB structure.

![OS enity creation](../img/i-challenged-low-code-with-code/os-entity-creation.png)

***OutSystems entity creation***

On the code side I need database migrations and the models. For migrations I'll use flyway which integrate into the spring boot application. I only need to write the SQL-scripts as files that will be run when the application starts. On top of the migrations I'll create spring data jdbc entity classes for them.

```kotlin
@Table("games")
data class Game(
    @Id
    val id: Long?,
    @Version
    val version: Long?,
    val name: String,
    val genre: String,
    val platform: String,
    val publisher: String,
    val rating: String,
    @Column("release_year")
    val releaseYear: Int,
    @Column("review_score")
    val reviewScore: Int,

    val highScores: Set<HighScore>) {

    fun getSortedScores(): List<HighScore> {
        return highScores.toList().sortedBy { it.score }
    }
}

@Table("high_scores")
data class HighScore(
    @Id
    val id: Long?,
    @Column("game_id")
    val game: Long?,
    @Column("gamer_name")
    val gamerName: String,
    val score: Long,
    val created: LocalDateTime
)
```

Spring data maps the DB tables to these data classes using the property names or the `@Column` annotation instructions. It also takes care of optimistic locking with the `@Version` annotation.

> **A note about optimistic locking.** Spring data JDBC supports optimistic locking at the aggregate root level, the game entity in this case. This is quite wide lock as you should be able to add multiple high scores independently. In this demo app it's just fine but in a real world case take this into consideration.

There really isn't whole lot of difference in the speed when creating these with OutSystems or with code.

### Accessing the data

OutSystems creates basic CRUD methods to access the data automatically and you can create your own aggregates as well. This is done with a excel like interface. On top of that OutSystem can use of custom SQL queries to access data. So the access pattern is really comprehensive but then again if you start to implement SQL queries you're at the same level as coding.

To match the magic of OutSystems spring data provides quick methods for DB access by simply creating a repository interface.

```kotlin
@Repository
interface GameRepository : PagingAndSortingRepository<Game, Long> {

    fun findByNameContainingIgnoreCase(name: String, pageable: Pageable): List<Game>

    @Query("select * from games where name like :name and review_score >= :minScore")
    fun findByNameAndMinimumScore(name: String, minScore: Int)

}
```

Spring automatically generates a implementation based on the signature of the interface. So 

`fun findByNameContainingIgnoreCase(name: String, pageable: Pageable): List<Game>`  

will create a method for finding a game where name like the name parameter. The pageable attribute  enables sort and paging for this query. Custom queries can be added as well like the  `findByNameAndMinimumScore`. On top of that note the extension of `PagingAndSortingRepository<Game, Long>` this creates a large set of CRUD methods for free. This matches and, in my opinion exceeds, the functionality found in OutSystems for writing simple queries.

For more complex queries we can use jdbc template to write pure SQL so it''s the same as with OutSystems. In my opinion this kind of hybrid a repository model works very nicely since you will need the basic CRUD methods as well as the more complicated ones. With spring data you get the CRUDs + extra basically for free.

## UI Layer

As with the data part the UI is also separated into two parts, displaying data and modifying it. 

###  Displaying data

The goal is to display a list of games in the UI. With OutSystems creating a listing of entities is basically just drag and drop maneuver, so it's instantaneous. If you need a edit view for the data that's again another drag and drop. This is the main benefit for OutSystems. The speed which you can create views is very fast. Although if more complex UI is needed the more work is needed but it is still fast to drag and drop components to construct a complete view. On top of this OutSystems has a large catalog of view templates that you can use as a basis for your application. Template creates the UI components and then you can select what data is used to populate them. You can also modify the template instances to suit the application needs. You can find the built in templates at

> https://outsystemsui.outsystems.com/OutSystemsUIWebsite/ScreenOverview?RuntimeId=2

For traditional coding there are scaffolding tools similar to rails that would generate views automatically (like https://projects.spring.io/spring-roo/ ), but in reality their usefulness is questionable. The next best thing is to use UI frameworks and components. There are many great alternatives for creating rich client applications but for the sake of speed I've chosen Vaadin flow. With Vaadin flow the UI is implemented at the backend and the actual client code is generated from the Kotlin / Java code. The programming style is reminiscent of desktop applications where components generate events that you listen to e.g. value changed and so on. Vaadin takes care of the communication between the client application and the backend so you can just concentrate on writing the logic.  On top of Vaadin flow I've also added karibu dsl library that enables structured coding style for vaadin flow UIs using the idea behind kotlin's type-safe builders

https://kotlinlang.org/docs/type-safe-builders.html

So to create a grid view of the games in the database I write the following code

```kotlin
appLayout {
    content {
        verticalLayout {
            h2("Games")
            grid(dataProvider = DataProviders.getDataProvider(gamesRepository)) {
                addColumn(Game::name).setHeader("Name").setSortProperty("name")
                addColumn(Game::platform).setHeader("Platform").setSortProperty("platform")
                addColumn(Game::publisher).setHeader("Publisher").setSortProperty("publisher")
                val rs = addColumn(Game::reviewScore).setHeader("Review score").setSortProperty("reviewScore")
                addColumn(Game::releaseYear).setHeader("Released").setSortProperty("releaseYear")
                sort(
                    GridSortOrderBuilder<Game>().thenDesc(rs).build()
                )
            }
        }
    }
}
```

The structured style immediately shows how the actual UI layout constructed. The key points to take away are the grids data provider and the mapping of grid columns to the database entity properties. The data provider is a Vaadin concept that, well provides data for the UI component. For this purpose I wrote a little helper object to generate data providers from spring data repositories.

```kotlin
fun <T, F> Query<T, F>.toSpringDataPageRequest() =
    PageRequest.of(offset / limit, limit, VaadinSpringDataHelpers.toSpringDataSort(this))

object DataProviders {

    fun <T,ID> getDataProvider(pagingAndSortingRepository: PagingAndSortingRepository<T,ID>): DataProvider<T, Void> {

        return DataProvider.fromCallbacks(
            { pagingAndSortingRepository.findAll(it.toSpringDataPageRequest()).stream() },
            { pagingAndSortingRepository.count().toInt() }
        )
    }
}
```

This uses callbacks to the repository to get the actual data as well as the count of the items.  Oh did I mention that the grid is lazy loading and sortable. Behind the scenes data is queried for the next page when user scrolls the grid. 

![Vaadin grid](../img/i-challenged-low-code-with-code/vaadin-grid.png)

***Vaadin games grid***

### Data modification

An application would be pretty useless if it wouldn't allow any write operations. With OutSystems this is yet again pretty straight forward drag and drop to generate a form that inserts data to the DB. It also provides basic validations based on the data type as well as custom validation support. So the conclusion is that it's pretty fast to implement forms with OutSystems.

With code we need to do some actual coding, surprise. Vaadin has a binder concept where you can bind objects to form fields and it will populate the date to the object instance. It supports validation which yo only write once and it's executed both in the client and the server. For the input fields there are a bunch ready made components such as a date picker and so on. Bellow is a code snippet for high score addition with it's own object model. 

> **Side note.** Using the DB entities int he UI by the way is one thing that I find concerning with OutSystems. In a complex system you should always have separate UI models so you don't couple the UI with the database model.

```kotlin
verticalLayout {
    addClassName("add-high-score-form")
    h4("Add new high score")
    formLayout {

        val binder = BeanValidationBinder(HighScoreUIModel::class.java)

        textField("Gamer name") {
            bind(binder).trimmingConverter()
            .withValidator({ name -> name?.isNotEmpty() ?: false}, "Name cannot be empty")
            .bind("gamerName")
        }

        integerField ("Score") {
            bind(binder)
            .withValidator({ score -> score ?: 0 > 0 }, "Score needs to be larger than 0")
            .bind("score")
        }

        dateTimePicker("Created") {
            bind(binder)
           .withValidator(
               { created -> created?.isBefore(LocalDateTime.now()) ?: false },
               "Time cannot be in the future or empty"
           )
           .bind("created")
        }

        binder.bean = HighScoreUIModel(gameId = gameId)

        horizontalLayout {
            button("Add") {
                addClickListener {
                    handleAddition(binder)
                }
            }
            justifyContentMode = FlexComponent.JustifyContentMode.END
            setWidthFull()
        }
    }
}

private fun handleAddition(binder: Binder<HighScoreUIModel>) {
    if (binder.validate().isOk) {
        EventBroker.sendEvent(
            HighScoreAdded(
                game = gamesService.addHighScoreToGame(binder.bean)
            )
        )
        binder.bean = HighScoreUIModel(gameId = gameId)
    }
}
```

For showing the high score and adding new ones I created a click listener to the games grid which opens a Vaadin dialog. The dialog has again a grid showing the high scores as well as the form for adding new ones. 

```kotl
addItemClickListener {
    val highScoreDialog = HighScoreDialog(it.item, gamesService)
    highScoreDialog.open()
}
```

![High score dialog](../img/i-challenged-low-code-with-code/vaadin-dialog.png)

So it's pretty fast and easy to create these forms with Vaadin.

#### Wait there's more

There are couple of nice thinks what you get with Vaadin which I'll just mention quickly.

```kotlin
@Push
class ApplicationShell : AppShellConfigurator 
```

With the `@Push` annotation you reactive functionality so you can "push" changes from the backend threads to the frontend through a websocket. I use this to synchronize changes from different users. I created a simple memory based event broker and I use it to refresh the high score dialog grid for added high scores

```kotlin
// Listener
with(EventBroker) {
    registerForEvents(HighScoreAdded::class.java) {
        if (it.game.id == game.id) {
            game = it.game
            // Push event to the front end with synchronized access
            ui.get().access {
                grid.setItems(DataProvider.ofCollection(game.getSortedScores()))
                grid.refresh()
            }

        }
    }
}

//---------

// Triggering
EventBroker.sendEvent(
    HighScoreAdded(
        game = gamesService.addHighScoreToGame(binder.bean)
    )
)
```

Pretty nice I'd say.

## Writing logic

Writing logic is a common task in many parts of an application. With OutSystems you use graphical presentation to implement your logic operations. This is depicted below. 

![Outsystems code flow](../img/i-challenged-low-code-with-code/outsystems-stars.png)

***OutSystems logic***

The above logic is basically this

```kotlin
val list = MutableList()
for(i < 5) {
    list.add(i < rating)
}
return list
```

Writing the above code is much faster than doing the graphical version. Also with Kotlin I would write the logic like this 

```kotlin
fun createStarArray(rating: Int) = (0..4).map { it < rating }
```

When it comes to implementing logical operations traditional coding is much faster and for a coder easier to read. For a non coder the graphical version is more clear.

## CI / CD

One really great thing about low code platforms, like OutSystems, is that they usually come with run environment and some level of automated deployment between different stages. Usually when implementing a bespoke solution these need to be done separately and they do take time. So how could I challenge this?  Modern cloud platforms are pretty great as they are basically infrastructure implemented with software but even that requires you to define what you need in a quite detailed manner. For achieve maximum speed I decided to host my application in Heroku. What that meant was that I headed to Heroku web site and registered an account and then created an application which I linked to the github repository. I also selected I wanted a postgresql database and I was done.

![Heroku](../img/i-challenged-low-code-with-code/heroku-ci.png)

Heroku automatically detected that I had an spring boot application and build and deployed it to staging. It also set the detabase environment variables so that the spring would pick them up and use that for it's database. This took literally 10 minutes and the cost for a small application is 0e. 

> **Note** the free level at Heroku isn't really feasible for production level software as 
>
> * It turns it self of if there's no traffic for 30 mins 
> * Has a cap of 10 000 rows in the DB.

I'd say it's pretty close to getting ready made environment. Heroku also has the concept of review apps where it will create a new environment from pull request for testing, it costs extra so I didn't enable them. On top of the CD functionality Heroku offers a CI testing as well but this is also a paid feature so I didn't use it.

The application in this blog is available for a limited time at

https://lowcode-challenge-staging.herokuapp.com/

and

https://lowcode-challenge-prod.herokuapp.com/

Also source code for it is available at

https://github.com/hnybom/low-code-vs-code

## Final thoughts

Let's have a quick comparison for the different categories

| Category          | OutSystems                                                   | Code                                                         |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Data Layer        | Automatic generation for basic access and support for complex queries with SQL | Automatic generation for basic functionality, signature based query generation as well ass support for SQL queries |
| UI Layer          | Large template and component library for creating views      | View components that are used for composing views            |
| Logic             | Graphical interface for writing logic which easy to read if the reader doesn't understand code. The implementation is cumbersome and slow compared to writing code. | Very powerful way of expressing logic in many different ways. This is the strong point of code. There of course is a steeper learning curve than in low-code |
| CD + environments | Three stage environment out of the box. Limited support of automatic testing. | Many public cloud options with different focus areas and complexities. You can select what you need. In any case requires some work. |

> **Note** I've not covered all of the features here so this is just a limited view of the low-code platforms. They many more features that increase development such as fast integration to APIs and to certain products such as SAP.

What it comes down to is choice. With OutSystems you get a whole platform with it's strong points as well as weaknesses. It's a whole package take it or leave it. It's also quite expensive so in many ways it's a strategic decision. On the code side there are huge amount of options, even too many I would say. You need expertise to select the right tools and components for your solution. 

So what about the speed of developing apps. In reality the development speed difference is not 5-7x  it might be like 1,5x faster when you develop real world applications and not just lists and forms that directly interact with the database or integration source. The real world benefit you gain from low-code is that it enables more people to do coding as the learning curve is not that steep. That doesn't mean you don't need to understand software architecture because you real need to. Otherwise the systems will become very hard to maintain and to develop further efficiently. 

For closing words I'd say it really doesn't matter what route you go each one will have it's ups and downs. I know what an anticlimax but that just is the through, sorry.