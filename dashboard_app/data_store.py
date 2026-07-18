from datetime import datetime

def init_store():
    return {
        "personnel": 0,
        "helmet": 0,
        "vest": 0,
        "risk": 0,
        "alert": False,
        "logs": [
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "status": "SAFE",
                "message": "Système initialisé avec succès"
            }
        ]
    }