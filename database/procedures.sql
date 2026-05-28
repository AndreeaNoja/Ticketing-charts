USE ticketing;
GO

/* ============================================================
   Proceduri pt KPI-uri:

   Filtre:
   - @status   = NULL sau filtru de status
   - @priority = NULL sau filtru de prioritate
   - @team     = NULL sau filtru de echipa
   - @startDate = NULL sau filtru de data de incepere
   - @endDate = NULL sau filtru de data de incheiere
   ============================================================ */

CREATE OR ALTER PROCEDURE dbo.GetKpiTotalTickets
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByStatus
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY s.STATUS_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByPriority
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY p.PRIORITY_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiAverageResolutionTime
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiUnresolvedTickets
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiResolvedTickets
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiOverdueTickets
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@team IS NULL OR tm.TEAM_NAME = @team)
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsPerTeam
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
      AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
      AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY tm.TEAM_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsAverageResolutionTimePerTeam
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY tm.TEAM_NAME
    ORDER BY avg_resolution_time DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier1
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY ISNULL(t.CATEGORY_TIER_1, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier2
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY ISNULL(t.CATEGORY_TIER_2, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier3
    @status VARCHAR(50) = NULL,
    @priority VARCHAR(50) = NULL,
    @team VARCHAR(100) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
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
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY ISNULL(t.CATEGORY_TIER_3, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO

CREATE OR ALTER PROCEDURE dbo.GetKpiSlaCompliance
    @status NVARCHAR(50) = NULL,
    @priority NVARCHAR(50) = NULL,
    @team NVARCHAR(50) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
AS
BEGIN
    SELECT 
        SUM(CASE WHEN t.RESOLVED_DATETIME <= t.ESTIMATED_RESOLUTION_DATETIME THEN 1 ELSE 0 END) as in_sla_count,
        SUM(CASE WHEN t.RESOLVED_DATETIME > t.ESTIMATED_RESOLUTION_DATETIME OR (t.RESOLVED_DATETIME IS NULL AND GETDATE() > t.ESTIMATED_RESOLUTION_DATETIME) THEN 1 ELSE 0 END) as out_sla_count
    FROM INCIDENT_TICKETS t
    JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE (@status IS NULL OR s.STATUS_NAME = @status)
      AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
      AND (@team IS NULL OR tm.TEAM_NAME = @team)
      AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
      AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO

CREATE OR ALTER PROCEDURE dbo.GetKpiSlaIntervals
    @status NVARCHAR(50) = NULL,
    @priority NVARCHAR(50) = NULL,
    @team NVARCHAR(50) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
AS
BEGIN
    SELECT 
        CASE 
            WHEN DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 <= 8.0 THEN 'Sub 8h'
            WHEN DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 <= 16.0 THEN '8h - 16h'
            WHEN DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 <= 32.0 THEN '16h - 32h'
            WHEN DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 <= 64.0 THEN '32h - 64h'
            ELSE 'Peste 64h'
        END as sla_interval,
        COUNT(*) as ticket_count
    FROM INCIDENT_TICKETS t
    JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    WHERE t.RESOLVED_DATETIME IS NOT NULL AND t.SUBMIT_DATETIME IS NOT NULL
      AND (@status IS NULL OR s.STATUS_NAME = @status)
      AND (@priority IS NULL OR p.PRIORITY_NAME = @priority)
      AND (@team IS NULL OR tm.TEAM_NAME = @team)
      AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
      AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY 
        CASE 
            WHEN DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 <= 8.0 THEN 'Sub 8h'
            WHEN DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 <= 16.0 THEN '8h - 16h'
            WHEN DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 <= 32.0 THEN '16h - 32h'
            WHEN DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 <= 64.0 THEN '32h - 64h'
            ELSE 'Peste 64h'
        END;
END;
GO