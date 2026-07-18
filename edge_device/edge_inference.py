import cv2
import time
from ultralytics import YOLO
from mqtt_publisher import MQTTPublisher

def main():
    # 1. Initialisation MQTT
    publisher = MQTTPublisher()
    publisher.connect()

    # 2. Modèle personnalisé chargé depuis Colab
    print("📥 Chargement de ton modèle YOLO personnalisé VALIDE (best.pt)...")
    model = YOLO("edge_device/weights/best.pt")

    print("\n🔍 Configuration des 14 classes Roboflow détectée.")
    
    # 3. Connexion au flux de l'iPhone
    IPHONE_VIDEO_URL = "http://192.168.1.170:8081/video"
    print(f"📡 Connexion au flux vidéo : {IPHONE_VIDEO_URL}")
    cap = cv2.VideoCapture(IPHONE_VIDEO_URL) 
    camera_id = "Zone_Extraction_Nord"

    # Optimisations anti-lag
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))

    print("🚀 Inférence intelligente connectée aux classes du modèle...")
    print("💡 Appuie sur Ctrl+C pour arrêter.")

    last_mqtt_send_time = 0
    mqtt_send_interval = 1.0 

    # --- Variables de lissage anti-clignotement (Effet mémoire) ---
    cooldown_counter = 0
    stored_missing_helmet = 0
    stored_missing_vest = 0
    stored_total = 0

    try:
        while cap.isOpened():
            for _ in range(5):
                cap.grab()
            
            ret, frame = cap.retrieve()
            if not ret:
                print("⚠️ Flux vidéo interrompu.")
                time.sleep(1)
                continue

            # Inférence (Seuil abaissé à 0.25 pour une meilleure réactivité à la maison)
            results = model(frame, conf=0.25, verbose=False)[0]

            person_count = 0
            hardhat_count = 0
            no_hardhat_count = 0
            vest_count = 0
            no_vest_count = 0

            # 4. Parcours des détections
            for box in results.boxes:
                cls_id = int(box.cls[0])
                nom_classe = model.names[cls_id]
                
                if nom_classe == "Person":
                    person_count += 1
                elif nom_classe == "Hardhat":
                    hardhat_count += 1
                elif nom_classe == "NO-Hardhat":
                    no_hardhat_count += 1
                elif nom_classe == "Safety Vest":
                    vest_count += 1
                elif nom_classe == "NO-Safety Vest":
                    no_vest_count += 1

            # Logique hybride de sécurité
            total_personnes = max(person_count, (hardhat_count + no_hardhat_count), (vest_count + no_vest_count))
            missing_helmet = max(no_hardhat_count, total_personnes - hardhat_count)
            missing_vest = max(no_vest_count, total_personnes - vest_count)

            # --- APPLICATION DU FILTRE ANTI-BRUIT ---
            if missing_helmet > 0 or missing_vest > 0:
                # Une infraction est détectée : on l'envoie immédiatement et on initialise le maintien
                cooldown_counter = 3  # Garde l'alerte active pendant au moins 3 secondes
                stored_missing_helmet = missing_helmet
                stored_missing_vest = missing_vest
                stored_total = total_personnes
            else:
                # L'IA ne voit plus d'infraction à cet instant précis
                if cooldown_counter > 0:
                    cooldown_counter -= 1
                    # On force le maintien des données de danger pour stabiliser Streamlit
                    missing_helmet = stored_missing_helmet
                    missing_vest = stored_missing_vest
                    total_personnes = stored_total
            # ----------------------------------------

            # Log console propre
            print(f"👀 [IA] Présents: {total_personnes} | Manque Casque: {missing_helmet} | Manque Gilet: {missing_vest}   ", end="\r")

            # 5. Synchronisation MQTT
            current_time = time.time()
            if current_time - last_mqtt_send_time >= mqtt_send_interval:
                publisher.envoyer_alerte(camera_id, total_personnes, missing_helmet, missing_vest)
                last_mqtt_send_time = current_time

    except KeyboardInterrupt:
        print("\n🛑 Arrêt manuel de l'IA par l'utilisateur.")
    
    finally:
        cap.release()
        publisher.disconnect()
        print("🔌 Déconnexion réussie.")

if __name__ == "__main__":
    main()