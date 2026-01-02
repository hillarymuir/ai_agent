# functions/get_files_info.py

import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    # get full path of target directory and confirm it is within permitted scope
    # and indeed is a directory
    working_dir_abs_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))
    if os.path.commonpath([working_dir_abs_path, target_dir]) != working_dir_abs_path:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    if not os.path.isdir(target_dir):
        return f"Error: \"{directory} is not a directory"
    
    # get info on contents of directory
    dir_contents_list = []
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        item_str = f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
        dir_contents_list.append(item_str)
    
    return "\n".join(dir_contents_list)

    # TODO: implement try/catch exception handling

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="""
    Lists files in a specified directory relative to the working directory, providing file size and directory status
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)