from flask import Blueprint

router = Blueprint("health_check", __name__, url_prefix="health_check")

@router.get("/")
def health_check():
    return {
        "status": "OK"
    }