from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import json
import logging

logging.basicConfig(level=logging.INFO)

class EventProducer:
    def __init__(self, bootstrap_servers, topic_name):
        self.topic_name = topic_name
        admin_client=KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        if len(admin_client.list_topics()) == 0:
            admin_client.create_topics(new_topics=[NewTopic(name=self.topic_name, num_partitions=3, replication_factor=3)])
        try:
            self.producer=KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v:json.dumps(v).encode('utf-8')
            )
            logging.info("Producer created")
        except Exception as e:
            logging.error(f"Could not create producer: {e}")
            raise

    def send_message(self, data):
        try:
            self.producer.send(self.topic_name, value=data)
            self.producer.flush()
            logging.info(f"Data has been sent to topic: {self.topic_name}")
        except Exception as e:
            logging.error(f"Failed to send data: {e}")
            raise

    def close(self):
        self.producer.close()
        logging.info("Producer closed")

