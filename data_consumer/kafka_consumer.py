from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration pour accéder à MongoDB installé sur Windows depuis un conteneur Docker
mongo_host = 'host.docker.internal'
mongo_port = 27017

# Connexion à MongoDB avec test de connexion
try:
    client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}', serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Test de la connexion
    logger.info("Connexion à MongoDB réussie.")
except Exception as e:
    logger.error(f"Erreur de connexion à MongoDB : {e}")

db = client['twitter_db']
collection = db['twitter_collection_raw']

# Consommateur Kafka
consumer = KafkaConsumer(
    'twitter_data_test_Kafka',
    bootstrap_servers='kafka:9092',  # Remplacer par le nom correct si besoin
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Boucle de consommation
for message in consumer:
    try:
        data = message.value
        logger.info(f"Message reçu : {data}")

        # Nettoyage ou renommage si nécessaire
        data['Tweet content'] = data.pop('Tweet Content', data.get('Tweet content', ''))

        # Insertion MongoDB
        collection.insert_one(data)
        logger.info("Document inséré dans MongoDB.")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'insertion : {e}")
