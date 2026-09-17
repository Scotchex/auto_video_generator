import ffmpeg

def add_subtitles(video_file="/Users/arda/Desktop/Projects/money_maker/src/output_video_with_audio.mp4", 
                  srt_file = "/Users/arda/Desktop/Projects/money_maker/src/subtitles.srt", 
                  output_file = "/Users/arda/Desktop/Projects/money_maker/outputs/output.mp4"):

    subtitle_style = (
        f"subtitles={srt_file}:force_style="
        "'FontName=KomikaAxis,FontSize=16,PrimaryColour=&H00FFFFFF&,BorderStyle=1,"
        "OutlineColour=&H00000000&,BackColour=&H00000000&,Alignment=2,MarginV=130,"
        "Outline=2,Shadow=2,FadeIn=500,FadeOut=500,Karaoke=1'"
    )

    (
        ffmpeg
        .input(video_file)
        .output(output_file, vf=subtitle_style)
        .run()
    )
