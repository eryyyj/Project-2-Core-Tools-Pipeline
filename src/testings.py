import pandas as pd
import numpy as np
import pytest

# importing the specific functions from the clean_data.py file to test them
from clean_data import drop_missing_titles, fill_nulls_with_unknown, deduplicate_records, clean_text_formatting, format_date_columns

# testing 1: drops the record with missing titles
def test_drop_missing_titles():
    """this testing verifies that rows with a null title are completely removed."""
    # creation of a fake dataframe with one valid title and one missing title
    fake_data = pd.DataFrame({
        "show_id": ["s1", "s2"],
        "title": ["Inception", np.nan] 
    })
    
    # running the function and feeding the fake data to it
    cleaned_df = drop_missing_titles(fake_data)
    
    # using assert statements to verify that the function works as expected
    assert len(cleaned_df) == 1, "The dataframe should only have 1 row left"
    assert cleaned_df.iloc[0]["title"] == "Inception", "The valid row should remain"


# testing 2: filling the null values with 'Unknown' in the dataframe
def test_fill_nulls_with_unknown():
    """this testing verifies that remaining NaN values are replaced with the string 'Unknown'."""
    # creating a fake dataframe with missing values in the 'director' and 'country' columns
    fake_data = pd.DataFrame({
        "director": ["Christopher Nolan", np.nan],
        "country": [np.nan, "United States"]
    })
    
    # calling the function while feeding the fake data to it
    cleaned_df = fill_nulls_with_unknown(fake_data)
    
    # using assert statements to verify that the function works as expected
    assert cleaned_df.iloc[1]["director"] == "Unknown", "Missing director should be 'Unknown'"
    assert cleaned_df.iloc[0]["country"] == "Unknown", "Missing country should be 'Unknown'"

# testing 3: dropping duplicate records based on the 'show_id' column
def test_deduplicate_records():
    """this testing verifies that duplicate records based on the 'show_id' column are removed."""
    # creating a fake dataframe with duplicate records
    fake_data = pd.DataFrame({
        "show_id": ["s1", "s1", "s2"],
        "title": ["Inception", "Inception", "The Matrix"]
    })
    
    # calling the function while feeding the fake data to it
    cleaned_df = deduplicate_records(fake_data)
    
    # using assert statements to verify that the function works as expected
    assert len(cleaned_df) == 2, "The dataframe should only have 2 unique rows"
    assert cleaned_df['show_id'].nunique() == 2, "There should be 2 unique show_ids"

# testing 4: cleaning text formatting by stripping whitespace and normalizing titles
def test_clean_text_formatting():
    """this testing verifies that whitespace is removed and titles are normalized to title case."""
    # creating a fake dataframe with leading/trailing whitespace and inconsistent title casing
    fake_data = pd.DataFrame({
        "title": ["  inception  ", "the matrix"],
        "type": ["movie", "MOVIE"]
    })
    
    # calling the function while feeding the fake data to it
    cleaned_df = clean_text_formatting(fake_data)
    
    # using assert statements to verify that the function works as expected
    assert cleaned_df.iloc[0]["title"] == "Inception", "Title should be stripped and in title case"
    assert cleaned_df.iloc[1]["title"] == "The Matrix", "Title should be stripped and in title case"
    assert cleaned_df.iloc[0]["type"] == "Movie", "Type should be normalized to title case"

# testing 5: formatting date columns to proper datetime and year formats
def test_format_date_columns():
    """this testing verifies that date strings are converted into proper datetime and year formats."""
    # creating a fake dataframe with date strings
    fake_data = pd.DataFrame({
        "date_added": ["January 1, 2020", "February 15, 2021"],
        "release_year": ["2010", "2015"]
    })
    
    # calling the function while feeding the fake data to it
    cleaned_df = format_date_columns(fake_data)
    
    # using assert statements to verify that the function works as expected
    assert cleaned_df.iloc[0]["date_added"] == pd.to_datetime("2020-01-01").date(), "Date should be converted to proper date format"
    assert cleaned_df.iloc[1]["release_year"] == 2015, "Release year should be converted to integer year format"