from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
from kpi import router as kpi_router, exec_procedure, CommonKpiFilters

app = FastAPI(title="Ticketing KPI API")

# accesezi API-ul din react
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Backend-ul este pornit și funcționează!"}

@app.get("/tickets")
def get_all_tickets(
    filters: dict = Depends(CommonKpiFilters),
    db: Session = Depends(get_db)
):
    result = exec_procedure(db, "GetTickets", filters).all()
    return [dict(row) for row in result]

# include routerul KPI in applicatie
app.include_router(kpi_router)