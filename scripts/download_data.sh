# Exit immediately if a command exits with a non-zero status
set -e

# path to the dataset on kaggle
DATASET="shivamb/netflix-shows"

# path to the directory where the dataset will be downloaded and extracted
TARGET_DIR="./data/raw"

# exception handling for missing kaggle command-line tool
if ! command -v kaggle &> /dev/null; then
    echo "Error: The 'kaggle' command-line tool is not installed."
    echo "Please run: pip install kaggle"
    exit 1
fi

# creates a directory if the target directory does not exist
echo "Creating directory at: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# downloading and unzipping the dataset from Kaggle
echo "Starting download for: $DATASET..."
kaggle datasets download -d "$DATASET" -p "$TARGET_DIR" --unzip

# success message after the dataset has been downloaded and extracted
echo "Success! Dataset downloaded and extracted to $TARGET_DIR"