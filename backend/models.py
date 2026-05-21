from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "USERS"

    USER_ID = Column(Integer, primary_key=True, index=True)
    FULL_NAME = Column(String(100), unique=True, nullable=False)
    EMAIL = Column(String(100))
    TEAM = Column(String(50), ForeignKey("TEAMS.TEAM_NAME"))

class Ticket(Base):
    __tablename__ = "INCIDENT_TICKETS"

    TICKET_NUMBER = Column(String(50), primary_key=True, index=True)
    COMPANY_ID = Column(Integer, ForeignKey("COMPANIES.COMPANY_ID"))
    TEAM_ID = Column(Integer, ForeignKey("TEAMS.TEAM_ID"))
    STATUS_ID = Column(Integer, ForeignKey("STATUSES.STATUS_ID"))
    PRIORITY_ID = Column(Integer, ForeignKey("PRIORITIES.PRIORITY_ID"))
    
    PROJECT = Column(String(100))
    ASSIGNED_PERSON = Column(String(100), ForeignKey("USERS.FULL_NAME"))
    SERVICE = Column(String(100))
    DESCRIPTION = Column(Text)
    NOTES = Column(Text)
    RESOLUTION = Column(Text)
    CATEGORY_TIER_1 = Column(String(100))
    CATEGORY_TIER_2 = Column(String(100))
    CATEGORY_TIER_3 = Column(String(100))
    SUBMIT_DATETIME = Column(DateTime)
    RESOLVED_DATETIME = Column(DateTime)
    CLOSED_DATETIME = Column(DateTime)
    LAST_MODIFIED_DATETIME = Column(DateTime)
    ESTIMATED_RESOLUTION_DATETIME = Column(DateTime)
    RESOLUTION_CATEGORY = Column(String(100))
    PENDING_DURATION = Column(Integer)
    