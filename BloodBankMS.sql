-- 1. Person Table
CREATE TABLE Person (
    Aadhar_number BIGINT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Date_of_birth DATE NOT NULL,
    Gender CHAR(1) CHECK (Gender IN ('M', 'F', 'O')),
    Blood_Type CHAR(3) CHECK (Blood_Type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
);

-- Contact Table
CREATE TABLE Contact (
    Contact_ID SERIAL PRIMARY KEY,
    Aadhar_number BIGINT REFERENCES Person(Aadhar_number) ON DELETE CASCADE,
    Contact_Number VARCHAR(15) NOT NULL
);

-- Address Table
CREATE TABLE Address (
    Address_ID SERIAL PRIMARY KEY,
    Aadhar_number BIGINT REFERENCES Person(Aadhar_number) ON DELETE CASCADE,
    D_no VARCHAR(10),
    Street_Name VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50)
);

-- 2. Branch Table
CREATE TABLE Branch (
    Branch_ID SERIAL PRIMARY KEY,
    Location VARCHAR(100) NOT NULL,
    Inauguration_Date DATE NOT NULL,
    Storage_Capacity INT NOT NULL
);

-- Branch_BloodType Table
CREATE TABLE Branch_BloodType (
    Branch_ID INT REFERENCES Branch(Branch_ID) ON DELETE CASCADE,
    Blood_Type CHAR(3) CHECK (Blood_Type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    PRIMARY KEY (Branch_ID, Blood_Type)
);

-- 3. Blood Management Table
CREATE TABLE Blood_Management (
    Blood_ID SERIAL PRIMARY KEY,
    Blood_Type CHAR(3) CHECK (Blood_Type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    Collection_Date DATE NOT NULL,
    Expiry_Date DATE NOT NULL,
    Donor_ID INT REFERENCES Donor(Donor_ID) ON DELETE SET NULL,
    Branch_ID INT REFERENCES Branch(Branch_ID) ON DELETE SET NULL
);

-- 4. Donor Management Table
CREATE TABLE Donor (
    Donor_ID SERIAL PRIMARY KEY,
    Last_Donation_Date DATE
);

-- 5. Recipient Management Table
CREATE TABLE Recipient (
    Recipient_ID SERIAL PRIMARY KEY,
    Quantity_Required INT NOT NULL
);

-- 6. Transactions Table
CREATE TABLE Transactions (
    Donation_ID SERIAL PRIMARY KEY,
    Donor_ID INT REFERENCES Donor(Donor_ID) ON DELETE SET NULL,
    Branch_ID INT REFERENCES Branch(Branch_ID) ON DELETE SET NULL,
    Donation_Date DATE NOT NULL,
    Payment_ID INT,
    Amount DECIMAL(10,2),
    Blood_ID INT REFERENCES Blood_Management(Blood_ID) ON DELETE SET NULL,
    Recipient_ID INT REFERENCES Recipient(Recipient_ID) ON DELETE SET NULL
);

-- Blood_Details Table (To remove transitive dependency)
CREATE TABLE Blood_Details (
    Blood_ID INT PRIMARY KEY REFERENCES Blood_Management(Blood_ID) ON DELETE CASCADE,
    Blood_Type CHAR(3) CHECK (Blood_Type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
);

-- Recipient_Details Table (To remove transitive dependency)
CREATE TABLE Recipient_Details (
    Recipient_ID INT PRIMARY KEY REFERENCES Recipient(Recipient_ID) ON DELETE CASCADE,
    Quantity_Required INT NOT NULL
);


SELECT * FROM Person;

SELECT * FROM Contact;

SELECT * FROM Address;

SELECT * FROM Branch;

SELECT * FROM Branch_BloodType;

SELECT * FROM Blood_Management;

SELECT * FROM Donor;

SELECT * FROM Recipient;

SELECT * FROM Transactions;

SELECT * FROM Blood_Details;

SELECT * FROM Recipient_Details;


DROP TABLE IF EXISTS Person;