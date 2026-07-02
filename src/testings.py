import pandas as pd
import numpy as np
import pytest

# Import the specific cleaning functions from your clean_data.py script
from clean_data import drop_missing_titles, fill_nulls_with_unknown

# TEST 1: Dropping Missing Titles
def test_drop_missing_titles():
    """Verifies that rows with a null title are completely removed."""
    # 1. Arrange: Create a fake DataFrame with one valid row and one invalid row
    fake_data = pd.DataFrame({
        "show_id": ["s1", "s2"],
        "title": ["Inception", np.nan] 
    })
    
    # 2. Act: Run our cleaning function on the fake data
    cleaned_df = drop_missing_titles(fake_data)
    
    # 3. Assert: Verify the results
    assert len(cleaned_df) == 1, "The dataframe should only have 1 row left"
    assert cleaned_df.iloc[0]["title"] == "Inception", "The valid row should remain"


# TEST 2: Filling Nulls
def test_fill_nulls_with_unknown():
    """Verifies that remaining NaN values are replaced with the string 'Unknown'."""
    # 1. Arrange: Create fake data missing a director and a country
    fake_data = pd.DataFrame({
        "director": ["Christopher Nolan", np.nan],
        "country": [np.nan, "United States"]
    })
    
    # 2. Act: Run our cleaning function
    cleaned_df = fill_nulls_with_unknown(fake_data)
    
    # 3. Assert: Verify the NaNs are gone
    assert cleaned_df.iloc[1]["director"] == "Unknown", "Missing director should be 'Unknown'"
    assert cleaned_df.iloc[0]["country"] == "Unknown", "Missing country should be 'Unknown'"