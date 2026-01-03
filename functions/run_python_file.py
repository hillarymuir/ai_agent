# functions/run_python_file.py

import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        # get full path of target file
        working_dir_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

        # checks: if file_path is outside working_directory, if file_path points to
        # an existing directory as opposed to a file, if file is a .py
        if os.path.commonpath([working_dir_abs_path, target_file]) != working_dir_abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        # build command to run
        command = ["python", target_file]
        if args:
            command.extend(args)

        # use subprocess to run file
        completed_process = subprocess.run(command, 
            cwd=os.path.dirname(target_file),
            capture_output=True,
            text=True,
            timeout=30)
        
        print(completed_process) #debug

        # build and return output string based on completed_process object
        output_str = "Process results:"
        if completed_process.returncode != 0:
            output_str += f"\nProcess exited with code {completed_process.returncode}"
        if not completed_process.stdout and not completed_process.stderr:
            output_str += "\nNo output produced"
        else:
            if completed_process.stdout:
                output_str += f"\nSTDOUT: {completed_process.stdout}"
            if completed_process.stderr:
                output_str += f"\nSTDERR: {completed_process.stderr}"
        return output_str
    
    # TODO: more specific exception handling
    except Exception as e:
        return f"Error executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="""
    Runs a python file located at the file path relative to the given working directory
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional keyword argument for an array of additional arguments for input into the python file being run",
                items=types.Schema(
                    type = types.Type.STRING,
                    description="a single argument to pass to the Python file"
                )
                
            ),
        },
    ),
)