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

/pdef_control start
/pdef_control stop
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

	~tempoChange.value(t, bpm, numBeats);
	~playPdefsForBpm.value(buf);

}, '/tempoChange', recvPort: 57120);

~pdfs=[\rhytm_bpm,\bass,\rhythm_bpm];

~startStopMusic = OSCFunc({ |msg, time, addr, recvPort|
    var command = msg[1].asSymbol;

    switch(command)
	{\start}  { ~pdfs.do({ |pdefName| Pdef(pdefName).play; }); "Pdefs started.\n".postln; }
	{\stop}  { ~pdfs.do({ |pdefName| Pdef(pdefName).stop; }); "Pdefs stopped.\n".postln; }
        { "Unknown command.\n".postln; }; //default

}, '/pdef_control',recvPort: 57120);

~bpmRanges = [
    (range: (30..90), pdefs: [\jogging_rhythm_bpm, \jogging_bass]),
    (range: (91..150), pdefs: [\club_sinepat_bpm, \club_bass, \club_rhythm_bpm]),
    (range: (151..290), pdefs: [\horror_heartbeat, \horror2])
];

~playPdefsForBpm = {
	arg bpm;
    var rangeItem;

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
(
(
Pdef(\horror_heartbeat, Pbind(
	\instrument, \horror,
	\dur, Pseq([0.5,1],inf),
	\doneAction, 2,
	\freq, 220,
	\amp, Pseq([0.11,0.1,],inf),
)));

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
	\amp, 0.01,
	\out, 0,
)));

Pdef(\horror2, Pbind(
	\instrument, \bpfsaw,
	\dur, 25,
	\freq, 8,
	\amp, 0.1,
	\atk, 0,
	// Set pan to a pattern alternating between -1 and 1
	\pan, Pexprand(-1, 1, inf),
	\out, 0,
)));

/*
################################Joggen#################################
*/



(
Pdef(\jogging_rhythm_bpm, Pbind(
    \instrument, \bufplay,
	\dur, Pseq([1,0.5,0.5,1,Prand([Pseq([0.5,0.5],1),Pseq([0.75, 0.25],1)],1)],inf), // BPM parameter
    \stretch, 1.875,
	\buf, Pseq([d[\l],Prand([d[\m],d[\h],\rest],1), Prand([d[\m],d[\h],\rest],1), Prand([d[\l],d[\m],d[\h]],1),Prand([d[\m],d[\h],\rest],1), Prand([d[\m],d[\h],\rest],1)], inf),
    \rate, 1,
	\amp, Pseq([Pexprand(0.1, 0.5,1), Pexprand(0.005, 0.2, 2)], inf),
)));

Pdef(\jogging_bass, Pbind(
    \instrument, \sawtooth,
	\dur, Pseq([1,1,1,1],inf),
	\freq, Pseq([110,110,110,110,146.83,146.83,146.83,146.83,146.83],inf),
    \atk, Pwhite(0.001, 0.002, inf),
    \rel, Pwhite(0.1,0.4, inf),
	\amp, Pseq([Pexprand(0.6,0.98,inf),Pexprand(0.001,0.2,inf),Pexprand(0.6,0.98,inf),Pexprand(0,0.2,inf)],inf),
    \pan, Pwhite(-0.8, 0.8, inf),

));



/*
################################Club#################################
*/

(
// Define a Pdef "sinepat_bpm"
Pdef(\club_sinepat_bpm, Pbind(
    \instrument, \sine,
	\dur, 0.5,  // BPM parameter
	\freq, Prand([Pseq([293.66,329.62,293.66,261.62,Pseq([\rest,261.62],4)]),Pseq([587.33,659.25,587.33,523.25],1), Pseq([783.99,698.45,659.25],1),Pseq([\rest,440],3),Pseq([Pseq([783.99, 830.60],3),Prand([Pseq([1046.50,987.76,1046.50,1174.66,1174.66,880],1),Pseq([698.45,659.25,622.25,587.33,554.36,523.25],1)]),1],1)],inf),
    \atk, Pwhite(0.1, 0.2, inf),
    \rel, Pwhite(0.1, 0.3, inf),
	\amp, Prand([0, 0.4], inf),
    \pan, Pwhite(-0.8, 0.8, inf),
));

Pdef(\club_bass, Pbind(
    \instrument, \bpfsaw,
	\dur, 1,
	\freq, Prand([Pseq([Prand([110,65.40,\rest],1), Prand([43.65,73.41,\rest],1), Prand([41.20, 48.99, 61,73],2),Prand([55, 65.40],1), Prand([73.41,87.30],1),Prand([41.20, 48.99],2)], 1),Pseq([110,110,110,110,146.83,146.83,146.83,146.83,146.83],3)],inf),
    \atk, Pwhite(0.01, 0.2, inf),
    \rel, Pwhite(0.1,0.5, inf),
	\amp, Pseq([Pexprand(0.1,0.2,inf),Pexprand(0.001,0.2,inf),Pexprand(0.06,0.098,inf),Pexprand(0,0.2,inf)],inf),
    \pan, Pwhite(-0.8, 0.8, inf),

)));


//Rest
// Define a Pdef "rhythm_bpm"
Pdef(\club_rhythm_bpm, Pbind(
    \instrument, \bufplay,
	\dur, 1, // BPM parameter
    \stretch, 1.875,
	\buf, Pseq([d[\l],Prand([d[\m],d[\h],\rest],1), Prand([d[\m],d[\h],\rest],1), Prand([d[\l],d[\m],d[\h]],1),Prand([d[\m],d[\h],\rest],1), Prand([d[\m],d[\h],\rest],1)], inf),
    \rate, 1,
	\amp, Pseq([Pexprand(0.1, 0.5,1), Pexprand(0.005, 0.2, 2)], inf),
)));

