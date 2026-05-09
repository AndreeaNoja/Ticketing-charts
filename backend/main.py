from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text, func

import models
from database import engine, get_db
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
    query = text("""
        SELECT 
            t.TICKET_NUMBER,
            s.STATUS_NAME as STATUS,
            p.PRIORITY_NAME as PRIORITY,
            c.COMPANY_NAME as COMPANY,
            tm.TEAM_NAME as TEAM,
            t.SERVICE,
            t.ASSIGNED_PERSON
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        JOIN COMPANIES c ON t.COMPANY_ID = c.COMPANY_ID
        JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    """)
    result = db.execute(query).mappings().all()
    return [dict(row) for row in result]

app.include_router(kpi_router)