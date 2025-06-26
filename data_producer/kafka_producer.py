from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import csv
import json
import logging
import random

from time import sleep
from faker import Faker

fake = Faker()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

kafka_server = 'kafka:9092'

# Exemple de données simulées
entities = ["CompanyA", "CompanyB", "OrganizationX", "IndividualY"]
sentiments = ["positive", "neutral", "negative"]

# Setup Kafka Admin Client to manage topics
admin_client = KafkaAdminClient(
    bootstrap_servers=kafka_server,
    client_id='twitter_producer'
)

topic_name = "twitter_data_test_Kafka"

# Check if the topic already exists and create it if not
try:
    existing_topics = admin_client.list_topics()
    if topic_name not in existing_topics:
        topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
        admin_client.create_topics(new_topics=[topic])
        logger.info(f"Created new topic: {topic_name}")
    else:
        logger.info(f"Topic '{topic_name}' already exists.")
except Exception as e:
    logger.error(f"Failed to create topic: {e}")
    exit(1)

# Setup Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=kafka_server,
    api_version=(0, 11),
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Génération de messages aléatoires en continu
try:
    while True:
        message = {
            "Tweet_ID": fake.random_int(min=10000, max=99999),
            "Entity": random.choice(entities),
            "Sentiment": random.choice(sentiments),
            "Tweet_Content": fake.sentence(nb_words=12)
        }

        producer.send(topic_name, value=message)
        logger.info(f"Tweet envoyé : {message}")
        sleep(1)
except KeyboardInterrupt:
    logger.info("Arrêt du producteur...")
finally:
    producer.flush()
    producer.close()
