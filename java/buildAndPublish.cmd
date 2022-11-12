SET JAVA_HOME=D:\work\jdk1.8.0_25-x64

call mvnw clean install -DskipTests=true

echo "Maven build finished"

call docker build . -t 192.168.69.236:32000/scrapper

echo "Docker build finished"

call docker push 192.168.69.236:32000/scrapper

echo "Docker push finished"