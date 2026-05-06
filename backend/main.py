from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from sqlalchemy import func

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

@app.get("/tickets/stats/priority")
def get_priority_stats(db: Session = Depends(get_db)):
    stats = db.query(models.Ticket.PRIORITY, func.count(models.Ticket.TICKET_NUMBER)) \
              .group_by(models.Ticket.PRIORITY).all()
    return {priority: count for priority, count in stats}

@app.get("/tickets/stats/status")
def get_status_stats(db: Session = Depends(get_db)):
    stats = db.query(models.Ticket.STATUS, func.count(models.Ticket.TICKET_NUMBER)) \
              .group_by(models.Ticket.STATUS).all()
    return {status: count for status, count in stats}

