import os
import json
import argparse
import random

def read_file_content(file_path):
    """Read the content of a file and return it as a string."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

def get_all_files_in_directory(directory_path):
    """Get the list of all files in a directory."""
    return [os.path.join(directory_path, f) for f in os.listdir(directory_path) if
            os.path.isfile(os.path.join(directory_path, f))]

def create_mxn_join_json(directory1, directory2, instruction):
    """Create a JSON array with MxN combinations of files from two directories."""
    files_dir1 = get_all_files_in_directory(directory1)
    files_dir2 = get_all_files_in_directory(directory2)

    result = []

    # Create MxN combinations of files
    for file1 in files_dir1:
        content1 = read_file_content(file1)
        for file2 in files_dir2:
            content2 = read_file_content(file2)
            result.append({
                "messages": [
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": content1},
                    {"role": "assistant", "content": content2}
                ]
            })
    random.shuffle(result)
    return result[:500]

def main(directory1, directory2, output_file, instruction):
    # Generate the JSON result
    json_result = create_mxn_join_json(directory1, directory2, instruction)

    # Write the result to a file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for item in json_result:
            out_file.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Create MxN join of files from two directories and store in JSON format.")
    parser.add_argument("directory1", help="Path to the first directory")
    parser.add_argument("directory2", help="Path to the second directory")
    parser.add_argument("output_file", help="Path to the output JSON file")
    parser.add_argument("instruction", help="Instruction string to be added to all JSON objects")

    args = parser.parse_args()

    # Run the main function with provided arguments
    main(args.directory1, args.directory2, args.output_file, args.instruction)