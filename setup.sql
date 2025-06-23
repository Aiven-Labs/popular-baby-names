-- Create the gender enum
CREATE TYPE gender AS ENUM ('male', 'female');

-- Create the names table
CREATE TABLE names (
    name TEXT PRIMARY KEY,
    gender gender NOT NULL
);

-- Create the years table
CREATE TABLE names_per_year (
    year INTEGER PRIMARY KEY,
    rank INTEGER,
    boy TEXT REFERENCES names(name),
    girl TEXT REFERENCES names(name)
  );
