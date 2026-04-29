import json
import random
import os

def load_signes():
    """Charge les signes depuis le fichier JSON."""
    file_path = "signes.json"
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_random_signe():
    """Récupère un signe au hasard."""
    signes = load_signes()
    if signes:
        return random.choice(signes)
    return None