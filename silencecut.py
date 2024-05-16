import subprocess
import re
import argparse


def detect_silence(input_file, silence_log):
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_file,
        "-af",
        "silencedetect=n=-20dB:d=1",
        "-f",
        "null",
        "-",
    ]
    with open(silence_log, "w") as log_file:
        subprocess.run(ffmpeg_command, stderr=log_file)


def parse_silence_log(log_file):
    silence_intervals = []
    with open(log_file, "r") as file:
        for line in file:
            start_match = re.search(r"silence_start: (\d+(\.\d+)?)", line)
            end_match = re.search(
                r"silence_end: (\d+(\.\d+)?).*\| silence_duration: (\d+(\.\d+)?)", line
            )
            if start_match:
                start_time = float(start_match.group(1))
            if end_match:
                end_time = float(end_match.group(1))
                silence_intervals.append((start_time, end_time))
    return silence_intervals


def get_video_duration(input_file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            input_file,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return float(result.stdout)


def generate_ffmpeg_command(input_file, output_file, silence_intervals, video_duration):
    if silence_intervals:
        segments = []
        current_position = 0

        for start, end in silence_intervals:
            if current_position < start:
                segments.append(f"between(t,{current_position},{start})")
            current_position = end

        if current_position < video_duration:
            segments.append(f"between(t,{current_position},{video_duration})")

        segments_str = "+".join(segments)
        filter_complex = f"[0:v]select='{segments_str}',setpts=N/FRAME_RATE/TB[v];[0:a]aselect='{segments_str}',asetpts=N/SR/TB[a]"
    else:
        # No silence detected; keep the entire video
        filter_complex = "[0:v]trim=start=0:end={0},setpts=PTS-STARTPTS[v];[0:a]atrim=start=0:end={0},asetpts=PTS-STARTPTS[a]".format(
            video_duration
        )

    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_file,
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-b:v",
        "19681k",
        "-preset",
        "medium",
        "-profile:v",
        "high",  # Match video encoding settings
        "-c:a",
        "aac",
        "-b:a",
        "110k",
        "-ar",
        "48000",  # Match audio encoding settings
        output_file,
    ]
    return ffmpeg_command


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Remove silent moments from a video.")
    parser.add_argument("-i", "--input", required=True, help="The input video file.")
    parser.add_argument("-o", "--output", required=True, help="The output video file.")
    args = parser.parse_args()

    # Assign arguments to variables
    input_file = args.input
    output_file = args.output

    silence_log = "silence_log.txt"

    # Step 1: Detect silence and generate log
    detect_silence(input_file, silence_log)

    # Step 2: Parse the silence log to get silence intervals
    silence_intervals = parse_silence_log(silence_log)

    # Step 3: Get video duration
    video_duration = get_video_duration(input_file)

    # Step 4: Generate FFmpeg command to trim silence
    ffmpeg_command = generate_ffmpeg_command(
        input_file, output_file, silence_intervals, video_duration
    )

    # Step 5: Execute the FFmpeg command
    subprocess.run(ffmpeg_command)


if __name__ == "__main__":
    main()
