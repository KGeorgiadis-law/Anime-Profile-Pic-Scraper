import shutil
import urllib
import os
from concurrent.futures import ThreadPoolExecutor

save_dir = os.path.dirname(os.path.realpath(__file__))
print("root saving directory", save_dir)
def save_image(image_url, image_dest):
   urllib.urlretrieve(image_url, image_dest)

def check_folder(folder_dir):
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)

def save_multiple_images(url_to_folder_dict):
    with ThreadPoolExecutor(max_workers=10) as e:
        for key in url_to_folder_dict.keys():
            folder_name = os.path.join(save_dir, url_to_folder_dict[key])
            check_folder(folder_name)
            image_name = os.path.join(folder_name, key.split("/")[-1], ".jpeg")
            e.submit(save_image, key, image_name)

