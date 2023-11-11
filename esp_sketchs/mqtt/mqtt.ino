#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WebServer.h>
#include <PubSubClient.h>
#include <WiFiClient.h>

#include "config.h"
#include "functions.h"

char temperatureCString[6];

uint8_t boiler_1_status = LOW;
uint8_t boiler_2_status = LOW;

DeviceAddress termometr[3];
uint8_t deviceCount = 0;

OneWire oneWire(ONE_WIRE_BUS); // Подключаем бибилотеку OneWire
// передаем объект oneWire объекту DS18B20:

DallasTemperature DS18B20(&oneWire);

// Функция получения данных от сервера

void callback(const MQTT::Publish& pub){
  Serial.print(pub.topic()); // выводим в сериал порт название топика
  Serial.print(" => ");
  Serial.print(pub.payload_string()); // выводим в сериал порт значение полученных данных

  String payload = pub.payload_string();

  if(String(pub.topic()) == "test/led") // проверяем из нужного ли нам топика пришли данные
  {
    int stled = payload.toInt(); // преобразуем полученные данные в тип integer
    digitalWrite(5,stled); // включаем или выключаем светодиод в зависимоти от полученных значений данных
  }
}

WiFiClient wclient;
PubSubClient client(wclient, mqtt_server, mqtt_port);

void setup() {
  delay(10);
  Serial.begin(115200);
  WiFi.hostname("boiler");
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.print("Connected, ");
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.macAddress());

  delay(10);
  
  DS18B20.begin();

//Адресса термометров
  deviceCount = DS18B20.getDeviceCount();
  float tempSensor1, tempSensor2, tempSensor3;
  Serial.print("Обнаруженно датчиков");
  Serial.println(deviceCount);
  Serial.println("HTTP server started");
 
  //Настройка пина для реле
  pinMode(4, OUTPUT);
  digitalWrite(4, boiler_1_status);
  pinMode(5, OUTPUT);
  digitalWrite(5, boiler_2_status);
}

void loop() {
  // подключаемся к wi-fi
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to ");
    Serial.print(ssid);
    Serial.println("...");
    WiFi.begin(ssid, pass);
  }
  // подключаемся к MQTT серверу
  if (WiFi.status() == WL_CONNECTED) {
    if (!client.connected()) {
      Serial.println("Connecting to MQTT server");
      if (client.connect(MQTT::Connect("boilerroom"))) {
        Serial.println("Connected to MQTT server");
        client.set_callback(callback);
        client.subscribe(BOILER_ONE);
        client.subscribe(BOILER_TWO); // подписывааемся по топик с данными для светодиода
      }  
      else {
        Serial.println("Could not connect to MQTT server");
      }
    } 

  if (client.connected()){
    client.loop();
    TempSend();
  }

  }
  // Функция отправки показаний с термодатчика
}

void getTemperature() {
  DS18B20.requestTemperatures();
  // Serial.println(DS18B20.getTempCByIndex(0));
  // Serial.println(DS18B20.getTempCByIndex(1));
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
    stat = "{\"boiler_1_status\": \"Boiler is on\"}";
    // Serial.print("Cтатус бойлера: ");
    // Serial.print(boiler_1_status);
    // Serial.println(stat);
    server.send(200, "application/json", stat);
  }
  else {
    stat = "{\"boiler_1_status\": \"Boiler is off\"}";
    // Serial.print("Cтатус бойлера: ");
    // Serial.print(boiler_1_status);
    // Serial.println(stat);
    server.send(200, "application/json", stat);
  }
}

void setboiler_1_statusOne() {
  if (!boiler_1_status) {
    boiler_1_status = HIGH;
    digitalWrite(4, boiler_1_status);
    // Serial.println("Статус котла изменен на Вкл");
    getboiler_1_status();
  }
  else {
    // Serial.print(boiler_1_status);
    server.send(200, "application/json", "{\"boiler_1_status\": \"Boiler is already on\"}");
  }
}

void setboiler_1_statusZero() {
  if (boiler_1_status) {
    boiler_1_status = LOW;
    digitalWrite(4, boiler_1_status);
    Serial.println("Статус котла изменен на Выкл");
    getboiler_1_status();
  }
  else {
    Serial.print(boiler_1_status);
    server.send(200, "application/json", "{\"boiler_1_status\": \"Boiler is already off\"}");
  }
}
