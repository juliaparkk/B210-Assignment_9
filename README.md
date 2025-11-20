# B210-Assignment_9
# a. What is the purpose of this program(s)?
The purpose of the program is to write a function that creates a dictionary of song titles based on their track_number and writes to a new CSV file.
# b. What does the program do, including what it takes for input, and what it gives as output?
The program reads the CSV as text, parses each line with split_csv_line (no csv module), normalizes the headers (strip, remove leading BOM, lowercase), and finds the indices for the track number and track name. For each data row, extracts: number = the value from the track number column (empty → "<missing>") and name = the value from the track name column. Builds a dictionary: keys = track number strings; values = lists of track titles that share that track number (this groups the same track number across different albums). Keys are sorted before writing; numeric-like keys are sorted numerically when possible.
The input is a CSV file (the default path in the script is taylor_discography.csv).
The output is Return value: a Python dict mapping track_number (string) → list of track_name strings, CSV file: default tracks_by_number.csv (two columns: track_number,track_titles), track_titles contains titles joined by | (pipe + spaces), Fields are properly quoted if they contain commas or quotes, Console output (when run as script): prints the output path, number of keys, and the first 10 keys with counts (e.g., 1 -> 21 titles).
# c. How do you use the program?
Save the file in VS Code as C:\Users\jinas\Downloads\Assignment 9 DIctionaries.py.
Pick the Python interpreter (Anaconda Python) in VS Code.
Run the script in the VS Code integrated terminal.
Edit the input/output paths if needed or call the function interactively.
Inspect the produced CSV and (optionally) debug or convert the script to accept command-line args.
