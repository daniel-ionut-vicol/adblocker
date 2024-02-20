export DB_URL="jdbc:mysql://192.168.69.207:3306/scrapper" DB_USER="scrapper" DB_PASS="trustno1x" DB_MIN_CONN="1" DB_MAX_CONN="10" DB_MAX_STS="100"
mvn clean install -DskipTests=true
java -jar ./scrapper/target/adblocker-0.0.1-SNAPSHOT-jar-with-dependencies.jar