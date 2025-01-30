import sqlite3

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect("lahman_baseball.sqlite")
cursor = conn.cursor()

# Create tables
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS People (
        playerID TEXT PRIMARY KEY,
        nameFirst TEXT,
        nameLast TEXT,
        birthYear INT,
        birthCountry TEXT,
        height INT,
        weight INT,
        bats TEXT,
        throws TEXT
    );

    CREATE TABLE IF NOT EXISTS Teams (
        yearID INT,
        teamID TEXT,
        franchID TEXT,
        name TEXT,
        W INT,
        L INT,
        R INT,
        RA INT,
        ERA FLOAT,
        PRIMARY KEY (yearID, teamID)
    );

    CREATE TABLE IF NOT EXISTS Batting (
        playerID TEXT,
        yearID INT,
        teamID TEXT,
        G INT,
        AB INT,
        H INT,
        HR INT,
        RBI INT,
        BB INT,
        SO INT,
        FOREIGN KEY (playerID) REFERENCES People(playerID),
        FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID)
    );

    CREATE TABLE IF NOT EXISTS Pitching (
        playerID TEXT,
        yearID INT,
        teamID TEXT,
        W INT,
        L INT,
        ERA FLOAT,
        SO INT,
        FOREIGN KEY (playerID) REFERENCES People(playerID),
        FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID)
    );

    CREATE TABLE IF NOT EXISTS Salaries (
        playerID TEXT,
        yearID INT,
        teamID TEXT,
        salary INT,
        FOREIGN KEY (playerID) REFERENCES People(playerID),
        FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID)
    );
    CREATE TABLE IF NOT EXISTS Awards (
        playerID TEXT,
        awardID TEXT,
        yearID INTEGER,
        lgID TEXT,
        tie TEXT,
        notes TEXT
);
""")

conn.commit()
conn.close()
print("✅ Database schema created successfully!")
