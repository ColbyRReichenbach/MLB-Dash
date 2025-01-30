import sqlite3
import pandas as pd

# 📌 Connect to Database
DB_PATH = "lahman_baseball.sqlite"
conn = sqlite3.connect(DB_PATH)

# 📌 Function to Export SQL Query Results as CSV
def export_query_to_csv(query, filename):
    df = pd.read_sql(query, conn)
    file_path = f"/Users/colbyreichenbach/Desktop/Portfolio/MLB_SQL/SQL_Queries/{filename}"
    df.to_csv(file_path, index=False)
    print(f"✅ Exported {filename} with {df.shape[0]} rows.")

# 📌 Export Data for Tableau
export_query_to_csv("SELECT * FROM League_Awards;", "League_Awards.csv")
export_query_to_csv("SELECT * FROM League_Performance;", "League_Performance.csv")
export_query_to_csv("SELECT * FROM League_Stats;", "League_Stats.csv")
export_query_to_csv("SELECT * FROM Team_Performance;", "Team_Performance.csv")
export_query_to_csv("SELECT * FROM Team_Salary_Efficiency;", "Team_Salary_Efficiency.csv")
export_query_to_csv("SELECT * FROM Player_Salary_Efficiency;", "Player_Salary_Efficiency.csv")
export_query_to_csv("SELECT * FROM Top_HR_Hitters;", "Top_HR_Hitters.csv")
export_query_to_csv("SELECT * FROM Top_Pitchers;", "Top_Pitchers.csv")
export_query_to_csv("SELECT * FROM Highest_Paid_Players;", "Highest_Paid_Players.csv")
export_query_to_csv("SELECT * FROM Awarded_Players_Salary;", "Awarded_Players_Salary.csv")
export_query_to_csv("SELECT * FROM Player_Career_Batting;", "Player_Career_Batting.csv")
export_query_to_csv("SELECT * FROM Player_Career_Pitching;", "Player_Career_Pitching.csv")
export_query_to_csv("SELECT * FROM Award_Winners_Stats;", "Award_Winners_Stats.csv")


# 📌 Close Connection
conn.close()
print("\n✅ All query results exported successfully. Ready for Tableau!")
