s.boot;
Server.killAll;
s.plotTree;

(
d = Dictionary.new;
d.add(\l -> PathName ("C:/Users/fabia/Music/Lumina/Vula/Drums/low").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\m -> PathName ("C:/Users/fabia/Music/Lumina/Vula/Drums/mid").entries.collect({ //Path change!
    arg sf;
    Buffer.read(s, sf.fullPath);
});
);
d.add(\h -> PathName ("C:/Users/fabia/Music/Lumina/Vula/Drums/high").entries.collect({ //Path change!
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
		var bpm = args[0].asFloat;
		var numBeats = args[1].asInteger;

		// Call the tempoChange function
		~tempoChange.value(t, bpm, numBeats);
	}
}, '/tempoChange');
)



~freqBus = Bus.control(s, 1);  // Create a control bus for frequency
~freqBus.set(440);  // Set an initial frequency value

~bpmBus = Bus.control(s, 1); // Create a control bus for BPM
~bpmBus.set(60); // Set an initial BPM value

t = TempoClock.new(120/60).permanent_(true); //tempoClock for changing overall Tempo

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

~tempoChange.value(t, 180, 8); //test
/*
(
// Modify the Pdef for the sine pattern
Pdef(\sinepat_bpm).quant_(1.875).add;

// Modify the Pdef for the rhythm pattern
Pdef(\rhythm_bpm).quant_(1.875).add;
)
*/
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


