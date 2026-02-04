from google.genai import types
import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_path, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_path, target_file_path]) == working_dir_path

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        print("Last 3: ", target_file_path[-3:])
        if not target_file_path.endswith(".py") and not target_file_path.endswith(".PY"):
            return f'Error: "{file_path}" is not a Python file'

        abs_file_path = os.path.abspath(target_file_path)

        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        process = subprocess.run(command, cwd=working_dir_path, capture_output=True, text= True, timeout=30)
        if process.returncode != 0:
            output = "Process exited with code X"
        if not process.stderr and not process.stdout:
            output = "No output produced"
        else:
            output = f"STDOUT: {process.stdout} STDERR: {process.stderr}"
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python script",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for the file you want to execute",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="an array of any args needed for the python executable",
            ),
        },
        required=["file_path"],
    ),
)

