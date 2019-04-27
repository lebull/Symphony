#include <ESP8266WebServer.h>

ESP8266WebServer server(80);
const char* www_username = "onelight";
const char* www_password = "asdf";
// allows you to set the realm of authentication Default:"Login Required"
const char* www_realm = "Custom Auth Realm";
// the Content of the HTML response in case of Unautherized Access Default:empty
String authFailResponse = "Authentication Failed";


void web_setup(){

  
  server.on("/", []() {
    if (!server.authenticate(www_username, www_password))
      //Basic Auth Method with Custom realm and Failure Response
      //return server.requestAuthentication(BASIC_AUTH, www_realm, authFailResponse);
      //Digest Auth Method with realm="Login Required" and empty Failure Response
      //return server.requestAuthentication(DIGEST_AUTH);
      //Digest Auth Method with Custom realm and empty Failure Response
      //return server.requestAuthentication(DIGEST_AUTH, www_realm);
      //Digest Auth Method with Custom realm and Failure Response
    {
      return server.requestAuthentication(DIGEST_AUTH, www_realm, authFailResponse);
    }
    Serial.print("hit on /");
    server.send(200, "text/plain", "Login OK");
  });

  server.on("/mode", []() {
    if (!server.authenticate(www_username, www_password))
      {return server.requestAuthentication(DIGEST_AUTH, www_realm, authFailResponse);}
    nextLightmode();
    server.send(200, "text/plain", "Mode Incremented");
  });

  
//  server.on("/brightness", []() {
//    if (!server.authenticate(www_username, www_password))
//      {return server.requestAuthentication(DIGEST_AUTH, www_realm, authFailResponse);}
//    nextBrightness();
//    server.send(200, "text/plain", "Brightness Incremented");
//  });

  server.on("/estimatedAmperage", []() {
    char message[32];
    int amperage = getEstimatedAmperage();
    sprintf(message, "%ld", amperage);
    server.send(200, "text/plain", message);
  });

//  server.on("/door/isMoving", [](){
//    if (!server.authenticate(www_username, www_password)){
//      return server.requestAuthentication(DIGEST_AUTH, www_realm, authFailResponse);
//    }
//
//        if(buttonLock){
//          server.send(200, "text/plain", "1");
//        }else{
//          server.send(200, "text/plain", "0");
//        }
//        
//  });

//  server.on("/range", []() {
//     Serial.print("hit on /range\n");
//    //Auth
//    if (!server.authenticate(www_username, www_password)){
//      return server.requestAuthentication(DIGEST_AUTH, www_realm, authFailResponse);
//    }
//
//    unsigned long range = getRange();
//    //long range = 1337;
//    //Serial.printf("Distance: %ld", range);
//    char message[32];
//    sprintf(message, "%ld", range);
//    server.send(200, "text/plain", message);
//  });
//
//   server.on("/door/toggle", []() {
//     Serial.print("hit on /door/toggle\n");
//    //Auth
//    if (!server.authenticate(www_username, www_password)){
//      return server.requestAuthentication(DIGEST_AUTH, www_realm, authFailResponse);
//    }
//
//    bool success = toggleDoor();
//
//    if(success){
//      server.send(200, "text/plain", "1");
//    }else{
//      server.send(400, "text/plain", "0");
//    }
//  });

  server.begin();

  Serial.print("Open http://");
  Serial.print(WiFi.localIP());
  Serial.println("/ in your browser to see it working");
}

void web_loop(){
  server.handleClient();
}
