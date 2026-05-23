from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional, Any

router = APIRouter(
    prefix="/kpi",
    tags=["kpi"]
)

# Constructia de filtre:
def build_filter_params(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    team: Optional[str] = None,
) -> dict[str, Optional[str]]:
    
    return {
        "status": status or None,
        "priority": priority or None,
        "team": team or None,
    }

# Functie care executa procedurile
def exec_procedure(db: Session, procedure_name: str, params: dict[str, Any]):
    query = text(
    f"""
        EXEC dbo.{procedure_name}
            @status = :status,
            @priority = :priority,
            @team = :team
    """)

    return db.execute(query, params).mappings()


# KPI 1: numar total de tickete - card
def get_all_tickets_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTotalTickets", filters).first()
    return {
        "label": "Total Tickets",
        "value": result["total_tickets"] if result else 0,
    }    

@router.get("/tickets/total")
def get_all_tickets(db: Session = Depends(get_db)):
    return get_all_tickets_data(db, build_filter_params())


# KPI 2: tickete aranjate dupa status: - pie chart
def get_tickets_by_status_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByStatus", filters).all()
    return [
        {
            "status": row["status"] if row["status"] is not None else "Necunoscut", 
            "count": row["ticket_count"]
        }
        for row in result
    ]

@router.get("/tickets/status/status-bar")
def get_tickets_by_status(db: Session = Depends(get_db)):
    return get_tickets_by_status_data(db, build_filter_params())


# KPI 3: tickete aranjate dupa prioritate: - bar chart
def get_tickets_by_priority_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByPriority", filters).all()
    return [
        {
            "priority": row["priority"] if row["priority"] is not None else "Necunoscut", 
            "count": row["ticket_count"]
        }
        for row in result
    ]

@router.get("/tickets/priority")
def get_tickets_by_priority(db: Session = Depends(get_db)):
    return get_tickets_by_priority_data(db, build_filter_params())



# KPI 4: timp mediu de rezolvare a ticketelor: - card
def get_average_resolution_time_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiAverageResolutionTime", filters).first()
    avg_seconds = result["avg_resolution_seconds"] if result["avg_resolution_seconds"] is not None else 0
    return {
        "label": "Average Resolution Time",
        "data": round(avg_seconds / 3600, 2),
        "unit": "h"
    }

@router.get("/tickets/average-resolution-time")
def get_average_resolution_time(db: Session = Depends(get_db)):
    return get_average_resolution_time_data(db, build_filter_params())
    

# KPI 5: numarul total de statusuri nerezolvate in procent din total: - card
def get_unresolved_percentage_data(db: Session, filters: dict[str, Any]):
    result_unresolved = exec_procedure(db, "GetKpiUnresolvedTickets", filters).first()
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
    return get_unresolved_percentage_data(db, build_filter_params())


# KPI 6: numarul total de statusuri rezolvate in procent din total: - card
def get_resolved_percentage_data(db: Session, filters: dict[str, Any]):
    result_resolved = exec_procedure(db, "GetKpiResolvedTickets", filters).first()
    resolved_count = result_resolved["resolved_count"]

    total_tickets = get_all_tickets_data(db, filters)["value"]
    percentage = round((resolved_count / total_tickets) * 100, 2) if total_tickets > 0 else 0.00
    return {
        "label": "Resolved Tickets Percentage:",
        "value": percentage,
        "unit": "%"
    }

@router.get("/tickets/status/resolved-percentage")
def get_resolved_percentage(db: Session = Depends(get_db)):
    return get_resolved_percentage_data(db, build_filter_params())


# KPI 7: numarul total de statusuri cu timpul de lucru depasit in procent din total: - card
def get_overdue_percentage_data(db: Session, filters: dict[str, Any]):
    result_overdue = exec_procedure(db, "GetKpiOverdueTickets", filters).first()
    overdue_count = result_overdue["overdue_count"]

    result_resolved = exec_procedure(db, "GetKpiResolvedTickets", filters).first()
    total_resolved = result_resolved["resolved_count"]
    percentage = round((overdue_count / total_resolved) * 100, 2) if total_resolved > 0 else 0.00
    return {
        "label": "Overdue Tickets Percentage:",
        "value": percentage,
        "unit": "%"
    }

@router.get("/tickets/status/overdue-percentage")
def get_overdue_percentage(db: Session = Depends(get_db)):
    return get_overdue_percentage_data(db, build_filter_params())


# KPI 8: numarul total de tickete pe echipa: - bar chart
def get_tickets_per_team_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsPerTeam", filters).all()
    return {
        "data": 
        [
            {
                "team": row["team"] if row["team"] is not None else "Necunoscut", 
                "count": row["ticket_count"]
            }
            for row in result
        ]
    }

@router.get("/tickets/team/tickets-per-team")
def get_tickets_per_team(db: Session = Depends(get_db)):
    return get_tickets_per_team_data(db, build_filter_params())


# KPI 9: timp mediu de rezolvare pe echipa: - bar chart
def get_average_resolution_time_per_team_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsAverageResolutionTimePerTeam", filters).all()
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
    return get_average_resolution_time_per_team_data(db, build_filter_params())


# KPI 10: tickete pe categorie (tier 1, tier 2, tier 3): - pie chart pentru fiecare
def get_tickets_by_category_1_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByCategoryTier1", filters).all()
    return [
        {
            "category": row["category"] if row["category"] is not None else "Necunoscut", 
            "count": row["ticket_count"]
        }
        for row in result
    ]

@router.get("/tickets/category/tier-1")
def get_tickets_by_category_1(db: Session = Depends(get_db)):
    return get_tickets_by_category_1_data(db, build_filter_params())


def get_tickets_by_category_2_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByCategoryTier2", filters).all()
    return [
        {
            "category": row["category"] if row["category"] is not None else "Necunoscut", 
            "count": row["ticket_count"]
        }
        for row in result
    ]

@router.get("/tickets/category/tier-2")
def get_tickets_by_category_2(db: Session = Depends(get_db)):
    return get_tickets_by_category_2_data(db, build_filter_params())


def get_tickets_by_category_3_data(db: Session, filters: dict):
    result = exec_procedure(db, "GetKpiTicketsByCategoryTier3", filters).all()
    return [
        {
            "category": row["category"] if row["category"] is not None else "Necunoscut", 
            "count": row["ticket_count"]
        }
        for row in result
    ]

@router.get("/tickets/category/tier-3")
def get_tickets_by_category_3(db: Session = Depends(get_db)):
    return get_tickets_by_category_3_data(db, build_filter_params())


# KPI ...

# Dashboard cu toate KPI-urile:
@router.get("/dashboard")
def get_kpi_dashboard(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    team: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    active_filters = build_filter_params(
        status = status,
        priority = priority,
        team = team,
    )

    total_tickets = get_all_tickets_data(db, active_filters)
    tickets_by_status = get_tickets_by_status_data(db, active_filters)
    tickets_by_priority = get_tickets_by_priority_data(db, active_filters)

    avg_resolution_result = get_average_resolution_time_data(db, active_filters)
    avg_resolution_time = avg_resolution_result["data"]

    unresolved_tickets = get_unresolved_percentage_data(db, active_filters)
    resolved_tickets = get_resolved_percentage_data(db, active_filters)
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
