s.boot;
Server.killAll;
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
/*
################################TESTING AREA#################################
*/
~tempoChange.value(t, 140/60, 10, { "Tempo change complete.".postln });
/*
################################COMMUNICATION#################################
*/

(
// OSCdef to free (stop) the Synth
OSCdef(\stopSynth, { |msg, time, addr, recvPort|
    //nodeID.do { |id| Synth.basicNew(\sineSynth, id).free };
	~stopAllInstruments.value;
}, '/stopAll');

// OSCdef for changing BPM
OSCdef(\changeBPM, { |msg, time, addr, recvPort|
    var newBPM, numBeats;
	newBPM = msg[1];
	numBeats= msg[2];

	~bpmBus.set(newBPM);

	("About to change to: "+newBPM).postln;

    // Call the function to update Pdefs with the new BPM
    ~tempoChange.value(t, newBPM, numBeats);
}, '/tempoChange');
)

/*
################################HELPER FUNCTION#################################
*/


~freqBus = Bus.control(s, 1);  // Create a control bus for frequency
~freqBus.set(440);  // Set an initial frequency value

~bpmBus = Bus.control(s, 1); // Create a control bus for BPM
~bpmBus.set(60); // Set an initial BPM value


//t.beats;

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
SynthDef(\sineSynth, { |freq = 440, amp = 0.5, out = 0|
	var sound = SinOsc.ar(freq) * amp;
	Out.ar(out, sound);
}).add;


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
/*
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
*/
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
).play(t,quant:1.875);
)



