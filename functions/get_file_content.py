import os

def get_file_content(working_directory, file_path):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        MAX_CHARS = 10000
        with open(target_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'


        return content
    except Exception as e:
        return f"Error: {e}"
