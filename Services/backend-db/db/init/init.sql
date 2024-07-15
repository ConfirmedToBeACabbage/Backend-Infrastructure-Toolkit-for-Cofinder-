-- User creation read_only
CREATE USER readonlyusr WITH PASSWORD 'testing1';
GRANT CONNECT ON DATABASE postgres TO readonlyusr;
GRANT USAGE ON SCHEMA public to readonlyusr;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonlyusr;

-- Write only users
CREATE USER writeonlyusr WITH PASSWORD 'testing2';
REVOKE SELECT ON ALL TABLES IN SCHEMA public FROM writeonlyusr;
GRANT CONNECT ON DATABASE postgres TO writeonlyusr;
GRANT USAGE ON SCHEMA public to writeonlyusr;
GRANT UPDATE, DELETE, INSERT ON ALL TABLES IN SCHEMA public TO writeonlyusr;
