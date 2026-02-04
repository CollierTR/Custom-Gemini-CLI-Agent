from google.genai import types
import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        abs_file_path = os.path.abspath(target_file_path)
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        # Do something here...
        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="A function to write to a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for the file you want to write to",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string that you want to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

