import json

import requests  # to get image from the web
import shutil  # to save it locally
from os import walk
import os


def download_images(path_fragments, path_saved_images):
    for file in os.listdir(path_fragments):
        with open(os.path.join(path_fragments, file), encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            image_url = data["surface_graphic"]["attribute"]["url"]
            filename = data["titleStmt_title"]
            r = requests.get(image_url, stream=True)

            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True

                # Open a local file with wb ( write binary ) permission.
                with open(os.path.join(path_saved_images, filename+".jpg"), 'wb') as f:
                    shutil.copyfileobj(r.raw, f)


download_images(r"C:\Users\schep\Documents\GitHub\Tocharian-Deep-Learning\data\fragments_zone",
                r"C:\Users\schep\Documents\GitHub\Tocharian-Deep-Learning\data\images")
