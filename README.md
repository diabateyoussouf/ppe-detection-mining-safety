# Mining Safety — IoT System

![Python](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=ffdd54) ![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=flat-square&logo=Raspberry-Pi&logoColor=white) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) ![YOLO26s](https://img.shields.io/badge/YOLOv10-Ultralytics-007ACC?style=flat-square) ![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-3C525F?style=flat-square&logo=eclipse-mosquitto&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)

## 📝 Introduction
Les industries minières et les chantiers d'extraction figurent parmi les environnements de travail les plus exigeants et dangereux au monde. Malgré des réglementations strictes, le non-port ou le port incorrect des Équipements de Protection Individuelle (EPI / PPE) reste l'une des causes majeures d'accidents graves. Traditionnellement, la vérification repose sur des inspections humaines visuelles, une méthode sujette à la fatigue et impossible à assurer en continu.

Le projet **Mining Safety** répond à ce défi en proposant une solution de rupture combinant l'**Intelligence Artificielle embarquée (Edge AI)** et l'**Internet des Objets (IoT)**. Ce système transforme une simple caméra de surveillance en un agent de sécurité autonome, capable de détecter en temps réel les infractions au port des équipements et d'alerter instantanément les superviseurs sur un tableau de bord dédié.

---

## ❓ Pourquoi ce projet ? (Motivations & Enjeux)
Le développement de ce système s'appuie sur quatre piliers fondamentaux :
* **La préservation des vies humaines :** L'objectif ultime est d'atteindre le "zéro accident" en détectant un oubli de casque ou de gilet *avant* qu'un ouvrier ne pénètre dans une zone à risque.
* **Gestion des contraintes réseau (Edge AI) :** Envoyer des flux vidéo en continu vers un cloud sature la bande passante de la mine. Faire l'inférence IA directement sur le Raspberry Pi permet de ne faire circuler que quelques octets de texte (alertes JSON), rendant le système ultra-léger et résilient.
* **Liaison locale haute performance :** Contrairement aux systèmes dépendants de la 4G, l'infrastructure repose ici entièrement sur un réseau local câblé ou sans fil (**Wi-Fi / RJ45**), assurant une latence minimale et une indépendance vis-à-vis d'Internet.
* **Capitalisation des compétences :** Ce projet valide un modèle architectural standardisé (Capture ➔ Inférence Locale ➔ Transport MQTT ➔ Dashboard Streamlit) directement calqué sur des architectures IoT de pointe, facilitant sa transposition à d'autres problématiques complexes (ex: surveillance de maison).

---

## 🖼️ Architecture Générale

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/cc9e741a-2e69-4325-a216-77674f842185" />

---

## 🏗️ Concept Système & Flux de Données

```text
  [ 🎥 Caméra Pi ] 
         │  (Flux vidéo local)
         ▼
  [ 🧠 Raspberry Pi / Smart Phone ] ───► Prétraitement (CLAHE / Contraste Mine)
         │               ───► Inférence IA (YOLOv10n local)
         ▼  
  [ 🛰️ Payload JSON ] ───► Métadonnées (Ex: "1 Ouvrier sans casque")
         │
         ▼  (Protocole MQTT — Liaison locale LAN)
  [ 📶 Wi-Fi / RJ45 ] 
         │
         ▼  (Abonnement / Subscribe)
  [ 📊 Dashboard Streamlit ] ───► Alertes visuelles & Statistiques en temps réel
```
## Objectifs Spécifiques de Réalisation
Acquisition & Prétraitement : Capture vidéo optimisée pour les variations de luminosité et la poussière des galeries minières via OpenCV (filtres adaptatifs type CLAHE).

Développement IA (Edge AI) : Inférence locale rapide à l'aide d'un modèle YOLO26s optimisé pour l'architecture matérielle nvidia.

Intégration IoT : Pipeline de communication asynchrone ultra-léger via un broker MQTT fonctionnant sur le réseau local (Wi-Fi / RJ45).

Analyse & Visualisation : Interface web interactive sous Streamlit pour le suivi des indicateurs clés (KPI) de sécurité et la gestion des alertes.

## Structure du Projet:
```text
ppe-detection-mining-safety/
├── edge_device/               # Scripts exécutés sur le materiel nvidia (Terrain)
│   ├── weights/               # Modèles YOLO légers exportés
│   ├── utils/                 # Fonctions de traitement d'image (CLAHE...)
│   ├── edge_inference.py      # Script principal (Vision + IA locale)
│   └── mqtt_publisher.py      # Module d'envoi des messages MQTT
│
├── dashboard_app/             # Application Serveur / Dashboard (Superviseur)
│   ├── app.py                 # Interface utilisateur Streamlit (inclut le subscriber)
│
└── requirements.txt           # Dépendances du projet
```
## Conclusion
En associant la vélocité du modèle de vision par ordinateur YOLO26s à la légèreté du protocole de messagerie MQTT, ce projet démontre la viabilité des architectures distribuées appliquées à la sécurité industrielle. Le prototype développé prouve qu'avec du matériel accessible et une pile logicielle optimisée (Python, Streamlit), il est possible de concevoir un système de surveillance performant, non intrusif pour la bande passante, et hautement réactif.

Plus qu'une simple application de détection d'objets, ce projet pose les bases d'une infrastructure IoT pour l'Industrie 4.0. Les perspectives d'évolution sont vastes, notamment l'intégration de la reconnaissance faciale pour identifier l'employé en infraction ou l'automatisation des barrières d'accès si les EPI ne sont pas détectés.

