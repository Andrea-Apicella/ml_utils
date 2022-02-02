import shutil
import os

source = "./urfd_folders/"
destination = "./urfd_folders/"
subfolders_names = os.listdir(source)
for subfolder_name in subfolders_names:
    if not subfolder_name.startswith('.'):
        subfolder_path = source + subfolder_name + '/'
        images_names = os.listdir(subfolder_path)
        for image_name in images_names:
            if not image_name.startswith('.'):
                print(subfolder_path + image_name)
                shutil.move(subfolder_path + image_name, destination)
                print('moving {}'.format(image_name))
