# Test-technique-WILI

## 🛠️ Installation des dépendances

Assurez-vous d'avoir Python 3.8+ installé.

```bash
pip install fastapi uvicorn sqlalchemy
```

## Comment lancer le serveur

Pour démarrer l'application, utilisez le serveur Uvicorn à la racine du projet:

```bash
    uvicorn main:app --reload
```

Le serveur sera alors accessible sur : <http://127.0.0.1:8000>

## Comment tester la route API

Vous pouvez tester le fonctionnement de l'API en vous Rendant sur <http://127.0.0.1:8000/docs> pour tester toutes les routes (GET et POST) visuellement

## Ce qui a été fait

- Configuration : Initialisation du dépôt Git avec les branches main et feature/test
- Backend : Création de l'API avec FastAPI, lecture du fichier signes.json et route /fa/random fonctionnelle
- Frontend : Fichier index.html utilisant fetch pour afficher le résultat sans rechargement de page
- Intégration d'une base de données SQLite pour stocker et renvoyer les prescriptions
- Paramètre ?n= pour renvoyer plusieurs signes
- Gestion des erreurs HTTP 500 en cas de fichier manquant
