from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from service import analyze_routes_service, analyze_po_pi_service, analyze_po_mtc_service

router = APIRouter()

# ======================
# 1. ROUTES
# ======================
@router.post("/routes")
async def analyze_routes(trucks_file: UploadFile = File(...), invoice_file: UploadFile = File(...)):
    try:
        result = await analyze_routes_service(trucks_file, invoice_file)
        return {"result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/po-vs-pi")
async def analyze_po_vs_pi(po_file: UploadFile = File(...), pi_file: UploadFile = File(...)):
    try:
        result = await analyze_po_pi_service(po_file, pi_file)
        return {"result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/po-vs-mtc")
async def analyze_po_vs_mtc(po_file: UploadFile = File(...), mtc_file: UploadFile = File(...)):
    try:
        result = await analyze_po_mtc_service(po_file, mtc_file)
        return {"result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ======================
# 4–8. Other services (stubbed)
# ======================

@router.post("/po-vs-commande")
async def analyze_po_vs_commande(po_file: UploadFile = File(...), supplier_file: UploadFile = File(...)):
    return {"result": "Not yet implemented"}

@router.post("/achat-vs-invoice")
async def analyze_achat_vs_invoice(achat_file: UploadFile = File(...), invoice_file: UploadFile = File(...), packing_file: UploadFile = File(...)):
    return {"result": "Not yet implemented"}


@router.post("/logistics")
async def analyze_logistics(logistics_file: UploadFile = File(...)):
    return {"result": "Not yet implemented"}

@router.post("/option7")
async def analyze_option7(file: UploadFile = File(...)):
    return {"result": "Not yet implemented"}

@router.post("/option8")
async def analyze_option8(file: UploadFile = File(...)):
    return {"result": "Not yet implemented"}

@router.post("/option9")
async def analyze_option9(file: UploadFile = File(...)):
    return {"result": "Not yet implemented"}
