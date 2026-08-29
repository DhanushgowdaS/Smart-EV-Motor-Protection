#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <math.h>

// ============================================================
// WIFI
// ============================================================

const char* WIFI_SSID = "Admin";
const char* WIFI_PASSWORD = "password";

// ============================================================
// RENDER SERVER
// ============================================================

const char* SERVER_URL =
    "https://smart-ev-motor-protection.onrender.com/data";

// ============================================================
// PIN CONFIGURATION
// ============================================================

const int VOLTAGE_PIN = 34;
const int CURRENT_PIN = 35;
const int TEMP_PIN = 4;
const int RELAY_PIN = 13;

// ============================================================
// DS18B20
// ============================================================

OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

// ============================================================
// ACS712-30A
// ============================================================

const float CURRENT_ZERO = 2.5605;
const float CURRENT_SENSITIVITY = 0.066;

// ============================================================
// VOLTAGE SENSOR
// ============================================================

const float VOLTAGE_RATIO = 5.0;

// ============================================================
// TREND SETTINGS
// ============================================================

const float CURRENT_CHANGE = 0.03;
const float TEMP_CHANGE = 0.3;

// ============================================================
// FAN TEMPERATURE SETTINGS
// ============================================================

const float FAN_ON_TEMP = 31.0;
const float FAN_OFF_TEMP = 30.0;

// ============================================================
// CRITICAL TEMPERATURE
// ============================================================

const float CRITICAL_TEMP = 35.0;

// ============================================================
// SPEED
// ============================================================

float speed = 0.0;

const float MAX_SPEED = 45.0;

// 0 → 45 km/h in approximately 5 seconds
const unsigned long SPEED_ACCELERATION_INTERVAL = 111;

// 45 → 0 km/h in approximately 7 seconds
const unsigned long SPEED_DECELERATION_INTERVAL = 156;

// Send data every 100 ms
const unsigned long SEND_INTERVAL = 100;

// ============================================================
// TIMERS
// ============================================================

unsigned long lastSpeedUpdate = 0;
unsigned long lastSendTime = 0;

// ============================================================
// VARIABLES
// ============================================================

float baseCurrent = 0;
float previousCurrent = 0;
float previousTemperature = 0;

// ============================================================
// SETUP
// ============================================================

void setup() {

  Serial.begin(115200);

  // ESP32 ADC
  analogReadResolution(12);

  analogSetPinAttenuation(
      VOLTAGE_PIN,
      ADC_11db
  );

  analogSetPinAttenuation(
      CURRENT_PIN,
      ADC_11db
  );

  // DS18B20
  sensors.begin();

  // Fan relay
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

  // Temperature sensor check
  Serial.print("Temperature Sensors Found: ");
  Serial.println(sensors.getDeviceCount());

  Serial.println();

  // ==========================================================
  // LEARN BASE CURRENT
  // ==========================================================

  Serial.println("Learning normal motor current...");

  double currentSum = 0;

  for (int i = 0; i < 2000; i++) {

    currentSum += analogReadMilliVolts(
        CURRENT_PIN
    );

    delayMicroseconds(100);
  }

  float currentVoltage =
      (currentSum / 2000.0) / 1000.0;

  baseCurrent =
      fabs(
          (currentVoltage - CURRENT_ZERO) /
          CURRENT_SENSITIVITY
      );

  previousCurrent = baseCurrent;

  // ==========================================================
  // INITIAL TEMPERATURE
  // ==========================================================

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

  // ==========================================================
  // WIFI
  // ==========================================================

  Serial.println("Connecting to WiFi...");

  WiFi.begin(
      WIFI_SSID,
      WIFI_PASSWORD
  );

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected!");

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println();

  Serial.println("Monitoring Started...");
  Serial.println();

  lastSpeedUpdate = millis();
  lastSendTime = millis();
}

// ============================================================
// READ CURRENT
// ============================================================

float readCurrent() {

  double sum = 0;

  const int samples = 500;

  for (int i = 0; i < samples; i++) {

    sum += analogReadMilliVolts(
        CURRENT_PIN
    );

    delayMicroseconds(100);
  }

  float sensorVoltage =
      (sum / samples) / 1000.0;

  float current =
      (sensorVoltage - CURRENT_ZERO) /
      CURRENT_SENSITIVITY;

  current = fabs(current);

  // Remove tiny noise
  if (current < 0.03) {
    current = 0;
  }

  return current;
}

// ============================================================
// READ VOLTAGE
// ============================================================

float readVoltage() {

  double sum = 0;

  const int samples = 100;

  for (int i = 0; i < samples; i++) {

    sum += analogReadMilliVolts(
        VOLTAGE_PIN
    );

    delayMicroseconds(100);
  }

  float sensorVoltage =
      (sum / samples) / 1000.0;

  float actualVoltage =
      sensorVoltage * VOLTAGE_RATIO;

  return actualVoltage;
}

// ============================================================
// READ TEMPERATURE
// ============================================================

float readTemperature() {

  sensors.requestTemperatures();

  float temperature =
      sensors.getTempCByIndex(0);

  return temperature;
}

// ============================================================
// UPDATE SPEED
// ============================================================

void updateSpeed(bool systemON) {

  unsigned long currentMillis = millis();

  unsigned long interval;

  if (systemON) {

    interval =
        SPEED_ACCELERATION_INTERVAL;

  } else {

    interval =
        SPEED_DECELERATION_INTERVAL;
  }

  if (
      currentMillis - lastSpeedUpdate
      >= interval
  ) {

    lastSpeedUpdate = currentMillis;

    // ========================================================
    // ACCELERATION
    // ========================================================

    if (systemON) {

      if (speed < MAX_SPEED) {

        speed += 1.0;

        if (speed > MAX_SPEED) {
          speed = MAX_SPEED;
        }
      }
    }

    // ========================================================
    // DECELERATION
    // ========================================================

    else {

      if (speed > 0) {

        speed -= 1.0;

        if (speed < 0) {
          speed = 0;
        }
      }
    }
  }
}

// ============================================================
// SEND DATA TO RENDER
// ============================================================

void sendDataToRender(
    float voltage,
    float current,
    float temperature,
    bool fanON,
    String status,
    bool systemON,
    String currentTrend,
    String temperatureTrend,
    String loadStatus,
    String motorStatus,
    float currentSpeed
) {

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println(
        "WiFi disconnected!"
    );

    return;
  }

  HTTPClient http;

  Serial.println(
      "Connecting to Render..."
  );

  http.begin(SERVER_URL);

  http.addHeader(
      "Content-Type",
      "application/json"
  );

  String jsonData =
      "{"
      "\"voltage\":" +
      String(voltage, 2) +

      ",\"current\":" +
      String(current, 2) +

      ",\"temperature\":" +
      String(temperature, 2) +

      ",\"fan\":" +
      String(fanON ? "true" : "false") +

      ",\"status\":\"" +
      status +
      "\"" +

      ",\"system\":" +
      String(systemON ? "true" : "false") +

      ",\"current_trend\":\"" +
      currentTrend +
      "\"" +

      ",\"temperature_trend\":\"" +
      temperatureTrend +
      "\"" +

      ",\"load_status\":\"" +
      loadStatus +
      "\"" +

      ",\"motor_status\":\"" +
      motorStatus +
      "\"" +

      ",\"speed\":" +
      String(currentSpeed, 0) +

      "}";

  Serial.println();
  Serial.println(
      "Sending data:"
  );

  Serial.println(jsonData);

  int httpResponseCode =
      http.POST(jsonData);

  Serial.print(
      "HTTP Response Code: "
  );

  Serial.println(
      httpResponseCode
  );

  if (httpResponseCode > 0) {

    String response =
        http.getString();

    Serial.print(
        "Server Response: "
    );

    Serial.println(response);
  }

  http.end();
}

// ============================================================
// MAIN LOOP
// ============================================================

void loop() {

  // ==========================================================
  // READ SENSORS
  // ==========================================================

  float current =
      readCurrent();

  float batteryVoltage =
      readVoltage();

  float temperature =
      readTemperature();

  // ==========================================================
  // SYSTEM ON / OFF
  // ==========================================================

  bool systemON;

  if (current > 0.05) {

    systemON = true;

  } else {

    systemON = false;
  }

  // ==========================================================
  // CURRENT TREND
  // ==========================================================

  String currentTrend;

  if (
      current >
      previousCurrent + CURRENT_CHANGE
  ) {

    currentTrend = "INCREASING";

  }

  else if (
      current <
      previousCurrent - CURRENT_CHANGE
  ) {

    currentTrend = "DECREASING";

  }

  else {

    currentTrend = "STABLE";
  }

  // ==========================================================
  // TEMPERATURE TREND
  // ==========================================================

  String temperatureTrend;

  if (
      temperature >
      previousTemperature + TEMP_CHANGE
  ) {

    temperatureTrend = "INCREASING";

  }

  else if (
      temperature <
      previousTemperature - TEMP_CHANGE
  ) {

    temperatureTrend = "DECREASING";

  }

  else {

    temperatureTrend = "STABLE";
  }

  // ==========================================================
  // LOAD STATUS
  // ==========================================================

  String loadStatus;

  if (
      currentTrend == "INCREASING"
  ) {

    loadStatus =
        "LOAD INCREASING";

  }

  else if (
      currentTrend == "DECREASING"
  ) {

    loadStatus =
        "LOAD DECREASING";

  }

  else {

    loadStatus =
        "LOAD STABLE";
  }

  // ==========================================================
  // FAN CONTROL
  // ==========================================================

  bool fanON = false;

  if (
      temperature >= FAN_ON_TEMP
  ) {

    fanON = true;

  }

  else if (
      temperature <= FAN_OFF_TEMP
  ) {

    fanON = false;
  }

  // Active LOW relay
  if (fanON) {

    digitalWrite(
        RELAY_PIN,
        LOW
    );

  }

  else {

    digitalWrite(
        RELAY_PIN,
        HIGH
    );
  }

  // ==========================================================
  // PROTECTION STATUS
  // ==========================================================

  String protectionStatus;

  // 35°C or above = CRITICAL
  if (
      temperature >= CRITICAL_TEMP
  ) {

    protectionStatus =
        "CRITICAL";
  }

  // 31°C to below 35°C = WARNING
  else if (
      temperature >= FAN_ON_TEMP
  ) {

    protectionStatus =
        "WARNING";
  }

  // Below 31°C = NORMAL
  else {

    protectionStatus =
        "NORMAL";
  }

  // ==========================================================
  // MOTOR STATUS
  // ==========================================================

  String motorStatus;

  if (systemON) {

    motorStatus = "ON";

  } else {

    motorStatus = "OFF";
  }

  // ==========================================================
  // SPEED
  // ==========================================================

  updateSpeed(systemON);

  // ==========================================================
  // SERIAL MONITOR
  // ==========================================================

  Serial.println();

  Serial.println(
      "------------------------------------------"
  );

  Serial.print(
      "System : "
  );

  if (systemON) {

    Serial.println("ON");

  } else {

    Serial.println("OFF");
  }

  Serial.print(
      "Battery Voltage : "
  );

  Serial.print(
      batteryVoltage,
      2
  );

  Serial.println(" V");

  Serial.print(
      "Motor Current   : "
  );

  Serial.print(
      current,
      3
  );

  Serial.println(" A");

  Serial.print(
      "Motor Temp      : "
  );

  Serial.print(
      temperature,
      2
  );

  Serial.println(" C");

  Serial.print(
      "Cooling Fan     : "
  );

  if (fanON) {

    Serial.println("ON");

  } else {

    Serial.println("OFF");
  }

  Serial.print(
      "System Status   : "
  );

  Serial.println(
      protectionStatus
  );

  Serial.print(
      "Speed           : "
  );

  Serial.print(
      speed,
      0
  );

  Serial.println(
      " km/h"
  );

  Serial.println(
      "------------------------------------------"
  );

  // ==========================================================
  // SEND DATA
  // ==========================================================

  unsigned long currentMillis =
      millis();

  if (
      currentMillis - lastSendTime
      >= SEND_INTERVAL
  ) {

    lastSendTime =
        currentMillis;

    sendDataToRender(
        batteryVoltage,
        current,
        temperature,
        fanON,
        protectionStatus,
        systemON,
        currentTrend,
        temperatureTrend,
        loadStatus,
        motorStatus,
        speed
    );
  }

  // ==========================================================
  // SAVE PREVIOUS VALUES
  // ==========================================================

  previousCurrent =
      current;

  previousTemperature =
      temperature;

  delay(10);
}
