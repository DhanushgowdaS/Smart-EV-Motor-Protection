#include <OneWire.h>
#include <DallasTemperature.h>

// =================================================
// PIN CONFIGURATION
// =================================================

const int VOLTAGE_PIN = 34;
const int CURRENT_PIN = 35;
const int TEMP_PIN    = 4;
const int RELAY_PIN   = 13;


// =================================================
// DS18B20
// =================================================

OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);


// =================================================
// ACS712-30A
// =================================================

const float CURRENT_ZERO = 2.5605;
const float CURRENT_SENSITIVITY = 0.066;


// =================================================
// VOLTAGE SENSOR
// =================================================

const float VOLTAGE_RATIO = 5.0;


// =================================================
// TREND SETTINGS
// =================================================

const float CURRENT_CHANGE = 0.03;  // A
const float TEMP_CHANGE = 0.3;      // °C


// =================================================
// FAN TEMPERATURE SETTINGS
// =================================================

const float FAN_ON_TEMP  = 31.0;
const float FAN_OFF_TEMP = 30.0;


// =================================================
// VARIABLES
// =================================================

float baseCurrent = 0;

float previousCurrent = 0;
float previousTemperature = 0;


// =================================================
// SETUP
// =================================================

void setup() {

  Serial.begin(115200);

  // ESP32 ADC
  analogReadResolution(12);

  analogSetPinAttenuation(VOLTAGE_PIN, ADC_11db);
  analogSetPinAttenuation(CURRENT_PIN, ADC_11db);

  // DS18B20
  sensors.begin();

  // Relay
  pinMode(RELAY_PIN, OUTPUT);

  // Active LOW relay
  // HIGH = FAN OFF
  digitalWrite(RELAY_PIN, HIGH);

  delay(2000);

  Serial.println();
  Serial.println("==========================================");
  Serial.println("       EV MOTOR PROTECTION SYSTEM");
  Serial.println("==========================================");
  Serial.println();

  // Check temperature sensor

  Serial.print("Temperature Sensors Found: ");
  Serial.println(sensors.getDeviceCount());

  Serial.println();

  // =================================================
  // LEARN BASE CURRENT
  // =================================================

  Serial.println("Learning normal motor current...");

  double currentSum = 0;

  for (int i = 0; i < 2000; i++) {

    currentSum += analogReadMilliVolts(CURRENT_PIN);

    delayMicroseconds(100);
  }

  float currentVoltage =
      (currentSum / 2000.0) / 1000.0;

  baseCurrent =
      fabs(
        (currentVoltage - CURRENT_ZERO)
        / CURRENT_SENSITIVITY
      );

  previousCurrent = baseCurrent;


  // =================================================
  // INITIAL TEMPERATURE
  // =================================================

  sensors.requestTemperatures();

  previousTemperature =
      sensors.getTempCByIndex(0);


  Serial.print("Base Current : ");
  Serial.print(baseCurrent, 3);
  Serial.println(" A");

  Serial.print("Initial Temp : ");
  Serial.print(previousTemperature, 2);
  Serial.println(" C");

  Serial.println();
  Serial.println("Monitoring Started...");
  Serial.println();
}


// =================================================
// READ CURRENT
// =================================================

float readCurrent() {

  double sum = 0;

  const int samples = 500;

  for (int i = 0; i < samples; i++) {

    sum += analogReadMilliVolts(CURRENT_PIN);

    delayMicroseconds(100);
  }

  float sensorVoltage =
      (sum / samples) / 1000.0;

  float current =
      (sensorVoltage - CURRENT_ZERO)
      / CURRENT_SENSITIVITY;

  current = fabs(current);

  // Remove tiny noise

  if (current < 0.03) {
    current = 0;
  }

  return current;
}


// =================================================
// READ BATTERY VOLTAGE
// =================================================

float readVoltage() {

  double sum = 0;

  const int samples = 100;

  for (int i = 0; i < samples; i++) {

    sum += analogReadMilliVolts(VOLTAGE_PIN);

    delayMicroseconds(100);
  }

  float sensorVoltage =
      (sum / samples) / 1000.0;

  float actualVoltage =
      sensorVoltage * VOLTAGE_RATIO;

  return actualVoltage;
}


// =================================================
// READ TEMPERATURE
// =================================================

float readTemperature() {

  sensors.requestTemperatures();

  float temperature =
      sensors.getTempCByIndex(0);

  return temperature;
}


// =================================================
// MAIN LOOP
// =================================================

void loop() {

  // =================================================
  // READ SENSORS
  // =================================================

  float current = readCurrent();

  float batteryVoltage = readVoltage();

  float temperature = readTemperature();


  // =================================================
  // CURRENT TREND
  // =================================================

  String currentTrend;

  if (current >
      previousCurrent + CURRENT_CHANGE) {

    currentTrend = "INCREASING";

  }

  else if (current <
           previousCurrent - CURRENT_CHANGE) {

    currentTrend = "DECREASING";

  }

  else {

    currentTrend = "STABLE";
  }


  // =================================================
  // TEMPERATURE TREND
  // =================================================

  String temperatureTrend;

  if (temperature >
      previousTemperature + TEMP_CHANGE) {

    temperatureTrend = "INCREASING";

  }

  else if (temperature <
           previousTemperature - TEMP_CHANGE) {

    temperatureTrend = "DECREASING";

  }

  else {

    temperatureTrend = "STABLE";
  }


  // =================================================
  // LOAD STATUS
  // =================================================
  //
  // IMPORTANT:
  // Load status is based ONLY on current trend.
  //
  // Temperature is handled separately.
  //

  String loadStatus;

  if (currentTrend == "INCREASING") {

    loadStatus = "LOAD INCREASING";

  }

  else if (currentTrend == "DECREASING") {

    loadStatus = "LOAD DECREASING";

  }

  else {

    loadStatus = "LOAD STABLE";
  }


  // =================================================
  // FAN CONTROL
  // =================================================

  bool fanON = false;

  // Temperature protection

  if (temperature >= FAN_ON_TEMP) {

    fanON = true;
  }

  else if (temperature <= FAN_OFF_TEMP) {

    fanON = false;
  }


  // Active LOW relay

  if (fanON) {

    digitalWrite(RELAY_PIN, LOW);

  }

  else {

    digitalWrite(RELAY_PIN, HIGH);
  }


  // =================================================
  // MOTOR PROTECTION STATUS
  // =================================================

  String protectionStatus;

  if (temperature >= FAN_ON_TEMP) {

    protectionStatus = "COOLING ACTIVE";

  }

  else if (currentTrend == "INCREASING") {

    protectionStatus = "LOAD RISING";

  }

  else {

    protectionStatus = "NORMAL";
  }


  // =================================================
  // SERIAL MONITOR
  // =================================================

  Serial.println();
  Serial.println("------------------------------------------");

  Serial.print("Battery Voltage : ");
  Serial.print(batteryVoltage, 2);
  Serial.println(" V");

  Serial.print("Motor Current   : ");
  Serial.print(current, 3);
  Serial.println(" A");

  Serial.print("Base Current    : ");
  Serial.print(baseCurrent, 3);
  Serial.println(" A");

  Serial.print("Current Trend   : ");
  Serial.println(currentTrend);

  Serial.print("Motor Temp      : ");
  Serial.print(temperature, 2);
  Serial.println(" C");

  Serial.print("Temp Trend      : ");
  Serial.println(temperatureTrend);

  Serial.print("Load Status     : ");
  Serial.println(loadStatus);

  Serial.print("Cooling Fan     : ");

  if (fanON) {
    Serial.println("ON");
  }

  else {
    Serial.println("OFF");
  }

  Serial.print("System Status   : ");
  Serial.println(protectionStatus);

  Serial.println("------------------------------------------");


  // =================================================
  // SAVE PREVIOUS VALUES
  // =================================================

  previousCurrent = current;

  previousTemperature = temperature;


  delay(1000);
}
