import os
import json


FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-2026-08-03-git-01a25f74cc-essentials_build\bin\ffmpeg.exe"
os.environ["IMAGEIO_FFMPEG_EXE"] = FFMPEG_PATH

from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

def load_edl(edl_path="sample_edl.json"):
    if os.path.exists(edl_path):
        with open(edl_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"error: cannot find document {edl_path}")
        return []

def run_pipeline():
    edl_data = load_edl()
    if not edl_data:
        return

    clips = []
    
    
    for item in edl_data:
        video_path = item.get("camera")
        if not video_path or not os.path.exists(video_path):
            print(f"Warning: cannot find document {video_path}，skip.")
            continue
            
        print(f"正在处理: {video_path} ({item['start']}s - {item['end']}s)...")
        clip = VideoFileClip(video_path).subclipped(item["start"], item["end"])
        
        
        txt_clip = TextClip(
            text=f"Cam: {video_path} | {item.get('action', '')}", 
            font_size=24, 
            color='white', 
            bg_color='black'
        ).with_position(('left', 'bottom')).with_duration(clip.duration)
        
        composite = CompositeVideoClip([clip, txt_clip])
        clips.append(composite)
    
    if not clips:
        print("No synthesizable fragments，Please check the video file name.")
        return

    
    print("Generating end credits (Closing Credits)...")
    credits_text = TextClip(
        text="BTIS3053 Project\nMulti-Camera AI Video Pipeline\nThank You For Watching!", 
        font_size=36, 
        color='gold', 
        bg_color='black',
        size=(clips[0].w, clips[0].h)
    ).with_duration(5)
    
    clips.append(credits_text)

   
    print("Rendering and exporting in 3 minutes final_graduation_video.mp4...")
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile("final_graduation_video.mp4", fps=30, codec="libx264")
    print("\n✅ Rendering successful! The exported 3-minute full video is: final_graduation_video.mp4[cite: 1, 2]")

if __name__ == "__main__":
    run_pipeline()