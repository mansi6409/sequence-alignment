#!/bin/bash

# Loop through files named file1.txt to file15.txt
for i in {1..15}
do
  # Construct the filename
  filename="../arch/out${i}.txt"
  
  # Check if the file exists
  if [ -f "$filename" ]; then
    # Use sed to print the 5th line of the file
    sed -n '4p' $filename
  else
    echo "$filename does not exist."
  fi
done

