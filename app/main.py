from fastapi.middleware.cors import CORSMiddleware
 
from database.database import connect_db, close_db
from api.routes import users_router, images_router
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()
 
 
app = FastAPI(title="Serveur d'enregistrement d'images", version="1.0.0", lifespan=lifespan)
 
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST"], allow_headers=["*"])
 
app.include_router(images_router)
 
 
@app.get("/")
async def root():
    return {"status": "ok", "docs": "/docs"}