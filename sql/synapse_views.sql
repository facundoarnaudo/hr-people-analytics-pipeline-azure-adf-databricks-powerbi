USE PeopleAnalytics;
GO

-- 1. Create a clean credential using the Workspace's native Managed Identity
IF NOT EXISTS (SELECT * FROM sys.database_scoped_credentials WHERE name = 'WorkspaceManagedIdentity')
BEGIN
    CREATE DATABASE SCOPED CREDENTIAL [WorkspaceManagedIdentity]
    WITH IDENTITY = 'Managed Identity';
END
GO

-- 2. Create the External Data Source pointing to your container
IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'MedallionDataSource')
BEGIN
    CREATE EXTERNAL DATA SOURCE [MedallionDataSource]
    WITH (
        LOCATION = 'https://dlpeopleanalytics2026.dfs.core.windows.net/medallion-data',
        CREDENTIAL = [WorkspaceManagedIdentity]
    );
END
GO

-- 3. Recreate the Employee view (Added CREATE OR ALTER for resilience)
CREATE OR ALTER VIEW gold.vw_employee_monthly_snapshot AS
SELECT *
FROM OPENROWSET(
    BULK 'gold/gold_employee_monthly_snapshot/',
    DATA_SOURCE = 'MedallionDataSource',
    FORMAT = 'DELTA'
) AS [result];
GO

-- 4. Recreate the Department view (Added CREATE OR ALTER for resilience)
CREATE OR ALTER VIEW gold.vw_department_monthly_kpi AS
SELECT *
FROM OPENROWSET(
    BULK 'gold/gold_department_monthly_kpi/',
    DATA_SOURCE = 'MedallionDataSource',
    FORMAT = 'DELTA'
) AS [result];
GO