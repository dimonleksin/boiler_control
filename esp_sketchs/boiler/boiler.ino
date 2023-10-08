#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WebServer.h>
// #include <HttpClient.h>
#include <WiFiClient.h>
// #include <ESP8266HTTPClient.h>

#define WIFI_SSID "Beeline_2G_F44659"
#define WIFI_PASS "pass_to_WiFi"
#define ONE_WIRE_BUS 0 // Пин подключения OneWire шины, 0 (D3)
#define CHAT_ID 829921481 //ID My Chat Telegramm
#define TOKEN  //API Token

//int HTTP_PORT = 443
char temperatureCString[6];
String json = "";
String stat = "";
uint8_t boiler_1_status = LOW;
uint8_t boiler_2_status = LOW;

DeviceAddress termometr[3];
uint8_t deviceCount = 0;

OneWire oneWire(ONE_WIRE_BUS); // Подключаем бибилотеку OneWire
// передаем объект oneWire объекту DS18B20: 
DallasTemperature DS18B20(&oneWire);

ESP8266WebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.hostname("boiler");
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
  server.on("/status-1", getboiler_1_status);
  server.on("/set-1-status/1", setboiler_1_statusOne);
  server.on("/set-1-status/0", setboiler_1_statusZero);
  // server.on("/status-2", getboiler_2_status);
  // server.on("/set-2-status/1", setboiler_2_statusOne);
  // server.on("/set-2-status/0", setboiler_2_statusZero);
  server.begin();
  //Настройка пина для реле
  pinMode(4, OUTPUT);
  digitalWrite(4, boiler_1_status);
  pinMode(5, OUTPUT);
  digitalWrite(5, boiler_2_status);
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
void getboiler_1_status() {
  if(boiler_1_status){
    stat = "{\"boiler_1_status\": \"Котел включен\"}";
    Serial.print("Cтатус бойлера: ");
    Serial.print(boiler_1_status);
    Serial.println(stat);
    server.send(200, "application/json", stat);
  }
  else {
    stat = "{\"boiler_1_status\": \"Котел выключен\"}";
    Serial.print("Cтатус бойлера: ");
    Serial.print(boiler_1_status);
    Serial.println(stat);
    server.send(200, "application/json", stat);
  }
}

// void getboiler_2_status() {
//   if(boiler_2_status){
//     stat = "{\"boiler_2_status\": \"Котел включен\"}";
//     Serial.print("Cтатус бойлера: ");
//     Serial.print(boiler_2_status);
//     Serial.println(stat);
//     server.send(200, "application/json", stat);
//   }
//   else {
//     stat = "{\"boiler_2_status\": \"Котел выключен\"}";
//     Serial.print("Cтатус бойлера: ");
//     Serial.print(boiler_2_status);
//     Serial.println(stat);
//     server.send(200, "application/json", stat);
//   }
// }

void setboiler_1_statusOne() {
  if (!boiler_1_status) {
    boiler_1_status = HIGH;
    digitalWrite(4, boiler_1_status);
    Serial.println("Статус котла изменен на Вкл");
    getboiler_1_status();
  }
  else {
    Serial.print(boiler_1_status);
    server.send(200, "application/json", "{\"boiler_1_status\": \"Котел уже включен\"}");
  }
}

// void setboiler_2_statusOne() {
//   if (!boiler_2_status) {
//     boiler_1_status = HIGH;
//     digitalWrite(5, boiler_1_status);
//     Serial.println("Статус котла изменен на Вкл");
//     getboiler_2_status();
//   }
//   else {
//     Serial.print(boiler_2_status);
//     server.send(200, "application/json", "{\"boiler_2_status\": \"Котел уже включен\"}");
//   }
// }


void setboiler_1_statusZero() {
  if (boiler_1_status) {
    boiler_1_status = LOW;
    digitalWrite(4, boiler_1_status);
    Serial.println("Статус котла изменен на Выкл");
    getboiler_1_status();
  }
  else {
    Serial.print(boiler_1_status);
    server.send(200, "application/json", "{\"boiler_1_status\": \"Котел уже выключен\"}");
  }
}
//Function for send Alarm to telegramm???

void loop() {
  server.handleClient();
}
