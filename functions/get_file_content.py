import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_norm = os.path.normpath(os.path.join(working_dir_abs,file_path))

        valid_file_path = os.path.commonpath([working_dir_abs,file_path_norm]) == working_dir_abs
        
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path_norm):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(file_path_norm, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
        
            
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return a string of files in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory where we are going to get the file content",
            ),
        },
        required=["file_path"]
    )
)  