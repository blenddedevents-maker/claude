#!/usr/bin/env bash
# Instala todo el kit de edición de imagen, vídeo, audio y 3D.
# Uso: bash herramientas/instalar-media.sh   (idempotente)
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y --no-install-recommends \
  imagemagick graphicsmagick inkscape gimp librsvg2-bin potrace webp libavif-bin libheif-examples \
  optipng pngquant jpegoptim gifsicle libimage-exiftool-perl \
  ffmpeg mediainfo mkvtoolnix handbrake-cli x264 x265 ffmpegthumbnailer \
  sox libsox-fmt-all lame flac opus-tools vorbis-tools rubberband-cli \
  blender xvfb fonts-noto fonts-noto-color-emoji fonts-dejavu fonts-liberation
pip3 install --root-user-action=ignore -q \
  pillow opencv-python-headless scikit-image imageio imageio-ffmpeg numpy scipy matplotlib \
  moviepy ffmpeg-python pydub librosa soundfile pedalboard noisereduce pyloudnorm mutagen \
  "rembg[cpu]" cairosvg svgwrite wand rawpy faster-whisper yt-dlp
npm install -g @remotion/cli sharp-cli svgo
echo "Kit multimedia instalado."
