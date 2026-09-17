import whisper

def transcribe():
    # Load the Whisper model
    model = whisper.load_model("medium.en")

    # Transcribe the audio
    result = model.transcribe("src/audio.mp3", task="transcribe")

    # Function to split text into chunks with limited words per line
    def split_text_by_words(text, max_words=3):
        words = text.split()
        return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

    # Function to generate .srt content with limited words per subtitle and correct timestamps
    def generate_srt(transcription, max_words_per_line=8):
        srt_content = ""
        subtitle_counter = 1

        for segment in transcription['segments']:
            # Get start and end times of the segment
            segment_start = segment['start']
            segment_end = segment['end']
            segment_duration = segment_end - segment_start
            
            # Split the text into smaller lines
            lines = split_text_by_words(segment['text'], max_words_per_line)

            # Calculate duration for each line
            line_duration = segment_duration / len(lines)

            for i, line in enumerate(lines):
                # Calculate start and end time for the current line
                start_time = format_timestamp(segment_start + i * line_duration)
                end_time = format_timestamp(segment_start + (i + 1) * line_duration)

                # Add subtitle number
                srt_content += f"{subtitle_counter}\n"
                
                # Add time range in SRT format
                srt_content += f"{start_time} --> {end_time}\n"
                
                # Add the transcription text for the current line
                srt_content += f"{line}\n\n"
                
                # Increment subtitle counter
                subtitle_counter += 1

        return srt_content

    # Helper function to format timestamps for SRT (hours, minutes, seconds, milliseconds)
    def format_timestamp(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds * 1000) % 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

    # Generate SRT content with shorter lines and correct timestamps
    srt_content = generate_srt(result, max_words_per_line=5)

    # Write the SRT content to a file
    with open("src/subtitles.srt", "w") as srt_file:
        srt_file.write(srt_content)

    print("SRT file with correct timestamps and limited words per line has been created: output_subtitles.srt")
