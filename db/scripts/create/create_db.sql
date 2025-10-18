CREATE DATABASE pisar
ON 
(
    NAME = N'pisar_data',
    FILENAME = N'C:\pisar\db\pisar.mdf',
    SIZE = 20MB,
    MAXSIZE = 200MB,
    FILEGROWTH = 5MB
)
LOG ON
(
    NAME = N'pisar_log',
    FILENAME = N'C:\pisar\db\pisar.ldf',
    SIZE = 10MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
)
COLLATE Cyrillic_General_100_CI_AS_SC_UTF8;
GO