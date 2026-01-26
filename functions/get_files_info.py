import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_path = os.path.abspath(working_directory)
        target_dir_path = os.path.normpath(os.path.join(working_dir_path, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_path, target_dir_path]) == working_dir_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir_path):
            return f'Error: "{directory}" is not a directory'
        dir_contents = os.scandir(target_dir_path)

        info_string = ""
        for entry in dir_contents:
            info_string += f"- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}\n"
        return info_string
    except Exception as e:
        return f"Error: {e}"
