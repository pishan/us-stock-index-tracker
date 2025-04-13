from fastapi import APIRouter
from fastapi.responses import FileResponse
from datetime import date
from src.app.services.index_builder import IndexBuilder
from src.app.services.performance import PerformanceService
from src.app.services.exporter import export_to_excel
from src.app.db.repositories.duckdb_repository import DuckDBIndexRepository

repo = DuckDBIndexRepository()
index_builder = IndexBuilder(repo)
performance_service = PerformanceService(repo)

router = APIRouter()


@router.post("/build-index")
def build_index(start_date: date, end_date: date = None):
    # convert to string if needed inside service
    return index_builder.build_index(start_date.isoformat(), end_date.isoformat() if end_date else None)


@router.get("/index-performance")
def get_index_performance(start_date: date, end_date: date):
    return performance_service.get_performance(start_date.isoformat(), end_date.isoformat())


@router.get("/index-composition")
def get_index_composition(date: date):
    return performance_service.get_composition(date.isoformat())


@router.get("/composition-changes")
def get_composition_changes(start_date: date, end_date: date):
    return performance_service.get_composition_changes(start_date.isoformat(), end_date.isoformat())


@router.post("/export-data")
def export_data(start_date: date, end_date: date):
    file_name, file_path = export_to_excel(repo, start_date.isoformat(), end_date.isoformat())
    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=file_name
    )

