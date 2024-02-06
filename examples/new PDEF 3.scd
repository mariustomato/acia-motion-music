s.boot;
Server.killAll;
s.plotTree;
s.meter;


(
d = Dictionary.new;
d.add(\l -> PathName ("C:/Users/fabia/Desktop/Dev/acia-motion-music/Samples/low").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\m -> PathName ("C:/Users/fabia/Desktop/Dev/acia-motion-music/Samples/mid").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\h -> PathName ("C:/Users/fabia/Desktop/Dev/acia-motion-music/Samples/high").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\n -> PathName ("C:/Users/fabia/Desktop/Dev/acia-motion-music/Samples/niente").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
)
(
// OSCdef for changing frequency
OSCdef(\changeFreq, { |msg, time, addr, recvPort|
    var newFreq;
    newFreq = msg[1];
    ~freqBus.set(newFreq);
}, '/changeFreq');
)

/*
(
// OSCdef for changing BPM
OSCFunc(\changeBPM, { |msg, time, addr, recvPort|
    var newBPM;
	~bpmBus.set(newBPM);
	newBPM = msg[3];

    // Call the function to update Pdefs with the new BPM
    ~tempoChange.value(t, newBPM, 8);
}, '/changeBPM');
)
*/

(
// Define the OSCFunc
~tempoChangeOSC = OSCFunc({ |msg, time, addr, args|
	// Check if the message matches the expected format
	if (msg[1] == \tempoChange) {
		// Extract parameters from the OSC message
		//var time = msg[1].asInteger;
		var bpm = msg[2].asFloat;
		var numBeats = msg[3].asInteger;

		// Call the tempoChange function
		~tempoChange.value(t, bpm, numBeats);
	}
}, '/tempoChange');

)




//~freqBus = Bus.control(s, 1);  // Create a control bus for frequency
//~freqBus.set(440);  // Set an initial frequency value
/*
~bpmBus = Bus.control(s, 1); // Create a control bus for BPM
~bpmBus.set(60); // Set an initial BPM value
*/

t = TempoClock.new(100/60).permanent_(true); //tempoClock for changing overall Tempo

//t.beats;

(
~tempoChange = { //gradual Tempo change
	arg clock, newTempo, numBeats;
	var i =0, tempoArray;
	tempoArray = Array.interpolation(numBeats, clock.tempo, newTempo/60);
	clock.schedAbs(clock.nextBar, {
		clock.tempo_(tempoArray[i]);
		i = i + 1;
		if(i < numBeats) {1} {\done.postln};
	});
};
)

/*(
~post = { t.tempo.postln; 1; };
t.schedAbs(t.nextBar, {~post.()});
)*/

~tempoChange.value(t, 240, 8); //test
/*
(
// Modify the Pdef for the sine pattern
Pdef(\sinepat_bpm).quant_(1.875).add;

// Modify the Pdef for the rhythm pattern
Pdef(\rhythm_bpm).quant_(1.875).add;
)
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
    env = EnvGen.kr(Env.new([0, 0.5, 0], [atk, rel], [1, -1]), doneAction: 2);
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

SynthDef(\pulseTest, {
	arg ampHz=4, fund=40, maxPartial=4, width=0.5;
	var amp1, amp2, freq1, freq2, sig1, sig2;
	amp1 = LFPulse.kr(ampHz, 0, 0.1) * 0.75;
	amp2 = LFPulse.kr(ampHz, 0.5, 0.1) * 0.75;
	freq1 = LFNoise0.kr(4).exprange(fund, fund*maxPartial).round(fund);
	freq2 = LFNoise0.kr(4).exprange(fund, fund*maxPartial).round(fund);
	freq1 = freq1 * LFPulse.kr(8, add:1);
	freq2 = freq2 * LFPulse.kr(6, add:1);
	sig1 = Pulse.ar(freq1, width, amp1);
	sig2 = Pulse.ar(freq2, width, amp2);
	sig1 = FreeVerb.ar(sig1, 0.7, 0.8, 0.25);
	sig2 = FreeVerb.ar(sig2, 0.7, 0.8, 0.25);
	Out.ar(0, sig1);
	Out.ar(1, sig2);
}).add;
)

(

/*Pdef(\my_pulse_pattern, Pbind(
    \instrument, \pulseTest,
	\dur, 12,
    \ampHz, 4,
    \fund, 20,
    \maxPartial, 8,
    \width, 0.5,
)).play(t, quant: Quant(4));
*/
// Patterns
// Define a Pdef "sinepat_bpm"
/*Pdef(\sinepat_bpm, Pbind(
    \instrument, \sine,
	\dur, Prand([1,2],inf),  // BPM parameter
	\freq, Pseq([Prand([440, 493.883, 554.365, 659.255, 739.989, 440, 415.305],2), Prand([415.305, 493.883, 554.365, 659.255, 739.9898],2)], inf),
    \atk, Pwhite(0.01, 0.79, inf),
    \rel, Pwhite(0.1, 1.001, inf),
	\amp, Prand([0, 0.4], inf),
    \pan, Pwhite(-0.8, 0.8, inf),
	\doneAction, 2, //wichtig?
)).play(t, quant: Quant(4));

Pdef(\sinepat_bpm2, Pbind(
    \instrument, \sawtooth,
    \dur, 4,  // BPM parameter
	\freq, Pseq([Prand([440, 277, 554, 659, 329, 392],2), Prand([460, 415, 329, 587],2)], inf),
    \atk, Pwhite(1, 1.1, inf),
    \rel, Pwhite(1, 2, inf),
	\amp, Pseq([0.001,0.01,0,0,0,0,0,Prand([0,0.01],2),0.01,0], inf),
    \pan, Pwhite(-0.8, 0.8, inf),
	\doneAction, 2, //wichtig?
)).play(t, quant: Quant(1));*/

// Define a Pdef "bass"
Pdef(\bass, Pbind(
    \instrument, \sawtooth,
	\dur, Pseq([Prand([2,1],1),2,2,2],inf),
	\freq, Pseq([Prand([55,65.40],1), Prand([43.65,73.41],1), Prand([41.20, 48.99, 61,73],2),Prand([55, 65.40],1), Prand([73.41,87.30],1),Prand([41.20, 48.99],2)], inf),
    \atk, Pwhite(0.1, 0.2, inf),
    \rel, Pwhite(0.1,0.4, inf),
	\amp, Pseq([Pexprand(0.6,0.98,inf),Pexprand(0.001,0.2,inf),Pexprand(0.6,0.98,inf),Pexprand(0,0.2,inf)],inf),
    \pan, Pwhite(-0.8, 0.8, inf),

)).play(t, quant: Quant(4));

// Define a Pdef "rhythm_bpm"
Pdef(\rhythm_bpm, Pbind(
    \instrument, \bufplay,
	\dur, Pseq([1,0.5,0.5,1,0.5,0.5],inf), // BPM parameter
    \stretch, 1.875,
	\buf, Pseq([d[\l],Prand([d[\m],d[\h],d[\n]],1), Prand([d[\m],d[\h],d[\n]],1), Prand([d[\l],d[\m],d[\h]],1),Prand([d[\m],d[\h],d[\n]],1), Prand([d[\m],d[\h],d[\n]],1)], inf),
    \rate, 1,
	\amp, Pseq([Pexprand(0.1, 0.5,1), Pexprand(0.005, 0.2, 2)], inf),
	\doneAction, 2, //wichtig?
)).play(t, quant: Quant(1));
)
