import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Date

def deduplicate_records(df):
    """this function drops the duplicate records based on the show_id column"""
    return df.drop_duplicates(subset=['show_id']).copy()

def drop_missing_titles(df):
    """this function drops rows with null values in the 'title' column"""
    return df.dropna(subset=["title"]).copy()

def clean_text_formatting(df):
    """this function removes whitespace across all columns and normalizes specific titles."""
    # removing the white spaces on every column
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    # normalising the title names (already stripped above, just need title case)
    df['title'] = df['title'].str.title()
    df['type'] = df['type'].str.title()
    return df

def fill_nulls_with_unknown(df):
    """this function changes the null values of all columns to 'Unknown'."""
    return df.fillna('Unknown')

def format_date_columns(df):
    """this function converts date strings into proper datetime and year formats."""
    # changing the data stype of date_added column to date type
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.date
    
    # changing the data type of release_year column to date year type
    df['release_year'] = pd.to_datetime(df['release_year'], format='%Y', errors='coerce').dt.year
    return df


def run_pipeline():
    # main execution
    print("Connecting to database...")
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/bootcamp")
    df = pd.read_sql("SELECT * FROM staging_raw", engine)
    
    # this code blocks is for cleaning the data by calling the functions defined above
    print(f"Original row count: {len(df)}")
    df = deduplicate_records(df)
    df = drop_missing_titles(df)
    df = clean_text_formatting(df)
    df = fill_nulls_with_unknown(df)
    df = format_date_columns(df)
    
    # after cleaning and transforming the data, we write it back to the database in a new table
    print("Writing clean data to Postgres...")
    df.to_sql(
        name="staging_clean", 
        con=engine, 
        if_exists="replace", 
        index=False,
        dtype={"date_added": Date()}  # Enforces strict DATE type so DBeaver drops the 00:00:00
    )
    
    # prints the confirmation when transforming and writing the data back to the database 
    print(f"Cleaned {len(df)} records and loaded into the staging_clean table in the database.")

if __name__ == "__main__":
    run_pipeline()