from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import utils
from database import SessionLocal, engine

# Création des tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Alphabet Generator API")

# Dépendance pour la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/fa/random")
def read_random_fa(n: int = 1, db: Session = Depends(get_db)):
    """
    Route principale renvoyant un ou plusieurs signes.
    Gère le paramètre n pour le bonus[cite: 60].
    """
    signes_liste = utils.load_signes()
    
    if signes_liste is None:
        # Gestion d'erreur 500 pour le bonus [cite: 61]
        raise HTTPException(status_code=500, detail="Fichier signes.json introuvable.")

    import random
    # Tirage de n signes (maximum la taille de la liste)
    n = max(1, min(n, len(signes_liste)))
    selection = random.sample(signes_liste, n)

    results = []
    for s in selection:
        # On cherche la prescription en DB (si elle existe)
        results.append({
            "signe": s["nom"],
            "description": s["description"]
        })

    return results if len(results) > 1 else results[0]