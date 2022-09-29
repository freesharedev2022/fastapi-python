from fastapi import APIRouter

router = APIRouter(
    tags=["root"]
)

@router.get("/")
def read_root():
    return {"code": 200, "message": "Success"}