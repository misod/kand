CREATE TABLE Daily_Surveillance (
Aircraft_ID VARCHAR(150) NOT NULL,
Logged_Date DATE,
Note VARCHAR(150),
UNIQUE(Aircraft_ID, Logged_Date)
);