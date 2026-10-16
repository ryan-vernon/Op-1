#!/usr/bin/env bash
# Downloads the OP-School playlist (audio as stereo wav, captions, and small video for synth/drum/mixer).
# The Mac's Python 3.9 is too old for current yt-dlp, so use uv's Python 3.12:
#   python3 -m pip install --user uv numpy scipy matplotlib imageio-ffmpeg && uv tool install --python 3.12 yt-dlp
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
FF=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
OUT="${1:-opschool}"; mkdir -p "$OUT/stereo" "$OUT/video"
PL="https://www.youtube.com/playlist?list=PLKw0bc1wG1add_Q3TL-ymU7z1rPLz3ron"
yt-dlp -q --ffmpeg-location "$FF" --skip-download --write-auto-subs --sub-langs en --sub-format vtt -o "$OUT/stereo/%(playlist_index)s_%(id)s.%(ext)s" "$PL"
yt-dlp -q --ffmpeg-location "$FF" -x --audio-format wav --postprocessor-args "ffmpeg:-ar 44100 -ac 2" -o "$OUT/stereo/%(playlist_index)s_%(id)s.%(ext)s" "$PL"
yt-dlp -q --ffmpeg-location "$FF" -f "bv*[height<=480]" --playlist-items 2,3,5 -o "$OUT/video/%(playlist_index)s_%(id)s.%(ext)s" "$PL"
