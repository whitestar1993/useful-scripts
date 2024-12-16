#!/bin/bash
# Created via Copilot, need to check code!

# Ensure a directory is provided
if [ -z "$1" ]; then
  echo "Usage: $0 directory"
  exit 1
fi

# Change to the specified directory
cd "$1" || exit

# Loop through each file in the directory
for file in *; do
  # Skip if not a regular file
  if [ ! -f "$file" ]; then
    continue
  fi

  # Get the file name without extension
  filename=$(basename "$file" | sed 's/\.[^.]*$//')

  # Create a directory with the file name
  mkdir -p "$filename"

  # Move the file into the newly created directory
  mv "$file" "$filename/"
done

echo "Files have been moved into individual folders."
