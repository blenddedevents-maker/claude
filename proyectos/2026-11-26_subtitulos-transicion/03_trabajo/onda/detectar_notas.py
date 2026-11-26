"""Detecta notas (polifónico, aproximado) de un WAV con CQT y las guarda en JSON: [inicio, fin, midi, intensidad]."""
import sys, json, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
hop = 256
C = np.abs(librosa.cqt(y, sr=sr, hop_length=hop, fmin=librosa.note_to_hz("C2"), n_bins=72, bins_per_octave=12))
Cdb = librosa.amplitude_to_db(C, ref=np.max)
T = C.shape[1]; t = librosa.frames_to_time(np.arange(T), sr=sr, hop_length=hop)
act = np.zeros_like(Cdb, bool)
for j in range(T):
    col = Cdb[:, j]; m = col.max()
    pk = [i for i in range(1, 71) if col[i] >= col[i-1] and col[i] >= col[i+1] and col[i] > m - 14 and col[i] > -45]
    for i in pk: act[i, j] = True
onset = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop, units="frames", backtrack=True)
ons = set(onset.tolist())
notes = []
for i in range(72):
    j = 0
    while j < T:
        if act[i, j]:
            k = j
            while k + 1 < T and (act[i, k+1] or (k + 2 < T and act[i, k+2])) and (k + 1 not in ons or k + 1 == j):
                k += 1
            d = t[k] - t[j]
            if d >= 0.07:
                notes.append([round(float(t[j]), 3), round(float(t[k] + hop / sr), 3), 36 + i, round(float(Cdb[i, j:k+1].mean()), 1)])
            j = k + 1
        else:
            j += 1
notes.sort()
json.dump(notes, open(sys.argv[2], "w"))
print(len(notes), "notas; rango midi", min(n[2] for n in notes), max(n[2] for n in notes))
from collections import Counter
print(Counter(n[2] for n in notes).most_common(15))
print(notes[:25])
