#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>

HTTPClient http;
//const char *ssid =  "Telecom-86544019";  
//const char *pass =  "NP0b3WlhtjWadSHRskMVeNSL";
const char *ssid = "TIM-22964249 2.4 Ghz";
const char *pass = "jOPypTckT9UsCLWXwBXBAgFN";

WiFiClient client;
 
void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  delay(10);               
  Serial.println("Connecting to ");
  Serial.println(ssid); 

  WiFi.begin(ssid, pass); 
  while (WiFi.status() != WL_CONNECTED) 
     {
        delay(500);
        Serial.print(".");
      } 
  Serial.println("");
  Serial.println("WiFi connected");
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() { // run over and over
  if (Serial.available() and WiFi.status() == WL_CONNECTED) {
    http.begin("http://gestorepiscine.herokuapp.com/logout/");
    String postData = Serial.readString();
    postData.trim();                     //clean input data
    Serial.println(postData);
    http.begin("http://gestorepiscine.herokuapp.com/piscina_request/");   
    http.addHeader("Content-Type", "application/x-www-form-urlencoded"); 
    int httpCode = http.POST(postData);   //Send the request
    String payload = http.getString();    //Get the response payload
    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload
    http.end();  //Close connection
  }
}
