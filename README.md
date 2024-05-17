# SilenceCut

* SilenceCut is a simple tool to remove silence from video files.
* It's a simple wrapper around FFmpeg.
* It's written in Python and uses the `ffmpeg-python` library.
* It's a command line tool.

## Prerequisites

* Python 3.x
* FFmpeg

## Installation

### macOS (using Homebrew)

```bash
brew install python3
brew install ffmpeg
```

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
```

### Windows

1. Install [Python 3](https://www.python.org/downloads/).
2. Install [FFmpeg](https://ffmpeg.org/download.html) and add it to your system PATH. use this [guide](https://www.wikihow.com/Install-FFmpeg-on-Windows).

### Install Python dependencies

```bash
pip install ffmpeg-python
```

## Usage

```bash
python3 silencecut.py -i '<path_to_input_file>' -o '<path_to_output_file>'
```

### Example

```bash
python3 silencecut.py -i ~/Desktop/input.mp4 -o ~/Desktop/output.mp4 --video_codec libx264 --video_bitrate 8M --video_preset medium --video_profile high --audio_codec aac --audio_bitrate 128k --audio_sample_rate 48000 --silence_level 30 --silence_duration 0.5
```

## Options

`-i` or `--input` : Path to the input video file. (***Required***)

`-o` or `--output` : Path to the output video file. (***Required***)

`-sl` or `--silence_level` : Silence level in dB. (*Optional*, default: `30`)

`-sd` or `--silence_duration` : Silence duration in seconds. (*Optional*, default: `0.5`)

`-vc` or `--video_codec` : Video codec. (*Optional*, default: `libx264`)

`-vb` or `--video_bitrate` : Video bitrate. (*Optional*, default: `8m`)

`-vp` or `--video_preset` : Video preset. (*Optional*, default: `medium`)

`-vpr` or `--video_profile` : Video profile. (*Optional*, default: `high`)

`-ac` or `--audio_codec` : Audio codec. (*Optional*, default: `aac`)

`-ab` or `--audio_bitrate` : Audio bitrate. (*Optional*, default: `128k`)

`-asr` or `--audio_sample_rate` : Audio sample rate. (*Optional*, default: `48000`)

## Recommended Values for YouTube Videos

1. **Video Codec**: `libx264`
2. **Video Bitrate**: Depending on the resolution and frame rate, YouTube recommends:
   * 1080p at 30fps: 8 Mbps
   * 1080p at 60fps: 12 Mbps
   * 1440p at 30fps: 16 Mbps
   * 1440p at 60fps: 24 Mbps
   * 2160p at 30fps: 35-45 Mbps
   * 2160p at 60fps: 53-68 Mbps
3. **Video Preset**: `medium` (for a balance between encoding speed and quality)
4. **Video Profile**: `high`
5. **Audio Codec**: `aac`
6. **Audio Bitrate**: 128 kbps or higher (e.g., 192 kbps or 256 kbps for better quality)
7. **Audio Sample Rate**: 48 kHz

### Example Values for 1080p at 30fps

* **Video Bitrate**: `8M`
* **Audio Bitrate**: `192k`
* **Silence Level**: `40` (depending on the noise level in the video, adjust as needed)
* **Silence Duration**: `0.5` (to quickly cut out short silent parts)

## Error Handling

If you encounter issues, check the following:

1. **FFmpeg Not Found**: Ensure FFmpeg is installed and added to your system PATH.
2. **Permission Denied**: Ensure you have permission to read the input file and write to the output file's location.
3. **Invalid Input**: Ensure the input file path and format are correct.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
