CREATE TABLE Flew (
Flight_No int NOT NULL,
Pilot_ID int NOT NULL,
Flight_Type VARCHAR(150) NOT NULL,
FOREIGN KEY (Flight_No) REFERENCES Flight_data(Flight_No),
FOREIGN KEY (Pilot_ID) REFERENCES Pilot(Pilot_ID)
);