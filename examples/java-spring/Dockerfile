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

