from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import utils
import models
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
    """
    signes_liste = utils.load_signes()
    
    if signes_liste is None:
        # Gestion d'erreur 500
        raise HTTPException(status_code=500, detail="Fichier signes.json introuvable.")

    import random
    # Tirage de n signes (maximum la taille de la liste)
    n = max(1, min(n, len(signes_liste)))
    selection = random.sample(signes_liste, n)

    results = []
    for s in selection:
        prescription = db.query(models.Prescription).filter(models.Prescription.signe_nom == s["nom"]).first()
        results.append({
            "signe": s["nom"],
            "description": s["description"],
            "prescription": prescription.texte if prescription else "Aucune prescription disponible."
        })

    return results if len(results) > 1 else results[0]


from pydantic import BaseModel

class PrescriptionCreate(BaseModel):
    signe_nom: str
    texte: str

@app.post("/fa/prescriptions")
def create_prescription(item: PrescriptionCreate, db: Session = Depends(get_db)):
    """Ajoute une nouvelle prescription liée à un signe."""
    signes = utils.load_signes()
    noms_valides = [s["nom"] for s in signes]
    
    if item.signe_nom not in noms_valides:
        raise HTTPException(status_code=400, detail="Nom de signe invalide.")

    # Création de l'entrée en base
    new_presc = models.Prescription(signe_nom=item.signe_nom, texte=item.texte)
    db.add(new_presc)
    db.commit()
    db.refresh(new_presc)
    return {"status": "success", "data": new_presc}



# CORS CONFIG

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# Monte le dossier static pour servir les fichiers
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')