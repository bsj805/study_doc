# 1장 카프카가 무엇인가?

pub-sub model을 통한 message queue.
메모리가 아닌, disk -based message queue . disk인데 어떻게 빠르냐? append only야.(sequential I/O)


## 카프카 용어정리

- Broker : segment file이라는 logical 단위를 이용해 message를 저장한다.
    - 각 topic에 대한 partition을 가진다.
    - consumer들은 특정 토픽의 partition을 가진 broker의 IP를 찾아 직접 접속 (pod 실패시 failover 어려움)
    - 같은 partition을 여러 broker에 나눠두면 같은 메시지를 여러 broker가 가지고 있는 셈이라 병렬처리가 가능.
        - 다만, consumer group rebalancing 할때 더 많은 consumer들이 조정되어야 한다. (왜일까~?)

- Segment: 한 partition에 여러 segment가 존재한다.
    - append only라서, segment의 맨 끝에 메시지를 추가한다.
        - log segment: message의 persistence ( durability 담당 )
        - index segment: logical offset으로 log segment 파일의 physical offset 찾기
        - timeindex segment: search by a timestamp
## 복제 (HA)
replica가 복제에 대한 책임이 있고, replica가 leader paritition에게 `fetch request` 를 요청하는 방식.


## 데이터 흐름

### producer
serialize -> partition -> Record batch in Record Accumulator(일정 시간동안 들어온 메시지 모으기)
-> compress -> flush(broker로 보내기)
### Consumer
Subscribe -> poll -> 사용자의 데이터 조작 성공 -> commit order
이러면 offset이 바뀐다. 해당 consumer group의 offset이 변해서, 같은 consumer group있으면 해당 그룹에는 처리된 메시지가 보이지 않는다.
partition 단위로 offset이 commit된다.

group coordinator가 broker에 존재해서, consumer group이 현재 소비해야 하는 topic과 partition을 leader consumer에게 전달한다.
consumer group이름이 다르다면 같은 partition의 메시지를 서로 다른 offset을 가지고있어서, 두번처리도 가능.

보통 consumer app application 단에서 중복 메시지 처리를 한다.

# 2장 KAFKA 설치, 구성

Broccoli : producer, consumer 테스트할 수 있고, discovery를 통해 consumer에 대해서 조작 UI제공.

# 3장, data processing

KAFKA는 작은 용량의 메시지를 (주로 1MB 미만) 대용량 처리해야하는 경우를 상정한다.

메시지 전송은
- At Most Once : 그냥 producer가 보냈다면 처리되었다고 판단
- At least once : 전송 재시도를 해서 중복 메시지가 발생할 수도 있으나, broker에서 ack오면 한번은 저장된거니까, ack올때까지 기다림
    - ack=1 설정하면 broker의 leader partition에만 도달해도. -ack = all 설정하면 모든 replication에 전달되었을때.
- Exactly Once: commit 함수를 써서 카프카 브로커에 커밋이 되었을때 메시지가 읽을 수 있게 된다. - 커밋이 안되는 상황이라면 (broker에서 저장안되면) exception

Exactly Once (EO) -> enable.idempotence=true.
>Idempotent Producer Guarantees 를 보면 어떻게 exactly once delivery를 보장하는지에 대한 개념이 설명된다. 요약하자면 각 Producer는 Unique한 ID를 가지고 메시지를 발행할때 Sequence Number를 함께 보낸다. 그리고 Broker는 PID, TopicPartition 별로 해당 Sequenece Number를 Memory상으로 기억한다. 그래서 Sequence Number를 보고 동일 메시지를 추적하는 것이다. 여기의 ProducerId는 최초에 InitProducerIdRequest API를 통해서 Broker로 요청을 하며, 그 응답값을 사용한다.
>PID를 생성하는 로직은 broker 에서 ProducerIdManager object class 에 의해서 생성된다. 로직은 단순히 increment 이다. 그래서 계속 producer 를 만들어 보면 PID 는 숫자1만 증가하는것을 볼 수 있다.

그냥 sequence number을 보면서 이전에 중복메시지 있으면 abort 하는등.


## Serializer 역할

KAFKA는 byte 배열만 사용. 메시지로 쓸 데이터 모델을 custom하게 정의하면 serializer , deserializer 만들어야.
여기 쓰일 좋은 형식이 protobuf.
