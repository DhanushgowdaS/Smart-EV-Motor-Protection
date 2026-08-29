#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// =================================================
// WIFI CONFIGURATION
// =================================================

const char* WIFI_SSID = "Admin";
const char* WIFI_PASSWORD = "password";

// Render API endpoint
const char* SERVER_URL =
    "https://smart-ev-motor-protection.onrender.com/data";


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

const float CURRENT_CHANGE = 0.03;
const float TEMP_CHANGE = 0.3;


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
// WIFI CONNECTION
// =================================================

void connectWiFi() {

  Serial.println();
  Serial.println("Connecting to WiFi...");

  WiFi.begin(
    WIFI_SSID,
    WIFI_PASSWORD
  );

  int attempts = 0;

  while (
    WiFi.status() != WL_CONNECTED &&
    attempts < 30
  ) {

    delay(500);

    Serial.print(".");

    attempts++;
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {

    Serial.println("WiFi Connected!");

    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

  }

  else {

    Serial.println("WiFi Connection Failed!");

  }
}


// =================================================
// SETUP
// =================================================

void setup() {

  Serial.begin(115200);

  // =================================================
  // ESP32 ADC
  // =================================================

  analogReadResolution(12);

  analogSetPinAttenuation(
    VOLTAGE_PIN,
    ADC_11db
  );

  analogSetPinAttenuation(
    CURRENT_PIN,
    ADC_11db
  );


  // =================================================
  // DS18B20
  // =================================================

  sensors.begin();


  // =================================================
  // RELAY
  // =================================================

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


  // =================================================
  // SYSTEM START MESSAGE
  // =================================================

  Serial.println();
  Serial.println("==========================================");
  Serial.println("       EV MOTOR PROTECTION SYSTEM");
  Serial.println("==========================================");
  Serial.println();


  // =================================================
  // CHECK TEMPERATURE SENSOR
  // =================================================

  Serial.print(
    "Temperature Sensors Found: "
  );

  Serial.println(
    sensors.getDeviceCount()
  );

  Serial.println();


  // =================================================
  // LEARN BASE CURRENT
  // =================================================

  Serial.println(
    "Learning normal motor current..."
  );

  double currentSum = 0;


  for (
    int i = 0;
    i < 2000;
    i++
  ) {

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
        (
          currentVoltage
          - CURRENT_ZERO
        )
        / CURRENT_SENSITIVITY
      );


  previousCurrent =
      baseCurrent;


  // =================================================
  // INITIAL TEMPERATURE
  // =================================================

  sensors.requestTemperatures();


  previousTemperature =
      sensors.getTempCByIndex(0);


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


  // =================================================
  // WIFI
  // =================================================

  connectWiFi();


  Serial.println();
  Serial.println(
    "Monitoring Started..."
  );

  Serial.println();
}


// =================================================
// READ CURRENT
// =================================================

float readCurrent() {

  double sum = 0;

  const int samples = 500;


  for (
    int i = 0;
    i < samples;
    i++
  ) {

    sum +=
      analogReadMilliVolts(
        CURRENT_PIN
      );

    delayMicroseconds(100);
  }


  float sensorVoltage =
      (sum / samples) / 1000.0;


  float current =
      (
        sensorVoltage
        - CURRENT_ZERO
      )
      / CURRENT_SENSITIVITY;


  current =
      fabs(current);


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


  for (
    int i = 0;
    i < samples;
    i++
  ) {

    sum +=
      analogReadMilliVolts(
        VOLTAGE_PIN
      );

    delayMicroseconds(100);
  }


  float sensorVoltage =
      (sum / samples) / 1000.0;


  float actualVoltage =
      sensorVoltage
      * VOLTAGE_RATIO;


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
// SEND DATA TO RENDER
// =================================================

void sendDataToRender(
  float batteryVoltage,
  float current,
  float temperature,
  bool fanON,
  String protectionStatus,
  bool systemON,
  String currentTrend,
  String temperatureTrend,
  String loadStatus,
  String motorStatus
) {

  // =================================================
  // CHECK WIFI
  // =================================================

  if (
    WiFi.status()
    != WL_CONNECTED
  ) {

    Serial.println(
      "WiFi disconnected."
    );

    connectWiFi();

    if (
      WiFi.status()
      != WL_CONNECTED
    ) {

      Serial.println(
        "Cannot send data."
      );

      return;
    }
  }


  // =================================================
  // HTTP CLIENT
  // =================================================

  HTTPClient http;


  Serial.println();
  Serial.println(
    "Connecting to Render..."
  );


  http.begin(
    SERVER_URL
  );


  // =================================================
  // HEADERS
  // =================================================

  http.addHeader(
    "Content-Type",
    "application/json"
  );


  // =================================================
  // JSON DATA
  //
  // The Render backend currently requires
  // ALL of these fields.
  // =================================================

  String jsonData = "{";

  jsonData +=
    "\"voltage\":"
    + String(
        batteryVoltage,
        2
      )
    + ",";


  jsonData +=
    "\"current\":"
    + String(
        current,
        2
      )
    + ",";


  jsonData +=
    "\"temperature\":"
    + String(
        temperature,
        2
      )
    + ",";


  jsonData +=
    "\"fan\":"
    + String(
        fanON ? "true" : "false"
      )
    + ",";


  jsonData +=
    "\"status\":\""
    + protectionStatus
    + "\",";


  jsonData +=
    "\"system\":"
    + String(
        systemON ? "true" : "false"
      )
    + ",";


  // =================================================
  // REQUIRED BACKEND FIELDS
  // =================================================

  jsonData +=
    "\"current_trend\":\""
    + currentTrend
    + "\",";


  jsonData +=
    "\"temperature_trend\":\""
    + temperatureTrend
    + "\",";


  jsonData +=
    "\"load_status\":\""
    + loadStatus
    + "\",";


  jsonData +=
    "\"motor_status\":\""
    + motorStatus
    + "\"";


  jsonData += "}";


  // =================================================
  // SERIAL JSON
  // =================================================

  Serial.println();

  Serial.println(
    "Sending data:"
  );

  Serial.println(
    jsonData
  );


  // =================================================
  // POST REQUEST
  // =================================================

  int httpResponseCode =
      http.POST(
        jsonData
      );


  // =================================================
  // RESPONSE
  // =================================================

  Serial.print(
    "HTTP Response Code: "
  );

  Serial.println(
    httpResponseCode
  );


  if (
    httpResponseCode > 0
  ) {

    String response =
        http.getString();


    Serial.print(
      "Server Response: "
    );

    Serial.println(
      response
    );

  }

  else {

    Serial.print(
      "HTTP Error: "
    );

    Serial.println(
      http.errorToString(
        httpResponseCode
      )
    );
  }


  // =================================================
  // CLOSE CONNECTION
  // =================================================

  http.end();
}


// =================================================
// MAIN LOOP
// =================================================

void loop() {

  // =================================================
  // READ SENSORS
  // =================================================

  float current =
      readCurrent();


  float batteryVoltage =
      readVoltage();


  float temperature =
      readTemperature();


  // =================================================
  // SYSTEM ON / OFF
  //
  // Here we assume the system is ON when
  // meaningful voltage is detected.
  //
  // Change 1.0 if your actual threshold is different.
  // =================================================

  bool systemON =
      batteryVoltage > 1.0;


  // =================================================
  // CURRENT TREND
  // =================================================

  String currentTrend;


  if (
    current
    >
    previousCurrent
    + CURRENT_CHANGE
  ) {

    currentTrend =
      "INCREASING";

  }

  else if (
    current
    <
    previousCurrent
    - CURRENT_CHANGE
  ) {

    currentTrend =
      "DECREASING";

  }

  else {

    currentTrend =
      "STABLE";
  }


  // =================================================
  // TEMPERATURE TREND
  // =================================================

  String temperatureTrend;


  if (
    temperature
    >
    previousTemperature
    + TEMP_CHANGE
  ) {

    temperatureTrend =
      "INCREASING";

  }

  else if (
    temperature
    <
    previousTemperature
    - TEMP_CHANGE
  ) {

    temperatureTrend =
      "DECREASING";

  }

  else {

    temperatureTrend =
      "STABLE";
  }


  // =================================================
  // LOAD STATUS
  // =================================================

  String loadStatus;


  if (
    currentTrend
    ==
    "INCREASING"
  ) {

    loadStatus =
      "LOAD INCREASING";

  }

  else if (
    currentTrend
    ==
    "DECREASING"
  ) {

    loadStatus =
      "LOAD DECREASING";

  }

  else {

    loadStatus =
      "LOAD STABLE";
  }


  // =================================================
  // FAN CONTROL
  // =================================================

  bool fanON = false;


  if (
    temperature
    >=
    FAN_ON_TEMP
  ) {

    fanON = true;

  }

  else if (
    temperature
    <=
    FAN_OFF_TEMP
  ) {

    fanON = false;
  }


  // =================================================
  // RELAY CONTROL
  // =================================================

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


  // =================================================
  // MOTOR PROTECTION STATUS
  // =================================================

  String protectionStatus;


  if (
    temperature
    >=
    FAN_ON_TEMP
  ) {

    protectionStatus =
      "COOLING ACTIVE";

  }

  else if (
    currentTrend
    ==
    "INCREASING"
  ) {

    protectionStatus =
      "LOAD RISING";

  }

  else {

    protectionStatus =
      "NORMAL";
  }


  // =================================================
  // MOTOR STATUS
  //
  // Required by Render backend.
  // =================================================

  String motorStatus;


  if (systemON) {

    motorStatus =
      "ON";

  }

  else {

    motorStatus =
      "OFF";
  }


  // =================================================
  // SERIAL MONITOR
  // =================================================

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

  Serial.println(
    " V"
  );


  Serial.print(
    "Motor Current   : "
  );

  Serial.print(
    current,
    3
  );

  Serial.println(
    " A"
  );


  Serial.print(
    "Motor Temp      : "
  );

  Serial.print(
    temperature,
    2
  );

  Serial.println(
    " C"
  );


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


  Serial.println(
    "------------------------------------------"
  );


  // =================================================
  // SEND DATA TO RENDER
  // =================================================

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
    motorStatus
  );


  // =================================================
  // SAVE PREVIOUS VALUES
  // =================================================

  previousCurrent =
      current;


  previousTemperature =
      temperature;


  // =================================================
  // WAIT 1 SECOND
  // =================================================

  delay(1000);
}
