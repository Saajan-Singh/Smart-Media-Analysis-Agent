import os
import cv2
from src import MEDIA_DIR

def extract_frames(video_path: str, interval_seconds: int = 3) -> list[str]:
    """
    Extract frames from a video file at a specified interval.

    Args:
        video_path: The absolute path to the video file.
        interval_seconds: How many seconds between each extracted frame.

    Returns:
        A list of filenames (just the names, not full paths) of the extracted frames.
    """
    if not os.path.exists(video_path):
        print(f"[video_utils] Error: Video file not found at {video_path}")
        return []

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[video_utils] Error: Could not open video file {video_path}")
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30  # Fallback just in case fps is not readable

    frame_skip = int(fps * interval_seconds)
    
    # We want to name frames using the original video filename stem
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    extracted_filenames = []
    frame_idx = 0
    saved_idx = 1
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_idx % frame_skip == 0:
            frame_filename = f"{base_name}_frame_{saved_idx:03d}.jpg"
            save_path = os.path.join(MEDIA_DIR, frame_filename)
            cv2.imwrite(save_path, frame)
            extracted_filenames.append(frame_filename)
            saved_idx += 1
            
        frame_idx += 1
        
    cap.release()
    print(f"[video_utils] Extracted {len(extracted_filenames)} frames from {base_name}")
    return extracted_filenames
