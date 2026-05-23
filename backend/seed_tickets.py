"""
Script de adaugare in baza de date a 1000 de noi tickete

A NU SE RULA DE 2 ORI, 
    altfel va adauga inca 1000 la ticketele deja existente!!!

RULATI DUPA ce ati rulat DEJA setup.sql si insert.sql!!!
"""

import random
from datetime import datetime, timedelta
from sqlalchemy import text
from database import SessionLocal


# Nr tickete
NUMBER_OF_TICKETS_TO_GENERATE = 1000


# Companiile deja existente în insert.sql.
COMPANIES = ["Vodafone", "Orange", "Digi", "Telekom"]


# Echipe mai multe
TEAM_DEFINITIONS = [
    {"name": "Support", "company": "Vodafone", "weight": 10},
    {"name": "Network", "company": "Orange", "weight": 10},
    {"name": "Frontend", "company": "Digi", "weight": 7},
    {"name": "Data", "company": "Telekom", "weight": 7},
    {"name": "DevOps", "company": "Telekom", "weight": 7},

    {"name": "Core Network", "company": "Vodafone", "weight": 12},
    {"name": "Radio Access Network", "company": "Orange", "weight": 12},
    {"name": "Transmission", "company": "Digi", "weight": 9},
    {"name": "Fiber Operations", "company": "Telekom", "weight": 9},
    {"name": "Hardware", "company": "Vodafone", "weight": 7},
    {"name": "Cloud Infrastructure", "company": "Orange", "weight": 8},
    {"name": "Security", "company": "Digi", "weight": 7},
    {"name": "NOC", "company": "Telekom", "weight": 12},
    {"name": "OSS BSS", "company": "Vodafone", "weight": 8},
    {"name": "Field Operations", "company": "Orange", "weight": 8},
    {"name": "QA Testing", "company": "Digi", "weight": 5},
    {"name": "Communications", "company": "Telekom", "weight": 5},
]


USERS_BY_TEAM_NAME = {
    "Support": [
        "Popescu Ion", "Popa Elena", "Tudor Alex", "Dumitrescu Andrei",
        "Moldovan Raluca", "Stan Mihai"
    ],
    "Network": [
        "Ionescu Maria", "Dobre Cristian", "Marinescu Vlad",
        "Nistor Paul", "Petrescu Ioana"
    ],
    "Frontend": [
        "Georgescu Ana", "Radu Mihai", "Toma Andreea",
        "Matei Robert", "Preda Elena"
    ],
    "Data": [
        "Vasilescu Dan", "Ilie Cristina", "Barbu Sorin",
        "Dima Alina", "Neagu Florin"
    ],
    "DevOps": [
        "Marin Sorin", "Stoica Vlad", "Lazar Bogdan",
        "Dragomir Ioana", "Balan Teodor"
    ],
    "Core Network": [
        "Munteanu Victor", "Serban Alexandru", "Oprea Mihai",
        "Gheorghe Radu", "Cojocaru Diana", "Tudose Gabriel"
    ],
    "Radio Access Network": [
        "Avram Lucian", "Voicu Stefan", "Dinu Roxana",
        "Nica Andrei", "Florea Daniel", "Pavel Cristina"
    ],
    "Transmission": [
        "Badea Claudiu", "Lupu Adrian", "Sava Ioana",
        "Chiriac Vlad", "Iordache Miruna"
    ],
    "Fiber Operations": [
        "Grigore Mihnea", "Constantin Raul", "Anghel Sorina",
        "Dobre Ioan", "Manole Elena"
    ],
    "Hardware": [
        "Bucur Razvan", "Tanasie Pavel", "Dragos Iulian",
        "Mihalache Stefan", "Sandu Bogdan"
    ],
    "Cloud Infrastructure": [
        "Enache Paul", "Ivan Rares", "Macovei Diana",
        "Iliescu Teodor", "Ganea Vlad"
    ],
    "Security": [
        "Rusu Adrian", "Mocanu Irina", "Varga Andrei",
        "Stanescu Matei", "Olteanu Victor"
    ],
    "NOC": [
        "Pana Gabriel", "Radu Cosmin", "Neacsu Laura",
        "Dobre Ana", "Manea Ionut", "Vasile Vlad"
    ],
    "OSS BSS": [
        "Tudorache Diana", "Bartos Andrei", "Coman Raluca",
        "Dumitru Felix", "Mihai Alexandra"
    ],
    "Field Operations": [
        "Petcu Florin", "Nedelcu Raul", "Danciu Stefan",
        "Barbu Vlad", "Costache Elena"
    ],
    "QA Testing": [
        "Cernat Andreea", "Sima Claudiu", "Negoita Maria",
        "Rosu Eduard"
    ],
    "Communications": [
        "Mazilu Ana", "Diaconu Paul", "Filip Ioana",
        "Botezatu Cristian"
    ],
}


STATUSES = {
    1: "Open",
    2: "In Progress",
    3: "Resolved",
    4: "Closed",
    5: "Pending",
}


PRIORITIES = {
    1: "Low",
    2: "Medium",
    3: "High",
    4: "Critical",
}


PROJECTS = [
    "Billing",
    "Network Modernization",
    "Customer Portal",
    "Reports",
    "CRM",
    "Mobile App",
    "API Gateway",
    "Infrastructure Upgrade",
    "Analytics",
    "Customer Support",
    "Monitoring",
    "Security Hardening",
    "Provisioning",
    "Internal Tools",
    "5G Core Rollout",
    "4G Optimization",
    "RAN Expansion",
    "Fiber Backbone Upgrade",
    "Cloud Migration",
    "OSS Integration",
    "BSS Automation",
    "Incident Automation",
    "Telemetry Platform",
    "NOC Dashboard",
    "Packet Core Upgrade",
    "VoLTE Stabilization",
    "Edge Deployment",
    "Data Warehouse",
    "Field Maintenance",
    "Access Management",
]


SERVICES = [
    "API",
    "Network",
    "UI",
    "DB",
    "Backend",
    "Server",
    "Auth",
    "Storage",
    "Monitoring",
    "Email",
    "DNS",
    "VPN",
    "RAN",
    "Core",
    "IMS",
    "VoLTE",
    "5G Core",
    "Packet Core",
    "Fiber",
    "Transmission",
    "OSS",
    "BSS",
    "Telemetry",
    "Load Balancer",
    "Firewall",
    "Router",
    "Switch",
    "Base Station",
    "Cloud VM",
    "Kubernetes",
]


CATEGORY_COMBINATIONS = [
    # Application
    ("App", "Backend", "API Error"),
    ("App", "Backend", "Timeout"),
    ("App", "Backend", "Sync"),
    ("App", "Backend", "Email"),
    ("App", "Frontend", "UI Bug"),
    ("App", "Frontend", "UI Issue"),
    ("App", "Auth", "Login Failure"),
    ("App", "Auth", "Token Expired"),
    ("App", "Data", "ETL Issue"),
    ("App", "Data", "Data Mismatch"),
    ("App", "Reporting", "Report Failure"),

    # Infrastructure
    ("Infra", "Network", "Packet Loss"),
    ("Infra", "Network", "Connection Issue"),
    ("Infra", "Network", "High Latency"),
    ("Infra", "DB", "Performance"),
    ("Infra", "DB", "Deadlock"),
    ("Infra", "Server", "Crash"),
    ("Infra", "Server", "Disk Space"),
    ("Infra", "Cloud", "VM Unavailable"),
    ("Infra", "Cloud", "Scaling Failure"),
    ("Infra", "Monitoring", "Alert Failure"),

    # Telecom-specific
    ("Telecom", "RAN", "Cell Down"),
    ("Telecom", "RAN", "Low Signal"),
    ("Telecom", "RAN", "Handover Failure"),
    ("Telecom", "Core Network", "Session Drop"),
    ("Telecom", "Core Network", "Bearer Issue"),
    ("Telecom", "Packet Core", "PDP Context Failure"),
    ("Telecom", "Packet Core", "Throughput Degradation"),
    ("Telecom", "IMS", "VoLTE Call Drop"),
    ("Telecom", "IMS", "SIP Registration Failure"),
    ("Telecom", "Transmission", "Link Down"),
    ("Telecom", "Transmission", "Optical Power Low"),
    ("Telecom", "Fiber", "Fiber Cut"),
    ("Telecom", "Fiber", "High Attenuation"),

    # Hardware
    ("Hardware", "Radio Equipment", "Module Failure"),
    ("Hardware", "Radio Equipment", "Overheating"),
    ("Hardware", "Power", "Power Supply Failure"),
    ("Hardware", "Power", "Battery Backup Low"),
    ("Hardware", "Router", "Interface Down"),
    ("Hardware", "Switch", "Port Flapping"),

    # Security
    ("Security", "Access", "Access Denied"),
    ("Security", "Firewall", "Blocked Traffic"),
    ("Security", "Certificate", "Expired Certificate"),
    ("Security", "Authentication", "MFA Failure"),

    # Operations
    ("Operations", "Field", "Maintenance Delay"),
    ("Operations", "Field", "Site Access Issue"),
    ("Operations", "NOC", "Escalation Delay"),
    ("Operations", "NOC", "Wrong Assignment"),
    ("Operations", "Communications", "Customer Notification Missing"),
]


DESCRIPTIONS_BY_CATEGORY = {
    "API Error": ["API 500 error", "Unexpected API response", "API unavailable"],
    "Timeout": ["Timeout error", "Request timeout", "Gateway timeout"],
    "Sync": ["Sync issue", "Data not synchronized", "CRM sync failed"],
    "Email": ["Email not sent", "SMTP queue blocked", "Notification delivery failed"],
    "UI Bug": ["Login page layout broken", "Modal not opening", "Wrong UI component state"],
    "UI Issue": ["Button misaligned", "Form validation issue", "Dropdown not working"],
    "Login Failure": ["User cannot log in", "Repeated login failure", "Invalid login response"],
    "Token Expired": ["Session token expired unexpectedly", "Refresh token not accepted"],
    "ETL Issue": ["ETL job failed", "Wrong aggregation in ETL", "Daily ETL did not complete"],
    "Data Mismatch": ["Data mismatch between systems", "Wrong customer data displayed"],
    "Report Failure": ["Report generation failed", "Scheduled report missing"],

    "Packet Loss": ["Packet loss detected", "Intermittent packet loss", "Packet loss above threshold"],
    "Connection Issue": ["Connection dropped", "VPN connection issue", "Intermittent disconnects"],
    "High Latency": ["High latency between nodes", "Latency above SLA threshold"],
    "Performance": ["Slow query", "Slow report loading", "Database performance issue"],
    "Deadlock": ["Database deadlock detected", "Transaction deadlock during update"],
    "Crash": ["Server down", "Service crashed", "Unexpected restart"],
    "Disk Space": ["Disk almost full", "Storage threshold exceeded", "Backup failed due to space"],
    "VM Unavailable": ["Cloud VM unavailable", "Virtual machine not responding"],
    "Scaling Failure": ["Autoscaling failed", "New instance did not start"],
    "Alert Failure": ["Monitoring alert missing", "False positive alert", "Alert not triggered"],

    "Cell Down": ["Radio cell down", "Base station sector unavailable"],
    "Low Signal": ["Low signal quality reported", "Poor RSRP values in area"],
    "Handover Failure": ["Handover failure between cells", "Mobility issue detected"],
    "Session Drop": ["User sessions dropping", "Unexpected session termination in core"],
    "Bearer Issue": ["Bearer establishment failed", "Default bearer not created"],
    "PDP Context Failure": ["PDP context activation failed", "Packet core context issue"],
    "Throughput Degradation": ["Throughput below expected level", "Low data rate reported"],
    "VoLTE Call Drop": ["VoLTE call drop", "Voice session terminated unexpectedly"],
    "SIP Registration Failure": ["SIP registration failed", "IMS registration rejected"],
    "Link Down": ["Transmission link down", "Microwave link unavailable"],
    "Optical Power Low": ["Optical power below threshold", "Fiber optical signal degraded"],
    "Fiber Cut": ["Fiber cut suspected", "Fiber route unavailable"],
    "High Attenuation": ["High attenuation on fiber span", "Signal loss on fiber path"],

    "Module Failure": ["Radio module failure", "Hardware module not responding"],
    "Overheating": ["Equipment overheating", "High temperature alarm"],
    "Power Supply Failure": ["Power supply failure", "Rectifier alarm triggered"],
    "Battery Backup Low": ["Battery backup low", "Backup power threshold breached"],
    "Interface Down": ["Router interface down", "Physical interface unavailable"],
    "Port Flapping": ["Switch port flapping", "Repeated interface up/down events"],

    "Access Denied": ["User cannot access resource", "Permission denied", "Role misconfiguration"],
    "Blocked Traffic": ["Firewall blocked required traffic", "Security policy blocking flow"],
    "Expired Certificate": ["TLS certificate expired", "Certificate validation failed"],
    "MFA Failure": ["MFA push not delivered", "Multi-factor authentication failed"],

    "Maintenance Delay": ["Field maintenance delayed", "Technician unavailable"],
    "Site Access Issue": ["Access to site denied", "Site access approval missing"],
    "Escalation Delay": ["Escalation delayed", "Ticket not escalated on time"],
    "Wrong Assignment": ["Ticket assigned to wrong team", "Incorrect routing group"],
    "Customer Notification Missing": ["Customer notification missing", "Incident update not sent"],
}


RESOLUTION_TEXTS = {
    "Fix": [
        "Fixed configuration",
        "Fixed code issue",
        "Restarted affected service",
        "Patched component",
        "Corrected invalid data",
        "Replaced faulty module",
        "Restored failed link",
        "Updated routing configuration",
    ],
    "Optimization": [
        "Added index",
        "Optimized query",
        "Reduced payload size",
        "Improved caching",
        "Rebalanced traffic",
        "Adjusted radio parameters",
        "Optimized resource allocation",
    ],
    "Config Change": [
        "Updated configuration",
        "Changed timeout value",
        "Adjusted service parameters",
        "Updated access rules",
        "Changed firewall rule",
        "Updated routing policy",
        "Changed monitoring threshold",
    ],
    "Workaround": [
        "Applied temporary workaround",
        "Rerouted traffic",
        "Manual correction applied",
        "Fallback path activated",
        "Temporary capacity increase applied",
    ],
}


NOTES_BY_STATUS = {
    "Open": [
        None,
        "New ticket",
        "Waiting for triage",
        "Initial analysis required",
        "Created by monitoring system",
    ],
    "In Progress": [
        "Investigating",
        "Logs checked",
        "Work in progress",
        "Assigned to specialist",
        "Reproducing issue",
        "Checking alarms",
    ],
    "Pending": [
        "Waiting client",
        "Waiting vendor",
        "Waiting approval",
        "Waiting field team",
        "Waiting maintenance window",
        "Waiting customer confirmation",
    ],
    "Resolved": [
        "Resolved after investigation",
        "Fix validated",
        "Logs checked",
        "Monitoring stable",
        "Service restored",
    ],
    "Closed": [
        "Closed by support",
        "Client confirmed",
        "Final validation done",
        "SLA report completed",
        "Closure approved",
    ],
}


def make_email(full_name: str) -> str:
    normalized = (
        full_name.lower()
        .replace("ă", "a")
        .replace("â", "a")
        .replace("î", "i")
        .replace("ș", "s")
        .replace("ş", "s")
        .replace("ț", "t")
        .replace("ţ", "t")
    )
    parts = normalized.split()
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[-1]}@nokia-demo.local"
    return f"{normalized}@nokia-demo.local"


def weighted_choice(options):
    values = [item[0] for item in options]
    weights = [item[1] for item in options]
    return random.choices(values, weights=weights, k=1)[0]


def get_company_ids(db):
    result = db.execute(text("""
        SELECT COMPANY_ID, COMPANY_NAME
        FROM COMPANIES
    """)).mappings().all()

    return {row["COMPANY_NAME"]: row["COMPANY_ID"] for row in result}


def ensure_teams_and_users(db):
    company_ids = get_company_ids(db)

    for team in TEAM_DEFINITIONS:
        team_name = team["name"]
        company_name = team["company"]

        if company_name not in company_ids:
            raise ValueError(f"Compania '{company_name}' nu există în tabela COMPANIES.")

        company_id = company_ids[company_name]

        existing_team = db.execute(
            text("""
                SELECT TEAM_ID
                FROM TEAMS
                WHERE TEAM_NAME = :team_name
            """),
            {"team_name": team_name}
        ).mappings().first()

        if not existing_team:
            db.execute(
                text("""
                    INSERT INTO TEAMS (TEAM_NAME, COMPANY_ID)
                    VALUES (:team_name, :company_id)
                """),
                {
                    "team_name": team_name,
                    "company_id": company_id,
                }
            )

    db.commit()

    # Inserăm userii după ce toate echipele există.
    for team_name, users in USERS_BY_TEAM_NAME.items():
        for full_name in users:
            existing_user = db.execute(
                text("""
                    SELECT USER_ID
                    FROM USERS
                    WHERE FULL_NAME = :full_name
                """),
                {"full_name": full_name}
            ).mappings().first()

            if not existing_user:
                db.execute(
                    text("""
                        INSERT INTO USERS (FULL_NAME, EMAIL, TEAM)
                        VALUES (:full_name, :email, :team)
                    """),
                    {
                        "full_name": full_name,
                        "email": make_email(full_name),
                        "team": team_name,
                    }
                )

    db.commit()


def get_team_runtime_data(db):
    result = db.execute(text("""
        SELECT 
            tm.TEAM_ID,
            tm.TEAM_NAME,
            tm.COMPANY_ID
        FROM TEAMS tm
    """)).mappings().all()

    team_data = {}
    for row in result:
        team_name = row["TEAM_NAME"]
        if team_name in USERS_BY_TEAM_NAME:
            team_data[row["TEAM_ID"]] = {
                "name": team_name,
                "company_id": row["COMPANY_ID"],
                "users": USERS_BY_TEAM_NAME[team_name],
                "weight": next(
                    team["weight"]
                    for team in TEAM_DEFINITIONS
                    if team["name"] == team_name
                )
            }

    return team_data


def get_next_ticket_number(db):
    result = db.execute(text("""
        SELECT MAX(CAST(SUBSTRING(TICKET_NUMBER, 4, 20) AS INT)) AS max_ticket_number
        FROM INCIDENT_TICKETS
        WHERE TICKET_NUMBER LIKE 'INC%'
    """)).mappings().first()

    max_number = result["max_ticket_number"] if result and result["max_ticket_number"] is not None else 0
    return max_number + 1


def generate_ticket(ticket_number: str, team_runtime_data: dict):
    team_options = [
        (team_id, team_info["weight"])
        for team_id, team_info in team_runtime_data.items()
    ]

    team_id = weighted_choice(team_options)
    team_info = team_runtime_data[team_id]

    company_id = team_info["company_id"]
    assigned_person = random.choice(team_info["users"])

    status_id = weighted_choice([
        (1, 22),  # Open
        (2, 25),  # In Progress
        (3, 25),  # Resolved
        (4, 18),  # Closed
        (5, 10),  # Pending
    ])

    priority_id = weighted_choice([
        (1, 22),  # Low
        (2, 36),  # Medium
        (3, 30),  # High
        (4, 12),  # Critical
    ])

    category_tier_1, category_tier_2, category_tier_3 = random.choice(CATEGORY_COMBINATIONS)

    project = random.choice(PROJECTS)
    service = random.choice(SERVICES)
    description = random.choice(DESCRIPTIONS_BY_CATEGORY[category_tier_3])

    start_date = datetime(2026, 1, 1, 8, 0, 0)
    submit_datetime = start_date + timedelta(
        days=random.randint(0, 119),
        hours=random.randint(0, 10),
        minutes=random.choice([0, 15, 30, 45]),
    )

    if priority_id == 4:
        sla_hours = random.choice([2, 3, 4, 6])
    elif priority_id == 3:
        sla_hours = random.choice([4, 6, 8, 12])
    elif priority_id == 2:
        sla_hours = random.choice([12, 16, 24, 36])
    else:
        sla_hours = random.choice([24, 36, 48, 72])

    estimated_resolution_datetime = submit_datetime + timedelta(hours=sla_hours)
    status_name = STATUSES[status_id]

    resolved_datetime = None
    closed_datetime = None
    resolution_category = None
    resolution = None
    pending_duration = 0

    if status_name in ["Resolved", "Closed"]:
        if random.random() < 0.74:
            resolution_hours = random.uniform(0.5, sla_hours * 0.9)
        else:
            resolution_hours = random.uniform(sla_hours * 1.1, sla_hours * 2.8)

        resolved_datetime = submit_datetime + timedelta(hours=resolution_hours)

        resolution_category = weighted_choice([
            ("Fix", 45),
            ("Optimization", 20),
            ("Config Change", 25),
            ("Workaround", 10),
        ])

        resolution = random.choice(RESOLUTION_TEXTS[resolution_category])

        if status_name == "Closed":
            closed_datetime = resolved_datetime + timedelta(
                hours=random.choice([1, 2, 4, 6, 12, 24])
            )

    elif status_name == "Pending":
        pending_duration = random.choice([15, 30, 45, 60, 90, 120, 180, 240, 360])

    notes = random.choice(NOTES_BY_STATUS[status_name])

    if closed_datetime is not None:
        last_modified_datetime = closed_datetime
    elif resolved_datetime is not None:
        last_modified_datetime = resolved_datetime
    else:
        last_modified_datetime = submit_datetime + timedelta(
            hours=random.randint(0, 36),
            minutes=random.choice([0, 15, 30, 45]),
        )

    return {
        "TICKET_NUMBER": ticket_number,
        "COMPANY_ID": company_id,
        "TEAM_ID": team_id,
        "STATUS_ID": status_id,
        "PRIORITY_ID": priority_id,
        "PROJECT": project,
        "ASSIGNED_PERSON": assigned_person,
        "SERVICE": service,
        "DESCRIPTION": description,
        "NOTES": notes,
        "RESOLUTION": resolution,
        "CATEGORY_TIER_1": category_tier_1,
        "CATEGORY_TIER_2": category_tier_2,
        "CATEGORY_TIER_3": category_tier_3,
        "SUBMIT_DATETIME": submit_datetime,
        "RESOLVED_DATETIME": resolved_datetime,
        "CLOSED_DATETIME": closed_datetime,
        "LAST_MODIFIED_DATETIME": last_modified_datetime,
        "ESTIMATED_RESOLUTION_DATETIME": estimated_resolution_datetime,
        "RESOLUTION_CATEGORY": resolution_category,
        "PENDING_DURATION": pending_duration,
    }


def main():
    db = SessionLocal()

    try:
        ensure_teams_and_users(db)
        team_runtime_data = get_team_runtime_data(db)

        if not team_runtime_data:
            raise RuntimeError("Nu există echipe disponibile pentru generare.")

        start_number = get_next_ticket_number(db)

        rows = []
        for i in range(NUMBER_OF_TICKETS_TO_GENERATE):
            ticket_number = f"INC{start_number + i:04d}"
            rows.append(generate_ticket(ticket_number, team_runtime_data))

        insert_query = text("""
            INSERT INTO INCIDENT_TICKETS (
                TICKET_NUMBER,
                COMPANY_ID,
                TEAM_ID,
                STATUS_ID,
                PRIORITY_ID,
                PROJECT,
                ASSIGNED_PERSON,
                SERVICE,
                DESCRIPTION,
                NOTES,
                RESOLUTION,
                CATEGORY_TIER_1,
                CATEGORY_TIER_2,
                CATEGORY_TIER_3,
                SUBMIT_DATETIME,
                RESOLVED_DATETIME,
                CLOSED_DATETIME,
                LAST_MODIFIED_DATETIME,
                ESTIMATED_RESOLUTION_DATETIME,
                RESOLUTION_CATEGORY,
                PENDING_DURATION
            )
            VALUES (
                :TICKET_NUMBER,
                :COMPANY_ID,
                :TEAM_ID,
                :STATUS_ID,
                :PRIORITY_ID,
                :PROJECT,
                :ASSIGNED_PERSON,
                :SERVICE,
                :DESCRIPTION,
                :NOTES,
                :RESOLUTION,
                :CATEGORY_TIER_1,
                :CATEGORY_TIER_2,
                :CATEGORY_TIER_3,
                :SUBMIT_DATETIME,
                :RESOLVED_DATETIME,
                :CLOSED_DATETIME,
                :LAST_MODIFIED_DATETIME,
                :ESTIMATED_RESOLUTION_DATETIME,
                :RESOLUTION_CATEGORY,
                :PENDING_DURATION
            )
        """)

        batch_size = 100
        inserted = 0

        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            db.execute(insert_query, batch)
            db.commit()
            inserted += len(batch)
            print(f"Inserted {inserted}/{len(rows)} tickets...")

        print(f"Done. Inserted {len(rows)} generated tickets.")

    except Exception as error:
        db.rollback()
        print("Error while inserting generated tickets:")
        print(error)

    finally:
        db.close()


if __name__ == "__main__":
    main()