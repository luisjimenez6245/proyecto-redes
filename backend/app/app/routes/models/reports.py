from fastapi_helpers import DefaultModelRouter
from crud import report_crud
from models import Report

router = DefaultModelRouter(Report, report_crud).router
