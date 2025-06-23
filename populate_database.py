#!/usr/bin/env python3

import csv
from pathlib import Path


def create_csv_files():
    """Create CSV files for PostgreSQL import."""
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

    # Create names CSV file
    names_csv_path = Path("names.csv")
    with open(names_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "gender"])
        for name, gender in sorted(names_set):
            writer.writerow([name, gender])
    
    print(f"Created {names_csv_path} with {len(names_set)} unique names")

    # Create names_per_year CSV file
    yearly_csv_path = Path("names_per_year.csv")
    with open(yearly_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["year", "rank", "boy", "girl"])
        for year, rank, boy_name, girl_name in sorted(yearly_data):
            # Handle None values for PostgreSQL NULL
            boy_val = boy_name if boy_name else ""
            girl_val = girl_name if girl_name else ""
            writer.writerow([year, rank, boy_val, girl_val])
    
    print(f"Created {yearly_csv_path} with {len(yearly_data)} yearly records")


def main():
    """Main function to create CSV files."""
    try:
        print("Creating CSV files for PostgreSQL import...")
        create_csv_files()
        print("CSV files created successfully!")
        print("\nTo import into PostgreSQL, use:")
        print("\\copy names FROM 'names.csv' WITH CSV HEADER;")
        print("\\copy names_per_year FROM 'names_per_year.csv' WITH CSV HEADER;")

    except Exception as e:
        print(f"Script failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
