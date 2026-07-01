set -e   # exit immediately on any error

DATA_URL="https://raw.githubusercontent.com/prasertcbs/basic-dataset/master/netflix_titles.csv"
OUTPUT_DIR="./data/raw"
OUTPUT_FILE="$OUTPUT_DIR/netflix_dataset.csv"

mkdir -p "$OUTPUT_DIR"

echo "[$(date)] Starting download from $DATA_URL"
curl -L -o "$OUTPUT_FILE" "$DATA_URL"
ROW_COUNT=$(wc -l < "$OUTPUT_FILE")
echo "[$(date)] Download complete: $ROW_COUNT lines saved to $OUTPUT_FILE"