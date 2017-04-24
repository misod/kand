CREATE TABLE Flight_Data (
Flight_No int PRIMARY KEY NOT NULL,
Takeoff DATETIME,
Landing DATETIME,
Logged_Date DATE,
Flight_Type VARCHAR(150) NOT NULL,
Glider_id VARCHAR(150) NOT NULL,
Towing_id VARCHAR(150),
Towing_Height int,
Towing_Takeoff TIME,
Towing_Landing TIME,
Status VARCHAR(150),
Notes VARCHAR(150),
FOREIGN KEY (Glider_ID) REFERENCES Glider(Glider_ID),
FOREIGN KEY (Towing_ID) REFERENCES Tow_Plane(Towing_ID)
);