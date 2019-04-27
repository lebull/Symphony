var dgram = require('dgram');
var util = require('./util.js');


function cleanup() {
    console.log("Cleaning up");
    client.close();
}
process.on('exit', cleanup.bind(null, { cleanup: true }));
process.on('SIGINT', cleanup.bind(null, { exit: true }));

// --- //

var PORT = 4210;
var HOST = '192.168.255.255';
var client = dgram.createSocket('udp4');

/**
 * @returns An array of bits in the format [r, g, b, r, g, b, r, g...]
 */
function calcMessage(){
    messageLength = 6 * 7 * 8; //6 bytes * 7 lights per segment * 8 segments

    var pixel = [parseInt(1 * 0xFF), parseInt(0.5 * 0xFF), parseInt(0.2 * 0xFF)]

    var pixels = [];
    for(var i = 0; i < 7 * 8; i++){
        pixels.push(pixel);
    }

    return Buffer.from(util.flatten(pixels));
}


function sendShit(message) {
    console.log(`sending ${message.length.toString()} bits`);
    client.send(message, 0, messageLength, PORT, HOST, function (err, bytes) {
        if (err) throw err;
        //console.log('UDP message sent to ' + HOST + ':' + PORT);
    });
}


setInterval(function(){
    sendShit(calcMessage());
},25);





