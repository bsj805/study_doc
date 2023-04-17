# Summary

This project is used to practice Reactor Kafka with Reactor in Spring boot


# Consumer data lifecycle

1. poll (get record from broker)
2. if record is not inside Fetcher queue, `Fetch request` is executed to get data from Broker
3. the recordBatch from Broker is stored to Fetcher queue
4. offset(metadata that denotes the position of last data read)
5. unzip `recordBatch` and return record to user application Thread


recordBatch is the events collected from publisher during few seconds. It is compressed to send to Broker for efficiency


# Configuration
https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/kafka/KafkaProperties.html

```java
@ConfigurationProperties(prefix="spring.kafka")
public class KafkaProperties extends Object
```
        Configuration properties for Spring for Apache Kafka.

@ConfigurationProperties is used to fill in object's variables given application.yml
Since we need to see Producer bootstrap-servers or Consumer bootstrap-servers,
https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/autoconfigure/kafka/KafkaProperties.Producer.html

if we go inside, we can see it has `setBootStrapServers(List<String>)` method.
You can see all the methods here : https://blog.voidmainvoid.net/169

```java
@Configuration
@RequiredArgsConstructor
public class KafkaConfig {

    private final KafkaProperties kafkaProperties;

```

it can be used with lombok.

Sender options to create `KafkaSender` class needs Map<String,Object> Like
```java
return new HashMap<>() {{
            put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, properties.getHosts());
            put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
            put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
            put(ProducerConfig.MAX_BLOCK_MS_CONFIG, 1000); // 전송 시간 제한을 1000ms로 설정
        }};
```
However, we can define all those in application.yml and use `kafkaProperties.buildProducerProperties();`
