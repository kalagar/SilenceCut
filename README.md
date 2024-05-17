# SilenceCut

* SilenceCut is a simple tool to remove silence from video files.
* It's a simple wrapper around ffmpeg.
* It's written in Python and uses the `ffmpeg-python` library.
* It's a command line tool.

## Installation

```bash
brew install python3
```

```bash
brew install ffmpeg
```

## Usage

```bash
python3 silencecut.py -i '<path_to_input_file>' -o '<path_to_output_file>'
```

## Options
<!-- implement same as main() -->
`-i` or `--input` : Path to the input video file. (*Required*)

`-o` or `--output` : Path to the output video file. (*Required*)

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

 1. Video Codec: libx264
 2. Video Bitrate: Depending on the resolution and frame rate, YouTube recommends:
    * 1080p at 30fps: 8 Mbps
    * 1080p at 60fps: 12 Mbps
    * 1440p at 30fps: 16 Mbps
    * 1440p at 60fps: 24 Mbps
    * 2160p at 30fps: 35-45 Mbps
    * 2160p at 60fps: 53-68 Mbps
 3. Video Preset: medium (for a balance between encoding speed and quality)
 4. Video Profile: high
 5. Audio Codec: aac
 6. Audio Bitrate: 128 kbps or higher (e.g., 192 kbps or 256 kbps for better quality)
 7. Audio Sample Rate: 48 kHz

### Example Values for 1080p at 30fps

* Video Bitrate: 8M
* Audio Bitrate: 192k
* Silence Level: 40 (depending on the noise level in the video, adjust as needed)
* Silence Duration: 0.5 (to quickly cut out short silent parts)
