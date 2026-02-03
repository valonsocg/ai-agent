import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_joined = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_file_path = os.path.commonpath([working_directory_abs,file_path_joined]) == working_directory_abs
        
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(file_path_joined):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_directory = os.path.dirname(file_path_joined)
        os.makedirs(parent_directory, exist_ok=True)
        
        with open(file_path_joined, "w") as f:
                f.write(content)
                
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
                
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes files in a specified directory relative to the working directory, providing the content to change",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory where is the file that we are going to write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write in the file located on the file_path relative to the working_directory",
            )
        },
        required=["file_path"]
    )
)  