
const int VOLTAGE_PIN = 34;

// Common 0–25V voltage sensor module
const float VOLTAGE_RATIO = 5.0;

void setup() {
  Serial.begin(115200);

  analogReadResolution(12);
  analogSetPinAttenuation(VOLTAGE_PIN, ADC_11db);

  Serial.println("Voltage Sensor Test");
}

void loop() {

  long sum = 0;

  for (int i = 0; i < 100; i++) {
    sum += analogReadMilliVolts(VOLTAGE_PIN);
    delayMicroseconds(100);
  }

  float sensorVoltage = (sum / 100.0) / 1000.0;

  float batteryVoltage = sensorVoltage * VOLTAGE_RATIO;

  Serial.print("Sensor Output: ");
  Serial.print(sensorVoltage, 3);
  Serial.print(" V | Battery Voltage: ");
  Serial.print(batteryVoltage, 2);
  Serial.println(" V");

  delay(1000);
}
