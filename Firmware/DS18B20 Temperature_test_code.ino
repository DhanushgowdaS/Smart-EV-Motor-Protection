#include <OneWire.h>
#include <DallasTemperature.h>

#define TEMP_PIN 4

OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

void setup() {

  Serial.begin(115200);

  sensors.begin();

  Serial.println("DS18B20 Temperature Sensor Test");

  Serial.print("Sensors found: ");
  Serial.println(sensors.getDeviceCount());
}

void loop() {

  sensors.requestTemperatures();

  float temperature =
      sensors.getTempCByIndex(0);

  Serial.print("Temperature: ");

  if (temperature == DEVICE_DISCONNECTED_C) {

    Serial.println("SENSOR DISCONNECTED");

  } else {

    Serial.print(temperature, 2);
    Serial.println(" °C");
  }

  delay(1000);
}
