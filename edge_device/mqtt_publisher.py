import json
from datetime import datetime
import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, broker="broker.hivemq.com", port=1883, topic="mine/safety/alerts"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        
    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            print(f"📡 Connecté au Broker MQTT : {self.broker}")
        except Exception as e:
            print(f"❌ Échec de connexion au Broker : {e}")

    def envoyer_alerte(self, camera_id, person_count, missing_helmet, missing_vest):
        # ⚡ OPTIMISATION : Données envoyées à la fois à la racine ET dans details
        # pour être compatible avec n'importe quelle configuration du Dashboard
        payload = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "camera_id": camera_id,
            "infraction_detected": True if (missing_helmet > 0 or missing_vest > 0) else False,
            "person_count": int(person_count),       # Racine
            "missing_helmet": int(missing_helmet),   # Racine
            "missing_vest": int(missing_vest),       # Racine
            "details": {                             # Sous-objet (au cas où)
                "person_count": int(person_count),
                "missing_helmet": int(missing_helmet),
                "missing_vest": int(missing_vest)
            }
        }
        self.client.publish(self.topic, json.dumps(payload), qos=1)
        print(f"🔔 [MQTT Send] : Pers={payload['person_count']} | Barbouillages={payload['missing_helmet']}/{payload['missing_vest']}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()