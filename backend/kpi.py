from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/kpi",
    tags=["kpi"]
)

# KPI 1: numar total de tickete: - card
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


# KPI 2: tickete aranjate dupa status: - pie chart
@router.get("/tickets/status/status-bar")
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

# KPI 3: tickete aranjate dupa prioritate: - bar chart
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

# KPI 4: timp mediu de rezolvare a ticketelor: -card
@router.get("/tickets/average-resolution-time")
def get_average_resolution_time(db: Session = Depends(get_db)):
    query = text(
    """ 
        SELECT AVG(DATEDIFF(SECOND, SUBMIT_DATETIME, RESOLVED_DATETIME)) as average_resolution_seconds
        FROM INCIDENT_TICKETS
        WHERE RESOLVED_DATETIME is not NULL AND SUBMIT_DATETIME is not NULL
    """)

    result = db.execute(query).mappings().first()
    avg_resolution_time = []
    for row in result:
        avg_seconds = row["avg_resolution_time"] if row["avg_resolution_time"] is not None else 0
        avg_resolution_time.append({
            "team": row["team"] if row["team"] is not None else "Necunoscut",
            "average_resolution_time_seconds": round(avg_seconds, 2),
            "average_resolution_time_minutes": round(avg_seconds / 60, 2),
            "average_resolution_time_hours": round(avg_seconds / 3600, 2)
        })
    
    return {
        "label": "Average Resolution Time",
        "data": avg_resolution_time
    }
    

# KPI 5: numarul total de statusuri nerezolvate in procent din total: -card
@router.get("/tickets/status/unresolved-percentage")
def get_unresolved_percentage(db: Session = Depends(get_db)):
    unresolved_query = text (
    """
        SELECT COUNT(*) as unresolved_count
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS = s.STATUS_ID
        WHERE s.STATUS_NAME != 'Closed' AND s.STATUS_NAME != 'Resolved'
    """)

    result_unresolved  = db.execute(unresolved_query).mappings().first()
    total_tickets_query = text(
    """
        SELECT COUNT(*) as total_tickets
        FROM INCIDENT_TICKETS 
    """
    )

    result_total = db.execute(total_tickets_query).mappings().first()
    unresolved_count = result_unresolved["unresolved_count"]
    total_tickets = result_total["total_tickets"]
    percentage = round((unresolved_count / total_tickets) * 100, 2) if total_tickets > 0 else 0.00
    return {
        "label": "Unresolved Tickets Percentage:",
        "value": percentage
    }

# KPI 6: numarul total de statusuri rezolvate in procent din total: - card
@router.get("/tickets/status/resolved-percentage")
def get_resolved_percentage(db: Session = Depends(get_db)):
    resolved_query = text (
    """
        SELECT COUNT(*) as resolved_count
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS = s.STATUS_ID
        WHERE s.STATUS_NAME = 'Closed' OR s.STATUS_NAME = 'Resolved'
    """)

    result_resolved  = db.execute(resolved_query).mappings().first()
    total_tickets_query = text(
    """
        SELECT COUNT(*) as total_tickets
        FROM INCIDENT_TICKETS 
    """
    )

    result_total = db.execute(total_tickets_query).mappings().first()
    resolved_count = result_resolved["resolved_count"]
    total_tickets = result_total["total_tickets"]
    percentage = round((resolved_count / total_tickets) * 100, 2) if total_tickets > 0 else 0.00
    return {
        "label": "Resolved Tickets Percentage:",
        "value": percentage
    }

# KPI 7: numarul total de statusuri cu timpul de lucru depasit in procent din total: - card
@router.get("/tickets/status/overdue-percentage")
def get_overdue_percentage(db: Session = Depends(get_db)):
    overdue_query = text (
    """ 
        SELECT COUNT(*) as overdue_count
        FROM INCIDENT_TICKETS t
        WHERE t.ESTIMATED_RESOLUTION_DATETIME < t.RESOLVED_DATETIME AND
              t.RESOLVED_DATETIME is not NULL
    """)

    result_overdue = db.execute(overdue_query).mappings().first()
    total_tickets_query = text(
    """
        SELECT COUNT(*) as total_tickets
        FROM INCIDENT_TICKETS 
    """
    )

    result_total = db.execute(total_tickets_query).mappings().first()
    overdue_count = result_overdue["overdue_count"]
    total_tickets = result_total["total_tickets"]
    percentage = round((overdue_count / total_tickets) * 100, 2) if total_tickets > 0 else 0.00
    return {
        "label": "Overdue Tickets Percentage:",
        "value": percentage
    }

# KPI 8: numarul total de tickete pe echipa: - bar chart
@router.get("/tickets/team/tickets-per-team")
def get_tickets_per_team(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT tm.TEAM_NAME as team, COUNt(*) as ticket_count
        FROM INCIDENT_TICKETS t
        JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
        Group BY tm.TEAM_NAME
    """)

    result = db.execute(query).mappings().all()
    return {
        "data": [
            {
                "team": row["team"] if row["team"] is not None else "Necunoscut",
                "count": row["ticket_count"]
            }
            for row in result
        ]
    }

# KPI 9: timp mediu de rezolvare pe echipa: - bar chart
@router.get("/tickets/team/average-resolution-time-per-team")
def get_average_resolution_time_per_team(db: Session = Depends(get_db)):
    query = text (
    """
        SELECT tm.TEAM_NAME as team, 
               AVG(CAST(DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) as FLOAT)) as avg_resolution_time
        FROM TEAMS tm
        LEFT JOIN INCIDENT_TICKETS t ON t.TEAM_ID = tm.TEAM_ID AND 
                                        t.RESOLVED_DATETIME is not NULL
        Group BY tm.TEAM_NAME
    """)

    result = db.execute(query).mappings().all()
    avg_resolution_time_per_team = []
    for row in result:
        avg_seconds = row["avg_resolution_time"] if row["avg_resolution_time"] is not None else 0
        avg_resolution_time_per_team.append({
            "team": row["team"] if row["team"] is not None else "Necunoscut",
            "average_resolution_time_seconds": round(avg_seconds, 2),
            "average_resolution_time_minutes": round(avg_seconds / 60, 2),
            "average_resolution_time_hours": round(avg_seconds / 3600, 2)
        })
    
    return {
        "label": "Average Resolution Time per Team:",
        "data": avg_resolution_time_per_team
    }
    

# KPI 10: tickete pe categorie (tier 1, tier 2, tier 3): - pie chart pentru fiecare
@router.get("/tickets/category/tier-1")
def get_tickets_by_category(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT t.CATEGORY_TIER_1 as category1, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        GROUP BY t.CATEGORY_TIER_1
    """)

    result = db.execute(query).mappings().all()
    return [
        {
            "Category Tier 1": row["category1"] if row["category1"] is not None else "Necunoscut",
            "count": row["ticket_count"]
        }
        for row in result
    ]

@router.get("/tickets/category/tier-2")
def get_tickets_by_category(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT t.CATEGORY_TIER_2 as category2, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        GROUP BY t.CATEGORY_TIER_2
    """)

    result = db.execute(query).mappings().all()
    return [
        {
            "Category Tier 2": row["category2"] if row["category2"] is not None else "Necunoscut",
            "count": row["ticket_count"]
        }
        for row in result
    ]

@router.get("/tickets/category/tier-3")
def get_tickets_by_category(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT t.CATEGORY_TIER_3 as category3, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        GROUP BY t.CATEGORY_TIER_3
    """)

    result = db.execute(query).mappings().all()
    return [
        {
            "Category Tier 3": row["category3"] if row["category3"] is not None else "Necunoscut",
            "count": row["ticket_count"]
        }
        for row in result
    ]

# KPI ...

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