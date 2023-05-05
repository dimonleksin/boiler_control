#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WebServer.h>

#define WIFI_SSID "Beeline_2G_F44659"
#define WIFI_PASS "11235813"
#define ONE_WIRE_BUS 0 // Пин подключения OneWire шины, 0 (D3)
#define CHAT_ID 829921481 //ID My Chat Telegramm
#define TOKEN  //API Token

//int HTTP_PORT = 443
char temperatureCString[6];
String json = "";
String stat = "";
uint8_t boilerStatus = LOW;

DeviceAddress termometr[3];
uint8_t deviceCount = 0;

OneWire oneWire(ONE_WIRE_BUS); // Подключаем бибилотеку OneWire
// передаем объект oneWire объекту DS18B20: 
DallasTemperature DS18B20(&oneWire);

ESP8266WebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("Connected, ");
  Serial.println(WiFi.localIP());

  delay(10);
  
  DS18B20.begin();

//Адресса термометров
  deviceCount = DS18B20.getDeviceCount();
  float tempSensor1, tempSensor2, tempSensor3;
  Serial.print("Обнаруженно датчиков");
  Serial.println(deviceCount);
  Serial.println("HTTP server started");
  //Отправка температуры
  server.on("/temp", getTemperature);
  //Отправка состояние бойлера
  server.on("/status", getBoilerStatus);
  server.on("/setstatus/1", setBoilerStatusOne);
  server.on("/setstatus/0", setBoilerStatusZero);
  server.begin();
  //Настройка пина для реле
  pinMode(4, OUTPUT);
  digitalWrite(4, boilerStatus);
}
void getTemperature() {
  DS18B20.requestTemperatures();
  Serial.println(DS18B20.getTempCByIndex(0));
  Serial.println(DS18B20.getTempCByIndex(1));
  json = "{\"tempBoiler\": \"";
  json += DS18B20.getTempCByIndex(0);
  json += "\", ";
  json += "\"tempHouse\": \"";
  json += DS18B20.getTempCByIndex(1);
  json += "\", ";
  json += "\"tempOutside\": \"";
  json += DS18B20.getTempCByIndex(2);
  json += "\"}";
  server.send(200, "application/json", json);
}
void getBoilerStatus() {
  if(boilerStatus){
    stat = "{\"boilerStatus\": \"Котел включен\"}";
    Serial.print("Cтатус бойлера: ");
    Serial.print(boilerStatus);
    Serial.println(stat);
    server.send(200, "application/json", stat);
  }
  else {
    stat = "{\"boilerStatus\": \"Котел выключен\"}";
    Serial.print("Cтатус бойлера: ");
    Serial.print(boilerStatus);
    Serial.println(stat);
    server.send(200, "application/json", stat);
  }
}
void setBoilerStatusOne() {
  if (!boilerStatus) {
    boilerStatus = HIGH;
    digitalWrite(4, boilerStatus);
    Serial.println("Статус котла изменен на Вкл");
    getBoilerStatus();
  }
  else {
    Serial.print(boilerStatus);
    server.send(200, "application/json", "{\"boilerStatus\": \"Котел уже включен\"}");
  }
}

void setBoilerStatusZero() {
  if (boilerStatus) {
    boilerStatus = LOW;
    digitalWrite(4, boilerStatus);
    Serial.println("Статус котла изменен на Выкл");
    getBoilerStatus();
  }
  else {
    Serial.print(boilerStatus);
    server.send(200, "application/json", "{\"boilerStatus\": \"Котел уже выключен\"}");
  }
}
//Function for send Alarm to telegramm
void AlarmTemp() {
  DS18B20.requestTemperatures();
  float temp_boiler = DS18B20.getTempCByIndex(0);
  float temp_house = DS18B20.getTempCByIndex(1);
  if(client.connect(api.telegram.org:443)){
    if(temp_boiler > 70.0) {
      client.println("GET " + "bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=Temperature Boiler Up to " + String(temp_boiler);
      client.println("Host: api.telegram.org");
      client.println("Connection: close");
      client.println();
    }
    if(temp_house < 5.0) {
      client.println("GET " + "bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=Temperature House Down to " + String(temp_house);
      client.println("Host: api.telegram.org");
      client.println("Connection: close");
      client.println();
  }
  else {
    Serial.println("Not connect to server")
  }
}
void loop() {
  server.handleClient();
  AlarmTemp();
}
