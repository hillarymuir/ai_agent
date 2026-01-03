# functions/get_file_content.py

import os
from google.genai import types

# get config
import sys
sys.path.append("..")
# pylint: disable=wrong-import-position
from ai_agent.config import MAX_CHARS
# pylint: enable=wrong-import-position

def get_file_content(working_directory, file_path):
    # get full path of target file and confirm it is within permitted scope
    # and indeed is a file
    working_dir_abs_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    if os.path.commonpath([working_dir_abs_path, target_file]) != working_dir_abs_path:
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.isfile(target_file):
        return f"Error: File not found or is not a regular file:\"{file_path}"
    
    # open and read file
    with open(target_file, "r") as f:
        file_content_str = f.read(MAX_CHARS)
        if f.read(1):
            file_content_str += f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"

    # return file contents as a string
    return file_content_str

    # TODO: implement try/catch exception handling

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="""
    Read contents of a file located at a particular file path in the working directory
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be read, relative to the working directory",
            ),
        },
    ),
)