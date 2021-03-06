SynthDef.new(\bell,
{|vib=0, scrub=0, echo=0, rate=1, verb=0.5, lpf=20000, amp=1, freq=0, buf=0, delay=0, echoOn=0, room=0.5, chop=0, slide=0, grain=0, pan=0, fmod=0, sus=1, bits=24, hpf=0, slidefrom=1|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp * 4);
sus=2.5;
osc=Decimator.ar((LPF.ar(HPF.ar(Klank.ar(`[[0.501, 1, 0.7, 2.002, 3, 9.6, 2.49, 11, 2.571, 3.05, 6.242, 12.49, 13, 16, 24], [0.002, 0.02, 0.001, 0.008, 0.02, 0.004, 0.02, 0.04, 0.02, 0.005, 0.05, 0.05, 0.02, 0.03, 0.04], [1.2, 1.2, 1.2, 0.9, 0.9, 0.9, 0.25, 0.25, 0.25, 0.14, 0.14, 0.14, 0.07, 0.07, 0.07]], Impulse.ar(0.25), freq, 0, 3), hpf), (lpf + 1)) * LFPulse.ar((chop / 2.5))), rate: 44100, bits: bits);
env=EnvGen.ar(Env([0, amp, amp, 0], [0, sus, 0], releaseTime: sus, level: amp, levels: [0, amp, amp, 0], curve: 'step', times: [0, sus, 0]), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;