import subprocess
import re
import argparse


def detect_silence(input_file, silence_log, silence_level, silence_duration):
    silence_params = f"n=-{silence_level}dB:d={silence_duration}"
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_file,
        "-af",
        f"silencedetect={silence_params}",
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


def generate_ffmpeg_command(
    input_file,
    output_file,
    silence_intervals,
    video_duration,
    video_codec,
    video_bitrate,
    video_preset,
    video_profile,
    audio_codec,
    audio_bitrate,
    audio_sample_rate,
):
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
        video_codec,
        "-b:v",
        video_bitrate,
        "-preset",
        video_preset,
        "-profile:v",
        video_profile,  # Video encoding settings
        "-c:a",
        audio_codec,
        "-b:a",
        audio_bitrate,
        "-ar",
        audio_sample_rate,  # Audio encoding settings
        output_file,
    ]
    return ffmpeg_command


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Remove silent moments from a video.")
    parser.add_argument("-i", "--input", required=True, help="The input video file.")
    parser.add_argument("-o", "--output", required=True, help="The output video file.")
    parser.add_argument(
        "-vc",
        "--video_codec",
        default="libx264",
        help="The video codec (default: libx264).",
    )
    parser.add_argument(
        "-vb",
        "--video_bitrate",
        default="8m",
        help="The video bitrate (default: 8m).",
    )
    parser.add_argument(
        "-vp",
        "--video_preset",
        default="medium",
        help="The video preset (default: medium).",
    )
    parser.add_argument(
        "-vpr",
        "--video_profile",
        default="high",
        help="The video profile (default: high).",
    )
    parser.add_argument(
        "-ac", "--audio_codec", default="aac", help="The audio codec (default: aac)."
    )
    parser.add_argument(
        "-ab",
        "--audio_bitrate",
        default="128k",
        help="The audio bitrate (default: 128k).",
    )
    parser.add_argument(
        "-asr",
        "--audio_sample_rate",
        default="48000",
        help="The audio sample rate (default: 48000).",
    )
    parser.add_argument(
        "-sl",
        "--silence_level",
        type=int,
        default=30,
        help="The silence detection level in dB (default: 30).",
    )
    parser.add_argument(
        "-sd",
        "--silence_duration",
        type=float,
        default=0.5,
        help="The silence detection duration in seconds (default: 0.5).",
    )
    args = parser.parse_args()

    # Assign arguments to variables
    input_file = args.input
    output_file = args.output
    video_codec = args.video_codec
    video_bitrate = args.video_bitrate
    video_preset = args.video_preset
    video_profile = args.video_profile
    audio_codec = args.audio_codec
    audio_bitrate = args.audio_bitrate
    audio_sample_rate = args.audio_sample_rate
    silence_level = args.silence_level
    silence_duration = args.silence_duration

    silence_log = "silence_log.txt"

    # Step 1: Detect silence and generate log
    detect_silence(input_file, silence_log, silence_level, silence_duration)

    # Step 2: Parse the silence log to get silence intervals
    silence_intervals = parse_silence_log(silence_log)

    # Step 3: Get video duration
    video_duration = get_video_duration(input_file)

    # Step 4: Generate FFmpeg command to trim silence
    ffmpeg_command = generate_ffmpeg_command(
        input_file,
        output_file,
        silence_intervals,
        video_duration,
        video_codec,
        video_bitrate,
        video_preset,
        video_profile,
        audio_codec,
        audio_bitrate,
        audio_sample_rate,
    )

    # Step 5: Execute the FFmpeg command
    subprocess.run(ffmpeg_command)


if __name__ == "__main__":
    main()
