---
layout: post
title: Reduce boilerplate in Java backends with records
author: janneri
excerpt: >
  Java 14 (March 2020) introduces records as a preview feature. Records provide a compact syntax for declaring simple, immutable data carrier classes, such as Point(x: int, y: int). This blog gives an example of records in REST/JSON APIs.
tags:
 - Java
 - Java 14
 - Records
 - Builder pattern
 - Gson
 - JEP 359
---

## Key Takeaways

- Java 14 (March 2020) introduces [records](https://openjdk.java.net/jeps/359) as a preview feature
- Records provide a compact syntax for declaring simple, immutable data carrier classes, such as ```Point(x: int, y: int) {}```
- This blog is about records and REST/JSON APIs
- Frameworks can easily translate values from and to JSON using records
- If you want to use the builder pattern, you still need code generation (IDE or annotation-based)

## Introduction to Java Records

![Java Versions](/img/java14-records/java-versions.png)

As illustrated in the picture above, Java 14, which is being released in March 2020 introduces a new interesting feature named [records](https://openjdk.java.net/jeps/359). 
This is how a record is declared:

```
record Point(x: int, y: int) {}
```

A record automatically acquires:
- a public constructor
- accessors to the fields
- equals() and hashCode()
- toString()

Previously, IDEs and annotation-based code generation have helped us generate these class members.
Although records are not a complete replacement for code generation tools,  it's very nice to have this support built into the language.

## Reducing Boilerplate, But How Much?

![data class proportion of all code](/img/java14-records/data-class-file-counts.png)

How much boilerplate code could be removed, if all data carrier classes were replaced by records? I picked three Java applications I've worked with lately and just counted the number of data carrier classes.
As you can see in the picture above, almost a quarter of the code is data carrier classes! 

Is there a genuine benefit in reducing boilerplate? You can always just generate the code, right? 
Generating code is fast, but still, less code means less time used maintaining, testing, reading and reviewing code.
And reducing boilerplate is just one of the benefits here. Records also:
1. encourage rich typing
2. encourage immutability
3. standardize the implementation of hashCode, equals and toString
4. discourage invalid reuse of data carrier classes, which makes APIs more clear and precise
5. enable implementation of new tools and features to Java   

Of course, it depends on the context, but to me it looks like we are talking about a significant effect on Java source code.

## Example App With Records and Gson

### Download and Setup Java 14

I wanted to test and play around with records and JSON serialization, so I 
- downloaded [the early access build of JDK 14](http://jdk.java.net/14/),
- extracted the tar.gz next to the other JDKs 
- and switched it on using [jEnv](https://www.jenv.be/):

```
jenv add /Library/Java/JavaVirtualMachines/jdk-14.jdk/Contents/Home/
jenv use 14
```

### Create a New Project With Maven

It looks like there's no support from Gradle yet, so I went along with Maven and created this pom.xml: 

```
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>fi.solita</groupId>
    <artifactId>java-14-test</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>14</maven.compiler.source>
        <maven.compiler.target>14</maven.compiler.target>
    </properties>

    <dependencies>

        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.8.6</version>
        </dependency>

        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.0</version>
                <configuration>
                    <release>14</release>
                    <compilerArgs>
                        --enable-preview
                    </compilerArgs>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.0.0-M4</version>
                <configuration>
                    <argLine>--enable-preview</argLine>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

Note! The compiler needs the ```--enable-preview```flag, otherwise you'll get a compilation failure saying: "records are a preview feature and are disabled by default".

### Implement a Sample Application

I created a ```test-java-14/src/test/java/fi/solita/BloggingAppTest.java``` and ran it with ```mvn test```.
This is what the whole thing looks like:

```
package fi.solita;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.junit.Test;
import java.util.List;


record Post(long blogId, String author, String title, String content) {}
record Blog(long id, List<Post> posts) {}


public class BloggingAppTest {
    private Gson gson = new GsonBuilder().setPrettyPrinting().create();

    @Test
    public void records_are_serialized_to_json() {
        var blog = createTestBlog();
        String json = gson.toJson(blog);
        System.out.println(json);

        // outputs:
        /*
        {
          "id": 1,
          "posts": [
            {
              "blogId": 1,
              "author": "Janne",
              "title": "This is title",
              "content": "This is content"
            }
          ]
        }
         */
    }

    @Test
    public void json_is_deserialized_to_a_record() {
        String json = gson.toJson(createTestBlog());
        var blog = gson.fromJson(json, Blog.class);
        System.out.println(blog);

        // outputs:
        // Blog[id=1, posts=[Post[blogId=1, author=Janne, title=This is title, content=This is content]]]
    }

    private static Blog createTestBlog() {
        var post = new Post(1, "Janne", "This is title", "This is content");
        var blog = new Blog(1, List.of(post));
        return blog;
    }
}
```

## Thoughts After the Experiment?

Records provide a compact syntax for declaring simple, immutable data carrier classes. Frameworks can easily translate values from and to JSON (or any other serialization format).

If you need to create instances of records by hand, you might get into trouble, because sometimes the data carrier classes contain a lot of fields.
It's easy to mistype the order of two parameters with the same type. Proper typing helps mitigate the problem. In addition, you can use the builder pattern. 
For example, [Github - RecordBuilder](https://github.com/Randgalt/record-builder) seems very nice and allows you to write:

```
@RecordBuilder
record Point(x: int, y: int) {}
```

After setting up the RecordBuilder annotation processor, it's easier to build instances, create copies and so on: 
```
var p1 = Point.builder().x(xCoord).y(yCoord).build();
```
 
To conclude, I would say that Java 14 version of records is definitely a nice step forward:
 1. they reduce boilerplate code in data carrier classes
 2. encourage rich typing and immutability
 3. data is modeled as data

The fact that data is modeled as data could be even more important than reducing boilerplate, because it allows tools and
future versions of Java support cool features such as [pattern matching](https://cr.openjdk.java.net/~briangoetz/amber/pattern-match.html)!

The new Java 14 will be released on March 17, 2020. In general, it's possible that some preview features will be removed or modified. I strongly believe, however, that records are here to stay and will change the way we program in Java. 

Happy coding and thanks for reading!

## Links

- You can find the complete [Java 14 schedule and list of features here](https://openjdk.java.net/projects/jdk/14/). 
- Here is a link to the sample project source code: [https://github.com/janneri/test-java-14-records](https://github.com/janneri/test-java-14-records).
