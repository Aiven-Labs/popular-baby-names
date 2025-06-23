# Popular Baby Names Database

## Data Source: Social Security Administration (ssa.gov)

This repository contains a PostgreSQL database system for storing and querying popular baby names data from 1880 through 2024. Originally containing CSV and JSON files, this project now includes database schema, data population scripts, and structured data storage capabilities.

**UPDATE: Added popular baby names for 2024.**

## Database Schema

The database consists of two main tables:

### `names` table
- `name` (TEXT, PRIMARY KEY): The baby name
- `gender` (ENUM): Either 'male' or 'female'

### `names_per_year` table
- `year` (INTEGER, PRIMARY KEY): The year of the data
- `rank` (INTEGER): The ranking position for that year
- `boy` (TEXT): Reference to most popular boy name at this rank
- `girl` (TEXT): Reference to most popular girl name at this rank

## Setup and Usage

### Prerequisites
- Python 3.x
- PostgreSQL database (Aiven or local)
- Required Python packages: `psycopg`, `csv`, `pathlib`

### Environment Setup
Set your database connection string:
```bash
export AIVEN_PG_CONNECTION_STRING="your_postgresql_connection_string"
```

### Database Initialization
1. Create the database schema:
   ```bash
   psql -f setup.sql
   ```

2. Populate the database with CSV data:
   ```bash
   python3 populate_database.py
   ```

## Data Structure

The repository contains CSV files organized by year directories (1880-2024), with each directory containing:
- `girl_boy_names_YYYY.csv`: Combined rankings of most popular names by year

## Features

- **Automated Data Loading**: The `populate_database.py` script automatically discovers and loads all CSV files
- **Data Integrity**: Foreign key constraints ensure data consistency
- **Conflict Handling**: ON CONFLICT clauses prevent duplicate entries during data loading
- **Error Handling**: Comprehensive error handling with rollback capabilities

## Original Data Access

The original CSV and JSON files for individual years remain accessible through the year directories:
- Most popular 1,000 names for boys and girls from 1880 through 2024
- Data sourced from the Social Security Administration's official records
