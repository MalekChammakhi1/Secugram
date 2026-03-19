# Secugram : Serveur de stockage d'images chiffrées

## Rôle de ce serveur

Ce serveur est un **pur service de stockage**. Son unique responsabilité est de recevoir une image envoyée par un **tiers de confiance** bien chiffrée puis de la **persister dans MongoDB**.

Aucune image n'est stockée en clair. Les données en base sont illisibles.

---

## Structure du projet

```
Secugram/                           BACKEND SECUGRAM (Stockage pur)
     ├── README.md                          → Documentation
     ├── requirements.txt                   → Dépendances Python
     │
     └── app/
        ├── main.py                         → Point d'entrée
        │
        ├── api/
        │   └── routes.py
        │
        │
        └── database/                        → Persistence des données
            ├── database.py
            └── models.py 
```

---

## Prérequis

- Python 3.10+
- MongoDB (local ou Atlas, voir ci-dessous)

---

## Installation

### 1. Cloner et créer l'environnement virtuel

```bash
git clone https://github.com/MalekChammakhi1/Secugram.git
cd secugram

python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configurer le fichier `.env`

```env
MONGO_URI=mongodb://localhost:27017     # ou URI Atlas (voir ci-dessous)
```

---

## MongoDB — deux options

### Option A — MongoDB local

**Ubuntu / Debian**
```bash
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS (Homebrew)**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Windows**
Télécharger l'installeur sur [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community), puis :
```powershell
net start MongoDB
```

Vérification :
```bash
mongosh --eval "db.runCommand({ connectionStatus: 1 })"
```

Dans `.env` :
```env
MONGO_URI=mongodb://localhost:27017
```

---

### Option B — MongoDB Atlas (cloud, aucune installation)

1. Créer un compte gratuit sur [cloud.mongodb.com](https://cloud.mongodb.com)
2. Créer un cluster **Free Tier (M0)**
3. Dans **Database Access** → créer un utilisateur avec mot de passe
4. Dans **Network Access** → ajouter votre IP (ou `0.0.0.0/0` pour tout autoriser)
5. Dans **Connect** → choisir *Drivers* → copier l'URI

Dans `.env` :
```env
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

---

## Lancer le serveur

```bash
uvicorn main:app --reload
```

L'API est disponible sur `http://localhost:8000`
La documentation interactive Swagger sur `http://localhost:8000/docs`

---
