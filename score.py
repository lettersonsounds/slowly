from pippi import dsp
from pippi import tune

dsp.quiet = False

dsp.timer('start')

def that(li):
    print 'layer', li

    freqs = tune.fromdegrees([ dsp.randint(1, 20) for f in range(dsp.randint(3, 6)) ], octave = 3)

    length = dsp.stf(dsp.rand(10, 20))

    layers = []

    for fi, freq in enumerate(freqs):
        print '    tone', fi, round(dsp.fts(length), 2)

        waveform = dsp.randchoose(['sine2pi', 'tri', 'hann'])
        waveform = dsp.wavetable(waveform, 512)

        window = dsp.randchoose(['sine', 'tri', 'hann'])
        window = dsp.wavetable(window, 512)

        pulsewidth = dsp.rand(0.1, 1)
        modFreq    = dsp.rand(0.1, 10.0) / dsp.fts(length)

        numgrains = length / 32
        numpoints = dsp.randint(2, 6)

        apoints = [0] + [dsp.rand(0, 1) for p in range(numpoints - 2)] + [0]
        ppoints = [dsp.rand(0, 1) for p in range(numpoints)]

        e = dsp.breakpoint(apoints, numgrains)
        p = dsp.breakpoint(ppoints, numgrains)

        mod = dsp.wavetable('random', 512)
        modRange = dsp.rand(0, 0.001)

        print '    ', round(freq, 2), round(modRange, 3), round(modFreq, 3)
        layer = dsp.pulsar(freq, length, pulsewidth, waveform, window, mod, modRange, modFreq, 0.1)

        layer = dsp.split(layer, dsp.flen(layer) / numgrains)
        layer = layer[:numgrains]

        layer = [ dsp.pan(dsp.amp(layer[i], e[i]), p[i]) for i in range(numgrains) ]

        layer = ''.join(layer)

        layers += [ layer ]

    out = dsp.mix(layers)

    return out

layers = []

for l in range(3):
    layer = ''.join([ that(w) for w in range(40) ])

    layers += [ layer ]

out = dsp.mix(layers)

dsp.write(out, 'slowly')

dsp.timer('stop')
