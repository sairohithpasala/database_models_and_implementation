CREATE TABLE IF NOT EXISTS [department] (
[dname] VARCHAR NULL,
[dnumber] INT NULL,
[mgr_ssn] INT NULL,
[mgr_start_date] VARCHAR NULL
);

INSERT INTO department VALUES
('Research',5,333445555,'22-MAY-1978'),
('Administration',4,987654321,'01-JAN-1985'),
('Headquarters',1,888665555,'19-JUN-1971'),
('Software',6,111111100,'15-MAY-1999'),
('Hardware',7,444444400,'15-MAY-1998'),
('Sales',8,555555500,'01-JAN-1997'),
('HR',9,112244668,'01-FEB-1989'),
('Networking',3,110110110,'15-MAY-2009'),
('QA',11,913323708,'2-FEB-2010');