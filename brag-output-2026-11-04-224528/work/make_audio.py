"""Synthesize the soundtrack for brag.mp4: lyre plucks, pad, bass, light drums and in-key SFX.

All music is in D major at 100 BPM (one beat = 0.6 s), so the cuts in brag.html land on the beat.
Usage: python make_audio.py <out.wav>
"""
import sys
import wave

import numpy as np

SR = 44100
END = 23.4
BEAT = 0.6
N = int(SR * END)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(7)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def add(sig, start, gain=1.0, pan=0.0):
    """Mix a mono signal into the stereo bus at a start time (seconds)."""
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for k in range(len(x)):  # One-pole filter. The signals are short, so a loop is fast enough.
        acc = (1 - a) * x[k] + a * acc
        y[k] = acc
    return y


def pluck(f, dur=1.4):
    """Lyre-like pluck: harmonics where the high ones die faster."""
    t = np.arange(int(SR * dur)) / SR
    s = np.zeros_like(t)
    for h, amp in enumerate([1, .5, .3, .18, .1, .06], start=1):
        s += amp * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (2.6 + 1.8 * h))
    return s * np.minimum(1, t / 0.004)


def bell(f, dur=2.2):
    t = np.arange(int(SR * dur)) / SR
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) + .35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4.5)
         + .18 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 8))
    return s * np.minimum(1, t / 0.003)


def pad(freqs, dur):
    t = np.arange(int(SR * dur)) / SR
    s = np.zeros_like(t)
    for f in freqs:
        for d in (-0.12, 0.12):
            s += np.sin(2 * np.pi * (f + d) * t) + .25 * np.sin(2 * np.pi * 2 * (f + d) * t)
    env = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.5)
    return s * env / len(freqs)


def kick():
    t = np.arange(int(SR * .35)) / SR
    f = 48 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)


def hat():
    t = np.arange(int(SR * .06)) / SR
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 6000)  # Keep only the top end.
    return n * np.exp(-t * 70)


def whoosh(dur=0.8):
    t = np.arange(int(SR * dur)) / SR
    n = rng.standard_normal(len(t))
    soft = lowpass(n, 900)
    bright = n - lowpass(n, 2500)
    env = np.sin(np.pi * t / dur) ** 2
    mixf = t / dur  # Gets brighter as it passes.
    return (soft * (1 - mixf) * 2.2 + bright * mixf * .35) * env


# D major. Chords per bar (one bar = 4 beats = 2.4 s).
CH = {"D": [62, 66, 69], "Bm": [59, 62, 66], "G": [55, 59, 62], "A": [57, 61, 64], "Em": [52, 55, 59]}
BARS = ["D", "Bm", "G", "A", "D", "Bm", "Em", "A", "G", "D"]

for b, name in enumerate(BARS):
    t0 = b * 4 * BEAT
    notes = CH[name]
    # Lyre arpeggio on eighth notes, one octave up.
    pattern = [0, 1, 2, 1, 0 + 3, 2, 1, 2]
    for k, idx in enumerate(pattern):
        tt = t0 + k * BEAT / 2
        if tt >= END - 0.4:
            break
        m = notes[idx % 3] + 12 * (1 + idx // 3)
        add(pluck(hz(m)), tt, gain=.16 if k % 2 == 0 else .11, pan=-.25 if k % 2 else .25)
    # Pad from the reveal on.
    if t0 + 2.4 > 3.0:
        start = max(t0, 2.7)
        add(pad([hz(n) for n in notes], t0 + 2.4 - start + .3), start, gain=.07)
    # Bass from the skill tree on.
    if t0 >= 6.0:
        add(pluck(hz(notes[0] - 24), 2.2) * 1.2, t0, gain=.22)

# Opening strum on the first downbeat.
for k, m in enumerate([50, 57, 62, 66, 69, 74]):
    add(pluck(hz(m), 2.5), k * 0.025, gain=.14, pan=(k - 2.5) / 6)

# Drums: kick on beats 1 and 3 from the skill tree to the outro, hats on the off-beats.
t = 6.6
while t < 21.6:
    add(kick(), t, gain=.5)
    t += 2 * BEAT
t = 10.2 + BEAT / 2
while t < 19.8:
    add(hat(), t, gain=.06 if t < 16.8 else .09, pan=.3)
    t += BEAT

# Whooshes centred on each cut.
for c in [3.0, 6.6, 10.2, 16.8, 19.8]:
    add(whoosh(), c - 0.5, gain=.09, pan=-.3)

# Chimes, all in D major pentatonic.
add(bell(hz(81)), 3.15, gain=.10, pan=-.2)   # "QA Manager"
add(bell(hz(86)), 3.95, gain=.10, pan=.2)    # "Mousy"
for i, m in enumerate([74, 76, 78, 81, 83]):  # Five project cards.
    add(bell(hz(m)), 10.5 + i * 0.3, gain=.08, pan=-.5 + i * .25)
# Click on "Try it live": short tick plus a bright chime.
tick = rng.standard_normal(int(SR * .02)) * np.exp(-np.arange(int(SR * .02)) / SR * 300)
add(tick, 14.7, gain=.12, pan=-.4)
add(bell(hz(90)), 14.7, gain=.07, pan=-.4)
# Outro: bell chord.
for m in [74, 78, 81, 86]:
    add(bell(hz(m), 3.5), 19.95, gain=.06)

# Master: gentle reverb-like echo, fade out, soft limiter, normalize.
for delay, g in [(0.18, .22), (0.31, .15), (0.47, .09)]:
    d = int(delay * SR)
    L[d:] += R[:-d] * g
    R[d:] += L[:-d] * g
fade = np.ones(N)
fn = int(1.2 * SR)
fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
L *= fade
R *= fade
mix = np.stack([L, R], axis=1)
mix = np.tanh(mix * 1.4) / 1.4
mix *= 0.89 / np.max(np.abs(mix))

with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("wrote", sys.argv[1])
