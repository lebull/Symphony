#include "wifi.h"
#include "light.h"
#include "web.h"
#include "ota.h"
#include "udp.h"

void setup() {
  Serial.begin(115200);

  web_setup();
  wifi_setup();
  ota_setup();
  udp_setup();
  light_setup();
}

void loop() {
  ota_loop();
  web_loop();
  udp_loop();
  light_loop();
}
