# functions/write_file.py

import os

def write_file(working_directory, file_path, content):
    # get full path of target file
    working_dir_abs_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

    # checks: if file_path is outside working_directory, if file_path points to
    # an existing directory as opposed to a file
    if os.path.commonpath([working_dir_abs_path, target_file]) != working_dir_abs_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    # make sure all parent directories of file_path exist
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    # open and overwrite contents of file
    with open(target_file, "w+") as f:
        f.write(content)

    # return success string
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'