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
`-i` or `--input` : Path to the input video file. (Required)

`-o` or `--output` : Path to the output video file. (Required)

`-sl` or `--silence_level` : Silence level in dB. (Optional, default: `50`)

`-sd` or `--silence_duration` : Silence duration in seconds. (Optional, default: `2`)

`-vc` or `--video_codec` : Video codec. (Optional, default: 'libx264')

`-vb` or `--video_bitrate` : Video bitrate. (Optional, default: '19681k')

`-vp` or `--video_preset` : Video preset. (Optional, default: 'medium')

`-vpr` or `--video_profile` : Video profile. (Optional, default: 'high')

`-ac` or `--audio_codec` : Audio codec. (Optional, default: 'aac')

`-ab` or `--audio_bitrate` : Audio bitrate. (Optional, default: '128k')

`-asr` or `--audio_sample_rate` : Audio sample rate. (Optional, default: 48000)
