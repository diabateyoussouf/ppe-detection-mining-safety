import json
import paho.mqtt.client as mqtt

# Configuration identique à celle du Publisher de l'iPhone / RPi
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "mine/safety/alerts"

def on_connect(client, userdata, flags, rc, properties=None):
    """ Callback déclenché lors de la connexion réussie au broker """
    if rc == 0:
        print(f"✅ Connecté au Broker MQTT ({MQTT_BROKER})")
        # Inscription au topic pour recevoir les alertes de l'iPhone
        client.subscribe(MQTT_TOPIC)
        print(f"👂 Écoute active sur le topic : '{MQTT_TOPIC}'...")
    else:
        print(f"❌ Échec de connexion, code retour : {rc}")

def on_message(client, userdata, msg):
    """ Callback déclenché à chaque réception d'un payload JSON """
    try:
        # Décodage du message brut reçu du réseau
        data = json.loads(msg.payload.decode("utf-8"))
        
        print("\n🚨 [NOUVELLE ALERTE SÉCURITÉ REÇUE] 🚨")
        print(f"⏱️ Heure locale : {data['timestamp']}")
        print(f"📹 Source : {data['camera_id']}")
        print(f"📊 Ouvriers visibles : {data['details']['person_count']}")
        print(f"❌ Manque CASQUE 🪖 : {data['details']['missing_helmet']}")
        print(f"❌ Manque GILET 🦺  : {data['details']['missing_vest']}")
        print("-" * 40)
        
    except Exception as e:
        print(f"⚠️ Erreur lors du décodage du message réseau : {e}")

def main():
    # Initialisation du client MQTT (Standardisé Paho v2)
    subscriber = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    
    # Association des fonctions de callback
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message

    print("🔌 Connexion au broker en cours...")
    subscriber.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Lancement d'une boucle infinie bloquante pour écouter le réseau en continu
    try:
        subscriber.loop_forever()
    except KeyboardInterrupt:
        print("\n🔌 Arrêt de l'écouteur MQTT local.")

if __name__ == "__main__":
    main()