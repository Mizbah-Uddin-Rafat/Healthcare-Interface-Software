CREATE DATABASE Healthcare;

USE Healthcare;

-- Create Users table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL -- SHA-256 hash length
);

-- Insert a user (password is 'password' hashed with SHA-256)
INSERT INTO Users (username, password) VALUES ('admin1', 'password');


-- Table: Hospital
CREATE TABLE Hospital (
    Hospital_ID INT PRIMARY KEY,
    Hospital_Name VARCHAR(255),
    Hospital_Address VARCHAR(255),
    Hospital_Phone_Number VARCHAR(15),
    State VARCHAR(50),
    Zip_Code VARCHAR(10)
);



-- Table: Patient
CREATE TABLE Patient (
    Patient_ID INT PRIMARY KEY,
    Patient_FName VARCHAR(255),
    Patient_LName VARCHAR(255),
    Patient_Address VARCHAR(255),
    Patient_Phone_Number VARCHAR(15),
    Pharmacy_ID INT
);


-- Table: Room
CREATE TABLE Room (
    Room_Num INT PRIMARY KEY,
    Patient_ID INT,
    Staff_ID INT,
    Admission_Date DATE,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);

-- Table: Pharmacy
CREATE TABLE Pharmacy (
    Pharmacy_ID INT PRIMARY KEY,
    Pharmacy_Name VARCHAR(255),
    Pharmacy_Address VARCHAR(255),
    Pharmacy_Phone_Number VARCHAR(15)
);

-- Table: Prescription


-- Table: Doctor
CREATE TABLE Doctor (
    Doctor_ID INT PRIMARY KEY,
    Doctor_FName VARCHAR(255),
    Doctor_LName VARCHAR(255),
    Department_ID INT,
    Doctor_Phone_Number VARCHAR(15),
    FOREIGN KEY (Department_ID) REFERENCES Department(Department_ID)
);

-- Table: Appointment
CREATE TABLE Appointment (
    Patient_ID INT,
    Doctor_ID INT,
    Date DATE,
    Time TIME,
    PRIMARY KEY (Patient_ID, Doctor_ID, Date, Time),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID)
);




-- Insert Data into Hospital
INSERT INTO Hospital VALUES (1, 'General Hospital', '123 Main St', '123-456-7890', 'California', '90001');
INSERT INTO Hospital VALUES (2, 'City Hospital', '456 Elm St', '987-654-3210', 'New York', '10001');
INSERT INTO Hospital VALUES (3, 'County Hospital', '789 Oak St', '555-555-5555', 'Texas', '73301');
INSERT INTO Hospital VALUES (4, 'Regional Hospital', '101 Maple St', '444-444-4444', 'Florida', '32004');
INSERT INTO Hospital VALUES (5, 'District Hospital', '202 Pine St', '333-333-3333', 'Nevada', '89001');
INSERT INTO Hospital VALUES (6, 'University Hospital', '303 Cedar St', '222-222-2222', 'Massachusetts', '02101');
INSERT INTO Hospital VALUES (7, 'Community Hospital', '404 Birch St', '111-111-1111', 'Arizona', '85001');
INSERT INTO Hospital VALUES (8, 'Metropolitan Hospital', '505 Walnut St', '999-999-9999', 'Ohio', '44101');
INSERT INTO Hospital VALUES (9, 'Suburban Hospital', '606 Fir St', '888-888-8888', 'Illinois', '60601');
INSERT INTO Hospital VALUES (10, 'Specialist Hospital', '707 Spruce St', '777-777-7777', 'Colorado', '80001');

-- Insert Data into Department
INSERT INTO Department VALUES (1, 'Cardiology', 1);
INSERT INTO Department VALUES (2, 'Neurology', 2);
INSERT INTO Department VALUES (3, 'Orthopedics', 3);
INSERT INTO Department VALUES (4, 'Pediatrics', 4);
INSERT INTO Department VALUES (5, 'Radiology', 5);
INSERT INTO Department VALUES (6, 'Oncology', 6);
INSERT INTO Department VALUES (7, 'Emergency', 7);
INSERT INTO Department VALUES (8, 'Dermatology', 8);
INSERT INTO Department VALUES (9, 'Gastroenterology', 9);
INSERT INTO Department VALUES (10, 'Urology', 10);

-- Insert Data into Patient
INSERT INTO Patient VALUES (1, 'Alice', 'Brown', '123 Oak St', '123-123-1234', 1);
INSERT INTO Patient VALUES (2, 'Bob', 'Smith', '456 Pine St', '456-456-4567', 2);
INSERT INTO Patient VALUES (3, 'Charlie', 'Johnson', '789 Maple St', '789-789-7890', 3);
INSERT INTO Patient VALUES (4, 'David', 'Williams', '101 Elm St', '101-101-1010', 4);
INSERT INTO Patient VALUES (5, 'Eve', 'Jones', '202 Cedar St', '202-202-2020', 5);
INSERT INTO Patient VALUES (6, 'Frank', 'Miller', '303 Walnut St', '303-303-3030', 6);
INSERT INTO Patient VALUES (7, 'Grace', 'Davis', '404 Birch St', '404-404-4040', 7);
INSERT INTO Patient VALUES (8, 'Hank', 'Wilson', '505 Spruce St', '505-505-5050', 8);
INSERT INTO Patient VALUES (9, 'Ivy', 'Moore', '606 Fir St', '606-606-6060', 9);
INSERT INTO Patient VALUES (10, 'Jack', 'Taylor', '707 Elm St', '707-707-7070', 10);

-- Insert Data into Room
INSERT INTO Room VALUES (101, 1, 1, '2023-01-01');
INSERT INTO Room VALUES (102, 2, 2, '2023-01-02');
INSERT INTO Room VALUES (103, 3, 3, '2023-01-03');
INSERT INTO Room VALUES (104, 4, 4, '2023-01-04');
INSERT INTO Room VALUES (105, 5, 5, '2023-01-05');
INSERT INTO Room VALUES (106, 6, 6, '2023-01-06');
INSERT INTO Room VALUES (107, 7, 7, '2023-01-07');
INSERT INTO Room VALUES (108, 8, 8, '2023-01-08');
INSERT INTO Room VALUES (109, 9, 9, '2023-01-09');
INSERT INTO Room VALUES (110, 10, 10, '2023-01-10');

-- Insert Data into Pharmacy
INSERT INTO Pharmacy VALUES (1, 'Pharma One', '123 Pharma St', '111-111-1111');
INSERT INTO Pharmacy VALUES (2, 'Pharma Two', '456 Pharma St', '222-222-2222');
INSERT INTO Pharmacy VALUES (3, 'Pharma Three', '789 Pharma St', '333-333-3333');
INSERT INTO Pharmacy VALUES (4, 'Pharma Four', '101 Pharma St', '444-444-4444');
INSERT INTO Pharmacy VALUES (5, 'Pharma Five', '202 Pharma St', '555-555-5555');
INSERT INTO Pharmacy VALUES (6, 'Pharma Six', '303 Pharma St', '666-666-6666');
INSERT INTO Pharmacy VALUES (7, 'Pharma Seven', '404 Pharma St', '777-777-7777');
INSERT INTO Pharmacy VALUES (8, 'Pharma Eight', '505 Pharma St', '888-888-8888');
INSERT INTO Pharmacy VALUES (9, 'Pharma Nine', '606 Pharma St', '999-999-9999');
INSERT INTO Pharmacy VALUES (10, 'Pharma Ten', '707 Pharma St', '000-000-0000');


-- Insert Data into Doctor
INSERT INTO Doctor VALUES (1, 'Dr. Adam', 'Smith', 1, '123-123-1234');
INSERT INTO Doctor VALUES (2, 'Dr. Brian', 'Johnson', 2, '456-456-4567');
INSERT INTO Doctor VALUES (3, 'Dr. Charlie', 'Williams', 3, '789-789-7890');
INSERT INTO Doctor VALUES (4, 'Dr. David', 'Brown', 4, '101-101-1010');
INSERT INTO Doctor VALUES (5, 'Dr. Edward', 'Jones', 5, '202-202-2020');
INSERT INTO Doctor VALUES (6, 'Dr. Frank', 'Miller', 6, '303-303-3030');
INSERT INTO Doctor VALUES (7, 'Dr. Grace', 'Davis', 7, '404-404-4040');
INSERT INTO Doctor VALUES (8, 'Dr. Hank', 'Wilson', 8, '505-505-5050');
INSERT INTO Doctor VALUES (9, 'Dr. Ivy', 'Moore', 9, '606-606-6060');
INSERT INTO Doctor VALUES (10, 'Dr. Jack', 'Taylor', 10, '707-707-7070');

-- Insert Data into Appointment
INSERT INTO Appointment VALUES (1, 1, '2023-01-01', '10:00:00');
INSERT INTO Appointment VALUES (2, 2, '2023-01-02', '11:00:00');
INSERT INTO Appointment VALUES (3, 3, '2023-01-03', '12:00:00');
INSERT INTO Appointment VALUES (4, 4, '2023-01-04', '13:00:00');
INSERT INTO Appointment VALUES (5, 5, '2023-01-05', '14:00:00');
INSERT INTO Appointment VALUES (6, 6, '2023-01-06', '15:00:00');
INSERT INTO Appointment VALUES (7, 7, '2023-01-07', '16:00:00');
INSERT INTO Appointment VALUES (8, 8, '2023-01-08', '17:00:00');
INSERT INTO Appointment VALUES (9, 9, '2023-01-09', '18:00:00');
INSERT INTO Appointment VALUES (10, 10, '2023-01-10', '19:00:00');


Select *
From appointment;

Select *
From patient;

Select *
From room


