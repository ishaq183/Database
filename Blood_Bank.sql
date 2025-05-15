CREATE TABLE donor(
	Donor_id SERIAL PRIMARY KEY,
	Name VARCHAR(20),
	Age INT NOT NULL,
	Gender VARCHAR(6) NOT NULL CHECK (Gender IN ('Male', 'Female')),
	CNIC VARCHAR(20) NOT null unique,
	CHECK (CNIC ~ '^[0-9]{5}-[0-9]{7}-[0-9]$'),
    CHECK (
        (Gender = 'Male' AND RIGHT(CNIC, 1)::INT % 2 = 1) OR
        (Gender = 'Female' AND RIGHT(CNIC, 1)::INT % 2 = 0)
    ),
	Blood_Group VARCHAR(3),
		CHECK (Blood_Group IN ('A+','A-','B+','B-','AB+','AB-','O+','O-')),
	Contact VARCHAR(13),
	CHECK (Contact ~ '^\+923[0-4][0-9]{7}$'),
	Address VARCHAR(255),
	Last_Donation_Date DATE,
	Medical_History TEXT
);

create table recipient(
		recipient_ID SERIAL primary key,
		Name VARCHAR(20),
		Age INT NOT NULL,
		Gender VARCHAR(6) NOT NULL CHECK (Gender IN ('Male', 'Female')),
		CNIC VARCHAR(20) NOT null unique,
		CHECK (CNIC ~ '^[0-9]{5}-[0-9]{7}-[0-9]$'),
   		CHECK (
        	(Gender = 'Male' AND RIGHT(CNIC, 1)::INT % 2 = 1) OR
        	(Gender = 'Female' AND RIGHT(CNIC, 1)::INT % 2 = 0)
    	),
		Blood_Group VARCHAR(3),
		CHECK (Blood_Group IN ('A+','A-','B+','B-','AB+','AB-','O+','O-')),
		Contact VARCHAR(13),
		CHECK (Contact ~ '^\+923[0-4][0-9]{7}$'),
		Address VARCHAR(255),
		required_blood_amount DECIMAL(5,2),
		emergency_status BOOLEAN	
 );

create table blood_bank(
	blood_bank_ID SERIAL primary key,
	name VARCHAR(100),
	location TEXT,
	Contact VARCHAR(20),
	CHECK (Contact ~ '^\+923[0-4][0-9]{7}$')
);

create table hospital(
	Hospital_ID SERIAL primary key,
	Name VARCHAR(100),
	location TEXT,
	Contact Varchar(20),
	CHECK (Contact ~ '^\+923[0-4][0-9]{7}$')
);

create table staff(
	Staff_ID SERIAL primary key,
	Name VARCHAR(20),
	Gender VARCHAR(6) NOT NULL CHECK (Gender IN ('Male', 'Female')),
	CNIC VARCHAR(20) NOT null unique,
	CHECK (CNIC ~ '^[0-9]{5}-[0-9]{7}-[0-9]$'),
    CHECK (
        (Gender = 'Male' AND RIGHT(CNIC, 1)::INT % 2 = 1) OR
        (Gender = 'Female' AND RIGHT(CNIC, 1)::INT % 2 = 0   )),
	role varchar (20),
	check (role in('Doctor','Nurse','Technician')),
	blood_bank_ID Int,
	Contact Varchar(15),
	CHECK (Contact ~ '^\+923[0-4][0-9]{7}$'),
	foreign key (blood_bank_ID) references blood_bank(blood_bank_ID)
);

create table admin(
	Admin_ID SERIAL primary key,
	Name VARCHAR(20),
	Gender VARCHAR(6) NOT NULL CHECK (Gender IN ('Male', 'Female')),
	CNIC VARCHAR(20) NOT null unique,
	CHECK (CNIC ~ '^[0-9]{5}-[0-9]{7}-[0-9]$'),
    CHECK (
        (Gender = 'Male' AND RIGHT(CNIC, 1)::INT % 2 = 1) OR
        (Gender = 'Female' AND RIGHT(CNIC, 1)::INT % 2 = 0   )),
	role varchar (60),
	check (role in('Database Administrator','System DBA','Data Analyst','Database Security Administrator','Supervisor')),
	Contact Varchar(15),
	CHECK (Contact ~ '^\+923[0-4][0-9]{7}$')
);

create table reception(
	Reception_ID SERIAL primary key,
	Donor_ID INT not null,
	Recipient_ID INT,
	Donation_Date Date not null,
	Blood_Quantity DECIMAL(5,2) not null,
	foreign key (Donor_ID) references donor(Donor_id),
	foreign key (Recipient_ID) references recipient(recipient_ID)
);

CREATE TABLE blood_request (
    Request_ID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Hospital_ID INT NULL,
    Recipient_ID INT NULL,
    Requester_Type VARCHAR(10),
    Blood_Type VARCHAR(4) NOT NULL,
    Requested_Quantity INT NOT NULL CHECK (Requested_Quantity > 0),
    Request_Status VARCHAR(20) DEFAULT 'Pending',
    Request_Date DATE NOT NULL,

    CHECK (Requester_Type IN ('Hospital', 'Recipient')),
    CHECK (Blood_Type IN ('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-')),
    CHECK (Request_Status IN ('Pending', 'Approved', 'Rejected')),

    FOREIGN KEY (Hospital_ID) REFERENCES hospital(Hospital_ID),
    FOREIGN KEY (Recipient_ID) REFERENCES recipient(Recipient_ID),

    CHECK (
        (Requester_Type = 'Hospital' AND Hospital_ID IS NOT NULL AND Recipient_ID IS NULL)
        OR
        (Requester_Type = 'Recipient' AND Recipient_ID IS NOT NULL AND Hospital_ID IS NULL)
    )
);

