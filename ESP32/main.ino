// ============================================================
// EV MOTOR PROTECTION SYSTEM
// ESP32 MAIN CODE
// ============================================================
//
// Sensors:
//   ACS712 30A  -> GPIO 35
//   DS18B20     -> GPIO 4
//   Voltage     -> VOLTAGE_PIN
//   Fan Relay   -> GPIO 13
//
// Relay:
//   ACTIVE LOW
//
// Communication:
//   ESP32 -> HTTP POST -> Backend
// ============================================================

#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <math.h>

// ============================================================
// WIFI SETTINGS
// ============================================================

const char* WIFI_SSID = "Admin";
const char* WIFI_PASSWORD = "password";

// PUT YOUR BACKEND URL HERE
// Example:
// https://your-backend.onrender.com/data
const char* SERVER_URL = "YOUR_BACKEND_URL/data";


// ============================================================
// PIN CONFIGURATION
// ============================================================

const int CURRENT_PIN = 35;

const int TEMP_PIN = 4;

const int RELAY_PIN = 13;


// ------------------------------------------------------------
// CHANGE THIS TO THE ADC PIN WHERE YOUR VOLTAGE SENSOR IS
// CONNECTED.
// ------------------------------------------------------------

const int VOLTAGE_PIN = 34;


// ============================================================
// ACS712-30A SETTINGS
// ============================================================

const float ZERO_VOLTAGE = 2.5605;

const float SENSITIVITY = 0.066;


// ============================================================
// VOLTAGE SENSOR SETTINGS
// ============================================================
//
// IMPORTANT:
// Change VOLTAGE_DIVIDER_RATIO according to your resistor
// voltage divider.
//
// Example:
// R1 = 30k
// R2 = 10k
//
// Ratio = (30 + 10) / 10 = 4.0
//
// If your voltage module already outputs a scaled voltage,
// use its appropriate ratio.
// ============================================================

const float VOLTAGE_DIVIDER_RATIO = 4.0;


// ============================================================
// FAN TEMPERATURE SETTINGS
// ============================================================

const float FAN_ON_TEMP = 31.0;

const float FAN_OFF_TEMP = 30.0;


// ============================================================
// CURRENT TREND SETTINGS
// ============================================================

const float CURRENT_TREND_THRESHOLD = 0.03;


// ============================================================
// TEMPERATURE TREND SETTINGS
// ============================================================

const float TEMP_TREND_THRESHOLD = 0.30;


// ============================================================
// CURRENT SENSOR
// ============================================================

const int CURRENT_SAMPLES = 300;


// ============================================================
// DS18B20
// ============================================================

OneWire oneWire(TEMP_PIN);

DallasTemperature sensors(&oneWire);


// ============================================================
// VARIABLES
// ============================================================

float current = 0.0;

float voltage = 0.0;

float temperature = 0.0;

float previousCurrent = 0.0;

float previousTemperature = 0.0;

float baselineCurrent = 0.0;

bool fanON = false;


// ============================================================
// READ ACS712 CURRENT
// ============================================================

float readCurrent()
{
    double sum = 0;

    for (int i = 0; i < CURRENT_SAMPLES; i++)
    {
        sum += analogReadMilliVolts(CURRENT_PIN);

        delayMicroseconds(100);
    }

    float sensorVoltage =
        (sum / CURRENT_SAMPLES) / 1000.0;

    float measuredCurrent =
        (sensorVoltage - ZERO_VOLTAGE) / SENSITIVITY;

    measuredCurrent = fabs(measuredCurrent);

    // Remove very small noise
    if (measuredCurrent < 0.03)
    {
        measuredCurrent = 0;
    }

    return measuredCurrent;
}


// ============================================================
// READ BATTERY VOLTAGE
// ============================================================

float readVoltage()
{
    const int samples = 50;

    double sum = 0;

    for (int i = 0; i < samples; i++)
    {
        sum += analogReadMilliVolts(VOLTAGE_PIN);

        delayMicroseconds(200);
    }

    float adcVoltage =
        (sum / samples) / 1000.0;

    float batteryVoltage =
        adcVoltage * VOLTAGE_DIVIDER_RATIO;

    return batteryVoltage;
}


// ============================================================
// READ TEMPERATURE
// ============================================================

float readTemperature()
{
    sensors.requestTemperatures();

    float temp =
        sensors.getTempCByIndex(0);

    if (temp == DEVICE_DISCONNECTED_C)
    {
        Serial.println("DS18B20 ERROR!");

        return -127.0;
    }

    return temp;
}


// ============================================================
// CURRENT TREND
// ============================================================

String getCurrentTrend()
{
    if (current > previousCurrent +
        CURRENT_TREND_THRESHOLD)
    {
        return "INCREASING";
    }

    if (current < previousCurrent -
        CURRENT_TREND_THRESHOLD)
    {
        return "DECREASING";
    }

    return "STABLE";
}


// ============================================================
// TEMPERATURE TREND
// ============================================================

String getTemperatureTrend()
{
    if (temperature >
        previousTemperature +
        TEMP_TREND_THRESHOLD)
    {
        return "INCREASING";
    }

    if (temperature <
        previousTemperature -
        TEMP_TREND_THRESHOLD)
    {
        return "DECREASING";
    }

    return "STABLE";
}


// ============================================================
// FAN CONTROL
// ============================================================

void controlFan()
{
    // FAN ON
    if (temperature >= FAN_ON_TEMP)
    {
        digitalWrite(RELAY_PIN, LOW);

        fanON = true;
    }

    // FAN OFF
    else if (temperature <= FAN_OFF_TEMP)
    {
        digitalWrite(RELAY_PIN, HIGH);

        fanON = false;
    }
}


// ============================================================
// MOTOR STATUS
// ============================================================

String getMotorStatus()
{
    // Emergency
    if (temperature >= 40.0)
    {
        return "EMERGENCY";
    }

    // Warning
    if (temperature >= 35.0)
    {
        return "WARNING";
    }

    return "NORMAL";
}


// ============================================================
// SEND DATA TO BACKEND
// ============================================================

void sendData()
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("WiFi disconnected");

        return;
    }

    String currentTrend =
        getCurrentTrend();

    String tempTrend =
        getTemperatureTrend();

    String motorStatus =
        getMotorStatus();


    // --------------------------------------------------------
    // LOAD STATUS
    // --------------------------------------------------------

    String loadStatus = "NORMAL";

    if (currentTrend == "INCREASING" &&
        tempTrend == "INCREASING")
    {
        loadStatus = "LOAD INCREASING";
    }

    else if (currentTrend == "DECREASING" &&
             tempTrend == "DECREASING")
    {
        loadStatus = "LOAD DECREASING";
    }


    // --------------------------------------------------------
    // CREATE JSON
    // --------------------------------------------------------

    String json = "{";

    json += "\"voltage\":";
    json += String(voltage, 2);

    json += ",";

    json += "\"current\":";
    json += String(current, 3);

    json += ",";

    json += "\"temperature\":";
    json += String(temperature, 2);

    json += ",";

    json += "\"current_trend\":\"";
    json += currentTrend;
    json += "\"";

    json += ",";

    json += "\"temperature_trend\":\"";
    json += tempTrend;
    json += "\"";

    json += ",";

    json += "\"load_status\":\"";
    json += loadStatus;
    json += "\"";

    json += ",";

    json += "\"motor_status\":\"";
    json += motorStatus;
    json += "\"";

    json += ",";

    json += "\"fan\":";
    json += fanON ? "true" : "false";

    json += "}";


    // --------------------------------------------------------
    // HTTP POST
    // --------------------------------------------------------

    HTTPClient http;

    http.begin(SERVER_URL);

    http.addHeader(
        "Content-Type",
        "application/json"
    );

    int responseCode =
        http.POST(json);

    Serial.print("Server Response: ");

    Serial.println(responseCode);

    http.end();
}


// ============================================================
// DISPLAY DATA
// ============================================================

void printData()
{
    Serial.println();
    Serial.println("------------------------------------------");

    Serial.print("Battery Voltage : ");
    Serial.print(voltage, 2);
    Serial.println(" V");

    Serial.print("Motor Current   : ");
    Serial.print(current, 3);
    Serial.println(" A");

    Serial.print("Current Trend   : ");
    Serial.println(getCurrentTrend());

    Serial.print("Motor Temp      : ");
    Serial.print(temperature, 2);
    Serial.println(" °C");

    Serial.print("Temp Trend      : ");
    Serial.println(getTemperatureTrend());

    Serial.print("Motor Status    : ");
    Serial.println(getMotorStatus());

    Serial.print("Fan             : ");

    if (fanON)
        Serial.println("ON");
    else
        Serial.println("OFF");

    Serial.println("------------------------------------------");
}


// ============================================================
// CONNECT WIFI
// ============================================================

void connectWiFi()
{
    Serial.print("Connecting to WiFi");

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    int attempts = 0;

    while (WiFi.status() != WL_CONNECTED &&
           attempts < 30)
    {
        delay(500);

        Serial.print(".");

        attempts++;
    }

    Serial.println();

    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("WiFi connected!");

        Serial.print("ESP32 IP: ");

        Serial.println(
            WiFi.localIP()
        );
    }

    else
    {
        Serial.println(
            "WiFi connection failed"
        );
    }
}


// ============================================================
// SETUP
// ============================================================

void setup()
{
    Serial.begin(115200);

    delay(1000);


    // ADC
    analogReadResolution(12);

    analogSetPinAttenuation(
        CURRENT_PIN,
        ADC_11db
    );

    analogSetPinAttenuation(
        VOLTAGE_PIN,
        ADC_11db
    );


    // Relay
    pinMode(
        RELAY_PIN,
        OUTPUT
    );

    // IMPORTANT:
    // Active LOW relay = HIGH means OFF
    digitalWrite(
        RELAY_PIN,
        HIGH
    );


    // Temperature sensor
    sensors.begin();


    Serial.println();
    Serial.println(
        "======================================"
    );

    Serial.println(
        "     EV MOTOR PROTECTION SYSTEM"
    );

    Serial.println(
        "======================================"
    );


    connectWiFi();


    // --------------------------------------------------------
    // INITIAL SENSOR READING
    // --------------------------------------------------------

    delay(2000);

    current = readCurrent();

    voltage = readVoltage();

    temperature = readTemperature();


    previousCurrent = current;

    previousTemperature = temperature;

    baselineCurrent = current;


    Serial.println();

    Serial.println(
        "Initial sensor readings:"
    );

    printData();
}


// ============================================================
// LOOP
// ============================================================

void loop()
{
    // Read sensors
    current = readCurrent();

    voltage = readVoltage();

    temperature = readTemperature();


    // Fan
    if (temperature > -100)
    {
        controlFan();
    }


    // Print
    printData();


    // Send to backend
    sendData();


    // Save previous values
    previousCurrent = current;

    previousTemperature = temperature;


    delay(1000);
}
