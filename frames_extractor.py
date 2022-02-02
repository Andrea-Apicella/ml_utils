import os
from natsort import natsorted
import glob
from pathlib import Path
import cv2
from tqdm import trange
import argparse


def listdir_nohidden_sorted(path):
    return natsorted(glob.glob(os.path.join(path, '*')))


def safe_mkdir(path):
    try:
        os.mkdir(path)
        return path
    except FileExistsError:
        pass


parser = argparse.ArgumentParser()
parser.add_argument('--video_path', type=str, required=True, help='Path of the video to extract frames from')
parser.add_argument('--frame_name', type=str, help='Optional frame name')
parser.add_argument('--frame_format', type=str, help='extracted frames format. jpg or png allowed. Default is png')
parser.add_argument('--dest', type=str, help='optional destination folder. Default is a new folder in the video path')

args = parser.parse_args()

video_name = Path(args.video_path).name
if not args.frame_name:
    dot_index = video_name.find('.')
    frame_name = video_name[:dot_index]
    dest_folder_name = frame_name
else:
    frame_name = args.frame_name

    dot_index = video_name.find('.')
    dest_folder_name = video_name[:dot_index]


if not args.frame_format:
    frame_format = 'png'
else:
    frame_format = args.frame_format

if not args.dest:
    name_index = args.video_path.find(video_name)
    video_dir = args.video_path[:name_index]
    dest = safe_mkdir(f'{video_dir}/{dest_folder_name}_extracted_frames')
else:
    dest = safe_mkdir(args.dest)


def main(video_path=args.video_path, frame_name=frame_name, frame_format=frame_format, dest=dest):
    capture = cv2.VideoCapture(video_path)
    count = 1
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'Found {total} frames in the video.')

    for _ in (t := trange(total)):
        success, frame = capture.read()
        if not success:
            break
        file = f'{dest}/{frame_name}_{str(count).zfill(len(str(total)))}.{frame_format}'
        if not os.path.exists(file):
            cv2.imwrite(file, frame)
            # print(f'extracting {file} to {dest} --- {count} frames moved.')
        else:
            print('file already exists.')
        count += 1
        t.set_description(f'Extracting frame {count}')


if __name__ == "__main__":
    main()
