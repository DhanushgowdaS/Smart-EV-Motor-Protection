const int CURRENT_PIN = 35;

const float ZERO_VOLTAGE = 2.5605;
const float SENSITIVITY = 0.066;   // ACS712-30A = 66mV/A

void setup() {

  Serial.begin(115200);

  analogReadResolution(12);
  analogSetPinAttenuation(CURRENT_PIN, ADC_11db);

  Serial.println("ACS712 Current Sensor Test");
}

void loop() {

  double sum = 0;

  const int samples = 2000;

  for (int i = 0; i < samples; i++) {

    sum += analogReadMilliVolts(CURRENT_PIN);

    delayMicroseconds(100);
  }

  float sensorVoltage =
      (sum / samples) / 1000.0;

  float current =
      (sensorVoltage - ZERO_VOLTAGE)
      / SENSITIVITY;

  current = fabs(current);

  if (current < 0.03) {
    current = 0;
  }

  Serial.print("Sensor Voltage: ");
  Serial.print(sensorVoltage, 4);

  Serial.print(" V | Current: ");
  Serial.print(current, 3);

  Serial.println(" A");

  delay(500);
}
