import subprocess
import re
import ffmpeg

def get_audio_duration(audio_file):
    result = subprocess.run(
        ['ffmpeg', '-i', audio_file],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    duration_match = re.search(r'Duration: (\d{2}:\d{2}:\d{2}\.\d{2})', result.stderr)
    if duration_match:
        return duration_match.group(1)
    else:
        raise ValueError("Could not determine audio duration.")

def time_to_seconds(time_str):
    """Convert HH:MM:SS.ms to seconds."""
    h, m, s = time_str.split(':')
    seconds, milliseconds = map(float, s.split('.'))
    total_seconds = int(h) * 3600 + int(m) * 60 + seconds + milliseconds / 100
    return total_seconds

def seconds_to_time_str(seconds):
    """Convert seconds to HH:MM:SS.ms format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}"

def trim_video_to_audio_length(video_file, audio_duration, output_file, title_duration):
    # Convert audio duration to seconds
    audio_duration_seconds = time_to_seconds(audio_duration)
    # Trim the video to match the audio length
    trimmed_duration = audio_duration_seconds + title_duration
    trimmed_duration_str = seconds_to_time_str(trimmed_duration)
    
    subprocess.run([
        'ffmpeg', '-i', video_file, '-ss', '0', '-t', trimmed_duration_str, '-c', 'copy', output_file
    ])

def add_silence_to_audio(audio_file, silence_duration, output_file):
    # Create silence audio as a WAV file
    silence_file = 'temp_silence.wav'
    ffmpeg.input('anullsrc=r=44100', f='lavfi', t=silence_duration).output(silence_file).run()
    
    # Concatenate silence and audio
    silence = ffmpeg.input(silence_file)
    audio = ffmpeg.input(audio_file)
    
    # Concatenate them and output to a new audio file
    ffmpeg.concat(silence, audio, v=0, a=1).output(output_file).run()

def combine_video_and_audio(video_file, audio_file, output_file):
    input_video = ffmpeg.input(video_file)
    input_audio = ffmpeg.input(audio_file)
    
    # Combine the video and the full audio
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_file).run()

def combine():
    audio_file = 'src/audio.mp3'  # Replace with your audio file
    video_file = 'src/input.mp4'   # Replace with your video file
    trimmed_video_file = 'src/trim_vid.mp4'  # Output trimmed video file name
    output_file = 'src/output_video_with_audio.mp4'  # Final output file name
    
    title_duration = 3  # Duration of title display (in seconds)
    
    try:
        # Get the audio duration
        audio_duration = get_audio_duration(audio_file)
        print(f"Audio Duration: {audio_duration}")
        
        # Trim the video to match audio length plus title duration
        trim_video_to_audio_length(video_file, audio_duration, trimmed_video_file, title_duration)
        print(f"Trimmed video saved as: {trimmed_video_file}")
        
        # Create a new audio file with silence at the beginning
        audio_with_silence_file = 'src/audio_with_silence.mp3'
        add_silence_to_audio(audio_file, title_duration, audio_with_silence_file)
        
        # Combine the trimmed video and the audio with silence
        combine_video_and_audio(trimmed_video_file, audio_with_silence_file, output_file)
        
        
    except Exception as e:
        print(f"An error occurred: {e}")

