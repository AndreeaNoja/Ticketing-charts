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
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByStatus
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY s.STATUS_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByPriority
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY p.PRIORITY_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiAverageResolutionTime
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiUnresolvedTickets
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
        AND (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiResolvedTickets
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
        AND (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiOverdueTickets
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
        AND (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsPerTeam
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
      AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
      AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY tm.TEAM_NAME
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsAverageResolutionTimePerTeam
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY tm.TEAM_NAME
    ORDER BY avg_resolution_time DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier1
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY ISNULL(t.CATEGORY_TIER_1, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier2
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY ISNULL(t.CATEGORY_TIER_2, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO


CREATE OR ALTER PROCEDURE dbo.GetKpiTicketsByCategoryTier3
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
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
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    GROUP BY ISNULL(t.CATEGORY_TIER_3, 'Necunoscut')
    ORDER BY ticket_count DESC;
END;
GO

CREATE OR ALTER PROCEDURE dbo.GetKpiSlaCompliance
    @status NVARCHAR(MAX) = NULL,
    @priority NVARCHAR(MAX) = NULL,
    @team NVARCHAR(MAX) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        SUM(CASE 
            WHEN t.RESOLVED_DATETIME <= DATEADD(HOUR, sc.SLA_HOURS, t.SUBMIT_DATETIME) THEN 1 
            ELSE 0 
        END) as in_sla_count,
        
        SUM(CASE 
            WHEN t.RESOLVED_DATETIME > DATEADD(HOUR, sc.SLA_HOURS, t.SUBMIT_DATETIME) 
                 OR (t.RESOLVED_DATETIME IS NULL AND GETDATE() > DATEADD(HOUR, sc.SLA_HOURS, t.SUBMIT_DATETIME)) THEN 1 
            ELSE 0 
        END) as out_sla_count
    FROM INCIDENT_TICKETS t
    INNER JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    INNER JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    INNER JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    INNER JOIN SLA_CONFIG sc ON t.PRIORITY_ID = sc.PRIORITY_ID
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
      AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
      AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate);
END;
GO

CREATE OR ALTER PROCEDURE dbo.GetKpiSlaIntervals
    @status NVARCHAR(MAX) = NULL,
    @priority NVARCHAR(MAX) = NULL,
    @team NVARCHAR(MAX) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- CTE 1: Dynamically generate lower and upper bounds from whatever is inside SLA_CONFIG
    WITH SlaBounds AS (
        SELECT 
            SLA_HOURS as upper_bound,
            -- LAG fetches the previous tier's hours to serve as this tier's starting point
            ISNULL(LAG(SLA_HOURS) OVER (ORDER BY SLA_HOURS ASC), 0) as lower_bound,
            -- Construct the chart string dynamically based on the exact configuration values
            CASE 
                WHEN LAG(SLA_HOURS) OVER (ORDER BY SLA_HOURS ASC) IS NULL 
                THEN 'Sub ' + CAST(SLA_HOURS AS VARCHAR(5)) + 'h'
                ELSE CAST(LAG(SLA_HOURS) OVER (ORDER BY SLA_HOURS ASC) AS VARCHAR(5)) + 'h - ' + CAST(SLA_HOURS AS VARCHAR(5)) + 'h'
            END as interval_label,
            SLA_HOURS as sort_order
        FROM SLA_CONFIG
    ),
    
    -- CTE 2: Create a catch-all row for tickets that breach the highest configured threshold
    MaxSlaCatchAll AS (
        SELECT upper_bound FROM SlaBounds WHERE upper_bound = (SELECT MAX(SLA_HOURS) FROM SLA_CONFIG)
    ),
    
    -- CTE 3: Combine all configuration bounds into a unified layout map
    AllIntervalsMap AS (
        SELECT lower_bound, upper_bound, interval_label, sort_order FROM SlaBounds
        UNION ALL
        SELECT upper_bound, 999999, 'Peste ' + CAST(upper_bound AS VARCHAR(5)) + 'h', upper_bound + 1 
        FROM MaxSlaCatchAll
    ),

    -- CTE 4: Gather the filtered incident tickets data and find their resolution durations
    TicketDurations AS (
        SELECT 
            DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0 as actual_hours
        FROM INCIDENT_TICKETS t
        INNER JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
        INNER JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
        INNER JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
        WHERE t.RESOLVED_DATETIME IS NOT NULL 
          AND t.SUBMIT_DATETIME IS NOT NULL
          AND (
                @status IS NULL
                OR s.STATUS_NAME IN (
                    SELECT LTRIM(RTRIM(value))
                    FROM STRING_SPLIT(@status, ',')
                )
            )
            AND (
                @priority IS NULL
                OR p.PRIORITY_NAME IN (
                    SELECT LTRIM(RTRIM(value))
                    FROM STRING_SPLIT(@priority, ',')
                )
            )
            AND (
                @team IS NULL
                OR tm.TEAM_NAME IN (
                    SELECT LTRIM(RTRIM(value))
                    FROM STRING_SPLIT(@team, ',')
                )
            )
          AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
          AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    )

    -- Final Query: Match ticket hours against our dynamic range maps and aggregate
    SELECT 
        m.interval_label as sla_interval,
        COUNT(t.actual_hours) as ticket_count
    FROM AllIntervalsMap m
    LEFT JOIN TicketDurations t ON t.actual_hours > m.lower_bound AND t.actual_hours <= m.upper_bound
    GROUP BY m.interval_label, m.sort_order
    ORDER BY m.sort_order ASC; -- Keeps your chart items ordering seamlessly from fastest to slowest
END;
GO

-- Procedura pentru toate ticketele din main.py:
CREATE OR ALTER PROCEDURE dbo.GetTickets
    @status VARCHAR(MAX) = NULL,
    @priority VARCHAR(MAX) = NULL,
    @team VARCHAR(MAX) = NULL,
    @startDate DATETIME = NULL,
    @endDate DATETIME = NULL
AS
BEGIN
    SET NOCOUNT ON;

   WITH SlaBounds AS (
        SELECT 
            SLA_HOURS as upper_bound,
            ISNULL(LAG(SLA_HOURS) OVER (ORDER BY SLA_HOURS ASC), 0) as lower_bound,
            CASE 
                WHEN LAG(SLA_HOURS) OVER (ORDER BY SLA_HOURS ASC) IS NULL 
                THEN 'Sub ' + CAST(SLA_HOURS AS VARCHAR(5)) + 'h'
                ELSE CAST(LAG(SLA_HOURS) OVER (ORDER BY SLA_HOURS ASC) AS VARCHAR(5)) + 'h - ' + CAST(SLA_HOURS AS VARCHAR(5)) + 'h'
            END as interval_label
        FROM SLA_CONFIG
    ),
    
    -- CTE 2: Determine your catch-all boundary maximum limit row
    MaxSlaCatchAll AS (
        SELECT upper_bound FROM SlaBounds WHERE upper_bound = (SELECT MAX(SLA_HOURS) FROM SLA_CONFIG)
    ),
    
    -- CTE 3: Combine all configuration bounds into a unified layout map
    AllIntervalsMap AS (
        SELECT lower_bound, upper_bound, interval_label FROM SlaBounds
        UNION ALL
        SELECT upper_bound, 999999, 'Peste ' + CAST(upper_bound AS VARCHAR(5)) + 'h'
        FROM MaxSlaCatchAll
    )

    SELECT 
        t.TICKET_NUMBER,
        s.STATUS_NAME AS STATUS,
        p.PRIORITY_NAME AS PRIORITY,
        c.COMPANY_NAME AS COMPANY,
        tm.TEAM_NAME AS TEAM,
        t.CATEGORY_TIER_1,
        t.CATEGORY_TIER_2,
        t.CATEGORY_TIER_3,
        t.SERVICE,
        t.ASSIGNED_PERSON,
        t.SUBMIT_DATETIME,
        t.RESOLVED_DATETIME,
        
        -- SLA Status calculation relying on 'sc'
        CASE 
            WHEN t.RESOLVED_DATETIME <= DATEADD(HOUR, sc.SLA_HOURS, t.SUBMIT_DATETIME) THEN 'In SLA'
            WHEN t.RESOLVED_DATETIME > DATEADD(HOUR, sc.SLA_HOURS, t.SUBMIT_DATETIME) 
                 OR (t.RESOLVED_DATETIME IS NULL AND GETDATE() > DATEADD(HOUR, sc.SLA_HOURS, t.SUBMIT_DATETIME)) THEN 'Out of SLA'
            ELSE 'In SLA'
        END AS SLA_STATUS,

        -- DYNAMIC READ: Extracts exact label text matched from our dynamic intervals matrix map CTE
        CASE 
            WHEN t.RESOLVED_DATETIME IS NULL THEN 'Nerezolvat'
            ELSE ISNULL(m.interval_label, 'Necunoscut')
        END AS SLA_INTERVAL

    FROM INCIDENT_TICKETS t
    JOIN STATUSES s ON t.STATUS_ID = s.STATUS_ID
    JOIN PRIORITIES p ON t.PRIORITY_ID = p.PRIORITY_ID
    JOIN COMPANIES c ON t.COMPANY_ID = c.COMPANY_ID
    JOIN TEAMS tm ON t.TEAM_ID = tm.TEAM_ID
    
    -- THE MISSING LINE: We must join SLA_CONFIG so 'sc.SLA_HOURS' exists!
    LEFT JOIN SLA_CONFIG sc ON t.PRIORITY_ID = sc.PRIORITY_ID
    
    LEFT JOIN AllIntervalsMap m ON (DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0) > m.lower_bound 
        AND (DATEDIFF(SECOND, t.SUBMIT_DATETIME, t.RESOLVED_DATETIME) / 3600.0) <= m.upper_bound
        
    WHERE (
            @status IS NULL
            OR s.STATUS_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@status, ',')
            )
        )
        AND (
            @priority IS NULL
            OR p.PRIORITY_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@priority, ',')
            )
        )
        AND (
            @team IS NULL
            OR tm.TEAM_NAME IN (
                SELECT LTRIM(RTRIM(value))
                FROM STRING_SPLIT(@team, ',')
            )
        )
        AND (@startDate IS NULL OR t.SUBMIT_DATETIME >= @startDate)
        AND (@endDate IS NULL OR t.SUBMIT_DATETIME < @endDate)
    ORDER BY t.SUBMIT_DATETIME DESC;
END;
GO