#!/bin/bash

# Loop through all .txt files in the current directory
for file in *.txt; do
  # Check if there are any .txt files
  if [ "$file" == "*.txt" ]; then
    echo "No .txt files found."
    break
  fi
  
  # Extract the base name without the extension
  base_name="${file%.txt}"
  
  # Rename the file by removing the .txt extension and adding .md
  mv "$file" "${base_name}.md"
  
  # Print a message indicating the conversion
  echo "Converted $file to ${base_name}.md"
done
