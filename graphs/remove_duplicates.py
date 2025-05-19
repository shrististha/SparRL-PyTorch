import sys


def remove_duplicate_lines(input_filepath):
    """
    Reads a file and returns a list of unique lines in their original order of appearance.

    Args:
        input_filepath (str): The path to the input text file.

    Returns:
        list: A list of unique lines (including their original newline characters)
              in the order they first appeared in the file.
              Returns None if an error occurs reading the file.
              Returns an empty list if the input file is empty.
    """
    seen_lines = set()  # Keep track of lines already encountered
    unique_lines_in_order = []  # Store unique lines in order

    try:
        # Use 'utf-8' encoding, change if your file uses something else
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            original_line_count = 0
            for line in infile:
                original_line_count += 1
                # Check if we've seen this exact line before
                if line not in seen_lines:
                    seen_lines.add(line)
                    unique_lines_in_order.append(line)  # Add the unique line (with its newline)

        print(f"Processed {original_line_count} lines from '{input_filepath}'.")
        return unique_lines_in_order

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_filepath}'", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading file '{input_filepath}': {e}", file=sys.stderr)
        return None


def save_lines_to_file(lines, output_filepath):
    """
    Saves a list of lines (strings) to a file.

    Args:
        lines (list): The list of lines to save. Each string should typically
                      end with a newline character if read directly from a file.
        output_filepath (str): The path to the output text file.

    Returns:
        bool: True if saving was successful, False otherwise.
    """
    # Optional: Check if output file exists and ask before overwriting

    try:
        # Use 'utf-8' encoding for writing
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            for line in lines:
                outfile.write(line)  # Write the line exactly as it was read
        print(f"Successfully saved {len(lines)} unique lines to '{output_filepath}'")
        return True
    except Exception as e:
        print(f"Error writing to file '{output_filepath}': {e}", file=sys.stderr)
        return False


input_file = "amazontop5000.txt"
unique_lines = remove_duplicate_lines(input_file)

if unique_lines is not None:
    print(f"Found {len(unique_lines)} unique lines.")

    save_lines_to_file(unique_lines, "amazontop5000_dedup.txt")
