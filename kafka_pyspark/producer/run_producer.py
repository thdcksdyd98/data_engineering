from producer import EventProducer
from data_generator import stream_data
import logging

BOOTSTRAP_SERVER = ['kafka0:9092', 'kafka1:9092', 'kafka2:9092']
TOPIC='test-topic'
STREAM_INTERVAL_SECONDS=1

def main():
    try:
        producer=EventProducer(bootstrap_servers=BOOTSTRAP_SERVER,topic_name=TOPIC)
        data_source=stream_data(interval_seconds=STREAM_INTERVAL_SECONDS)
        for data in data_source:
            producer.send_message(data)
    except KeyboardInterrupt:
        logging.info("Stopped by user")
    except Exception as e:
        logging.error(f"Unexpected exception: {e}")
    finally:
        if 'producer' in locals() and producer:
            producer.close()

if __name__=="__main__":
    main()