CREATE TABLE Glider_Checked (
Glider_ID VARCHAR(150) PRIMARY KEY NOT NULL,
Logged_Date DATE,
UNIQUE(Glider_ID, Logged_Date),
FOREIGN KEY (Glider_ID, Logged_Date) REFERENCES Daily_Surveillance(Aircraft_ID, Logged_Date),
FOREIGN KEY (Glider_ID) REFERENCES Glider(Glider_ID)
);