USE ticketing;
GO

INSERT INTO COMPANIES (COMPANY_NAME) VALUES ('Vodafone'), ('Orange'), ('Digi'), ('Telekom');
GO

INSERT INTO TEAMS (TEAM_NAME, COMPANY_ID) VALUES ('Support', 1), ('Network', 2), ('Frontend', 3), ('Data', 4), ('DevOps', 4);
GO

INSERT INTO USERS (FULL_NAME, EMAIL, TEAM) VALUES 
('Popescu Ion', 'ion.popescu@vodafone.com', 'Support'),
('Ionescu Maria', 'maria.ionescu@orange.com', 'Network'),
('Georgescu Ana', 'ana.georgescu@digi.com', 'Frontend'),
('Vasilescu Dan', 'dan.vasilescu@telekom.com', 'Data'),
('Popa Elena', 'elena.popa@vodafone.com', 'Support'),
('Radu Mihai', 'mihai.radu@digi.com', 'Frontend'),
('Enache Paul', 'paul.enache@vodafone.com', 'Support'),
('Marin Sorin', 'sorin.marin@telekom.com', 'DevOps'),
('Ilie Cristina', 'cristina.ilie@telekom.com', 'Data'),
('Tudor Alex', 'alex.tudor@orange.com', 'Support');
GO

INSERT INTO STATUSES (STATUS_NAME) VALUES ('Open'), ('In Progress'), ('Resolved'), ('Closed'), ('Pending');
GO

INSERT INTO PRIORITIES (PRIORITY_NAME) VALUES ('Low'), ('Medium'), ('High'), ('Critical');
GO

INSERT INTO INCIDENT_TICKETS(
    TICKET_NUMBER, STATUS_ID, PRIORITY_ID, COMPANY_ID, TEAM_ID, PROJECT, ASSIGNED_PERSON, 
    SERVICE, DESCRIPTION, NOTES, RESOLUTION, CATEGORY_TIER_1, CATEGORY_TIER_2, 
    CATEGORY_TIER_3, SUBMIT_DATETIME, RESOLVED_DATETIME, CLOSED_DATETIME, 
    LAST_MODIFIED_DATETIME, ESTIMATED_RESOLUTION_DATETIME, RESOLUTION_CATEGORY, PENDING_DURATION
)VALUES 
('INC0001', 1, 3, 1, 1, 'Billing', 'Popescu Ion', 'API', 'API 500 error', NULL, NULL, 'App', 'Backend', 'API Error', '2026-03-20 10:00', NULL, NULL, '2026-03-20 10:00', '2026-03-20 14:00', NULL, 0),
('INC0002', 2, 4, 2, 2, 'Network', 'Ionescu Maria', 'Network', 'Packet loss', 'Investigating', NULL, 'Infra', 'Network', 'Packet Loss', '2026-03-19 08:00', NULL, NULL, '2026-03-20 09:00', '2026-03-19 12:00', NULL, 30),
('INC0003', 3, 2, 3, 3, 'Portal', 'Georgescu Ana', 'UI', 'Login issue', 'Replicated', 'Fixed JS', 'App', 'Frontend', 'UI Bug', '2026-03-18 14:00', '2026-03-18 16:30', NULL, '2026-03-18 16:30', '2026-03-18 18:00', 'Fix', 0),
('INC0004', 4, 1, 4, 4, 'Reports', 'Vasilescu Dan', 'DB', 'Slow query', 'Index issue', 'Added index', 'Infra', 'DB', 'Performance', '2026-03-17 09:00', '2026-03-17 12:00', '2026-03-17 13:00', '2026-03-17 13:00', '2026-03-17 17:00', 'Optimization', 0),
('INC0005', 5, 3, 1, 1, 'CRM', 'Popa Elena', 'Backend', 'Sync issue', 'Waiting client', NULL, 'App', 'Backend', 'Sync', '2026-03-21 11:00', NULL, NULL, '2026-03-21 12:00', '2026-03-21 15:00', NULL, 120),
('INC0006', 1, 2, 2, 3, 'Mobile App', 'Radu Mihai', 'UI', 'Button misaligned', NULL, NULL, 'App', 'Frontend', 'UI Issue', '2026-03-22 09:30', NULL, NULL, '2026-03-22 09:30', '2026-03-23 13:00', NULL, 0),
('INC0007', 3, 3, 3, 1, 'API Gateway', 'Enache Paul', 'API', 'Timeout error', 'Logs checked', 'Increased timeout', 'App', 'Backend', 'Timeout', '2026-03-20 07:00', '2026-03-20 10:00', NULL, '2026-03-20 10:00', '2026-03-20 11:00', 'Config Change', 0),
('INC0008', 4, 4, 4, 5, 'Infra', 'Marin Sorin', 'Server', 'Server down', 'Restarted', 'Restart server', 'Infra', 'Server', 'Crash', '2026-03-16 02:00', '2026-03-16 03:00', '2026-03-16 04:00', '2026-03-16 04:00', '2026-03-16 03:00', 'Fix', 0),
('INC0009', 2, 2, 1, 4, 'Analytics', 'Ilie Cristina', 'DB', 'Data mismatch', 'Checking ETL', NULL, 'App', 'Data', 'ETL Issue', '2026-03-23 10:00', NULL, NULL, '2026-03-23 11:00', '2026-03-23 16:00', NULL, 15),
('INC0010', 5, 1, 2, 1, 'CRM', 'Tudor Alex', 'Backend', 'Email not sent', 'Waiting SMTP', NULL, 'App', 'Backend', 'Email', '2026-03-24 08:00', NULL, NULL, '2026-03-24 09:00', '2026-03-24 12:00', NULL, 60);
GO


INSERT INTO SLA_CONFIG (PRIORITY_ID, SLA_HOURS) VALUES 
(4, 8),  
(3, 16),  
(2, 32), 
(1, 64);


