import sys
import os

def extract_content(filename):
    """
    Extract the snyk-delta summary from a file.

    Args:
        filename (str): The name of the file to extract content from.

    Returns:
        str: The extracted content after the last occurrence of the pattern.
            Returns None if the file is invalid or the pattern is not found.
    """
    # Check if file exists
    if not os.path.isfile(filename):
        print("File not found:", filename)
        return None

    # Search for the last occurrence of the underscore pattern from the snyk-delta output
    with open(filename, 'r') as file:
        lines = file.readlines()

    last_match = None
    for index, line in enumerate(lines):
        if '_____________________________' in line:
            last_match = index

    # If no match found, return None
    if last_match is None:
        print("Invalid file")
        return None
    else:
        # Extract content after the last match
        return ''.join(lines[last_match + 1:])

if __name__ == "__main__":
    # Check if filename is provided
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<filename>")
        sys.exit(1)

    filename = sys.argv[1]
    content = extract_content(filename)
    if content is not None:
        print(content, end='')