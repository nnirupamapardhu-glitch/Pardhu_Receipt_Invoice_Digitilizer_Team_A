from fastapi import APIRouter, UploadFile, File, Depends
import os
import shutil
from app.services.ocr_service import extract_text_from_image
from app.services.llm_service import extract_invoice_data
from app.repositories.invoice_repo import create_invoice
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/invoice", tags=["invoice"])

# Upload Route
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = extract_text_from_image(file_path)
    structure_data = extract_invoice_data(raw_text)

    saved_invoice = create_invoice(
        db,
        structure_data,
        file_path,
        user_id=1
    )

    return {
        "filename": file.filename,
        "extracted_text": structure_data,
        "message": "Invoice saved successfully",
        "invoice_id": saved_invoice.id,
        "invoice_number": saved_invoice.invoice_number,
        "vendor_name": saved_invoice.vendor_name,
        "total_amount": saved_invoice.total_amount
    }


# NEW ROUTE: Fetch All Invoices
@router.get("/all")
def get_all_invoices(db: Session = Depends(get_db)):
    from app.models import Invoice

    invoices = db.query(Invoice).all()

    return [
        {
            "id": invoice.id,
            "filename": invoice.file_path.split("/")[-1] if invoice.file_path else "",
            "invoice_number": invoice.invoice_number,
            "vendor_name": invoice.vendor_name,
            "total_amount": invoice.total_amount,
            "date": invoice.date,
        }
        for invoice in invoices
    ]
