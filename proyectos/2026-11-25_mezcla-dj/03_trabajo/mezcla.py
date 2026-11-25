"""Mezcla DJ: A (melodia silbada 25-11-2026) -> B (Las Munequitas, 100 BPM).

Uso: python3 mezcla.py <version>   (ej. v01)
Requiere ffmpeg con rubberband, librosa, scipy, soundfile, pyloudnorm.
"""
import subprocess, sys, os
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, sosfilt, sosfiltfilt

VER = sys.argv[1] if len(sys.argv) > 1 else "v01"
HERE = os.path.dirname(os.path.abspath(__file__))
ENT = os.path.join(HERE, "..", "02_assets", "entrada")
OUT = os.path.join(HERE, "..", "04_salidas", "borradores")
TMP = os.path.join(HERE, "tmp"); os.makedirs(TMP, exist_ok=True)
SR = 44100

# --- parametros medidos (ver LOG.md) ---------------------------------------
B_BPM, B_DOWNBEAT = 100.0, 2.276          # primer golpe de B
BEAT = 60 / B_BPM
A_TUNE_ST = 0.23                           # A esta -23 cents -> afinar a 440
A_SPLIT = 17.85                            # silencio entre frase 3 y 4 de A
A_P4_FIRST, A_P4_LAST = 18.00, 20.72       # 1a nota (La) y nota final (Fa) frase 4
R = (4 * BEAT) / (A_P4_LAST - A_P4_FIRST)  # factor duracion -> 4 negras a 100 BPM


def ff(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def load(p):
    y, sr = sf.read(p, always_2d=True); assert sr == SR; return y.T.astype(np.float64)


def db(x): return 10 ** (x / 20)


# --- 1. preparar A: limpieza + afinacion + time-stretch frase 4 ------------
src_a = os.path.join(ENT, "cancion-a_25-11-2026.m4a")
pitch = 2 ** (A_TUNE_ST / 12)
clean = "highpass=f=250,afftdn=nf=-30:nr=12,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=2"
ff(["-i", src_a, "-t", str(A_SPLIT), "-af",
    f"{clean},rubberband=pitch={pitch}:pitchq=quality:formant=preserved", "-ar", str(SR), "-ac", "2",
    f"{TMP}/a1.wav"])
ff(["-ss", str(A_SPLIT), "-i", src_a, "-af",
    f"{clean},rubberband=tempo={1/R}:pitch={pitch}:pitchq=quality:formant=preserved:transients=smooth",
    "-ar", str(SR), "-ac", "2", f"{TMP}/a2.wav"])
ff(["-i", os.path.join(ENT, "cancion-b_las-munequitas.mp3"), "-map", "0:a", "-ar", str(SR), "-ac", "2",
    f"{TMP}/b.wav"])

a1, a2, b = load(f"{TMP}/a1.wav"), load(f"{TMP}/a2.wav"), load(f"{TMP}/b.wav")
n_split = int(A_SPLIT * SR)
a1 = a1[:, :n_split]
fade = int(0.02 * SR)                      # micro-fundidos anti-click en el corte
a1[:, -fade:] *= np.linspace(1, 0, fade); a2[:, :fade] *= np.linspace(0, 1, fade)
a = np.concatenate([a1, a2], axis=1)

# tiempos en la linea de salida
T1 = A_SPLIT + (A_P4_FIRST - A_SPLIT) * R    # La de la frase 4 = compas 1 de B
T_DROP = T1 + 4 * BEAT                       # Fa final = compas 2 de B (bass drop)
B_START = T1 - B_DOWNBEAT
print(f"R={R:.4f}  T1={T1:.3f}s  drop={T_DROP:.3f}s  B entra en {B_START:.3f}s")

# --- 2. igualar sonoridad A vs B -------------------------------------------
meter = pyln.Meter(SR)
lb = meter.integrated_loudness(b[:, int(20 * SR):int(120 * SR)].T)
la = meter.integrated_loudness(a.T)
a *= db(lb - 1.5 - la)                      # A 1.5 dB por debajo del cuerpo de B
print(f"LUFS B={lb:.1f}  A={la:.1f} -> {lb-1.5:.1f}")

# --- 3. reverb de convolucion suave para A (sala ~1.4 s) --------------------
rng = np.random.default_rng(7)
ir_len = int(1.4 * SR); t = np.arange(ir_len) / SR
ir = rng.standard_normal((2, ir_len)) * np.exp(-t / 0.32)
ir = sosfilt(butter(2, [300, 6000], "band", fs=SR, output="sos"), ir)
ir[:, :int(0.018 * SR)] = 0                 # pre-delay 18 ms
ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
from scipy.signal import fftconvolve
wet = np.stack([fftconvolve(a[c], ir[c]) for c in range(2)])
a = np.pad(a, ((0, 0), (0, wet.shape[1] - a.shape[1])))
a = a + wet * db(-15)

# --- 4. echo-out a 3/4 de beat sobre la nota final de A --------------------
n_drop = int(T_DROP * SR)
env_tail = np.zeros(a.shape[1]); env_tail[n_drop - int(0.05 * SR):] = 1
send = a * env_tail
dly = int(0.75 * BEAT * SR); fb = 0.5
hp_lp = butter(2, [500, 4500], "band", fs=SR, output="sos")
echo = np.zeros((2, a.shape[1] + dly * 10))
tap = send.copy()
for k in range(1, 9):
    tap = sosfilt(hp_lp, tap) * fb
    ch = k % 2                               # ping-pong L/R
    echo[ch, k * dly:k * dly + tap.shape[1]] += tap[ch] + 0.35 * tap[1 - ch]
a = np.pad(a, ((0, 0), (0, echo.shape[1] - a.shape[1]))) + echo * 0.9

# --- 5. B: bass-swap + barrido de filtro ------------------------------------
lp = butter(4, 160, "low", fs=SR, output="sos")
b_low = sosfiltfilt(lp, b); b_high = b - b_low
b_thin = sosfiltfilt(butter(2, 900, "high", fs=SR, output="sos"), b_high)

total = int(B_START * SR) + b.shape[1]
mix = np.zeros((2, total))
mix[:, :min(a.shape[1], total)] += a[:, :total]

nb = b.shape[1]; tb = (np.arange(nb) / SR) + B_START       # tiempo de salida de cada muestra de B


def ramp(t, t0, t1, v0, v1):
    return np.clip(v0 + (v1 - v0) * (t - t0) / (t1 - t0), min(v0, v1), max(v0, v1))


# entrada de B: volumen sube desde B_START, filtro HP se abre hasta el drop
g_in = ramp(tb, B_START, T1, db(-24), db(-5))
g_in = np.where(tb >= T1, ramp(tb, T1, T_DROP, db(-5), 1.0), g_in)
open_ = ramp(tb, B_START, T_DROP, 0.0, 1.0) ** 2            # 0 = filtrado, 1 = abierto
highs = open_ * b_high + (1 - open_) * b_thin
bass = ramp(tb, T_DROP - 0.01, T_DROP + 0.01, 0.0, 1.0)   # bass swap en el Fa final
b_proc = (highs + b_low * bass) * g_in
s = int(B_START * SR)
mix[:, s:s + nb] += b_proc

# --- 6. master: limitador simple (true-peak -1 dBTP) + loudness -------------
mix *= db(-1.0)
ff_in = f"{TMP}/premaster.wav"; sf.write(ff_in, mix.T, SR, subtype="FLOAT")
name = f"mezcla-dj_25-11-2026_a_las-munequitas_{VER}"
ff(["-i", ff_in, "-af", "alimiter=limit=0.89:attack=5:release=60:level=false",
    "-ar", str(SR), "-c:a", "pcm_s24le", f"{OUT}/{name}.wav"])
ff(["-i", f"{OUT}/{name}.wav", "-c:a", "libmp3lame", "-b:a", "320k",
    "-metadata", f"title=Mezcla DJ {VER}", f"{OUT}/{name}.mp3"])
print("OK", f"{OUT}/{name}.wav")
