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
(
OSCdef(\changeFreq, { |msg, time, addr, recvPort|
    var newFreq;
    newFreq = msg[1]; // Assuming the frequency is the first argument
    ~freqBus.set(newFreq);
}, '/changeFreq');
)
~freqBus = Bus.control(s, 1);  // Create a control bus for frequency
~freqBus.set(440);  // Set an initial frequency value


(
SynthDef.new(\sine, {
    arg freqBus, atk=0.005, rel=0.3, amp=1, pan=0;
    var sig, env, freq;
    freq = In.kr(freqBus, 1); // Read frequency from control bus
    sig = SinOsc.ar(freq);
    env = EnvGen.kr(Env.new([0,1,0],[atk,rel],[1,-1]),doneAction:2);
    sig = Pan2.ar(sig, pan, amp);
    sig = sig * env;
    Out.ar(0, sig);
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
		\dur, Pseq([0.9375, 1.875, 0.46875, 0.46875], inf).trace,
		\freqBus, ~freqBus.index,
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