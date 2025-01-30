import sqlite3
import pandas as pd
import os

# 📌 Define database path
DB_PATH = "lahman_baseball.sqlite"

# 📌 Connect to SQLite Database (Creates it if not exists)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print(f"✅ Connected to SQLite Database: {DB_PATH}")


# 📌 Function to Load CSV Files into SQL Tables
def load_csv_to_sql(filename, table_name):
    try:
        filepath = os.path.join("/Users/colbyreichenbach/Desktop/Portfolio/MLB_SQL/lahman_data"
                                "/cleaned_and_processed_data/", filename)  # Adjust path if needed
        df = pd.read_csv(filepath)

        # Ensure column names are clean (strip whitespace, lowercase)
        df.columns = df.columns.str.strip()

        # Load DataFrame into SQL
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"✅ {table_name} table created with {df.shape[0]} rows.")
    except Exception as e:
        print(f"❌ Error loading {table_name}: {e}")


# 📌 List of Cleaned CSV Files and Their Corresponding Table Names
csv_files = {
    "People_Cleaned_Final.csv": "People",
    "Batting_Cleaned_Final.csv": "Batting",
    "Pitching_Cleaned_Final.csv": "Pitching",
    "Teams_Cleaned_Final.csv": "Teams",
    "Salaries_Cleaned_Final.csv": "Salaries",
    "Awards_Cleaned_Final.csv": "Awards"
}

# 📌 Load Each CSV File into SQLite
for file, table in csv_files.items():
    load_csv_to_sql(file, table)

# 📌 Verify Tables Were Created
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\n📂 Tables in Database:", tables)

# 📌 Commit and Close Connection
conn.commit()
conn.close()

print("✅ Database setup complete. You can now query the tables!")
