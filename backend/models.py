from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from database import Base

class Ticket(Base):
    __tablename__ = "INCIDENT_TICKETS"

    TICKET_NUMBER = Column(String(50), primary_key=True, index=True)
    COMPANY_ID = Column(Integer, ForeignKey("COMPANIES.COMPANY_ID"))
    TEAM_ID = Column(Integer, ForeignKey("TEAMS.TEAM_ID"))
    STATUS_ID = Column(Integer, ForeignKey("STATUSES.STATUS_ID"))
    PRIORITY_ID = Column(Integer, ForeignKey("PRIORITIES.PRIORITY_ID"))
    
    PROJECT = Column(String(100))
    ASSIGNED_PERSON = Column(String(100))
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

# class Status(Base):
#     __tablename__ = "STATUSES"

#     STATUS_ID = Column(Integer, primary_key = True, index = True)
#     STATUS_NAME = Column(String(50))

# class Company(Base):
#     __tablename__ = "COMPANIES"

#     COMPANY_ID = Column(Integer, primary_key = True, index = True)
#     COMPANY_NAME = Column(String(100))

# class Team(Base):
#     __tablename__ = "TEAMS"

#     TEAM_ID = Column(Integer, primary_key = True, index = True)
#     COMPANY_ID = Column(Integer, ForeignKey("COMPANIES.COMPANY_ID"))
#     TEAM_NAME = Column(String(100))

# class Priority(Base):
#     __tablename__ = "STATUSES"

#     PRIORITY_ID = Column(Integer, primary_key = True, index = True)
#     PRIORITY_NAME = Column(String(50))