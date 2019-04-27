#include <WiFiUdp.h>

WiFiUDP Udp;

const unsigned int localUdpPort = 4210;

uint8_t incomingPacket[3 * 7 * 8];
//char replyPacket[] = "Hi there! Got the message :-)";

void udp_setup() {
  Serial.printf("Starting udp on port %d\n", localUdpPort);
  Udp.begin(localUdpPort);
}

void udp_loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = '\0';
    }
    Serial.printf("UDP packet contents: %i, %i, %i\n", 
      incomingPacket[0], incomingPacket[1], incomingPacket[2]
    );

    setByBuffer(incomingPacket);
  
    //Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    //Udp.write(replyPacket);
    //Udp.endPacket();
  }
}
