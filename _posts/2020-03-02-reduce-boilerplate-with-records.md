---
layout: post
title: Reduce boilerplate in Java backends with records
author: janneri
excerpt: >
  Java 14 (March 2020) introduces records as a preview feature. Records provide a compact syntax for declaring simple, immutable data carrier classes, such as Point(x: int, y: int). This blog gives an example of records in rest/json APIs.
tags:
 - Java
 - Java 14
 - Records
 - JEP 359
---

# Reduce boilerplate in Java backends with records

# Key takeaways
- Java 14 (March 2020) introduces [records](https://openjdk.java.net/jeps/359) as a preview feature
- Records provide a compact syntax for declaring simple, immutable data carrier classes, such as ```Point(x: int, y: int) {}```
- This blog is about records and rest/json APIs
- Frameworks can easily translate values from and to json using records
- If you want builder-pattern, you still need (IDE or annotation based) code generation    

# Introduction to Java records

![Java Versions](/img/java14-records/java-versions.png)

As illustrated in the picture above, Java 14 released in March 2020 introduces a new interesting feature named [records](https://openjdk.java.net/jeps/359). 
This is how records are declared:

```
record Point(x: int, y: int) {}
```

A record automatically acquires:
- a public constructor
- accessors to the fields
- equals() and hashCode()
- toString()

Previously IDEs and annotation based code generation have helped us generate these members.
Although records are not a complete replacement for code generation tools,  it's very nice to have this support built into the language.

# Example app with records and Gson

## Download and setup Java 14

I wanted to test and play around with records and json serialization, so I 
- downloaded [the early access build of JDK 14](http://jdk.java.net/14/),
- extracted the tar.gz next to the other jdk:s 
- and switched it on using [jEnv](https://www.jenv.be/):

```
jenv add /Library/Java/JavaVirtualMachines/jdk-14.jdk/Contents/Home/
jenv use 14
```

## Create a new project with Maven

It looks like there's no support from Gradle yet, so I went along with Maven, and created this pom.xml: 

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

Note! The compiler needs a flag "--enable-preview", otherwise you'll get a compilation failure saying: "records are a preview feature and are disabled by default".

## Implement a sample application

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

## Thoughts after the experiment?

Records provide a compact syntax for declaring simple, immutable data carrier classes. Frameworks can easily translate values from and to json (or any other serialization format).

If you need to create instances of records by hand, you might get into trouble, because sometimes the data carrier classes contain a lot of fields.
It's easy to mistype the order of two parameters with the same type. Proper typing helps mitigate the problem. In addition you can use the builder pattern. 
For example, [Github - RecordBuilder](https://github.com/Randgalt/record-builder) seems very nice and allows you to write:

```
@RecordBuilder
record Point(x: int, y: int) {}
```

After setting up the RecordBuilder annotation processor, it's easier to build instances, create copies and so on: 
```
var p1 = Point.builder().x(xCoord).y(yCoord).build();
```
 
To conclude, I would say that Java 14 version of records is a definitely a nice step forward.
 1. they reduce boilerplate from data carrier classes
 2. data is modeled as data

The fact that data is modeled as data is even more important then reducing boilerplate, because it allows tools and
future versions of Java support cool features such as [pattern matching](https://cr.openjdk.java.net/~briangoetz/amber/pattern-match.html)!

The new Java 14 will be released March 17, 2020. In general, it's possible that preview features are removed or change. I strongly believe, that records are here to stay and change the way we program Java. 

Happy coding and thanks for reading!

## Links

- You can find the complete [Java 14 schedule and list of features here](https://openjdk.java.net/projects/jdk/14/). 
- Here is a link to the sample project source code: [https://github.com/janneri/test-java-14-records](https://github.com/janneri/test-java-14-records).
