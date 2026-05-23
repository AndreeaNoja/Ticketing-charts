USE ticketing;
GO

/* ============================================================
   Proceduri pt KPI-uri:

   Filtre:
   - @status   = NULL sau filtru de status
   - @priority = NULL sau filtru de prioritate
   - @team     = NULL sau filtru de echipa
   ============================================================ */

CREATE OR ALTER PROCEDURE dbo.GetKpiTotalTickets
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT COUNT(*) AS total_tickets
    FROM INCIDENT_TICKETS t
    LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByStatus
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT s.STATUS_NAME as status, COUNT(*) as ticket_count
    FROM INCIDENT_TICKETS t
    JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
    GROUP BY s.STATUS_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByPriority
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT p.PRIORITY_NAME as priority, COUNT(*) as ticket_count
    FROM INCIDENT_TICKETS t
    JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
    GROUP BY p.PRIORITY_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiAverageResolutionTime
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT ISNULL(AVG(CAST(DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) as FLOAT)), 0) as avg_resolution_seconds
    FROM INCIDENT_TICKETS t
    LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE t.RESOLVED_DATETIME is not NULL 
        AND t.SUBMIT_DATETIME is not NULL
        AND (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiUnresolvedTickets
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT COUNT(*) as unresolved_count
    FROM INCIDENT_TICKETS t
    JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE s.STATUS_NAME NOT IN ('Closed', 'Resolved')
        AND (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiResolvedTickets
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT COUNT(*) as resolved_count
    FROM INCIDENT_TICKETS t
    JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE s.STATUS_NAME IN ('Closed', 'Resolved')
        AND (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiOverdueTickets
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT COUNT(*) as overdue_count
    FROM INCIDENT_TICKETS t
    JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE t.ESTIMATED_RESOLUTION_DATETIME < t.RESOLVED_DATETIME 
        AND t.RESOLVED_DATETIME is not NULL
        AND (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsPerTeam
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT tm.TEAM_NAME as team, COUNT(*) as ticket_count
    FROM INCIDENT_TICKETS t
    JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
      AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
      AND (@team IS NULL OR tm.TEAM_NAME = @team)
    GROUP BY tm.TEAM_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsAverageResolutionTimePerTeam
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT 
        tm.TEAM_NAME as team, 
        ISNULL(AVG(CAST(DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) as FLOAT)), 0) as avg_resolution_time
    FROM TEAMS tm
    LEFT JOIN INCIDENT_TICKETS t ON t.TEAM_ID = tm.TEAM_ID AND t.RESOLVED_DATETIME is not NULL
    LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
    GROUP BY tm.TEAM_NAME
    ORDER BY avg_resolution_time DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier1
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT 
        ISNULL(t.CATEGORY_TIER_1, 'Necunoscut') as category, 
        COUNT(*) as ticket_count
    FROM INCIDENT_TICKETS t
    LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
    GROUP BY ISNULL(t.CATEGORY_TIER_1, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier2
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT 
        ISNULL(t.CATEGORY_TIER_2, 'Necunoscut') as category, 
        COUNT(*) as ticket_count
    FROM INCIDENT_TICKETS t
    LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
    GROUP BY ISNULL(t.CATEGORY_TIER_2, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier3
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON; 

    SELECT 
        ISNULL(t.CATEGORY_TIER_3, 'Necunoscut') as category, 
        COUNT(*) as ticket_count
    FROM INCIDENT_TICKETS t
    LEFT JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    LEFT JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    LEFT JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
        AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
    GROUP BY ISNULL(t.CATEGORY_TIER_3, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO