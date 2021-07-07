from fastapi import Response
import os
from zipfile import ZipFile
import zipfile
import io
from typing import List
import random
import time
import fastapi as _fastapi

def get_all_file_paths(directory):

    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths

def zip_files(directory_name):
    # path to folder which needs to be zipped
    directory = f'./{directory_name}'

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)

    # printing the list of all files to be zipped
    print('Following files will be zipped:')
    for file_name in file_paths:
        print(file_name)

    # writing files to a zipfile
    zip_io = io.BytesIO()
    with ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)

    print('All files zipped successfully!')

    res = Response(zip_io.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={directory_name}.zip'
    })

    return res

def _get_image_filenames(directory_name: str) -> List[str]:
    return os.listdir(directory_name)

def get_random_meme(directory_name: str) -> str:
    images = _get_image_filenames(directory_name)
    random_image = random.choice(images)
    path = f'{directory_name}/{random_image}'
    return path

def _is_image(filename: str):
    valid_extensions = (".png", ".jpg", ".jpeg", ".gif")
    return filename.endswith(valid_extensions)

def upload_image(directory_name: str, image: _fastapi.UploadFile):
    if _is_image(image.filename):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        image_name = timestr + image.filename.replace(" ", "-")
        with open(f"{directory_name}/{image_name}", "wb+") as image_upload:
            image_upload.write(image.file.read())

        return f"{directory_name}/{image_name}"

    return None