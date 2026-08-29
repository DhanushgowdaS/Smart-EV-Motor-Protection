#include <WiFi.h>
#include <HTTPClient.h>

// ============================================================
// WIFI
// ============================================================

const char* WIFI_SSID = "Admin";
const char* WIFI_PASSWORD = "password";


// ============================================================
// SERVER
// ============================================================

const char* SERVER_URL =
    "https://smart-ev-motor-protection.onrender.com/data";


// ============================================================
// SENSOR PINS
// ============================================================

// Change these according to your actual hardware

#define VOLTAGE_PIN 34
#define CURRENT_PIN 35
#define TEMPERATURE_PIN 32

// System ON/OFF input
#define SYSTEM_PIN 27

// Cooling fan control
#define FAN_PIN 26


// ============================================================
// VARIABLES
// ============================================================

float voltage = 0.0;
float current = 0.0;
float temperature = 0.0;

bool systemOn = false;
bool fanOn = false;

String systemStatus = "NORMAL";


// ============================================================
// SETUP
// ============================================================

void setup()
{
    Serial.begin(115200);

    delay(1000);

    Serial.println();
    Serial.println("=================================");
    Serial.println(" SMART EV MOTOR PROTECTION SYSTEM");
    Serial.println(" ESP32 DATA SENDER");
    Serial.println("=================================");
    Serial.println();


    // --------------------------------------------------------
    // PIN CONFIGURATION
    // --------------------------------------------------------

    pinMode(SYSTEM_PIN, INPUT);
    pinMode(FAN_PIN, OUTPUT);

    digitalWrite(FAN_PIN, LOW);


    // --------------------------------------------------------
    // WIFI CONNECTION
    // --------------------------------------------------------

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    Serial.print("Connecting to WiFi");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);

        Serial.print(".");
    }

    Serial.println();
    Serial.println("WiFi Connected!");

    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());

    Serial.println();
}


// ============================================================
// READ VOLTAGE
// ============================================================

float readVoltage()
{
    int rawValue = analogRead(VOLTAGE_PIN);

    float adcVoltage =
        (rawValue / 4095.0) * 3.3;

    /*
       IMPORTANT:

       This is only the ADC voltage.

       If you are using a voltage divider,
       multiply by the correct divider ratio.

       Example:

       11.0V battery
       voltage divider ratio = 4.0

       actual voltage = adcVoltage * 4.0
    */

    float actualVoltage =
        adcVoltage * 16.0;

    return actualVoltage;
}


// ============================================================
// READ CURRENT
// ============================================================

float readCurrent()
{
    int rawValue = analogRead(CURRENT_PIN);

    float adcVoltage =
        (rawValue / 4095.0) * 3.3;

    /*
       CURRENT SENSOR CALIBRATION

       This depends on your actual sensor.

       For example, ACS712 / ACS758
       will have different calibration.

       This value is only a starting point.
    */

    float sensorZero =
        1.65;

    float sensitivity =
        0.100;

    float currentValue =
        (adcVoltage - sensorZero)
        / sensitivity;

    if (currentValue < 0)
    {
        currentValue =
            -currentValue;
    }

    return currentValue;
}


// ============================================================
// READ TEMPERATURE
// ============================================================

float readTemperature()
{
    /*
       TEMPORARY ADC TEMPERATURE INPUT

       Replace this function with the actual
       temperature sensor code later.

       If using DS18B20, we will replace this
       with OneWire + DallasTemperature.
    */

    int rawValue =
        analogRead(TEMPERATURE_PIN);

    float temperatureValue =
        (rawValue / 4095.0) * 100.0;

    return temperatureValue;
}


// ============================================================
// DETERMINE SYSTEM STATUS
// ============================================================

void calculateSystemStatus()
{
    if (!systemOn)
    {
        systemStatus = "NORMAL";

        fanOn = false;

        digitalWrite(
            FAN_PIN,
            LOW
        );

        return;
    }


    // --------------------------------------------------------
    // TEMPERATURE PROTECTION
    // --------------------------------------------------------

    if (temperature >= 70)
    {
        systemStatus = "CRITICAL";

        fanOn = true;
    }

    else if (temperature >= 55)
    {
        systemStatus = "WARNING";

        fanOn = true;
    }

    else
    {
        systemStatus = "NORMAL";

        fanOn = false;
    }


    // --------------------------------------------------------
    // FAN
    // --------------------------------------------------------

    digitalWrite(
        FAN_PIN,
        fanOn ? HIGH : LOW
    );
}


// ============================================================
// SEND DATA TO RENDER
// ============================================================

void sendData()
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println(
            "WiFi disconnected!"
        );

        return;
    }


    HTTPClient http;


    // --------------------------------------------------------
    // START HTTP CONNECTION
    // --------------------------------------------------------

    http.begin(
        SERVER_URL
    );


    // --------------------------------------------------------
    // JSON CONTENT TYPE
    // --------------------------------------------------------

    http.addHeader(
        "Content-Type",
        "application/json"
    );


    // --------------------------------------------------------
    // CREATE JSON
    // --------------------------------------------------------

    String jsonData = "{";

    jsonData +=
        "\"voltage\":" +
        String(voltage, 2) +
        ",";

    jsonData +=
        "\"current\":" +
        String(current, 2) +
        ",";

    jsonData +=
        "\"temperature\":" +
        String(temperature, 2) +
        ",";

    jsonData +=
        "\"current_trend\":\"NORMAL\",";

    jsonData +=
        "\"temperature_trend\":\"NORMAL\",";

    jsonData +=
        "\"load_status\":\"" +
        String(systemOn ? "ON" : "OFF") +
        "\",";

    jsonData +=
        "\"motor_status\":\"" +
        String(systemOn ? "RUNNING" : "OFF") +
        "\",";

    jsonData +=
        "\"fan\":" +
        String(fanOn ? "true" : "false");

    jsonData += "}";


    // --------------------------------------------------------
    // PRINT JSON
    // --------------------------------------------------------

    Serial.println();
    Serial.println(
        "Sending data:"
    );

    Serial.println(
        jsonData
    );


    // --------------------------------------------------------
    // POST
    // --------------------------------------------------------

    int httpCode =
        http.POST(
            jsonData
        );


    // --------------------------------------------------------
    // SERVER RESPONSE
    // --------------------------------------------------------

    if (httpCode > 0)
    {
        Serial.print(
            "HTTP Response Code: "
        );

        Serial.println(
            httpCode
        );


        String response =
            http.getString();

        Serial.print(
            "Server Response: "
        );

        Serial.println(
            response
        );
    }

    else
    {
        Serial.print(
            "HTTP POST Failed: "
        );

        Serial.println(
            http.errorToString(
                httpCode
            )
        );
    }


    // --------------------------------------------------------
    // CLOSE CONNECTION
    // --------------------------------------------------------

    http.end();
}


// ============================================================
// MAIN LOOP
// ============================================================

void loop()
{
    // --------------------------------------------------------
    // READ SYSTEM STATE
    // --------------------------------------------------------

    systemOn =
        digitalRead(
            SYSTEM_PIN
        );


    // --------------------------------------------------------
    // READ SENSORS
    // --------------------------------------------------------

    voltage =
        readVoltage();

    current =
        readCurrent();

    temperature =
        readTemperature();


    // --------------------------------------------------------
    // CALCULATE STATUS + FAN
    // --------------------------------------------------------

    calculateSystemStatus();


    // --------------------------------------------------------
    // SERIAL MONITOR
    // --------------------------------------------------------

    Serial.println();
    Serial.println(
        "-------------------------------"
    );

    Serial.print(
        "System: "
    );

    Serial.println(
        systemOn ? "ON" : "OFF"
    );


    Serial.print(
        "Voltage: "
    );

    Serial.print(
        voltage
    );

    Serial.println(
        " V"
    );


    Serial.print(
        "Current: "
    );

    Serial.print(
        current
    );

    Serial.println(
        " A"
    );


    Serial.print(
        "Temperature: "
    );

    Serial.print(
        temperature
    );

    Serial.println(
        " C"
    );


    Serial.print(
        "Status: "
    );

    Serial.println(
        systemStatus
    );


    Serial.print(
        "Fan: "
    );

    Serial.println(
        fanOn ? "ON" : "OFF"
    );


    // --------------------------------------------------------
    // SEND TO RENDER
    // --------------------------------------------------------

    sendData();


    // --------------------------------------------------------
    // SEND EVERY 3 SECONDS
    // --------------------------------------------------------

    delay(3000);
}
