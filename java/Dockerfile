FROM openjdk:11
USER root
WORKDIR /usr/scrapper
COPY ./target/adblocker-0.0.1-SNAPSHOT-jar-with-dependencies.jar /usr/scrapper
CMD ["java", "-jar", "adblocker-0.0.1-SNAPSHOT-jar-with-dependencies.jar"]