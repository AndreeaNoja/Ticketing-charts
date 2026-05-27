from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime, timedelta
from typing import Optional

import models
from database import engine, get_db
from kpi import router as kpi_router

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
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    team: Optional[str] = Query(None),
    startDate: Optional[date] = Query(None),
    endDate: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT 
            t.TICKET_NUMBER,
            s.STATUS_NAME as STATUS,
            p.PRIORITY_NAME as PRIORITY,
            c.COMPANY_NAME as COMPANY,
            tm.TEAM_NAME as TEAM,
            t.CATEGORY_TIER_1,
            t.CATEGORY_TIER_2,
            t.CATEGORY_TIER_3,
            t.SERVICE,
            t.ASSIGNED_PERSON,
            t.SUBMIT_DATETIME
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        JOIN COMPANIES c ON t.COMPANY_ID = c.COMPANY_ID
        JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
        WHERE (:status IS NULL OR s.STATUS_NAME = :status)
          AND (:priority IS NULL OR p.PRIORITY_NAME = :priority)
          AND (:team IS NULL OR tm.TEAM_NAME = :team)
          AND (:start_date IS NULL OR t.SUBMIT_DATETIME >= :start_date)
          AND (:end_date IS NULL OR t.SUBMIT_DATETIME < :end_date)
        ORDER BY t.SUBMIT_DATETIME DESC
    """)

    start_date = datetime.combine(startDate, datetime.min.time()) if startDate else None
    # endDate is inclusive for the user; SQL predicate uses < next_day
    end_date = datetime.combine(endDate + timedelta(days=1), datetime.min.time()) if endDate else None
    params = {
        "status": status or None,
        "priority": priority or None,
        "team": team or None,
        "start_date": start_date,
        "end_date": end_date,
    }

    result = db.execute(query, params).mappings().all()
    return [dict(row) for row in result]

# include routerul KPI in applicatie
app.include_router(kpi_router)