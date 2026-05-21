from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional

router = APIRouter(
    prefix="/kpi",
    tags=["kpi"]
)


# Helper engine function to inject dynamically generated WHERE filters safely
def apply_filters_to_query(base_sql: str, filters: dict) -> tuple[str, dict]:
    where_clauses = []
    bind_params = {}

    if filters.get("status"):
        # Assuming you want to search by status name
        where_clauses.append("s.STATUS_NAME = :status")
        bind_params["status"] = filters["status"]

    if filters.get("priority"):
        where_clauses.append("p.PRIORITY_NAME = :priority")
        bind_params["priority"] = filters["priority"]

    if filters.get("team"):
        where_clauses.append("tm.TEAM_NAME = :team")
        bind_params["team"] = filters["team"]

    if where_clauses:
        # Check if base query already includes a WHERE clause to append appropriately
        conjunction = " AND " if "WHERE" in base_sql.upper() else " WHERE "
        base_sql += conjunction + " AND ".join(where_clauses)

    # print("\n--- DEBUG: SQL QUERY ---")
    # print(f"Generated SQL: {base_sql}")
    # print(f"Parameters: {bind_params}\n------------------------\n")

    return base_sql, bind_params


# Updated KPI 1 Helper
def get_all_tickets_data(db: Session, filters: dict):
    # We must explicitly join tables here to filter by name metrics if passed
    base_query = """
        SELECT COUNT(*) as total_tickets
        FROM INCIDENT_TICKETS t
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    """
    sql, params = apply_filters_to_query(base_query, filters)
    result = db.execute(text(sql), params).mappings().first()
    return {"label": "Total Tickets", "value": result["total_tickets"]}

# KPI 1: numar total de tickete: - card
@router.get("/tickets/total")
def get_all_tickets(db: Session = Depends(get_db)):
    return get_all_tickets_data(db, {})


# KPI 2: tickete aranjate dupa status: - pie chart
# Updated KPI 2 Helper
def get_tickets_by_status_data(db: Session, filters: dict):
    base_query = """
        SELECT s.STATUS_NAME as status, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    """
    sql, params = apply_filters_to_query(base_query, filters)
    sql += " GROUP BY s.STATUS_NAME"

    result = db.execute(text(sql), params).mappings().all()
    return [
        {"status": row["status"] if row["status"] is not None else "Necunoscut", "count": row["ticket_count"]}
        for row in result
    ]

@router.get("/tickets/status/status-bar")
def get_tickets_by_status(db: Session = Depends(get_db)):
    return get_tickets_by_status_data(db, {})

# KPI 3: tickete aranjate dupa prioritate: - bar chart
# Updated KPI 3 Helper
def get_tickets_by_priority_data(db: Session, filters: dict):
    base_query = """
        SELECT p.PRIORITY_NAME as priority, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    """
    sql, params = apply_filters_to_query(base_query, filters)
    sql += " GROUP BY p.PRIORITY_NAME ORDER BY ticket_count DESC"

    result = db.execute(text(sql), params).mappings().all()
    return [
        {"priority": row["priority"] if row["priority"] is not None else "Necunoscut", "count": row["ticket_count"]}
        for row in result
    ]

@router.get("/tickets/priority")
def get_tickets_by_priority(db: Session = Depends(get_db)):
    return get_tickets_by_priority_data(db, {})



# KPI 4: timp mediu de rezolvare a ticketelor: - card
def get_average_resolution_time_data(db: Session, filters: dict):
    base_query = """ 
        SELECT AVG(CAST(DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) as FLOAT)) as avg_resolution_seconds
        FROM INCIDENT_TICKETS t
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
        WHERE t.RESOLVED_DATETIME is not NULL AND t.SUBMIT_DATETIME is not NULL
    """
    sql, params = apply_filters_to_query(base_query, filters)
    result = db.execute(text(sql), params).mappings().first()
    avg_seconds = result["avg_resolution_seconds"] if result["avg_resolution_seconds"] is not None else 0
    return {
        "label": "Average Resolution Time",
        "data": round(avg_seconds / 3600, 2),
        "unit": "h"
    }

@router.get("/tickets/average-resolution-time")
def get_average_resolution_time(db: Session = Depends(get_db)):
    return get_average_resolution_time_data(db, {})
    

# KPI 5: numarul total de statusuri nerezolvate in procent din total: - card
def get_unresolved_percentage_data(db: Session, filters: dict):
    base_query = """
        SELECT COUNT(*) as unresolved_count
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
        WHERE s.STATUS_NAME NOT IN ('Closed', 'Resolved')
    """
    sql, params = apply_filters_to_query(base_query, filters)
    result_unresolved = db.execute(text(sql), params).mappings().first()
    unresolved_count = result_unresolved["unresolved_count"]

    total_tickets = get_all_tickets_data(db, filters)["value"]
    percentage = round((unresolved_count / total_tickets) * 100, 2) if total_tickets > 0 else 0.00
    return {
        "label": "Unresolved Tickets Percentage:",
        "value": percentage,
        "unit": "%"
    }

@router.get("/tickets/status/unresolved-percentage")
def get_unresolved_percentage(db: Session = Depends(get_db)):
    return get_unresolved_percentage_data(db, {})

# KPI 6: numarul total de statusuri rezolvate in procent din total: - card
def get_resolved_tickets_data(db: Session, filters: dict):
    base_query = """
        SELECT COUNT(*) as resolved_count
        FROM INCIDENT_TICKETS t
        JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
        WHERE s.STATUS_NAME IN ('Closed', 'Resolved')
    """
    sql, params = apply_filters_to_query(base_query, filters)
    result_resolved = db.execute(text(sql), params).mappings().first()
    return result_resolved["resolved_count"]

def get_unrounded_resolved_percentage(db: Session, filters: dict):
    resolved_count = get_resolved_tickets_data(db, filters)
    total_tickets = get_all_tickets_data(db, filters)["value"]
    percentage = round((resolved_count / total_tickets) * 100, 2) if total_tickets > 0 else 0.00
    return {
        "label": "Resolved Tickets Percentage:",
        "value": percentage,
        "unit": "%"
    }

@router.get("/tickets/status/resolved-percentage")
def get_resolved_percentage(db: Session = Depends(get_db)):
    return get_unrounded_resolved_percentage(db, {})

# KPI 7: numarul total de statusuri cu timpul de lucru depasit in procent din total: - card
def get_overdue_percentage_data(db: Session, filters: dict):
    base_query = """ 
        SELECT COUNT(*) as overdue_count
        FROM INCIDENT_TICKETS t
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
        WHERE t.ESTIMATED_RESOLUTION_DATETIME < t.RESOLVED_DATETIME AND
              t.RESOLVED_DATETIME is not NULL
    """
    sql, params = apply_filters_to_query(base_query, filters)
    result_overdue = db.execute(text(sql), params).mappings().first()
    overdue_count = result_overdue["overdue_count"]

    total_resolved = get_resolved_tickets_data(db, filters)
    percentage = round((overdue_count / total_resolved) * 100, 2) if total_resolved > 0 else 0.00
    return {
        "label": "Overdue Tickets Percentage:",
        "value": percentage,
        "unit": "%"
    }

@router.get("/tickets/status/overdue-percentage")
def get_overdue_percentage(db: Session = Depends(get_db)):
    return get_overdue_percentage_data(db, {})


# KPI 8: numarul total de tickete pe echipa: - bar chart
def get_tickets_per_team_data(db: Session, filters: dict):
    base_query = """
        SELECT tm.TEAM_NAME as team, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    """
    sql, params = apply_filters_to_query(base_query, filters)
    sql += " GROUP BY tm.TEAM_NAME ORDER BY ticket_count DESC"
    result = db.execute(text(sql), params).mappings().all()
    return {
        "data": [
            {"team": row["team"] if row["team"] is not None else "Necunoscut", "count": row["ticket_count"]}
            for row in result
        ]
    }

@router.get("/tickets/team/tickets-per-team")
def get_tickets_per_team(db: Session = Depends(get_db)):
    return get_tickets_per_team_data(db, {})

# KPI 9: timp mediu de rezolvare pe echipa: - bar chart
def get_average_resolution_time_per_team_data(db: Session, filters: dict):
    base_query = """
        SELECT tm.TEAM_NAME as team, 
               AVG(CAST(DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) as FLOAT)) as avg_resolution_time
        FROM TEAMS tm
        LEFT JOIN INCIDENT_TICKETS t ON t.TEAM_ID = tm.TEAM_ID AND t.RESOLVED_DATETIME is not NULL
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    """
    sql, params = apply_filters_to_query(base_query, filters)
    sql += " GROUP BY tm.TEAM_NAME ORDER BY avg_resolution_time DESC"

    result = db.execute(text(sql), params).mappings().all()
    avg_resolution_time_per_team = []
    for row in result:
        avg_seconds = row["avg_resolution_time"] if row["avg_resolution_time"] is not None else 0
        avg_resolution_time_per_team.append({
            "team": row["team"] if row["team"] is not None else "Necunoscut",
            "average_resolution_time_hours": round(avg_seconds / 3600, 2)
        })
    return avg_resolution_time_per_team


@router.get("/tickets/team/average-resolution-time-per-team")
def get_average_resolution_time_per_team(db: Session = Depends(get_db)):
    return get_average_resolution_time_per_team_data(db, {})


# KPI 10: tickete pe categorie (tier 1, tier 2, tier 3): - pie chart pentru fiecare
def get_tickets_by_category_1_data(db: Session, filters: dict):
    base_query = """
        SELECT t.CATEGORY_TIER_1 as category1, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    """
    sql, params = apply_filters_to_query(base_query, filters)
    sql += " GROUP BY t.CATEGORY_TIER_1"
    result = db.execute(text(sql), params).mappings().all()
    return [{"category": row["category1"] if row["category1"] is not None else "Necunoscut", "count": row["ticket_count"]} for row in result]

@router.get("/tickets/category/tier-1")
def get_tickets_by_category_1(db: Session = Depends(get_db)):
    return get_tickets_by_category_1_data(db, {})

def get_tickets_by_category_2_data(db: Session, filters: dict):
    base_query = """
        SELECT t.CATEGORY_TIER_2 as category2, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    """
    sql, params = apply_filters_to_query(base_query, filters)
    sql += " GROUP BY t.CATEGORY_TIER_2"
    result = db.execute(text(sql), params).mappings().all()
    return [{"category": row["category2"] if row["category2"] is not None else "Necunoscut", "count": row["ticket_count"]} for row in result]

@router.get("/tickets/category/tier-2")
def get_tickets_by_category_2(db: Session = Depends(get_db)):
    return get_tickets_by_category_2_data(db, {})

def get_tickets_by_category_3_data(db: Session, filters: dict):
    base_query = """
        SELECT t.CATEGORY_TIER_3 as category3, COUNT(*) as ticket_count
        FROM INCIDENT_TICKETS t
        LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    """
    sql, params = apply_filters_to_query(base_query, filters)
    sql += " GROUP BY t.CATEGORY_TIER_3"
    result = db.execute(text(sql), params).mappings().all()
    return [{"category": row["category3"] if row["category3"] is not None else "Necunoscut", "count": row["ticket_count"]} for row in result]

@router.get("/tickets/category/tier-3")
def get_tickets_by_category_3(db: Session = Depends(get_db)):
    return get_tickets_by_category_3_data(db, {})

# KPI ...

# Dashboard cu primele 3 KPI-uri:
@router.get("/dashboard")
def get_kpi_dashboard(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    team: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    print(f"\nDEBUG: Incoming Query Params -> Status: {status}, Priority: {priority}, Team: {team}\n")

    active_filters = {
        "status": status,
        "priority": priority,
        "team": team
    }
    total_tickets = get_all_tickets_data(db, active_filters)
    tickets_by_status = get_tickets_by_status_data(db, active_filters)
    tickets_by_priority = get_tickets_by_priority_data(db, active_filters)

    avg_resolution_result = get_average_resolution_time_data(db, active_filters)
    avg_resolution_time = avg_resolution_result["data"]

    unresolved_tickets = get_unresolved_percentage_data(db, active_filters)
    resolved_tickets = get_unrounded_resolved_percentage(db, active_filters)
    overdue_tickets = get_overdue_percentage_data(db, active_filters)

    tickets_per_team_result = get_tickets_per_team_data(db, active_filters)
    tickets_per_team = tickets_per_team_result["data"]
    avg_res_time_per_team = get_average_resolution_time_per_team_data(db, active_filters)

    category_tier_1 = get_tickets_by_category_1_data(db, active_filters)
    category_tier_2 = get_tickets_by_category_2_data(db, active_filters)
    category_tier_3 = get_tickets_by_category_3_data(db, active_filters)

    return {
        "total_tickets": total_tickets,
        "tickets_by_status": tickets_by_status,
        "tickets_by_priority": tickets_by_priority,
        "avg_res_time": {
            "label": avg_resolution_result["label"],
            "value": avg_resolution_time,
            "unit": avg_resolution_result["unit"]
        },
        "unresolved_tickets": unresolved_tickets,
        "resolved_tickets": resolved_tickets,
        "overdue_tickets": overdue_tickets,
        "tickets_per_team": tickets_per_team,
        "avg_res_time_per_team": avg_res_time_per_team,
        "category_tier_1": category_tier_1,
        "category_tier_2": category_tier_2,
        "category_tier_3": category_tier_3
    }
