s.boot;
Server.killAll;
s.plotTree;

(
d = Dictionary.new;
d.add(\l -> PathName ("C:/Users/fabia/Music/Lumina/Vula/Drums/low").entries.collect({
	arg sf;
	Buffer.read(s, sf.fullPath);
});
);
d.add(\m -> PathName ("C:/Users/fabia/Music/Lumina/Vula/Drums/mid").entries.collect({
	arg sf;
	Buffer.read(s, sf.fullPath);
});
);
d.add(\h -> PathName ("C:/Users/fabia/Music/Lumina/Vula/Drums/high").entries.collect({
	arg sf;
	Buffer.read(s, sf.fullPath);
});
);
)

~chooseRandomFrequency = { |values| values.choose };


(
SynthDef.new(\sine, {
	arg freq=440, atk=0.005, rel=0.3, amp=1, pan=0;
	var sig, env;
	sig = SinOsc.ar(freq);
	env = EnvGen.kr(Env.new([0,1,0],[atk,rel],[1,-1]),doneAction:2);
	sig =Pan2.ar(sig, pan, amp);
	sig = sig * env;
	Out.ar(0,sig);
}).add;

SynthDef.new(\bufplay, {
	arg buf=0, rate =1, amp=1;
	var sig;
	sig = PlayBuf.ar(2, buf, BufRateScale.ir(buf) * rate, doneAction: 2);
	sig = sig * amp;
	Out.ar(0, sig);
}).add;
)


(
Pdef(
	\sinepat,
	Pbind(
		\instrument, \sine,
		\dur, Pfunc { ~chooseRandomFrequency.value([0.9375, 1.875, 0.46875, 0.46875])}.trace,
		\freq, Pfunc { ~chooseRandomFrequency.value([300, 400, 500, 600, 330, 440, 220, 550, ]) },
		\atk, Pwhite(0.5, 1.0, inf),
	\rel, Pwhite(0.5,1.0, inf),
	\amp, Pexprand(0.01, 1, inf),
	\pan, Pwhite(-08, 0.8, inf),
	);
).play(quant:1.875);
)

(
Pdef(
	\rhythm,
	Pbind(
		\instrument, \bufplay,
		\dur, Pseq([1/8], inf),
		\stretch, 1.875,
		\buf, Prand(
			[
				Prand(d[\l],1),
				Prand(d[\h]++d[\m]++d[\l],7),
				Prand(d[\h], 1),
				Prand(d[\h]++d[\m]++d[\l],7),
			], inf
		),
		\rate, 1,
		\amp, Pseq([0.8, Pexprand(0.005,0.2,7)], inf),
	);
).play(quant:1.875);
)

/*

(
p = Pbind(
	\instrument, \sine,
	\dur, Pwhite(1, 2, inf),
	\freq, Pfunc { ~chooseRandomFrequency.value([300, 400, 500, 600, 440, 442, 550, ]) }.trace,
	\atk, Pwhite(0.5, 3.0, inf),
	\rel, Pwhite(1.0,10.0, inf),
	\amp, Pexprand(0.01, 0.2, inf),
	\pan, Pwhite(-08, 0.8, inf),
).play
)


(
p = Pbind(
	\instrument, \sine,
	\dur, Pwhite(0.8, 2, inf),
	\midinote, 33,
	\harmonic, Pexprand(1, 80, inf).round.trace,
	\atk, Pwhite(0.5, 0.8, inf),
	\rel, Pwhite(1.0,1.1, inf),
	\amp, Pkey(\harmonic).reciprocal * 0.3,
	\pan, Pwhite(-0.8, 0.8, inf),
).play
)

p.stop;
*/
