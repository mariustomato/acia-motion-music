Server.killAll;

(
s.boot;
s.plotTree;
s.meter;

t = TempoClock.new(100/60).permanent_(true); //tempoClock for changing overall Tempo


(
d = Dictionary.new;
d.add(\l -> PathName ("C:/Users/kleen/Dev/acia-motion-music/Samples/low").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\m -> PathName ("C:/Users/kleen/Dev/acia-motion-music/Samples/mid").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\h -> PathName ("C:/Users/kleen/Dev/acia-motion-music/Samples/high").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\h -> PathName ("C:/Users/kleen/Dev/acia-motion-music/Samples/hihat").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);

d.keys.do{arg key;
	d[key].do{ arg file;
		file.postln;
	};
};
)
)
/*
################################TESTING AREA#################################
*/

/*
################################COMMUNICATION#################################
*/

(
// Define the OSCFunc
~tempoChangeOSC = OSCFunc({ |msg, time, addr, recvPort|
	// Check if the message matches the expected format
	// Extract parameters from the OSC message
	//var time = msg[1].asInteger;
	var bpm = msg[1].asFloat;
	var numBeats = msg[2].asInteger;
	var buf=(bpm*60).asInteger;

	"changing tmempo".postln;

	~tempoChange.value(t, bpm, numBeats);
	~playPdefsForBpm.value(buf);

}, '/tempoChange', recvPort: 57120);

~pdfs=[\rhytm_bpm,\bass,\rhythm_bpm];

~startStopMusic = OSCFunc({ |msg, time, addr, recvPort|
    var command = msg[1].asSymbol;

    switch(command)
	{\start}  { ~playPdefsForBpm.value(t.tempo*60);  "Pdefs started.\n".postln; }
	{\stop}  { Pdef.all.do { |pdef| pdef.stop }; "Pdefs stopped.\n".postln; }
        { "Unknown command.\n".postln; }; //default

}, '/pdef_control',recvPort: 57120);

~bpmRanges = [
    (range: (0..60), pdefs: [\heartbeat,\horror1,\horror2]),
    (range: (61..80), pdefs: [\joggen1,\joggen2,\bass]),
	(range: (91..110), pdefs: [\bass_club,\club1,\club2,\club3,\rhythm,\rhythm2]),
    (range: (111..290), pdefs: [\experimental,\ex2,\ex3])
];

~playPdefsForBpm = {
	arg bpm;
    var rangeItem;

	"calling bpm with".postln;
	bpm.postln;

	rangeItem = ~bpmRanges.detect({ |item| item.range.includes(bpm) });

    Pdef.all.do { |pdef| pdef.stop };
	if (rangeItem.notNil,{
        rangeItem.pdefs.do({ |pdefName|
            Pdef(pdefName).play(tempoClock: t);
        });
    },{
        "No matching BPM range found for current BPM: %\n".postln;
    });
};

)


/*
################################HELPER FUNCTION#################################
*/
ServerOptions.devices;//first to check name
s.options.device = "hdmi_ausgang_hier_einsetzen";



(
~tempoChange = { //gradual Tempo change
	arg clock, newTempo, numBeats;
	var i =0, tempoArray;
	tempoArray = Array.interpolation(numBeats, clock.tempo, newTempo/60);
	clock.schedAbs(clock.nextBar, {
		clock.tempo_(tempoArray[i]);
		i = i + 1;
		if(i < numBeats) {1} {"done".postln};
	});
};
)

/*
################################MUSIC#################################
(
################################Synth#################################
*/

(
// SynthDefs
SynthDef(\sine, {
    arg freq = 440, dur = 1, atk = 0.1, rel = 0.1, amp = 0.1, pan = 0;

    var env, sig;
    sig = SinOsc.ar(freq);
    env = EnvGen.kr(Env.new([0,1,0],[atk,rel],[1,-1]),doneAction:2);
    sig = Pan2.ar(sig, pan, amp);
    sig = sig * env;
    Out.ar(0, sig);
}).add;

SynthDef(\sawtooth, {
    arg freq = 440, dur = 1, atk = 0.1, rel = 0.1, amp = 0.1, pan = 0;

    var env, sig;
    sig = Saw.ar(freq);
    env = EnvGen.kr(Env.new([0, 0.5, 0.2, 0.1, 0], [atk, rel], [1, -1]), doneAction: 2);
    sig = Pan2.ar(sig, pan, amp);
    sig = sig * env;
    Out.ar(0, sig);
}).add;

SynthDef(\bufplay, {
    arg buf=0, dur = 14, rate=1, amp=1;
    var sig;
    sig = PlayBuf.ar(2, buf, BufRateScale.ir(buf) * rate, doneAction: 2);
    sig = sig * amp;
    Out.ar(0, sig);
}).add;

SynthDef(\horror, {
    arg out = 0, freq = 220, gate = 1, amp = 0.5;

    var env, sound;

    // Envelope
    env = EnvGen.kr(Env.perc(0.01, 1), gate, doneAction: 2);

    // Noise generator
    sound = PinkNoise.ar(amp);

    // Filter
    sound = RLPF.ar(sound, freq * LFNoise0.kr(0.5).range(0.5, 2), 0.2);

    // Apply envelope
    sound = sound * env * amp;

    Out.ar(out, sound);
}).add;

SynthDef(\bpfsaw, {
	arg atk=2, sus=0, rel=3, c1=1, c2=(-1),
	freq=500, detune=0.2, pan=0, cfhzmin=0.1, cfhzmax=0.3, cfmin=500, cfmax=2000, rqmin=0.1, rqmax=0.2,
	lsf=200, ldb=0, amp=1, out=0;
	var sig, env, panLFO;
	env = EnvGen.kr(Env([0,1,1,0],[atk,sus,rel],[c1,0,c2]),doneAction:2);
	// Define a pattern for panning alternating between -0.8 and 0.8
	panLFO = LFPulse.kr(0.1).range(-1, 1);
	sig = Saw.ar(freq * {LFNoise1.kr(0.5, detune).midiratio} ! 2);
	sig = BPF.ar(
		sig,
		{LFNoise1.kr(
			LFNoise1.kr(4).exprange(cfhzmin, cfhzmax)
		).exprange(cfmin, cfmax)} ! 2,
		{LFNoise1.kr(0.1).exprange(rqmin, rqmax)} ! 2
	);
	sig = BLowShelf.ar(sig, lsf, 0.5, ldb);
	// Use the panEnv pattern for panning
	sig = Balance2.ar(sig[0], sig[1], pan * panLFO);
	sig = sig * env * amp;
	Out.ar(out, sig);
}).add;
)
/*
################################Horror#################################
*/

(
(
Pdef(\heartbeat, Pbind(
	\instrument, \horror,
	\dur, Pseq([0.5,1],inf),
	\doneAction, 2,
	\freq, 220,
	\quant,1,
	\amp, Pseq([0.11,0.1,],inf),
));

Pdef(\horror1, Pbind(
	\instrument, \bpfsaw,
	\dur, 12,
	\midinote, Pxrand([
		[100,88,80,87],
		[90,92,94,100,102,101],
		[80,100,87,86,102],
		[99,100,101,102],
	],inf),
	\detune, Pexprand(0.05,0.2,inf),
	\cfmin, 100,
	\cfmax, 1500,
	\rqmin, Pexprand(0.01,0.15, inf),
	\atk, Pwhite(2.0,2.5,inf),
	\rel, Pwhite(4,5,inf),
	\ldb, 6,
	\amp, 0.4,
	\out, 0,
	\quant,1,
));

Pdef(\horror2, Pbind(
	\instrument, \bpfsaw,
	\dur, 25,
	\freq, 8,
	\amp, 0.1,
	\atk, 0,
	// Set pan to a pattern alternating between -1 and 1
	\pan, Pexprand(-1, 1, inf),
	\out, 0,
	\quant,3,
));
);

/*
################################Joggen#################################
*/



(
Pdef(\joggen1, Pbind(
	\instrument, \bufplay,
	\dur, 1,
	\buf, Pseq([Prand([
		[[d[\l],d[\m]],d[\m],d[\m],d[\m]],
		[[d[\m],d[\h]],d[\m],d[\m],d[\m]],
		[d[\m],d[\m],d[\m],d[\m],]
	],1)],inf),
	\amp, 0.5,
	\pan, 0,
	\quant,1,
));

Pdef(\joggen2,Pbind(
	\instrument, \bpfsaw,
	\dur, Pseq([1.5,2.5,4],inf),
	\midinote, Pseq([
		[69,73,76],
		[71,75,78],
		Pxrand([
			[72,76,79],
			[72,76,79],
			[69,74,78]
	],1)],inf),
	\detune, Pwhite(0.1,0.19,inf),
	\cfmin, 100,
	\cfmax, 1500,
	\rqmin, Pexprand(0.1,0.15, inf),
	\atk, Pwhite(0.5,0.9,inf),
	\rel, Pwhite(1,1.2,inf),
	\ldb, Pwhite(0,0.5,inf),
	\amp, 0.87,
	\pan, Pwhite(-0.8,0.8,inf),
	\out, 0,
	\quant,1,
));

Pdef(\bass, Pbind(
    \instrument, \sawtooth,
	\dur, 0.5,
	\midinote, Pseq([Pseq([45],3),Pxrand([Pseq([57],5),Pseq([47],5)],1),Pxrand([Pseq([48],8),Pseq([50],8),Pseq([48,50],4),Pseq([45],8),Pseq([57,48],4)],1)],inf),
    \atk, Pwhite(0.001, 0.002, inf),
    \rel, Pwhite(0.1,0.4, inf),
	\amp, Pseq([Pexprand(0.4,0.5,inf),Pexprand(0.001,0.2,inf),Pexprand(0.4,0.5,inf),Pexprand(0,0.2,inf)],inf),
    \pan, Pwhite(-0.8, 0.8, inf),
	\quant,1,
));

);



/*
################################Club#################################
*/
(
// Define a Pdef "sinepat_bpm"
Pdef(\bass_club, Pbind(
    \instrument, \sawtooth,
	\dur, Pseq([2,2,Pseq([1,2,0.5,0.5],inf)],inf),  // BPM parameter
	\midinote, Pseq([Pseq([\rest],2),Pseq([Pseq([36],4),Pseq([41],4),Pseq([45],4),Pseq([43,43,31,31],1)],inf)],inf),
    \atk, Pwhite(0.001, 0.002, inf),
    \rel, Pwhite(0.1,0.4, inf),
	\amp, Pseq([0.5,0.2,0.3,0.2],inf),
    \pan, Pwhite(-0.8, 0.8, inf),
	\quant,1,
));

Pdef(\club1,Pbind(
	\instrument, \bpfsaw,
	\dur, Pseq([Pseq([0.5],2),Pseq([0.25],4),Pseq([0.125],8),Pseq([0.0625],4)],inf),
	\freq, 1,
	\detune, 0,
	\cfmin, 1500,
	\cfmax, 1500,
	\atk, Pwhite(0.01,0.03,inf),
	\rel, Pwhite(0.1,0.2,inf),
	\ldb, Pwhite(0,0.5,inf),
	\amp, 0.9,
	\pan, Pwhite(-0.8,0.8,inf),
	\out, 0,
	\quant,1,
));

Pdef(\club2,Pbind(
	\instrument, \bpfsaw,
	\dur, Pseq([Pseq([0.5],2),Pseq([0.25],4),Pseq([0.125],8),Pseq([0.0625],4)],inf),
	\freq, Pseq([Pseq([1],18),Pseq([\rest],inf)],inf),
	\detune, 0,
	\cfmin, 1500,
	\cfmax, 1500,
	\atk, Pwhite(0.01,0.03,inf),
	\rel, Pwhite(0.1,0.2,inf),
	\ldb, Pwhite(0,0.5,inf),
	\amp, 0.9,
	\pan, Pwhite(-0.8,0.8,inf),
	\out, 0,
	\quant,1,
));

Pdef(\club3, Pbind(
	\instrument, \bpfsaw,
	\dur, Pseq([4,4,1,1,1,Pseq([1],inf)],inf),
	\midinote, Pseq([\rest,\rest,Pseq([84,84,84,83,83,83,83,83,84,84,84,84,83,83,83,79],1),Pseq([84,84,84,83,\rest,79,Pseq([\rest],2),Pseq([84,84,84,\rest,83,83],1),Pseq([\rest],2)],inf)],inf),
	\cfmin, 1500,
	\cfmax, 1500,
	\atk, Pwhite(0.01,0.03,inf),
	\rel, Pwhite(0.1,0.4,inf),
	\ldb, Pwhite(0,5,inf),
	\amp, 0.9,
	\pan, Pwhite(-0.8,0.8,inf),
	\out, 0,
	\quant,1,
));

/*
Pdef(\rhythm, Pbind(
    \instrument, \bufplay,
    \dur, 0.25, // BPM parameter
    \stretch, 1.875,
    \buf, Pseq([Pseq([\rest],16), Pseq(d[\hh], inf)], inf),
    \rate, 1,
    \amp, Pseq([Pexprand(0.1, 0.5, 1), Pexprand(0.005, 0.2, 2)], inf),
    \quant, 1,
));
)
*/


Pdef(\rhythm2, Pbind(
	\instrument, \bufplay,
	\dur, 1,
	\stretch, 1.875,
	\buf, Pseq([Pseq([\rest],4),Pseq([[d[\l],d[\m],d[\h]],d[\m],d[\m],d[\m]],inf)],inf),
	\rate, 1,
	\amp, Pseq([0.5,0.2,0.2,0.2],inf),
	\quant,1,
));
);

/*
################################experimental#################################
*/
(
Pdef(\experimental,Pbind(
	\instrument, \bpfsaw,
	\dur, Pwhite(0.01,5,inf),
	\freq, Prand([Pexprand(2,1500,1),
		Pwhite(100,600,2),
	],inf),
	\detune, Pexprand(0.01,9,inf),
	\cfmin, 100,
	\cfmax, 1500,
	\atk, Pwhite(0.1,10,inf),
	\rel, Pwhite(0.1,10,inf),
	\ldb, Pwhite(0,6,inf),
	\amp, Pwhite(0.1,0.87,inf),
	\pan, Pwhite(-0.8,0.8,inf),
	\out, 0,
	\quant,1,
));

Pdef(\ex2, Pbind(
	\instrument, \bpfsaw,
	\dur, Pwhite(1,25,1),
	\freq, Pwhite(1,40,inf),
	\amp, 0.87,
	\atk, 0,
	// Set pan to a pattern alternating between -1 and 1
	\pan, Pexprand(-1, 1, inf),
	\out, 0,
	\quant,3,
));

Pdef(\ex3, Pbind(
	\instrument, \bpfsaw,
	\dur, 1,
	\freq, 1,
	\amp, Pwhite(0.1,0.87,inf),
	\atk, 0,
	\ldb, Pwhite(0,6,inf),
	// Set pan to a pattern alternating between -1 and 1
	\pan, Pexprand(-1, 1, inf),
	\out, 0,
	\quant,3,
));
)
)
