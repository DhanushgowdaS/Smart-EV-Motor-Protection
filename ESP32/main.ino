#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <math.h>


// ============================================================
// WIFI CONFIGURATION
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
const int TEMP_PIN    = 4;
const int RELAY_PIN   = 13;


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

const float FAN_ON_TEMP  = 31.0;
const float FAN_OFF_TEMP = 30.0;


// ============================================================
// SIMULATED SPEED SETTINGS
// ============================================================

float speed = 0.0;

const float MAX_SPEED = 45.0;


// ============================================================
// SPEED TIMING
// ============================================================
//
// ON:
// 0 -> 45 km/h in approximately 5 seconds
//
// 45 / 5 = 9 km/h per second
//
// Therefore:
// 1 km/h every approximately 111 ms
//
// OFF:
// 45 -> 0 km/h in approximately 7 seconds
//
// 45 / 7 = 6.43 km/h per second
//
// Therefore:
// 1 km/h every approximately 156 ms
// ============================================================

const unsigned long SPEED_ACCELERATION_INTERVAL = 111;
const unsigned long SPEED_DECELERATION_INTERVAL = 156;


// ============================================================
// RENDER SEND INTERVAL
// ============================================================

const unsigned long SEND_INTERVAL = 500;


// ============================================================
// SPEED TIMER
// ============================================================

unsigned long lastSpeedUpdate = 0;


// ============================================================
// RENDER TIMER
// ============================================================

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


  // ==========================================================
  // ESP32 ADC
  // ==========================================================

  analogReadResolution(12);

  analogSetPinAttenuation(
      VOLTAGE_PIN,
      ADC_11db
  );

  analogSetPinAttenuation(
      CURRENT_PIN,
      ADC_11db
  );


  // ==========================================================
  // DS18B20
  // ==========================================================

  sensors.begin();


  // ==========================================================
  // RELAY
  // ==========================================================

  pinMode(
      RELAY_PIN,
      OUTPUT
  );


  // Active LOW relay
  // HIGH = FAN OFF

  digitalWrite(
      RELAY_PIN,
      HIGH
  );


  delay(2000);


  // ==========================================================
  // START MESSAGE
  // ==========================================================

  Serial.println();
  Serial.println("==========================================");
  Serial.println("       EV MOTOR PROTECTION SYSTEM");
  Serial.println("==========================================");
  Serial.println();


  // ==========================================================
  // TEMPERATURE SENSOR CHECK
  // ==========================================================

  Serial.print(
      "Temperature Sensors Found: "
  );

  Serial.println(
      sensors.getDeviceCount()
  );

  Serial.println();


  // ==========================================================
  // LEARN BASE CURRENT
  // ==========================================================

  Serial.println(
      "Learning normal motor current..."
  );

  double currentSum = 0;


  for (int i = 0; i < 2000; i++) {

    currentSum +=
        analogReadMilliVolts(
            CURRENT_PIN
        );

    delayMicroseconds(100);
  }


  float currentVoltage =
      (currentSum / 2000.0) / 1000.0;


  baseCurrent =
      fabs(
          (currentVoltage - CURRENT_ZERO)
          / CURRENT_SENSITIVITY
      );


  previousCurrent =
      baseCurrent;


  // ==========================================================
  // INITIAL TEMPERATURE
  // ==========================================================

  sensors.requestTemperatures();


  previousTemperature =
      sensors.getTempCByIndex(0);


  // ==========================================================
  // PRINT INITIAL VALUES
  // ==========================================================

  Serial.print(
      "Base Current : "
  );

  Serial.print(
      baseCurrent,
      3
  );

  Serial.println(" A");


  Serial.print(
      "Initial Temp : "
  );

  Serial.print(
      previousTemperature,
      2
  );

  Serial.println(" C");

  Serial.println();


  // ==========================================================
  // CONNECT WIFI
  // ==========================================================

  Serial.println(
      "Connecting to WiFi..."
  );


  WiFi.begin(
      WIFI_SSID,
      WIFI_PASSWORD
  );


  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");
  }


  Serial.println();

  Serial.println(
      "WiFi Connected!"
  );


  Serial.print(
      "IP Address: "
  );

  Serial.println(
      WiFi.localIP()
  );


  Serial.println();


  // ==========================================================
  // MONITORING STARTED
  // ==========================================================

  Serial.println(
      "Monitoring Started..."
  );

  Serial.println();


  // Start timers

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

    sum +=
        analogReadMilliVolts(
            CURRENT_PIN
        );

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


// ============================================================
// READ BATTERY VOLTAGE
// ============================================================

float readVoltage() {

  double sum = 0;

  const int samples = 100;


  for (int i = 0; i < samples; i++) {

    sum +=
        analogReadMilliVolts(
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
// UPDATE SIMULATED SPEED
// ============================================================
//
// Speed is updated independently from Render.
//
// ON:
// 1 km/h every 111 ms
//
// OFF:
// 1 km/h every 156 ms
//
// This gives approximately:
//
// 0 -> 45 = 5 seconds
//
// 45 -> 0 = 7 seconds
// ============================================================

void updateSpeed(bool systemON) {

  unsigned long currentMillis = millis();


  unsigned long interval;


  if (systemON) {

    interval =
        SPEED_ACCELERATION_INTERVAL;
  }

  else {

    interval =
        SPEED_DECELERATION_INTERVAL;
  }


  if (
      currentMillis - lastSpeedUpdate
      >= interval
  ) {

    lastSpeedUpdate =
        currentMillis;


    // ========================================================
    // SYSTEM ON
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
    // SYSTEM OFF
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


  // ==========================================================
  // CHECK WIFI
  // ==========================================================

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println(
        "WiFi disconnected!"
    );

    return;
  }


  // ==========================================================
  // HTTP CLIENT
  // ==========================================================

  HTTPClient http;


  Serial.println(
      "Connecting to Render..."
  );


  http.begin(
      SERVER_URL
  );


  http.addHeader(
      "Content-Type",
      "application/json"
  );


  // ==========================================================
  // JSON DATA
  // ==========================================================

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


  // ==========================================================
  // PRINT JSON
  // ==========================================================

  Serial.println();

  Serial.println(
      "Sending data:"
  );

  Serial.println(
      jsonData
  );


  // ==========================================================
  // POST DATA
  // ==========================================================

  int httpResponseCode =
      http.POST(
          jsonData
      );


  Serial.print(
      "HTTP Response Code: "
  );

  Serial.println(
      httpResponseCode
  );


  // ==========================================================
  // SERVER RESPONSE
  // ==========================================================

  if (httpResponseCode > 0) {

    String response =
        http.getString();


    Serial.print(
        "Server Response: "
    );

    Serial.println(
        response
    );
  }


  // ==========================================================
  // CLOSE HTTP
  // ==========================================================

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
  //
  // Motor current > 0.05 A = SYSTEM ON
  //
  // Motor current <= 0.05 A = SYSTEM OFF
  // ==========================================================

  bool systemON;


  if (current > 0.05) {

    systemON = true;
  }

  else {

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

    currentTrend =
        "INCREASING";
  }

  else if (
      current <
      previousCurrent - CURRENT_CHANGE
  ) {

    currentTrend =
        "DECREASING";
  }

  else {

    currentTrend =
        "STABLE";
  }


  // ==========================================================
  // TEMPERATURE TREND
  // ==========================================================

  String temperatureTrend;


  if (
      temperature >
      previousTemperature + TEMP_CHANGE
  ) {

    temperatureTrend =
        "INCREASING";
  }

  else if (
      temperature <
      previousTemperature - TEMP_CHANGE
  ) {

    temperatureTrend =
        "DECREASING";
  }

  else {

    temperatureTrend =
        "STABLE";
  }


  // ==========================================================
  // LOAD STATUS
  // ==========================================================

  String loadStatus;


  if (
      currentTrend ==
      "INCREASING"
  ) {

    loadStatus =
        "LOAD INCREASING";
  }

  else if (
      currentTrend ==
      "DECREASING"
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
      temperature >=
      FAN_ON_TEMP
  ) {

    fanON = true;
  }

  else if (
      temperature <=
      FAN_OFF_TEMP
  ) {

    fanON = false;
  }


  // ==========================================================
  // RELAY CONTROL
  // ==========================================================

  if (fanON) {

    // Active LOW relay

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
  // MOTOR PROTECTION STATUS
  // ==========================================================

  String protectionStatus;


  if (
      temperature >=
      FAN_ON_TEMP
  ) {

    protectionStatus =
        "COOLING ACTIVE";
  }

  else if (
      currentTrend ==
      "INCREASING"
  ) {

    protectionStatus =
        "LOAD RISING";
  }

  else {

    protectionStatus =
        "NORMAL";
  }


  // ==========================================================
  // MOTOR STATUS
  // ==========================================================

  String motorStatus;


  if (systemON) {

    motorStatus =
        "ON";
  }

  else {

    motorStatus =
        "OFF";
  }


  // ==========================================================
  // UPDATE SPEED
  // ==========================================================

  updateSpeed(
      systemON
  );


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

    Serial.println(
        "ON"
    );
  }

  else {

    Serial.println(
        "OFF"
    );
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

    Serial.println(
        "ON"
    );
  }

  else {

    Serial.println(
        "OFF"
    );
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
  // SEND TO RENDER EVERY 500 ms
  // ==========================================================

  unsigned long currentMillis = millis();


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


  // ==========================================================
  // SMALL LOOP DELAY
  // ==========================================================

  delay(10);
}
