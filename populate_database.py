#!/usr/bin/env python3

import os
import csv
from pathlib import Path
import psycopg


def connect_to_database():
    """Connect to PostgreSQL database using Aiven connection string."""
    connection_string = os.getenv("AIVEN_PG_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("Environment variable 'AIVEN_PG_CONNECTION_STRING' is not set")

    try:
        conn = psycopg.connect(connection_string)
        return conn
    except psycopg.Error as e:
        print(f"Error connecting to database: {e}")
        raise


def create_tables(conn):
    """Create tables based on setup.sql schema."""
    try:
        with conn.cursor() as cur:
            setup_sql = Path("setup.sql").read_text()
            cur.execute(setup_sql)
        conn.commit()
        print("Tables created successfully")
    except psycopg.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
        raise


def load_data(conn):
    """Load names and yearly data from CSV files."""
    names_set = set()
    yearly_data = []

    # Find all CSV files with combined boy/girl names
    csv_files = list(Path(".").glob("*/girl_boy_names_*.csv"))

    for csv_file in csv_files:
        try:
            # Extract year from directory name
            year = int(csv_file.parent.name)

            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rank = int(row["Rank"])
                    girl_name = row.get("Girl Name", "").strip() or None
                    boy_name = row.get("Boy Name", "").strip() or None

                    # Collect unique names
                    if girl_name:
                        names_set.add((girl_name, "female"))
                    if boy_name:
                        names_set.add((boy_name, "male"))

                    # Collect yearly data
                    yearly_data.append((year, rank, boy_name, girl_name))

        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            continue

    # Insert names first (required for foreign key constraints)
    try:
        with conn.cursor() as cur:
            names_data = list(names_set)
            cur.executemany(
                "INSERT INTO names (name, gender) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING",
                names_data,
            )
        conn.commit()
        print(f"Inserted {len(names_data)} unique names")
    except psycopg.Error as e:
        print(f"Error inserting names: {e}")
        conn.rollback()
        raise

    # Insert yearly data
    try:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO names_per_year (year, rank, boy, girl) VALUES (%s, %s, %s, %s) ON CONFLICT (year) DO NOTHING",
                yearly_data,
            )
        conn.commit()
        print(f"Inserted {len(yearly_data)} yearly records")
    except psycopg.Error as e:
        print(f"Error inserting yearly data: {e}")
        conn.rollback()
        raise


def main():
    """Main function to populate the database."""
    try:
        print("Connecting to database...")
        conn = connect_to_database()

        print("Creating tables...")
        create_tables(conn)

        print("Loading data...")
        load_data(conn)

        print("Database population completed successfully!")

    except Exception as e:
        print(f"Script failed: {e}")
        return 1
    finally:
        if "conn" in locals():
            conn.close()

    return 0


if __name__ == "__main__":
    exit(main())
