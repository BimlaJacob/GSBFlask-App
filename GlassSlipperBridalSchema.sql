-- Create the database
CREATE DATABASE GlassSlipperBridal;
GO

-- Use the database
USE GlassSlipperBridal;
GO

-- Table for Customers
CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY, 
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL
);
GO

-- Insert customers into the Customers table
INSERT INTO Customers (Name, Email)
VALUES 
('Belle Charming', 'belle.charming@gmail.com'),
('Ella Sparkle', 'ella.sparkle@gmail.com'),
('Aurora Swift', 'aurora.swift@gmail.com'),
('Ariel Williamson', 'ariel.williamson@gmail.com'),
('Taylor Kelce', 'taylor.kelce@gmail.com'),
('Elsa Glint', 'elsa.glint@gmail.com'),
('Sofia Rosewood', 'sofia.rosewood@gmail.com'),
('Lila Snowflake', 'lila.snowflake@gmail.com'),
('Ruby Starshine', 'ruby.starshine@gmail.com'),
('Daisy Meadows', 'daisy.meadows@gmail.com'),
('Luna Blossom', 'luna.blossom@gmail.com'),
('Violet Harmony', 'violet.harmony@gmail.com'),
('Ivy Raindrop', 'ivy.raindrop@gmail.com');
GO

-- Table for Staff Members
CREATE TABLE Staff (
    StaffID INT IDENTITY(1,1) PRIMARY KEY, 
    Name NVARCHAR(100) NOT NULL,
    Role NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Phone NVARCHAR(15) NOT NULL
);
GO

-- Insert employees into the Staff table
INSERT INTO Staff (Name, Role, Email, Phone)
VALUES 
('Charlotte Wilson', 'Manager', 'charlottewilson@gmail.com', '555-234-5678'),
('Brittany Lynn', 'Consultant', 'brittanylynn@gmail.com', '555-345-6789'),
('Kylie Kelce', 'Consultant', 'princesskylina@gmail.com', '555-456-7890'),
('Angelica Hamilton', 'Consultant', 'angelicahamilton@gmail.com', '555-567-8901');
GO

-- Table for Appointments
CREATE TABLE Appointments (
    AppointmentID INT IDENTITY(1,1) PRIMARY KEY, 
    CustomerID INT NOT NULL,
    StaffID INT NOT NULL,
    AppointmentDate DATE NOT NULL,
    AppointmentTime NVARCHAR(10) NOT NULL CHECK (AppointmentTime IN ('10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM')), 
    UNIQUE (AppointmentDate, AppointmentTime),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);
GO

-- Insert appointments into the Appointments table
INSERT INTO Appointments (CustomerID, StaffID, AppointmentDate, AppointmentTime)
VALUES 
(1, 1, '2024-12-30', '10 AM'),
(2, 2, '2025-01-02', '11 AM'),
(3, 3, '2025-01-03', '12 PM'),
(4, 4, '2025-01-08', '1 PM'),
(5, 1, '2025-01-09', '2 PM'),
(6, 2, '2025-01-10', '3 PM'),
(7, 3, '2025-01-15', '10 AM'),
(8, 4, '2025-01-16', '11 AM'),
(9, 1, '2025-01-17', '12 PM'),
(10, 2, '2025-01-22', '1 PM'),
(11, 3, '2025-01-23', '2 PM'),
(12, 4, '2025-01-24', '3 PM'),
(13, 1, '2025-01-29', '10 AM'),
(4, 2, '2025-01-30', '11 AM'),
(5, 3, '2025-01-31', '12 PM'),
(6, 4, '2025-02-05', '1 PM'),
(7, 1, '2025-02-06', '2 PM'),
(8, 2, '2025-02-07', '3 PM'),
(9, 3, '2025-02-12', '10 AM'),
(10, 4, '2025-02-13', '11 AM'),
(11, 1, '2025-02-14', '12 PM'),
(12, 2, '2025-02-19', '1 PM'),
(13, 3, '2025-02-20', '2 PM'),
(1, 4, '2025-02-21', '3 PM');
GO

BACKUP DATABASE GlassSlipperBridal
TO DISK = 'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\Backup\GlassSlipperBridal.bak'
WITH FORMAT, INIT;
