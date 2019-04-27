// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)

#include <Adafruit_NeoPixel.h>
#include "light_util.h"



enum lightmode{
  RAINBOW_WHEEL,
  RAINBOW_FLAT,
  MAX_LIGHTMODE
};

enum brightnessmode{
  OFF,
  DIM,
  MED,
  BRIGHT,
  MAX_BRIGHTNESS //Just to help enum
};

int current_brightness = BRIGHT;


int current_lightmode = RAINBOW_WHEEL;



//void refreshBrightness(){
//  int actualBrightness;
//
//  switch(current_brightness){
//    case OFF:
//      actualBrightness = 0;
//      break;
//    case DIM:
//      actualBrightness = 10;
//      break;
//    case MED:
//      actualBrightness = 30;
//      break;
//    case BRIGHT:
//      actualBrightness = 100;
//      break;
//    default:
//      actualBrightness = 10;
//  }
//  
//  strip.setBrightness(255);
//}

void nextLightmode(){
  current_lightmode = (current_lightmode + 1) % (MAX_LIGHTMODE);
}

//void nextBrightness(){
//  current_brightness = (current_brightness + 1) % (MAX_BRIGHTNESS);
//  refreshBrightness();
//}

void setByBuffer(uint8_t *p){
  for(int8_t i = 0; i < LIGHT_COUNT; i++){
    strip.setPixelColor(i, strip.Color(
      *(p + i*3 + 0), 
      *(p + i*3 + 1), 
      *(p + i*3 + 2)
    ));
  }

   //
}

void light_setup(){

  enum lightmode current_lightmode = RAINBOW_WHEEL;
  enum brightnessmode current_brightness = MED;
  
  strip.begin();
  //current_brightness = BRIGHT;
  //refreshBrightness();
  strip.setBrightness(255);
}

void light_loop(){
  int t = millis()/64;

//  switch(current_lightmode){
//    case RAINBOW_WHEEL :
//      rainbowCycle(t);
//      break;
//      
//    case RAINBOW_FLAT :
//      rainbowFlatCycle(t);
//      break;
//  }
//  
  strip.show(); // Initialize all pixels to 'off'
}
