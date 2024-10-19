#!/bin/bash

# Check if both arguments are provided
if [ $# -ne 3 ]; then
  echo "Usage: $0 <search_directory> <destination_directory> <version>"
  exit 1
fi

SEARCH_DIR="$1"
DESTINATION="$2"
VERSION="$3"

# Create destination directory if it doesn't exist
mkdir -p "$DESTINATION"

# Find directories matching TASK.+ regex in the supplied search directory
find "$SEARCH_DIR" -type d -name 'RAPID*' | while read -r dir; do
  # Find all files in the subdirectories of the matched directory
  FILENAME="$(basename "$(dirname "$dir")").md"
  echo -e "This is the source code of a module in the ${VERSION} language. Below you can see the source code in Markdown syntax.\n" > "$DESTINATION/$FILENAME"
  echo -e "Folder structure of this project:\n\n" >> "$DESTINATION/$FILENAME"
  echo -e "\`\`\`$(tree "$dir" --charset=ascii --prune -I '.DS_Store')\`\`\`\n" >> "$DESTINATION/$FILENAME"
  
  find "$dir" -type f ! -name '.DS_Store' | while read -r file; do
    echo -e "This is the file named $(basename "$file"):\n" >> "$DESTINATION/$FILENAME"
    echo -e "\`\`\`$VERSION" >> "$DESTINATION/$FILENAME"
    # Copy files to the destination directory
    cat "$file" >> "$DESTINATION/$FILENAME"
    echo -e "\n\`\`\`\n\n" >> "$DESTINATION/$FILENAME"
  done
done

echo "Files created at $DESTINATION."
