#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "secret";
const char* password = "secret";

const char* a_on  = "1010100101101001010101100101011001010101010101010110100101010101";
const char* a_off = "1010100101101001010101100101011001010101010101010110101001010101";
const char* b_on  = "1010100101101001010101100101011001010101010101010110100101010110";
const char* b_off = "1010100101101001010101100101011001010101010101010110101001010110";
const char* c_on  = "1010100101101001010101100101011001010101010101010110100101011001";
const char* c_off = "1010100101101001010101100101011001010101010101010110101001011001";
const char* d_on  = "1010100101101001010101100101011001010101010101010110100101011010";
const char* d_off = "1010100101101001010101100101011001010101010101010110101001011010";

const int short_delay = 250;   // us
const int long_delay  = 1250;  // us
const int sync_delay  = 2500;  // us
const int pause_delay = 10000; // us

const int repeats = 10;
const int codelength = 64;

ESP8266WebServer server(80);

#define TX_PIN 5

void transmit(const char* code) {
  int i,j;

  digitalWrite(LED_BUILTIN, LOW);
  server.send(200, "text/plain", "OK");
  Serial.print("Sending ");
  Serial.write(code, codelength);
  Serial.println("");

  for(i = 0; i < repeats; i++)
  {
    // send sync
    digitalWrite(TX_PIN, HIGH);
    delayMicroseconds(short_delay);
    digitalWrite(TX_PIN, LOW);
    delayMicroseconds(sync_delay);

    // send code
    for(j = 0; j < codelength;j++)
    {
       if('1' == code[j])
       {
         digitalWrite(TX_PIN, HIGH);
         delayMicroseconds(short_delay);
         digitalWrite(TX_PIN, LOW);
         delayMicroseconds(short_delay);
       }
       else if('0' == code[j])
       {
         digitalWrite(TX_PIN, HIGH);
         delayMicroseconds(short_delay);
         digitalWrite(TX_PIN, LOW);
         delayMicroseconds(long_delay);
       }
    }

    // send pause
    digitalWrite(TX_PIN, HIGH);
    delayMicroseconds(short_delay);
    digitalWrite(TX_PIN, LOW);
    delayMicroseconds(pause_delay);
  }

  //delayMicroseconds(500000);
  
  digitalWrite(LED_BUILTIN, HIGH);
}

void handle_a_on() {
  transmit(a_on);
}

void handle_a_off() {
  transmit(a_off);
}

void handle_b_on() {
  transmit(b_on);
}

void handle_b_off() {
  transmit(b_off);
}

void handle_c_on() {
  transmit(c_on);
}

void handle_c_off() {
  transmit(c_off);
}

void handle_d_on() {
  transmit(d_on);
}

void handle_d_off() {
  transmit(d_off);
}

void handleNotFound(){
  digitalWrite(LED_BUILTIN, LOW);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(LED_BUILTIN, HIGH);
}

void setup(void){
  // Setup led
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  pinMode(TX_PIN, OUTPUT);
  digitalWrite(TX_PIN, HIGH);

  // Setup serial
  Serial.begin(115200);

  // Setup Wifi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to wifi ");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/a_on", handle_a_on);
  server.on("/a_off", handle_a_off);
  server.on("/b_on", handle_b_on);
  server.on("/b_off", handle_b_off);
  server.on("/c_on", handle_c_on);
  server.on("/c_off", handle_c_off);
  server.on("/d_on", handle_d_on);
  server.on("/d_off", handle_d_off);

  server.on("/inline", [](){
    server.send(200, "text/plain", "this works as well");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void){
  server.handleClient();
}
