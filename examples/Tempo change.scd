Server.killAll;
(
s.options.memSize = 8192 * 2;
s.boot;
s.plotTree;
t = TempoClock.new(120/60).permanent_(true); //tempoClock for changing overall Tempo
(
d = Dictionary.new;
d.add(\l -> PathName ("C:/Users/kleen/Dev/Music/Drums/low").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\m -> PathName ("C:/Users/kleen/Dev/Music/Drums/mid").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\h -> PathName ("C:/Users/kleen/Dev/Music/Drums/high").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
)
)
/*
################################TESTING AREA#################################
*/
~tempoChange.value(t, 140/60, 10, { "Tempo change complete.".postln });
Pdef(\my_pulse_pattern, Pbind(
    \instrument, \pulseTest,
    \ampHz, 4,
    \fund, 20,
    \maxPartial, 8,
    \width, 0.5,
)).play(t, quant: Quant(4));
/*
################################COMMUNICATION#################################
*/

(
<<<<<<< HEAD
// Define the OSCFunc
~tempoChangeOSC = OSCFunc({ |msg, time, addr, args|
	// Check if the message matches the expected format
	if (msg[1] == \tempoChange) {
		// Extract parameters from the OSC message
		//var time = msg[1].asInteger;
		var bpm = msg[1].asFloat;
		var numBeats = msg[2].asInteger;
=======
// OSCdef to free (stop) the Synth
OSCdef(\stopSynth, { |msg, time, addr, recvPort|
    //nodeID.do { |id| Synth.basicNew(\sineSynth, id).free };
	~stopAllInstruments.value;
}, '/stopAll');
>>>>>>> 9dfbafc5f4876ca0342b4f650738990fc843516a

// OSCdef for changing BPM
OSCdef(\changeBPM, { |msg, time, addr, recvPort|
    var newBPM, duration;
	newBPM = msg[1];
	duration= msg[2];

	~bpmBus.set(newBPM);

	("About to change to: "+newBPM).postln;

    // Call the function to update Pdefs with the new BPM
    ~tempoChange.value(t, newBPM, duration);
}, '/tempoChange');
)

/*
################################HELPER FUNCTION#################################
*/

<<<<<<< HEAD
/*
~freqBus = Bus.control(s, 1);  // Create a control bus for frequency
~freqBus.set(440);  // Set an initial frequency value

~bpmBus = Bus.control(s, 1); // Create a control bus for BPM
~bpmBus.set(60); // Set an initial BPM value
*/

t = TempoClock.new(100/60).permanent_(true); //tempoClock for changing overall Tempo

//t.beats;
=======

>>>>>>> 9dfbafc5f4876ca0342b4f650738990fc843516a

(
~tempoChange = { |clock, newTempo, duration, onComplete|
    var numSteps = 100;  // Number of increments in tempo change
    var stepTime = duration / numSteps;
    var currentStep = 0;
    var currentTempo = clock.tempo;
    var tempoStep = (newTempo - currentTempo) / numSteps;

    var changeFunc;

    changeFunc = {
        if(currentStep < numSteps, {
            clock.tempo = clock.tempo + tempoStep;
            currentStep = currentStep + 1;
            clock.sched(stepTime, changeFunc);
        }, {
            clock.tempo = newTempo;  // Ensure we end on exact new tempo
            onComplete.value;
        });
    };

    clock.sched(stepTime, changeFunc);
};
~stopAllInstruments = {
    // Stop all currently playing Synths on the default server
    s.queryAllNodes;
    s.defaultGroup.freeAll;

    // Stop all running Patterns
    Pdef.all.do({ |pdef| pdef.stop; });

    "All instruments stopped.".postln;
};
)


/*
################################MUSIC#################################
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
    env = EnvGen.kr(Env.new([0, 1, 0], [atk, rel], [1, -1]), doneAction: 2);
    sig = Pan2.ar(sig, pan, amp);
    sig = sig * env;
    Out.ar(0, sig);
}).add;

SynthDef.new(\bufplay, {
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
// Patterns
// Define a Pdef "sinepat_bpm"
Pdef(\sinepat_bpm, Pbind(
    \instrument, \sine,
<<<<<<< HEAD
    \dur, 1,  // BPM parameter
    \freqBus, 440,
    \atk, Pwhite(0.1, 0.2, inf),
    \rel, Pwhite(0.1, 0.2, inf),
    \amp, Pexprand(0.1, 1, inf),
=======
	\dur, Prand([1,2],inf),  // BPM parameter
	\freq, Pseq([Prand([440, 493.883, 554.365, 659.255, 739.989, 440, 415.305],2), Prand([415.305, 493.883, 554.365, 659.255, 739.9898],2)], inf),
    \atk, Pwhite(0.01, 0.79, inf),
    \rel, Pwhite(0.1, 1.001, inf),
	\amp, Prand([0, 0.4], inf),
>>>>>>> 9dfbafc5f4876ca0342b4f650738990fc843516a
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
)).play(t, quant: Quant(4));

// Define a Pdef "bass"
Pdef(\bass, Pbind(
    \instrument, \sine,
    \dur, 1,
    \freq, Pseq([220, 220, 110, 165, 165], inf),
    \atk, Pwhite(0.1, 0.4, inf),
    \rel, Pwhite(1, 1,2, inf),
	\amp, Prand([0, 0.9], inf),
    \pan, Pwhite(-0.8, 1, inf),

)).play(t, quant: Quant(4));

// Define a Pdef "rhythm_bpm"
Pdef(\rhythm_bpm, Pbind(
    \instrument, \bufplay,
    \dur, 0.5, // BPM parameter
    \stretch, 1.875,
    \buf, Prand([
        Prand([d[\l]], 1),
        Prand(d[\h]++d[\m]++d[\l], 7),
        Prand([d[\h]], 1),
        Prand(d[\h]++d[\m]++d[\l], 7),
    ], inf),
    \rate, 1,
    \amp, Pseq([0.1, Pexprand(0.005, 0.2, 7)], inf),
	\doneAction, 2, //wichtig?
)).play(t, quant: Quant(4));
)