// const Speaker = require("speaker");
// const AudioContext = require("web-audio-engine").StreamAudioContext;
// const context = new AudioContext();
 
// const osc = context.createOscillator();
// const amp = context.createGain();
 
// const sourceAudio = new AudioNo

// osc.type = "square";
// osc.frequency.setValueAtTime(987.7666, 0);
// osc.frequency.setValueAtTime(1318.5102, 0.075);
// osc.start(0);
// osc.stop(2);
// osc.connect(amp);
// osc.onended = () => {
//   context.close().then(() => {
//     process.exit(0);
//   });
// };
 
// amp.gain.setValueAtTime(0.25, 0);
// amp.gain.setValueAtTime(0.25, 0.075);
// amp.gain.linearRampToValueAtTime(0, 2);
// amp.connect(context.destination);
 
// context.pipe(new Speaker());
// context.resume();
const OfflineAudioContext = require("web-audio-engine").OfflineAudioContext;
const context = new OfflineAudioContext(2, 44100 * 10, 44100);

context.startRendering().then((audioBuffer) => {
    console.log(audioBuffer);
  });