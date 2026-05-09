from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from sqlalchemy import func
from kpi import router as kpi_router

app = FastAPI(title="Ticketing KPI API")

#accesezi API-ul din react
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
def get_all_tickets(db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).all()
    return tickets

app.include_router(kpi_router)