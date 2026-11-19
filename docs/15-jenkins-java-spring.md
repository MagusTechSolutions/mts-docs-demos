# ☕ Jenkins demo: Java Spring Boot

Let's build and containerize a tiny Spring Boot service using the MTS Java pipeline.

Use [examples/java-spring](https://github.com/MagusTechSolutions/mts-docs-demos/tree/master/examples/java-spring) as a complete starting point.

> **Open the starter in a browser IDE:** [Java Spring source browser](code-browser/java-spring.md). You can expand, copy, and save every file.

## 1. Run locally

```bash
mvn clean test
mvn spring-boot:run
```

Verify it:

```bash
curl http://localhost:8080/
curl http://localhost:8080/actuator/health
```

## 2. Review the MTS contract

[`pipeline.yml`](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/java-spring/pipeline.yml):

```yaml
app: demo-spring
stack: java
project: demo
artifacts:
  - 'target/*.jar'
  - 'imageRef.properties'
  - 'pipeline.properties'
```

The Dockerfile creates the expected `target/*.jar` and starts it:

```dockerfile
FROM maven:3.9.11-amazoncorretto-21 AS build
WORKDIR /workspace
COPY pom.xml .
COPY src src
RUN mvn -ntp -Dmaven.test.skip package

FROM amazoncorretto:21-alpine
COPY --from=build /workspace/target/demo-spring-*.jar /app/app.jar
ENTRYPOINT ["java","-jar","/app/app.jar"]
```

## 3. Understand the build stages

The standard Java path expects a Maven wrapper and:

```bash
chmod +x mvnw
./mvnw clean install -ntp -Dmaven.test.skip
./mvnw --batch-mode test
```

This starter uses `custom.build_commands` so a new repository without a generated wrapper can start with `mvn`:

```yaml
custom:
  build_commands:
    - "mvn -B clean test"
```

Once the wrapper is committed, remove that custom block to use the standard Java path.

## 4. Add Spinnaker later

```yaml
spinnaker_app: demo-spring
environments:
  - name: develop
    deploy: true
    spinnaker:
      pipeline: deploy-dev
      parameters:
        namespace: demo
        appname: demo-spring
```

## 5. Verify the Jenkins run

Check the console for:

- the loaded shared-library revision;
- `Loaded pipeline config from pipeline.yml`;
- successful tests;
- Docker build and registry push;
- `IMAGE_NAME=...@sha256:...`;
- optional Spinnaker execution.

## Topic Q&A

### 1. Why use Java 21?
The `stack: java` route selects the Java 21 MTS agent, matching this starter's `pom.xml`.

### 2. Does the Docker build run tests?
Not in this Dockerfile. The Jenkins Java pipeline runs tests before the image stage.

### 3. Is SonarQube mandatory?
No. Enable `sonar: true` only after its Jenkins environment and credential are configured.

### 4. Why include Actuator?
Kubernetes probes can use `/actuator/health` to determine readiness and liveness.

### 5. When should I use the standard Maven wrapper path?
Commit `mvnw` and remove the custom command so the library can use its standard Java workflow.

## MTS Labs Q&A

### 1. Which agent runs `stack: java`?
The shared library maps it to `java21`.

### 2. Where is this image published?
The path is `mts-release/demo/demo-spring` or `mts-sandbox/demo/demo-spring`, depending on branch.

### 3. Which MTS credential might Spring pipelines receive?
Existing Java callers pass a JWT secret credential when the application requires it.

### 4. Which reference supplies the health pattern?
The bridge API gateway deployment uses Spring Actuator health probes.

### 5. How does the image reach MKP?
Jenkins writes a digest reference and Spinnaker deploys it through the selected pipeline.

## Troubleshooting questions

### Why did the Java agent fail to compile the project?
Confirm Java 21 compatibility in `pom.xml` and that the configured agent exists.

### Why did `./mvnw` fail?
Commit the Maven wrapper or retain the demo's explicit `mvn -B clean test` custom command.

### Why is Kubernetes restarting Spring despite successful startup?
Compare the configured health path and port with the running application; inspect probe events.

### Why are no JAR artifacts archived?
Check that Maven produced `target/*.jar` and that the artifact glob remains in `pipeline.yml`.

