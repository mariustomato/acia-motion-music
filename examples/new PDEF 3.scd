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
	//msg.postln;

	// Call the tempoChange function
	~tempoChange.value(t, bpm, numBeats);

}, '/tempoChange', recvPort: 57120);

~pdfs=[\rhytm_bpm,\bass,\rhythm_bpm];

~startStopMusic = OSCFunc({ |msg, time, addr, recvPort|
    var command = msg[1].asSymbol;

    switch(command)
	{\start}  { ~pdfs.do({ |pdefName| Pdef(pdefName).play; }); "Pdefs started.\n".postln; }
	{\stop}  { ~pdfs.do({ |pdefName| Pdef(pdefName).stop; }); "Pdefs stopped.\n".postln; }
        { "Unknown command.\n".postln; }; //default

}, '/pdef_control',recvPort: 57120);

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
		if(i < numBeats) {1} {\done.postln};
	});
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
Pdef(\rhythm_bpm, Pbind(
    \instrument, \bufplay,
	\dur, Pseq([1,0.5,0.5,1,Prand([Pseq([0.5,0.5],1),Pseq([0.75, 0.25],1)],1)],inf), // BPM parameter
    \stretch, 1.875,
	\buf, Pseq([d[\l],Prand([d[\m],d[\h],\rest],1), Prand([d[\m],d[\h],\rest],1), Prand([d[\l],d[\m],d[\h]],1),Prand([d[\m],d[\h],\rest],1), Prand([d[\m],d[\h],\rest],1)], inf),
    \rate, 1,
	\amp, Pseq([Pexprand(0.1, 0.5,1), Pexprand(0.005, 0.2, 2)], inf),
)).play(t, quant: Quant(1));

Pdef(\bass, Pbind(
    \instrument, \sawtooth,
	\dur, Pseq([1,1,1,1],inf),
	\freq, Pseq([110,110,110,110,146.83,146.83,146.83,146.83,146.83],inf),
    \atk, Pwhite(0.001, 0.002, inf),
    \rel, Pwhite(0.1,0.4, inf),
	\amp, Pseq([Pexprand(0.6,0.98,inf),Pexprand(0.001,0.2,inf),Pexprand(0.6,0.98,inf),Pexprand(0,0.2,inf)],inf),
    \pan, Pwhite(-0.8, 0.8, inf),

)).play(t, quant: Quant(1));

)

// Define a Pdef "sinepat_bpm"
Pdef(\sinepat_bpm, Pbind(
    \instrument, \sine,
	\dur, 0.5,  // BPM parameter
	\freq, Prand([Pseq([293.66,329.62,293.66,261.62,Pseq([\rest,261.62],4)]),Pseq([587.33,659.25,587.33,523.25],1), Pseq([783.99,698.45,659.25],1),Pseq([\rest,440],3),Pseq([Pseq([783.99, 830.60],3),Prand([Pseq([1046.50,987.76,1046.50,1174.66,1174.66,880],1),Pseq([698.45,659.25,622.25,587.33,554.36,523.25],1)]),1],1)],inf),
    \atk, Pwhite(0.1, 0.2, inf),
    \rel, Pwhite(0.1, 0.3, inf),
	\amp, Prand([0, 0.4], inf),
    \pan, Pwhite(-0.8, 0.8, inf),
)).play(t, quant: Quant(0.5));

Pdef(\bass, Pbind(
    \instrument, \sawtooth,
	\dur, 1,
	\freq, Prand([Pseq([Prand([110,65.40,\rest],1), Prand([43.65,73.41,\rest],1), Prand([41.20, 48.99, 61,73],2),Prand([55, 65.40],1), Prand([73.41,87.30],1),Prand([41.20, 48.99],2)], 1),Pseq([110,110,110,110,146.83,146.83,146.83,146.83,146.83],3)],inf),
    \atk, Pwhite(0.01, 0.2, inf),
    \rel, Pwhite(0.1,0.5, inf),
	\amp, Pseq([Pexprand(0.1,0.23,inf),Pexprand(0.001,0.2,inf),Pexprand(0.06,0.098,inf),Pexprand(0,0.2,inf)],inf),
    \pan, Pwhite(-0.8, 0.8, inf),

)).play(t, quant: Quant(1));


//Rest
// Define a Pdef "rhythm_bpm"
Pdef(\rhythm_bpm, Pbind(
    \instrument, \bufplay,
	\dur, 1, // BPM parameter
    \stretch, 1.875,
	\buf, Pseq([d[\l],Prand([d[\m],d[\h],\rest],1), Prand([d[\m],d[\h],\rest],1), Prand([d[\l],d[\m],d[\h]],1),Prand([d[\m],d[\h],\rest],1), Prand([d[\m],d[\h],\rest],1)], inf),
    \rate, 1,
	\amp, Pseq([Pexprand(0.1, 0.5,1), Pexprand(0.005, 0.2, 2)], inf),
)).play(t, quant: Quant(1));
)
