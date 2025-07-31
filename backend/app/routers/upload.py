from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for processing.
    Accepts PDF/JPG files for OCR and AI processing.
    """
    if file.content_type not in ["application/pdf", "image/jpeg", "image/jpg"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF and JPG files are supported."
        )
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File uploaded successfully",
        "status": "processing"
    }