#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "test";
const char* password = "test";

const char* serverUrl = "http://192.168.68.54:7720/data";

int PulseSensorPurplePin = 14;
int Signal;

#define DS18B20_SENSOR_PIN 12 // GPIO 12 (D12) for DS18B20 sensor

OneWire oneWire(DS18B20_SENSOR_PIN); // Setup a oneWire instance to communicate with any OneWire devices
DallasTemperature sensors(&oneWire); // Pass oneWire reference to DallasTemperature library

void setup() {
  Serial.begin(115200);

  pinMode(PulseSensorPurplePin, INPUT);

  sensors.begin(); // Initialize DS18B20 temperature sensor

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  int heartRate = random(70, 81); // Generate random heart rate between 70 and 80

  sensors.requestTemperatures(); // Request temperature readings
  float temperature = sensors.getTempCByIndex(0); // Get temperature in Celsius

  // Print sensor readings
  Serial.print("Heart Rate: ");
  Serial.print(heartRate);
  Serial.print("\tTemperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  // Prepare JSON payload
  String payload = "{\"heartRate\": " + String(heartRate) + ", \"temperature\": " + String(temperature) + "}";

  // Send HTTP POST request
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(payload);
  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);
  http.end();

  delay(2000); // Adjust delay as needed
}