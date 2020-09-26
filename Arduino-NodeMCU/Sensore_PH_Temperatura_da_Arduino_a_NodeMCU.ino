#include <SoftwareSerial.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2 // Data wire is conn0ect to the Arduino digital pin 2

#define SensorPin 0          //pH meter Analog output to Arduino Analog Input 0
unsigned long int avgValue;  //Store the average value of the sensor feedback
float b;
int buf[10], temp;
OneWire oneWire(ONE_WIRE_BUS);// Setup a oneWire instance to communicate with any OneWire devices
DallasTemperature sensors(&oneWire);// Pass our oneWire reference to Dallas Temperature sensor 
SoftwareSerial espSerial(5, 6);

//INFORMAZIONI UTENTE
//String username = "Luca0079";
//String username = "TestUser";
String username = "Alessandro1996";
String psw = "gestorepiscina1";
int n_piscina = 1;
int minutes = 10;
unsigned long one_minute = 10000;

void setup(){
  pinMode(13,OUTPUT);  
  Serial.begin(9600);
  espSerial.begin(9600);  
  sensors.begin();
  delay(2000);
}

void loop(){
  float tmpT = 0;
  float tmpPH = 0;
  avg(&tmpT, &tmpPH);
  String postData = "temperature=" + String(tmpT)+"&ph="+ String(tmpPH)+"&user="+ username+"&password="+ psw+"&n_piscina="+String(n_piscina);
  Serial.print(postData);
  espSerial.println(postData);   
  delay(100);
  digitalWrite(13, LOW); 
}

float avg(float *tmpT, float *tmpPH){
  
  for (int k = 0; k < minutes; k++){
    //TEMPERATURE
    sensors.requestTemperatures(); // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
    float t = sensors.getTempCByIndex(0);
    Serial.println(" Celsius temperature: ");
    Serial.print(t); 
    Serial.print(" Fahrenheit temperature: ");
    Serial.print(sensors.getTempFByIndex(0));
    *tmpT += t;
    
    //PH
    for(int i=0;i<10;i++)       //Get 10 sample value from the sensor for smooth the value
    { 
      buf[i]=analogRead(SensorPin);
      delay(10);
    }
    for(int i=0;i<9;i++){        //sort the analog from small to large
      for(int j=i+1;j<10;j++){
        if(buf[i]>buf[j]){
          temp=buf[i];
          buf[i]=buf[j];
          buf[j]=temp;
        }
      }
    }
    avgValue=0;
    for(int i=2;i<8;i++)                      //take the average value of 6 center sample
      avgValue+=buf[i];
    float phValue=(float)avgValue*5.0/1024/6; //convert the analog into millivolt
    phValue=3.5*phValue; //convert the millivolt into pH value
    Serial.print(" pH:");  
    Serial.print(phValue,2);
    digitalWrite(13, HIGH);
    *tmpPH += phValue;
    
    delay(one_minute);
    Serial.print("");
  }
  *tmpT /= minutes;
  *tmpPH /= minutes;
}
