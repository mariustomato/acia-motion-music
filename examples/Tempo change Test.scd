s.boot;
Server.killAll;
s.plotTree;

// Define a dictionary to store buffers
(
var d = Dictionary.new;
d.add(\l, PathName("C:/Users/fabia/Music/Lumina/Vula/Drums/low").entries.collect { |sf|
    Buffer.read(s, sf.fullPath);
});
d.add(\m, PathName("C:/Users/fabia/Music/Lumina/Vula/Drums/mid").entries.collect { |sf|
    Buffer.read(s, sf.fullPath);
});
d.add(\h, PathName("C:/Users/fabia/Music/Lumina/Vula/Drums/high").entries.collect { |sf|
    Buffer.read(s, sf.fullPath);
});
)

// OSCdef for changing frequency
(
var ~freqBus;
OSCdef(\changeFreq, { |msg, time, addr, recvPort|
    var newFreq = msg[1];
    ~freqBus.set(newFreq);
}, '/changeFreq');
)

// OSCdef for changing BPM
(
var ~bpmBus;
OSCdef(\changeBPM, { |msg, time, addr, recvPort|
    var newBPM = msg[1]; // Fix index to get the correct value
    ~bpmBus.set(newBPM);
    // Call the function to update Pdefs with the new BPM
    ~tempoChange.value(t, newBPM, 8);
}, '/changeBPM');
)

// Define the tempo change OSCFunc
(
var ~tempoChangeOSC;
~tempoChangeOSC = OSCFunc({ |msg, time, addr, args|
    // Check if the message matches the expected format
    if (msg[1] == \tempoChange) {
        // Extract parameters from the OSC message
        var bpm = args[0].asFloat;
        var numBeats = args[1].asInteger;

        // Call the tempoChange function
        ~tempoChange.value(t, bpm, numBeats);
    }
}, '/tempoChange');
)

// Create control buses for frequency and BPM
~freqBus = Bus.control(s, 1);
~freqBus.set(440);

~bpmBus = Bus.control(s, 1);
~bpmBus.set(60);

// Define the tempoChange function
(
var ~tempoChange;
~tempoChange = { |clock, newTempo, numBeats|
    var i = 0;
    var tempoArray = Array.interpolation(numBeats, clock.tempo, newTempo / 60);

    clock.schedAbs(clock.nextBar, {
        clock.tempo_(tempoArray[i]);
        i = i + 1;
        if (i < numBeats) {
            1; // Continue scheduling
        } {
            \done.postln;
        }
    });
};
)

// Example usage: Change tempo gradually
~tempoChange.value(t, 180, 8);

// ... (rest of your SynthDefs and Pdefs)

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
// Define a Pdef "notes"
Pdef(\sinepat_bpm, Pbind(
    \instrument, \sine,
    \dur, 1,  // BPM parameter
    \freqBus, ~freqBus.index,
    \atk, Pwhite(0.1, 0.2, inf),
    \rel, Pwhite(0.1, 0.2, inf),
    \amp, Pexprand(0.1, 1, inf),
    \pan, Pwhite(-0.8, 0.8, inf),
		)).play(t, quant: Quant(4));

// Define a Pdef "beat"
Pdef(\rhythm_bpm, Pbind(
    \instrument, \bufplay,
    \dur, 4, // BPM parameter
    \stretch, 1.875,
    \buf, Prand([
        Prand(d[\l], 1),
        Prand(d[\h]++d[\m]++d[\l], 7),
        Prand(d[\h], 1),
        Prand(d[\h]++d[\m]++d[\l], 7),
    ], inf),
    \rate, 1,
    \amp, Pseq([0.8, Pexprand(0.005, 0.2, 7)], inf),
)).play(t, quant: Quant(4));
)



