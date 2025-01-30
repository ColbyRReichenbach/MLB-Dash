import sqlite3

# 📌 Connect to Database
DB_PATH = "lahman_baseball.sqlite"  # Update if needed
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 📌 List of SQL Queries (Each Statement as a Separate Query)
sql_queries = [
    """DROP VIEW IF EXISTS League_Awards;""",
    """CREATE VIEW League_Awards AS
    SELECT a.yearID, a.awardID, a.playerID, a.notes AS Position, a.tie AS Tie, 
           p.nameFirst || ' ' || p.nameLast AS playerName
    FROM Awards a
    JOIN People p ON a.playerID = p.playerID
    ORDER BY a.yearID DESC, a.awardID;""",

    """DROP VIEW IF EXISTS League_Performance;""",
    """CREATE VIEW League_Performance AS
    SELECT yearID, teamID, SUM(W) AS TotalWins, SUM(R) AS TotalRuns, SUM(HR) AS TotalHRs, 
           ROUND(AVG(ERA), 2) AS AvgERA
    FROM Teams
    GROUP BY yearID, teamID
    ORDER BY yearID DESC, TotalWins DESC;""",

    """DROP VIEW IF EXISTS League_Batting_Stats;""",
    """CREATE VIEW League_Batting_Stats AS
    SELECT yearID, 
           SUM(HR) AS TotalHRs, 
           ROUND(SUM(H * 1.0) / NULLIF(SUM(AB), 0), 3) AS AvgBA,  
           SUM(RBI) AS TotalRBI,
           ROUND(SUM((H + BB + HBP) * 1.0) / NULLIF(SUM(AB + BB + HBP + SF), 0), 3) AS OBP,  
           ROUND(SUM((H - "2B" - "3B" - HR) + ("2B" * 2) + ("3B" * 3) + (HR * 4)) / NULLIF(SUM(AB), 0), 3) AS SLG,
           ROUND(
               ROUND(SUM((H + BB + HBP) * 1.0) / NULLIF(SUM(AB + BB + HBP + SF), 0), 3) + 
               ROUND(SUM((H - "2B" - "3B" - HR) + ("2B" * 2) + ("3B" * 3) + (HR * 4)) / NULLIF(SUM(AB), 0), 3),
           3) AS OPS  
    FROM Batting
    GROUP BY yearID
    ORDER BY yearID DESC;""",

    """DROP VIEW IF EXISTS League_Pitching_Stats;""",
    """CREATE VIEW League_Pitching_Stats AS
    SELECT yearID, 
           SUM(SO) AS TotalStrikeouts, 
           ROUND(AVG(ERA), 2) AS AvgERA, 
           SUM(W) AS TotalWins,
           ROUND((SUM(SO) * 9.0) / NULLIF(SUM(W + L), 0), 2) AS K_9,  
           ROUND((SUM(BB) * 9.0) / NULLIF(SUM(W + L), 0), 2) AS BB_9,
           ROUND(SUM(BB + H) / NULLIF(SUM(W + L), 0), 2) AS WHIP  
    FROM Pitching
    GROUP BY yearID
    ORDER BY yearID DESC;""",

    """DROP VIEW IF EXISTS Player_Career_Batting;""",

    """CREATE VIEW Player_Career_Batting AS
    SELECT 
        b.yearID, b.playerID, b.teamID, 
        p.nameFirst || ' ' || p.nameLast AS player_name, 
        b.AB,
        b.HR, 
        ROUND(b.H * 1.0 / NULLIF(b.AB, 0), 3) AS AVG,  
        b.RBI, 
        ROUND(SUM((b.H + b.BB + b.HBP) * 1.0) / NULLIF(SUM(b.AB + b.BB + b.HBP + b.SF), 0), 3) AS OBP,
        ROUND(SUM((b.H - b."2B" - b."3B" - b.HR) + (b."2B" * 2) + (b."3B" * 3) + (b.HR * 4)) / NULLIF(SUM(b.AB), 0), 3) AS SLG,
     -- Calculate OPS without referencing OBP/SLG aliases
        ROUND(
            (SUM((b.H + b.BB + b.HBP) * 1.0) / NULLIF(SUM(b.AB + b.BB + b.HBP + b.SF), 0)) + 
            (SUM((b.H - b."2B" - b."3B" - b.HR) + (b."2B" * 2) + (b."3B" * 3) + (b.HR * 4)) / NULLIF(SUM(b.AB), 0)), 
        3) AS OPS  
        FROM Batting b
    JOIN People p ON b.playerID = p.playerID
    WHERE b.AB >= 1
    GROUP BY b.yearID, b.playerID, b.teamID
    ORDER BY b.yearID DESC;""",

    """DROP VIEW IF EXISTS Player_Career_Pitching;""",
    """CREATE VIEW Player_Career_Pitching AS
    SELECT p.yearID, p.playerID, p.teamID, 
           pe.nameFirst || ' ' || pe.nameLast AS player_name, 
           p.ERA, 
           p.SO, 
           p.BFP,
           p.BAOPP,
           ROUND((p.SO * 9.0) / NULLIF(p.IPOuts / 3.0, 0), 2) AS K_9,  
           ROUND((p.BB * 9.0) / NULLIF(p.IPOuts / 3.0, 0), 2) AS BB_9,
           ROUND((p.BB + p.H) / NULLIF(p.IPOuts / 3.0, 0), 2) AS WHIP
    FROM Pitching p
    JOIN People pe ON p.playerID = pe.playerID
    WHERE p.BFP >= 1
    ORDER BY p.yearID DESC;""",

    """DROP VIEW IF EXISTS Awarded_Players_Salary;""",
    """CREATE VIEW Awarded_Players_Salary AS
    SELECT 
        a.yearID, 
        p.nameFirst || ' ' || p.nameLast AS player_name, 
        a.awardID, 
        s.salary
    FROM Awards a
    JOIN Salaries s ON a.playerID = s.playerID AND a.yearID = s.yearID
    JOIN People p ON a.playerID = p.playerID
    ORDER BY s.salary DESC;""",
    
    """DROP VIEW IF EXISTS Top_HR_Hitters;""",
    """CREATE VIEW Top_HR_Hitters AS
    SELECT b.yearID, b.teamID, b.playerID, 
           p.nameFirst || ' ' || p.nameLast AS playerName, 
           b.HR,
           RANK() OVER (PARTITION BY b.yearID ORDER BY b.HR DESC) AS Rank
    FROM Batting b
    JOIN People p ON b.playerID = p.playerID
    WHERE b.HR > 0;""",

    """DROP VIEW IF EXISTS Top_Pitchers;""",
    """CREATE VIEW Top_Pitchers AS
    SELECT p.yearID, p.teamID, p.playerID, 
           pe.nameFirst || ' ' || pe.nameLast AS playerName, 
           p.ERA, p.SO, 
           ROUND((p.SO * 9.0) / NULLIF((p.W + p.L), 0), 2) AS K_9,  
           ROUND((p.BB * 9.0) / NULLIF((p.W + p.L), 0), 2) AS BB_9,
           ROUND((p.BB + p.H) / NULLIF((p.W + p.L), 0), 2) AS WHIP,  
           RANK() OVER (PARTITION BY p.yearID ORDER BY p.ERA ASC) AS Rank
    FROM Pitching p
    JOIN People pe ON p.playerID = pe.playerID
    WHERE p.SO >= 50;""",

    """DROP VIEW IF EXISTS Award_Winners_Stats;""",
    """CREATE VIEW Award_Winners_Stats AS
    SELECT 
        a.yearID,
        a.awardID,
        COALESCE(b.teamID, pcf.teamID) AS teamID, -- Get teamID from either batting or pitching
        t.name AS teamName,  -- Use correct column from Teams
        t.lgID,
        t.divID,
        p.nameFirst || ' ' || p.nameLast AS playerName
    
       

    FROM Awards a
    LEFT JOIN People p ON a.playerID = p.playerID
    LEFT JOIN Player_Career_Batting b ON a.playerID = b.playerID AND a.yearID = b.yearID
    LEFT JOIN PLayer_Career_Pitching pcf ON a.playerID = pcf.playerID AND a.yearID = pcf.yearID
    LEFT JOIN Teams t ON COALESCE(b.teamID, pcf.teamID) = t.teamID AND a.yearID = t.yearID;
"""
]

# 📌 Execute Queries One by One
for query in sql_queries:
    try:
        cursor.execute(query.strip())  # Removes extra spaces
        print(f"✅ Executed: {query.split('AS')[0]}...")
    except sqlite3.Error as e:
        print(f"❌ Error executing query: {e}")

# 📌 Commit and Close Connection
conn.commit()
conn.close()

print("\n✅ All SQL Views have been created successfully.")
