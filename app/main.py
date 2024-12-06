from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import auth, users, products, sales

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Système de Gestion pour Petites Entreprises",
             description="API pour la gestion des petites entreprises",
             version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(auth.router, prefix="/auth", tags=["Authentification"])
app.include_router(users.router, prefix="/users", tags=["Utilisateurs"])
app.include_router(products.router, prefix="/products", tags=["Produits"])
app.include_router(sales.router, prefix="/sales", tags=["Ventes"])

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans le Système de Gestion pour Petites Entreprises"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
