
import os
from natsort import natsorted
import glob


def listdir_nohidden_sorted(path):
    return natsorted(glob.glob(os.path.join(path, '*')))


def safe_mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def extract_frames(video_path, frame_name, frame_format, dest):
    import cv2
    capture = cv2.VideoCapture(video_path)
    count = 1
    safe_mkdir(dest)

    while True:
        success, frame = capture.read()
        if not success:
            break

        safe_mkdir(dest)
        file = f'{dest}/{frame_name}{str(count).zfill(6)}.{frame_format}'
        if not os.path.exists(file):
            cv2.imwrite(file, frame)
            print(f'extracting {file} to {dest} --- {count} frames moved.')
        else:
            print('file already exists.')
        count += 1


def ef_v2(video_path, frame_name, frame_format, dest):
    import cv2
    from tqdm import trange
    capture = cv2.VideoCapture(video_path)
    count = 1
    safe_mkdir(dest)
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'Found {total} frames in the video.')

    for _ in (t := trange(total)):
        success, frame = capture.read()
        if not success:
            break
        safe_mkdir(dest)
        file = f'{dest}/{frame_name}{str(count).zfill(6)}.{frame_format}'
        if not os.path.exists(file):
            cv2.imwrite(file, frame)
            # print(f'extracting {file} to {dest} --- {count} frames moved.')
        else:
            print('file already exists.')
        count += 1
        t.set_description(f'Extracting frame {count}')
