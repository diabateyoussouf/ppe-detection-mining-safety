import json
import threading
from datetime import datetime
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

def on_message(store):
    def callback(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())

            # Lecture flexible (Racine ou sous-objet details pour éviter les KeyError)
            p = payload.get("person_count", payload.get("details", {}).get("person_count", 0))
            mh = payload.get("missing_helmet", payload.get("details", {}).get("missing_helmet", 0))
            mv = payload.get("missing_vest", payload.get("details", {}).get("missing_vest", 0))

            # Mise à jour des compteurs globaux
            store["personnel"] = p
            store["helmet"] = max(0, p - mh)
            store["vest"] = max(0, p - mv)

            current_time = datetime.now().strftime("%H:%M:%S")
            is_danger = (mh > 0 or mv > 0)

            # --- LOGIQUE DE FILTRAGE DES LOGS ---
            last_log = store["logs"][0] if store["logs"] else None
            current_status = "DANGER" if is_danger else "SAFE"
            current_msg = f"Manque Casque: {mh} | Manque Gilet: {mv}" if is_danger else "Personnel conforme"

            # On n'écrit un log QUE s'il y a un changement réel pour éviter de saturer la liste
            should_log = False
            if not last_log or last_log["status"] != current_status:
                should_log = True
            elif current_status == "DANGER" and last_log["message"] != current_msg:
                should_log = True

            if is_danger:
                store["alert"] = True
                store["risk"] = 85  # Augmenté à 85% pour que la jauge vire bien au rouge !
            else:
                store["alert"] = False
                store["risk"] = 5

            if should_log:
                store["logs"].insert(
                    0,
                    {
                        "time": current_time,
                        "status": current_status,
                        "message": current_msg
                    }
                )
                store["logs"] = store["logs"][:10]  # Garde les 10 derniers événements

        except Exception as e:
            print(f"❌ Erreur parsing MQTT Dashboard : {e}")

    return callback

def start_mqtt(store):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message(store)
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.subscribe(MQTT_TOPIC)
        threading.Thread(target=client.loop_forever, daemon=True).start()
    except Exception as e:
        print(f"❌ Connexion au Broker MQTT impossible : {e}")
        
    return client