# 💻 Browser IDE: Java Spring Boot

Welcome to the copyable source browser for the [Java Spring Boot tutorial](../15-jenkins-java-spring.md). Expand a file to read or copy it. Each file also includes GitHub view and raw download links.

> [!NOTE]
> This page requires no JavaScript. If Outline removes HTML details elements, the file contents remain visible as ordinary Markdown code blocks.

## Explorer

```text
📁 java-spring
│   └── 📄 Dockerfile
│   └── 📄 Jenkinsfile
│   └── 📄 pipeline.yml
│   └── 📄 pom.xml
│   ├── 📁 src
│   │   ├── 📁 main
│   │   │   ├── 📁 java
│   │   │   │   ├── 📁 net
│   │   │   │   │   ├── 📁 mtslab
│   │   │   │   │   │   ├── 📁 demo
│   │   │   │   │   │   │   └── 📄 DemoApplication.java
│   │   ├── 📁 test
│   │   │   ├── 📁 java
│   │   │   │   ├── 📁 net
│   │   │   │   │   ├── 📁 mtslab
│   │   │   │   │   │   ├── 📁 demo
│   │   │   │   │   │   │   └── 📄 DemoApplicationTests.java
```

[Browse the complete `java-spring` starter on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/tree/master/examples/java-spring) · [Download the repository as a ZIP](https://github.com/MagusTechSolutions/mts-docs-demos/archive/refs/heads/master.zip)

## Use the complete starter

1. Create a local folder named `java-spring`.
2. Expand and copy each file below, or download it from its raw link.
3. Save it at the exact displayed path.
4. Commit the copied folder as the root of a new application repository.

## Files

<details>
<summary><strong>📄 Dockerfile</strong></summary>

**Save as:** `Dockerfile` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/java-spring/Dockerfile) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/java-spring/Dockerfile)

```dockerfile
FROM maven:3.9.11-amazoncorretto-21 AS build
WORKDIR /workspace
COPY pom.xml .
COPY src src
RUN mvn -B -ntp -Dmaven.test.skip package

FROM amazoncorretto:21-alpine
WORKDIR /app
COPY --from=build /workspace/target/demo-spring-*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

</details>

<details>
<summary><strong>📄 Jenkinsfile</strong></summary>

**Save as:** `Jenkinsfile` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/java-spring/Jenkinsfile) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/java-spring/Jenkinsfile)

```groovy
library identifier: 'buildPipeline@master',
  retriever: modernSCM([
    $class: 'GitSCMSource',
    credentialsId: 'github-repo-token',
    remote: 'https://github.com/MagusTechSolutions/mts-jenkins-lib.git'
  ])

buildPipeline(configFile: 'pipeline.yml')
```

</details>

<details>
<summary><strong>📄 pipeline.yml</strong></summary>

**Save as:** `pipeline.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/java-spring/pipeline.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/java-spring/pipeline.yml)

```yaml
app: demo-spring
stack: java
project: demo

custom:
  build_commands:
    - "mvn -B clean test"

artifacts:
  - 'target/*.jar'
  - 'imageRef.properties'
  - 'pipeline.properties'

spinnaker_app: demo-spring
environments:
  - name: feature/
    deploy: true
    spinnaker:
      pipeline: deploy-dev
      parameters:
        namespace: demo
        appname: demo-spring
  - name: develop
    deploy: true
    spinnaker:
      pipeline: deploy-dev
      parameters:
        namespace: demo
        appname: demo-spring
  - name: master
    deploy: true
    spinnaker:
      pipeline: deploy-prod
      parameters:
        namespace: demo
        appname: demo-spring
```

</details>

<details>
<summary><strong>📄 pom.xml</strong></summary>

**Save as:** `pom.xml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/java-spring/pom.xml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/java-spring/pom.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.5.7</version>
    <relativePath/>
  </parent>
  <groupId>net.mtslab.demo</groupId>
  <artifactId>demo-spring</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <properties>
    <java.version>21</java.version>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
```

</details>

<details>
<summary><strong>📄 src/main/java/net/mtslab/demo/DemoApplication.java</strong></summary>

**Save as:** `src/main/java/net/mtslab/demo/DemoApplication.java` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/java-spring/src/main/java/net/mtslab/demo/DemoApplication.java) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/java-spring/src/main/java/net/mtslab/demo/DemoApplication.java)

```java
package net.mtslab.demo;

import java.util.Map;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @RestController
    static class DemoController {

        @GetMapping("/")
        Map<String, String> hello() {
            return Map.of("message", "Hello from MTS Spring Boot");
        }
    }
}
```

</details>

<details>
<summary><strong>📄 src/test/java/net/mtslab/demo/DemoApplicationTests.java</strong></summary>

**Save as:** `src/test/java/net/mtslab/demo/DemoApplicationTests.java` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/java-spring/src/test/java/net/mtslab/demo/DemoApplicationTests.java) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/java-spring/src/test/java/net/mtslab/demo/DemoApplicationTests.java)

```java
package net.mtslab.demo;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class DemoApplicationTests {

    @Test
    void contextLoads() {
    }
}
```

</details>
