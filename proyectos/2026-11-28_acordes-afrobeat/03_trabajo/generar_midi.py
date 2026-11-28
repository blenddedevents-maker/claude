import mido, random
random.seed(7)
BPM, TPB = 108, 480
S = TPB // 4  # semicorchea
# Fmaj9 - Em7 - Am9 - Dm9  (IV - iii - vi - ii en La menor)
ACORDES = [
    [53, 57, 60, 64, 67],  # Fmaj9: F3 A3 C4 E4 G4
    [52, 55, 59, 62],      # Em7:   E3 G3 B3 D4
    [57, 60, 64, 67, 71],  # Am9:   A3 C4 E4 G4 B4
    [50, 53, 57, 60, 64],  # Dm9:   D3 F3 A3 C4 E4
]
# patrón sincopado tipo afrobeats (semicorcheas dentro del compás)
PATRON = [(0, 2, 100), (3, 2, 85), (6, 3, 95), (10, 2, 80), (12, 2, 90), (14, 2, 75)]

def guardar(nombre, eventos):
    mid = mido.MidiFile(ticks_per_beat=TPB)
    t = mido.MidiTrack(); mid.tracks.append(t)
    t.append(mido.MetaMessage('track_name', name=nombre.split('/')[-1][:-4]))
    t.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM)))
    t.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))
    msgs = []
    for ini, dur, nota, vel in eventos:
        msgs.append((ini, 1, mido.Message('note_on', note=nota, velocity=vel)))
        msgs.append((ini + dur, 0, mido.Message('note_off', note=nota, velocity=0)))
    msgs.sort(key=lambda m: (m[0], m[1]))
    ahora = 0
    for tick, _, m in msgs:
        m.time = tick - ahora; ahora = tick; t.append(m)
    mid.save(nombre)

stabs, pads = [], []
for compas in range(8):
    acorde = ACORDES[compas % 4]
    base = compas * 16 * S
    for paso, dur, vel in PATRON:
        for i, n in enumerate(acorde):
            hum = random.randint(0, 8)  # pequeño "strum" humano
            stabs.append((base + paso * S + hum + i * 4, dur * S - 20, n, max(1, vel + random.randint(-6, 6))))
    for n in acorde:
        pads.append((base, 16 * S - 10, n, 70))

guardar('../04_salidas/borradores/afrobeat-acordes-stabs_108bpm_v01.mid', stabs)
guardar('../04_salidas/borradores/afrobeat-acordes-pad_108bpm_v01.mid', pads)
print('ok')
