import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("lahman_baseball.sqlite")

# Query to check available tables
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql(query, conn)

print("📋 Tables in the database:")
print(tables)

# Check column names of Batting table
query = "PRAGMA table_info(Awards);"
columns = pd.read_sql(query, conn)
print(columns)

conn.close()