SET JAVA_HOME=D:\work\jdk1.8.0_25-x64

mvnw clean install -DskipTests=true

docker build . -t 192.168.69.236:32000/scrapper

docker push 192.168.69.236:32000/scrapper