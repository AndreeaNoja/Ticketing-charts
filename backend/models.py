from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Ticket(Base):
    __tablename__ = "INCIDENT_TICKETS"
    TICKET_NUMBER = Column(String, primary_key=True, index=True)
    STATUS = Column(String)
    PRIORITY = Column(String)
    COMPANY = Column(String)
    PROJECT = Column(String)
    TEAM = Column(String)
    ASSIGNED_PERSON = Column(String)
    SERVICE = Column(String)
    DESCRIPTION = Column(String)
    NOTES = Column(String)
    RESOLUTION = Column(String)
    CATEGORY_TIER_1 = Column(String)
    CATEGORY_TIER_2 = Column(String)
    CATEGORY_TIER_3 = Column(String)
    SUBMIT_DATETIME = Column(DateTime)
    RESOLVED_DATETIME = Column(DateTime)
    CLOSED_DATETIME = Column(DateTime)
    LAST_MODIFIED_DATETIME = Column(DateTime)
    ESTIMATED_RESOLUTION_DATETIME = Column(DateTime)
    RESOLUTION_CATEGORY = Column(String)
    PENDING_DURATION = Column(Integer)