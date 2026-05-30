from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional, Any
from datetime import date, datetime, timedelta

router = APIRouter(
    prefix="/kpi",
    tags=["kpi"]
)

# Constructia de filtre:
def CommonKpiFilters(
    status: list[str] | None = Query(None),
    priority: list[str] | None = Query(None),
    team: list[str] | None = Query(None),
    startDate: Optional[date] = Query(None),
    endDate: Optional[date] = Query(None),
) -> dict[str, Any]:

    start_dt = datetime.combine(startDate, datetime.min.time()) if startDate else None
    end_dt = datetime.combine(endDate + timedelta(days=1), datetime.min.time()) if endDate else None

    return {
        "status": list_to_csv(status),
        "priority": list_to_csv(priority),
        "team": list_to_csv(team),
        "startDate": start_dt,
        "endDate": end_dt
    }

# Functie care transforma listele in CSV
def list_to_csv(values: list[str] | None) -> str | None:
    if not values:
        return None
    
    cleaned_values = [value.strip() for value in values if value and value.strip()]
    if not cleaned_values:
        return None
    
    return ",".join(cleaned_values)

# Functie care executa procedurile
def exec_procedure(db: Session, procedure_name: str, params: dict[str, Any]):
    query = text(f"""
        EXEC dbo.{procedure_name}
            @status = :status,
            @priority = :priority,
            @team = :team,
            @startDate = :startDate,
            @endDate = :endDate
    """)
    return db.execute(query, params).mappings()


# --- DATA UTILITIES (LOGIC ENGINE) ---

# KPI 1: numar total de tickete - card
def get_all_tickets_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTotalTickets", filters).first()
    return {
        "label": "Total Tickets",
        "value": result["total_tickets"] if result else 0,
    }

# KPI 2: tickete aranjate dupa status: - pie chart
def get_tickets_by_status_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByStatus", filters).all()
    return [
        {"status": row["status"] if row["status"] is not None else "Necunoscut", "count": row["ticket_count"]}
        for row in result
    ]

# KPI 3: tickete aranjate dupa prioritate: - bar chart
def get_tickets_by_priority_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByPriority", filters).all()
    return [
        {"priority": row["priority"] if row["priority"] is not None else "Necunoscut", "count": row["ticket_count"]}
        for row in result
    ]

# KPI 4: timp mediu de rezolvare a ticketelor: - card
def get_average_resolution_time_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiAverageResolutionTime", filters).first()
    avg_seconds = result["avg_resolution_seconds"] if result and result["avg_resolution_seconds"] is not None else 0
    return {
        "label": "Average Resolution Time",
        "data": round(avg_seconds / 3600, 2),
        "unit": "h"
    }

# KPI 5: numarul total de statusuri nerezolvate in procent din total: - card
def get_unresolved_percentage_data(db: Session, filters: dict[str, Any]):
    result_unresolved = exec_procedure(db, "GetKpiUnresolvedTickets", filters).first()
    unresolved_count = result_unresolved["unresolved_count"] if result_unresolved else 0
    total_tickets = get_all_tickets_data(db, filters)["value"]
    return {
        "label": "Unresolved Tickets Percentage:",
        "value": round((unresolved_count / total_tickets) * 100, 2) if total_tickets > 0 else 0.00,
        "unit": "%"
    }

# KPI 6: numarul total de statusuri rezolvate in procent din total: - card
def get_resolved_percentage_data(db: Session, filters: dict[str, Any]):
    result_resolved = exec_procedure(db, "GetKpiResolvedTickets", filters).first()
    resolved_count = result_resolved["resolved_count"] if result_resolved else 0
    total_tickets = get_all_tickets_data(db, filters)["value"]
    return {
        "label": "Resolved Tickets Percentage:",
        "value": round((resolved_count / total_tickets) * 100, 2) if total_tickets > 0 else 0.00,
        "unit": "%"
    }

# KPI 7: numarul total de statusuri cu timpul de lucru depasit in procent din total: - card
def get_overdue_percentage_data(db: Session, filters: dict[str, Any]):
    result_overdue = exec_procedure(db, "GetKpiOverdueTickets", filters).first()
    overdue_count = result_overdue["overdue_count"] if result_overdue else 0
    result_resolved = exec_procedure(db, "GetKpiResolvedTickets", filters).first()
    total_resolved = result_resolved["resolved_count"] if result_resolved else 0
    return {
        "label": "Overdue Tickets Percentage:",
        "value": round((overdue_count / total_resolved) * 100, 2) if total_resolved > 0 else 0.00,
        "unit": "%"
    }

# KPI 8: numarul total de tickete pe echipa: - bar chart
def get_tickets_per_team_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsPerTeam", filters).all()
    return {
        "data": [{"team": row["team"] if row["team"] is not None else "Necunoscut", "count": row["ticket_count"]} for
                 row in result]
    }

# KPI 9: timp mediu de rezolvare pe echipa: - bar chart
def get_average_resolution_time_per_team_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsAverageResolutionTimePerTeam", filters).all()
    return [
        {
            "team": row["team"] if row["team"] is not None else "Necunoscut",
            "average_resolution_time_hours": round((row["avg_resolution_time"] or 0) / 3600, 2)
        }
        for row in result
    ]

# KPI 10: tickete pe categorie (tier 1, tier 2, tier 3): - pie chart pentru fiecare
def get_tickets_by_category_1_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByCategoryTier1", filters).all()
    return [{"category": row["category"] if row["category"] is not None else "Necunoscut", "count": row["ticket_count"]}
            for row in result]


def get_tickets_by_category_2_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByCategoryTier2", filters).all()
    return [{"category": row["category"] if row["category"] is not None else "Necunoscut", "count": row["ticket_count"]}
            for row in result]


def get_tickets_by_category_3_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiTicketsByCategoryTier3", filters).all()
    return [{"category": row["category"] if row["category"] is not None else "Necunoscut", "count": row["ticket_count"]}
            for row in result]


# KPI 11: procent de conformitate SLA (In SLA vs Out SLA) - Gauge / Card
def get_sla_compliance_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiSlaCompliance", filters).first()
    in_sla = result["in_sla_count"] if result and result["in_sla_count"] is not None else 0
    out_sla = result["out_sla_count"] if result and result["out_sla_count"] is not None else 0
    total = in_sla + out_sla

    compliance_rate = round((in_sla / total) * 100, 2) if total > 0 else 100.00
    return {
        "label": "SLA Compliance Rate",
        "value": compliance_rate,
        "unit": "%",
        "breakdown": {
            "in_sla": in_sla,
            "out_sla": out_sla
        }
    }


# KPI 12: Distributia ticketelor pe intervale orare - Bar Chart / List
def get_sla_intervals_data(db: Session, filters: dict[str, Any]):
    result = exec_procedure(db, "GetKpiSlaIntervals", filters).all()
    return [
        {
            "interval": row["sla_interval"],
            "count": row["ticket_count"]
        }
        for row in result
    ]


# --- HTTP ENDPOINTS ---

@router.get("/tickets/total")
def get_all_tickets(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_all_tickets_data(db, filters)


@router.get("/tickets/status/status-bar")
def get_tickets_by_status(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_tickets_by_status_data(db, filters)


@router.get("/tickets/priority")
def get_tickets_by_priority(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_tickets_by_priority_data(db, filters)


@router.get("/tickets/average-resolution-time")
def get_average_resolution_time(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_average_resolution_time_data(db, filters)


@router.get("/tickets/status/unresolved-percentage")
def get_unresolved_percentage(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_unresolved_percentage_data(db, filters)


@router.get("/tickets/status/resolved-percentage")
def get_resolved_percentage(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_resolved_percentage_data(db, filters)


@router.get("/tickets/status/overdue-percentage")
def get_overdue_percentage(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_overdue_percentage_data(db, filters)


@router.get("/tickets/team/tickets-per-team")
def get_tickets_per_team(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_tickets_per_team_data(db, filters)


@router.get("/tickets/team/average-resolution-time-per-team")
def get_average_resolution_time_per_team(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_average_resolution_time_per_team_data(db, filters)


@router.get("/tickets/category/tier-1")
def get_tickets_by_category_1(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_tickets_by_category_1_data(db, filters)


@router.get("/tickets/category/tier-2")
def get_tickets_by_category_2(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_tickets_by_category_2_data(db, filters)


@router.get("/tickets/category/tier-3")
def get_tickets_by_category_3(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_tickets_by_category_3_data(db, filters)

@router.get("/tickets/sla-compliance")
def get_sla_compliance(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_sla_compliance_data(db, filters)

@router.get("/tickets/sla-intervals")
def get_sla_intervals(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    return get_sla_intervals_data(db, filters)


# Dashboard cu toate KPI-urile:
@router.get("/dashboard")
def get_kpi_dashboard(filters: dict = Depends(CommonKpiFilters), db: Session = Depends(get_db)):
    avg_resolution_result = get_average_resolution_time_data(db, filters)
    return {
        "total_tickets": get_all_tickets_data(db, filters),
        "tickets_by_status": get_tickets_by_status_data(db, filters),
        "tickets_by_priority": get_tickets_by_priority_data(db, filters),
        "avg_res_time": {
            "label": avg_resolution_result["label"],
            "value": avg_resolution_result["data"],
            "unit": avg_resolution_result["unit"]
        },
        "unresolved_tickets": get_unresolved_percentage_data(db, filters),
        "resolved_tickets": get_resolved_percentage_data(db, filters),
        "overdue_tickets": get_overdue_percentage_data(db, filters),
        "tickets_per_team": get_tickets_per_team_data(db, filters)["data"],
        "avg_res_time_per_team": get_average_resolution_time_per_team_data(db, filters),
        "category_tier_1": get_tickets_by_category_1_data(db, filters),
        "category_tier_2": get_tickets_by_category_2_data(db, filters),
        "category_tier_3": get_tickets_by_category_3_data(db, filters),
        "sla_compliance": get_sla_compliance_data(db, filters),
        "sla_intervals": get_sla_intervals_data(db, filters)
    }

# --- Campuri dinamice pentru filtre mai sigure ---
# Echipe:
def get_teams(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT TEAM_NAME FROM TEAMS ORDER BY TEAM_NAME
    """)
    result = db.execute(query).mappings().all()
    return [row["TEAM_NAME"] for row in result]

# Statusuri:
def get_statuses(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT STATUS_NAME FROM STATUSES ORDER BY STATUS_NAME
    """)
    result = db.execute(query).mappings().all()
    return [row["STATUS_NAME"] for row in result]

# Prioritati:
def get_priorities(db: Session = Depends(get_db)):
    query = text(
    """
        SELECT PRIORITY_NAME FROM PRIORITIES ORDER BY PRIORITY_NAME
    """)
    result = db.execute(query).mappings().all()
    return [row["PRIORITY_NAME"] for row in result]

# Dashboard cu toate KPI-urile:
@router.get("/filters")
def get_data_for_filters(db: Session = Depends(get_db)):
    status_result = get_statuses(db)
    priority_result = get_priorities(db)
    team_result = get_teams(db)

    return {
        "statuses": status_result,
        "priorities": priority_result,
        "teams": team_result
    }