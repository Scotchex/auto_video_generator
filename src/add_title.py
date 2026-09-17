import datetime

def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_srt(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def shift_time(time_str, delta):
    """Shift the time in 'HH:MM:SS,ms' format by the specified delta (in seconds)."""
    time_format = "%H:%M:%S,%f"
    time_obj = datetime.datetime.strptime(time_str, time_format)
    shifted_time = time_obj + datetime.timedelta(seconds=delta)
    return shifted_time.strftime(time_format)[:-3]  # Remove microseconds part

def add_title_and_shift_subtitles(title_text, srt_file = "/Users/arda/Desktop/Projects/money_maker/src/subtitles.srt", title_duration=3, shift_seconds=0):
    lines = read_srt(srt_file)
    new_lines = []
    
    # Insert the title as the first subtitle
    title_entry = [
        "1\n",
        f"00:00:00,000 --> 00:00:{str(title_duration).zfill(2)},000\n",
        f"{title_text}\n\n"
    ]
    new_lines.extend(title_entry)
    
    # Process existing subtitles, shift them by the specified seconds
    subtitle_index = 2  # Start with subtitle number 2 since title is number 1
    
    for i in range(0, len(lines), 4):  # Each subtitle has 4 lines (index, timestamp, text, newline)
        if len(lines[i].strip()) == 0:
            continue  # Skip empty lines
        
        # Subtitle index
        new_lines.append(f"{subtitle_index}\n")
        subtitle_index += 1
        
        # Shift time
        start_time, end_time = lines[i+1].strip().split(" --> ")
        new_start_time = shift_time(start_time, title_duration + shift_seconds)
        new_end_time = shift_time(end_time, title_duration + shift_seconds)
        new_lines.append(f"{new_start_time} --> {new_end_time}\n")
        
        # Subtitle text
        new_lines.append(lines[i+2])  # Keep the subtitle text the same
        
        # Add newline after each subtitle entry
        new_lines.append("\n")
    
    # Write the modified subtitles to a new file
    write_srt(srt_file, new_lines)
