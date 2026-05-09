from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/kpi",
    tags=["kpi"]
)

# KPI 1: numar total de tickete:
@router.get("/tickets/total")
def get_all_tickets(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT COUNT(*) as total_tickets
        FROM INCIDENT_TICKETS
    """)

    result = db.execute(query).mappings().first()
    return {
        "label": "Total Tickets",
        "value": result["total_tickets"]
    }


# KPI 2: tickete aranjate dupa status:
@router.get("/tickets/status")
def get_tickets_by_status(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT s.STATUS_NAME as status, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        GROUP BY s.STATUS_NAME
    """)

    result = db.execute(query).mappings().all()
    return [
        {
            "status": row["status"] if row["status"] is not None else "Necunoscut",
            "count": row["ticket_count"]
        }
        for row in result
    ]

# KPI 3: tickete aranjate dupa prioritate:
@router.get("/tickets/priority")
def get_tickets_by_priority(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT p.PRIORITY_NAME as priority, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        GROUP BY p.PRIORITY_NAME
        ORDER BY ticket_count DESC
    """)

    result = db.execute(query).mappings().all()
    return [
        {
            "priority": row["priority"] if row["priority"] is not None else "Necunoscut",
            "count": row["ticket_count"]
        }
        for row in result
    ]

# KPI 4: timp mediu de rezolvare a ticketelor:
@router.get("/tickets/average-resolution-time")
def get_average_resolution_time(db: Session = Depends(get_db)):
    query = text(
    """ 
        SELECT AVG(DATEDIFF(SECOND, SUBMIT_DATETIME, RESOLVED_DATETIME)) as average_resolution_seconds
        FROM INCIDENT_TICKETS
        WHERE RESOLVED_DATETIME is not NULL AND SUBMIT_DATETIME is not NULL
    """)

    result = db.execute(query).mappings().first()
    return {
        "label": "Average Resolution Time:",
        "value": result["average_resolution_seconds"]
    }

# KPI ..

# Dashboard cu primele 3 KPI-urile:
@router.get("/dashboard")
def get_kpi_dashboard(db: Session = Depends(get_db)):
    total_tickets_query = text(
    """
        SELECT COUNT(*) as total_tickets
        FROM INCIDENT_TICKETS
    """)

    status_query = text(
    """
        SELECT 
            s.STATUS_NAME as status,
            COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        GROUP BY s.STATUS_NAME
    """)

    priority_query = text(
    """
        SELECT 
            p.PRIORITY_NAME as priority,
            COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        GROUP BY p.PRIORITY_NAME
        ORDER BY ticket_count DESC
    """)

    total_tickets_result = db.execute(total_tickets_query).mappings().first()
    status_result = db.execute(status_query).mappings().all()
    priority_result = db.execute(priority_query).mappings().all()

    return {
        "total_tickets": 
        {
            "label": "Total Tickets",
            "value": total_tickets_result["total_tickets"]
        },

        "tickets_by_status": 
        [
            {
                "status": row["status"] if row["status"] is not None else "Necunoscut",
                "count": row["ticket_count"]
            }
            for row in status_result
        ],

        "tickets_by_priority": 
        [
            { 
                "priority": row["priority"] if row["priority"] is not None else "Necunoscut",
                "count": row["ticket_count"]
            }
            for row in priority_result
        ]
    }