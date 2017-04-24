CREATE TABLE Tow_Checked (
Towing_ID VARCHAR(150) PRIMARY KEY NOT NULL,
Logged_Date DATE,
UNIQUE(Towing_ID, Logged_Date),
FOREIGN KEY (Towing_ID, Logged_Date) REFERENCES Daily_Surveillance(Aircraft_ID, Logged_Date),
FOREIGN KEY (Towing_ID) REFERENCES Tow_Plane(Towing_ID)
);