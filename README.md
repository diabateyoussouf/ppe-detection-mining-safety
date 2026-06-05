# ppe-detection-mining-safety
<img width="3999" height="3391" alt="image" src="https://github.com/user-attachments/assets/23393f0c-6360-45ed-bf8b-d20b67a77557" />

# Mining Safety — IoT System

Ce projet est un système de surveillance intelligent basé sur l'**IoT** et l'**Edge AI** conçu pour sécuriser les environnements miniers. Il détecte en temps réel si le personnel porte correctement ses Équipements de Protection Individuelle (EPI : casque, gilet) et transmet instantanément des métadonnées d'alerte via le protocole MQTT vers un tableau de bord centralisé.

---

##  Stack Technologique & Logos

| Composant | Technologies Utilisées |
| :--- | :--- |
| **Langage Principal** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) |
| **Matériel / Edge** | ![Raspberry Pi](https://img.shields.io/badge/-Raspberry%20Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi&logoColor=white) |
| **Vision par Ordinateur** | ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white) ![YOLOv10](https://img.shields.io/badge/YOLOv10-Ultralytics-007ACC?style=for-the-badge) |
| **Protocole IoT** | ![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-3C525F?style=for-the-badge&logo=eclipse-mosquitto&logoColor=white) |
| **Visualisation / UI** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) |

---

## Architecture & Concept Système

Le projet adopte une architecture découplée orientée **Edge Computing**. Contrairement aux systèmes classiques qui saturent la bande passante en envoyant des flux vidéo bruts, l'intelligence est déportée localement sur le capteur (le Raspberry Pi).

```text
  [ 🎥 Caméra Pi ] 
         │  (Flux vidéo local)
         ▼
  [ 🧠 Raspberry Pi ] ───► Prétraitement (CLAHE / Contraste Mine)
         │               ───► Inférence IA (YOLOv10n local)
         ▼  
  [ 🛰️ Payload JSON ] ───► Métadonnées (Ex: "1 Ouvrier sans casque")
         │
         ▼  (Protocole MQTT — Broker)
  [ 🌐 Internet / 4G ] 
         │
         ▼  (Abonnement / Subscribe)
  [ 📊 Dashboard Streamlit ] ───► Alertes visuelles & Statistiques en temps réel
