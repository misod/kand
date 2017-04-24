CREATE TABLE Surveilled (
Aircraft_ID VARCHAR(150) PRIMARY KEY NOT NULL,
Logged_Date DATE,
Pilot_ID int,
UNIQUE(Aircraft_ID, Logged_Date),
FOREIGN KEY (Aircraft_ID, Logged_Date) REFERENCES Daily_Surveillance(Aircraft_ID, Logged_Date),
FOREIGN KEY (Pilot_ID) REFERENCES Pilot(Pilot_ID)
);