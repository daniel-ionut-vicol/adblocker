FROM ubuntu:latest

RUN apt-get update && apt-get install -y openjdk-11-jdk firefox

WORKDIR /usr/scrapper
COPY ./scrapper/target/adblocker-0.0.1-SNAPSHOT-jar-with-dependencies.jar /usr/scrapper
CMD ["java", "-jar", "adblocker-0.0.1-SNAPSHOT-jar-with-dependencies.jar"]