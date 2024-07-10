import cv2
import os


def make_video_from_png(folder_path, output_video_path, fps=24):
    # Get the list of PNG files in the specified folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    # Sort files in alphabetical order
    files.sort()

    # Get dimensions of the first image assuming all images are the same size
    img = cv2.imread(os.path.join(folder_path, files[0]))
    height, width, _ = img.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Iterate through images and write to video file
    for filename in files:
        img = cv2.imread(os.path.join(folder_path, filename))
        out.write(img)  # Write out frame to video

    # Release everything if job is finished
    out.release()


# Example usage:
folder_path = r'X:\VFX\sgn\shot\JJW_BS_001\stablediffusion\out'
output_video_path = r'X:\VFX\sgn\shot\JJW_BS_001\stablediffusion\out\output.mp4'
make_video_from_png(folder_path, output_video_path)