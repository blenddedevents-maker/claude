#!/usr/bin/env bash
# Resumable renderer: worker K of N renders 25-frame chunks into OUT/chunks, skipping finished ones.
# usage: render_chunks.sh OUT WORKER NWORKERS [W H]
OUT=$1; K=$2; NW=$3; W=${4:-3840}; H=${5:-2160}; CH=25; mkdir -p "$OUT/chunks"
cd "$(dirname "$0")/.."
for ((s=K*CH; s<900; s+=NW*CH)); do
  f=$OUT/chunks/c_$(printf %04d $s).mkv
  n=$(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 "$f" 2>/dev/null)
  [ "$n" = "$CH" ] && continue
  for try in 1 2 3; do
    OUTFILE=$f.tmp.mkv node src/render.mjs $W $H 60 15 "$OUT" $s $CH 2>&1 | grep -E "^frame|^done|Error" | tail -2
    n=$(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 "$f.tmp.mkv" 2>/dev/null)
    [ "$n" = "$CH" ] && { mv "$f.tmp.mkv" "$f"; echo "chunk $s ok"; break; }
    echo "chunk $s retry $try"
  done
done
echo "worker $K finished"
