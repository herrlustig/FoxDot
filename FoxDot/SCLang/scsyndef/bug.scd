SynthDef.new(\bug,
{|vib=0, grain=0, echoOn=0, scrub=0, room=0.3, chop=0, bits=24, slide=0, echo=0, delay=0, rate=1, verb=0.25, sus=1, slidefrom=1, fmod=0, lpf=20000, amp=1, freq=0, buf=0, hpf=0, pan=0|
var osc, env;
amp = amp / 2;
freq = freq + fmod;
freq = Line.ar(freq * slidefrom, freq * (1 + slide), sus);
freq = Vibrato.kr(freq, rate: vib);
amp=(amp / 5);
osc=Decimator.ar((LPF.ar(HPF.ar((Pulse.ar([freq, (freq * 1.0001)], width: [0.09, 0.16, 0.25]) * SinOsc.ar((rate * 4))), hpf), (lpf + 1)) * LFPulse.ar((chop / sus))), rate: 44100, bits: bits);
env=EnvGen.ar(Env.perc((sus * 1.5), level: amp, releaseTime: sus), doneAction: 2);
	Out.ar(0, Pan2.ar(FreeVerb.ar(osc * env, verb, room), pan))}).add;