import logging
import os
import sys

def generate_header(header_path, source):
  """Generate a header file for the C++ functions in the source folder.

  The header file contains the function declarations for each C++ file in the source folder.

  Args:
    header_path (str): The full path to the header file to be generated.
    source (str): The path to the source folder that contains the C++ files.

  Returns:
    None
  """
  header_file_name = os.path.basename(header_path)
  header_file_name_upper = header_file_name.upper().replace(".", "_")
  header_contents = "#ifndef " + header_file_name_upper + "\n#define " + header_file_name_upper + "\n\n"
  header_contents += "#include \"test_types.hpp\"\n\n"

  for filename in os.listdir(source):
    if filename.endswith(".cpp"):
      function_name = filename[:-4]
      header_contents += "TestCaseStats " + function_name + "();\n"
      logging.info("Parsed file: %s", filename)
  header_contents += "\n#endif /* " + header_file_name_upper + " */\n"

  with open(header_path, "w") as header_file:
    header_file.write(header_contents)
  logging.info("Header file generated at: %s", header_path)

if __name__ == "__main__":
  """Main entry point for the script.

  The script generates a header file for the C++ functions in the source folder and saves it at the specified path.
  """
  logging.basicConfig(level=logging.INFO, format="%(message)s")
  if len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("Usage: python header_generator.py <header_path> <source>")
    print("Generate a header file for the C++ functions in the source folder and save it at the specified path.")
    print("")
    print("  header_path  The full path to the header file to be generated.")
    print("  source       The path to the source folder that contains the C++ files.")
    sys.exit(0)
  elif len(sys.argv) != 3:
    logging.error("Invalid number of arguments. Use --help for usage information.")
    sys.exit(1)
  else:
    header_path = sys.argv[1]
    source = sys.argv[2]
    logging.info("Generating header file '%s' from source: %s", header_path, source)
    generate_header(header_path, source)
