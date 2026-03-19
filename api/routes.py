from datetime import datetime, timezone
 
from bson import ObjectId
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
 
from database.database import get_database
from database.models import UserCreate, UserOut, ImageOut
from security import hash_password, encrypt_bytes
 
ALLOWED_MIME = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_SIZE_BYTES = 10 * 1024 * 1024
 
images_router = APIRouter(prefix="/images", tags=["Images"])
 
 
@images_router.post("/upload", response_model=ImageOut, status_code=201)
async def upload_image(
    file: UploadFile = File(...),
    owner_id: str    = Form(...),
):
    db = get_database()
 
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(
            status_code=415,
            detail=f"Type non supporté : {file.content_type}. Acceptés : {', '.join(sorted(ALLOWED_MIME))}",
        )
 
    raw_bytes = await file.read()
    if len(raw_bytes) > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Fichier trop volumineux ({len(raw_bytes) // 1024} Ko). Limite : 10 Mo.",
        )
 
    try:
        owner_oid = ObjectId(owner_id)
    except Exception:
        raise HTTPException(status_code=400, detail="owner_id invalide (format ObjectId attendu)")
 
    owner = await db["users"].find_one({"_id": owner_oid})
    if not owner:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
 
    encrypted_bytes: bytes = encrypt_bytes(raw_bytes)
 
    now = datetime.now(timezone.utc)
    image_doc = {
        "filename":       file.filename,
        "content_type":   file.content_type,
        "size_bytes":     len(raw_bytes),
        "encrypted_data": encrypted_bytes,
        "owner_id":       owner_oid,
        "uploaded_at":    now,
    }
    result = await db["images"].insert_one(image_doc)
 
    return ImageOut(
        id=str(result.inserted_id),
        filename=file.filename,
        content_type=file.content_type,
        size_bytes=len(raw_bytes),
        owner_id=owner_id,
        uploaded_at=now,
    )