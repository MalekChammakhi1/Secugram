from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from functools import lru_cache
 
 
class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    db_name: str = "myapp_db"
    secret_key: str = "changeme"
    encryption_key: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
 
    class Config:
        env_file = ".env"
        extra = "ignore"
 
 
@lru_cache
def get_settings() -> Settings:
    return Settings()
 
 
class Database:
    client: AsyncIOMotorClient = None
 
 
db_instance = Database()
 
 
async def connect_db():
    settings = get_settings()
    db_instance.client = AsyncIOMotorClient(settings.mongo_uri)
    print(f"MongoDB connecté → {settings.mongo_uri} / {settings.db_name}")
 
 
async def close_db():
    """Ferme la connexion MongoDB à l'arrêt de l'app."""
    if db_instance.client:
        db_instance.client.close()
        print("MongoDB déconnecté")
 
 
def get_database():
    """Retourne l'objet base de données Motor."""
    settings = get_settings()
    return db_instance.client[settings.db_name]