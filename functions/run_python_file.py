import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_norm = os.path.normpath(os.path.join(working_dir_abs,file_path))

        valid_file_path = os.path.commonpath([working_dir_abs,file_path_norm]) == working_dir_abs
        
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path_norm):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        absolute_file_path = os.path.abspath(file_path_norm)
        command = ["python", absolute_file_path]
        
        if args:
            command.extend(args)

        completed_process = subprocess.run(command,cwd=working_dir_abs, capture_output=True, text =True,  timeout=30)
        
        output_string = ""
        if not completed_process.returncode == 0:
            output_string+= f"Process exited with code {completed_process.returncode}" 
        
        if not completed_process.stdout and not completed_process.stderr:
            output_string += "No output produced"
        
        else:
            output_string += f"STDOUT: {completed_process.stdout}"    
            output_string += f"STDERR: {completed_process.stderr}"
        
        return output_string
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Returns an output string of running a python file in a specified directory relative to the working directory, providing or not arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory where is the file that we are going to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="optional arguments"
                ),
            ),
        },
        required=["file_path"]
    )
)
