#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <math.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const char* WIFI_SSID = "Admin";
const char* WIFI_PASSWORD = "password";

const char* SERVER_URL =
    "https://smart-ev-motor-protection.onrender.com/data";

const int VOLTAGE_PIN = 34;
const int CURRENT_PIN = 35;
const int TEMP_PIN = 4;
const int RELAY_PIN = 13;

const int MOTOR_PWM_PIN = 17;

#define OLED_SDA 21
#define OLED_SCL 22
#define OLED_ADDRESS 0x3C

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    &Wire,
    OLED_RESET
);

bool oledOK = false;

OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

const float CURRENT_ZERO = 2.5605;
const float CURRENT_SENSITIVITY = 0.066;

const float VOLTAGE_RATIO = 5.0;

const float CURRENT_CHANGE = 0.03;
const float TEMP_CHANGE = 0.3;

const float FAN_ON_TEMP = 31.0;
const float FAN_OFF_TEMP = 30.0;

const float CRITICAL_TEMP = 35.0;

const float MAX_SPEED = 45.0;

const int PWM_MAX = 255;

// 0 -> 255 in approximately 5 seconds
const unsigned long ACCELERATION_TIME = 5000;

// 255 -> 0 in approximately 7 seconds
const unsigned long DECELERATION_TIME = 7000;

// Send to Render every 100 ms
const unsigned long SEND_INTERVAL = 100;

unsigned long lastSendTime = 0;

float baseCurrent = 0;
float previousCurrent = 0;
float previousTemperature = 0;

float speed = 0.0;
int motorPWM = 0;

unsigned long motorRampStart = 0;

float speedAtStop = 0;

bool lastSystemState = false;

// ============================================================
// OLED
// ============================================================

void updateOLED(
    float temperature,
    float voltage,
    float current,
    bool fanON
) {
    if (!oledOK) {
        return;
    }

    display.clearDisplay();

    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);

    display.setCursor(40, 2);
    display.print("TEMP: ");
    display.print(temperature, 1);
    display.print("C");

    display.setCursor(0, 22);
    display.print("V: ");
    display.print(voltage, 2);
    display.print(" V");

    display.setCursor(68, 22);
    display.print("A: ");
    display.print(current, 2);
    display.print(" A");

    display.setCursor(43, 44);
    display.print("FAN: ");

    if (fanON) {
        display.print("ON");
    } else {
        display.print("OFF");
    }

    display.display();
}

// ============================================================
// MOTOR SPEED CONTROL
// ============================================================

void updateMotor(bool systemON) {

    unsigned long now = millis();

    // System just turned ON
    if (systemON && !lastSystemState) {

        motorRampStart = now;
        speed = 0.0;
    }

    // System just turned OFF
    if (!systemON && lastSystemState) {

        motorRampStart = now;
        speedAtStop = speed;
    }

    // ========================================================
    // ACCELERATION
    // ========================================================

    if (systemON) {

        unsigned long elapsed =
            now - motorRampStart;

        if (elapsed >= ACCELERATION_TIME) {

            speed = MAX_SPEED;

        } else {

            speed =
                ((float)elapsed /
                 (float)ACCELERATION_TIME)
                * MAX_SPEED;
        }
    }

    // ========================================================
    // DECELERATION
    // ========================================================

    else {

        unsigned long elapsed =
            now - motorRampStart;

        if (speedAtStop <= 0.0) {

            speed = 0.0;

        } else if (elapsed >= DECELERATION_TIME) {

            speed = 0.0;

        } else {

            speed =
                speedAtStop *
                (1.0 -
                 ((float)elapsed /
                  (float)DECELERATION_TIME));
        }
    }

    // ========================================================
    // SPEED TO PWM
    // ========================================================

    motorPWM =
        (int)((speed / MAX_SPEED) * PWM_MAX);

    motorPWM =
        constrain(
            motorPWM,
            0,
            PWM_MAX
        );

    // ========================================================
    // BTS7960 RPWM
    // ========================================================

    analogWrite(
        MOTOR_PWM_PIN,
        motorPWM
    );

    lastSystemState = systemON;
}

// ============================================================
// CURRENT SENSOR
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
        (sensorVoltage - CURRENT_ZERO) /
        CURRENT_SENSITIVITY;

    current = fabs(current);

    if (current < 0.03) {
        current = 0;
    }

    return current;
}

// ============================================================
// VOLTAGE SENSOR
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
// TEMPERATURE SENSOR
// ============================================================

float readTemperature() {

    sensors.requestTemperatures();

    float temperature =
        sensors.getTempCByIndex(0);

    return temperature;
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
        String(currentSpeed, 1) +

        "}";

    Serial.println();
    Serial.println("Sending data:");
    Serial.println(jsonData);

    int responseCode =
        http.POST(jsonData);

    Serial.print(
        "HTTP Response Code: "
    );

    Serial.println(
        responseCode
    );

    if (responseCode > 0) {

        String response =
            http.getString();

        Serial.print(
            "Server Response: "
        );

        Serial.println(
            response
        );
    }

    http.end();
}

// ============================================================
// SETUP
// ============================================================

void setup() {

    Serial.begin(115200);

    // ========================================================
    // ADC
    // ========================================================

    analogReadResolution(12);

    analogSetPinAttenuation(
        VOLTAGE_PIN,
        ADC_11db
    );

    analogSetPinAttenuation(
        CURRENT_PIN,
        ADC_11db
    );

    // ========================================================
    // MOTOR
    // ========================================================

    pinMode(
        MOTOR_PWM_PIN,
        OUTPUT
    );

    analogWrite(
        MOTOR_PWM_PIN,
        0
    );

    // ========================================================
    // OLED
    // ========================================================

    Wire.begin(
        OLED_SDA,
        OLED_SCL
    );

    if (
        display.begin(
            SSD1306_SWITCHCAPVCC,
            OLED_ADDRESS
        )
    ) {

        oledOK = true;

        display.clearDisplay();

        display.setTextColor(
            SSD1306_WHITE
        );

        display.setTextSize(1);

        display.setCursor(
            20,
            25
        );

        display.println(
            "EV PROTECTION"
        );

        display.display();

        delay(1500);

        display.clearDisplay();
        display.display();

    } else {

        oledOK = false;

        Serial.println(
            "OLED initialization failed!"
        );
    }

    // ========================================================
    // DS18B20
    // ========================================================

    sensors.begin();

    // ========================================================
    // FAN RELAY
    // ========================================================

    pinMode(
        RELAY_PIN,
        OUTPUT
    );

    digitalWrite(
        RELAY_PIN,
        HIGH
    );

    delay(2000);

    // ========================================================
    // STARTUP
    // ========================================================

    Serial.println();
    Serial.println(
        "=========================================="
    );

    Serial.println(
        "       EV MOTOR PROTECTION SYSTEM"
    );

    Serial.println(
        "=========================================="
    );

    Serial.println();

    Serial.print(
        "Temperature Sensors Found: "
    );

    Serial.println(
        sensors.getDeviceCount()
    );

    Serial.println();

    // ========================================================
    // CURRENT CALIBRATION
    // ========================================================

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
        (currentSum / 2000.0) /
        1000.0;

    baseCurrent =
        fabs(
            (currentVoltage - CURRENT_ZERO) /
            CURRENT_SENSITIVITY
        );

    previousCurrent =
        baseCurrent;

    // ========================================================
    // INITIAL TEMPERATURE
    // ========================================================

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

    Serial.println(
        " A"
    );

    Serial.print(
        "Initial Temp : "
    );

    Serial.print(
        previousTemperature,
        2
    );

    Serial.println(
        " C"
    );

    // ========================================================
    // WIFI
    // ========================================================

    Serial.println();
    Serial.println(
        "Connecting to WiFi..."
    );

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    while (
        WiFi.status() != WL_CONNECTED
    ) {

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

    Serial.println(
        "Monitoring Started..."
    );

    Serial.println();

    lastSendTime =
        millis();
}

// ============================================================
// LOOP
// ============================================================

void loop() {

    // ========================================================
    // READ SENSORS
    // ========================================================

    float current =
        readCurrent();

    float batteryVoltage =
        readVoltage();

    float temperature =
        readTemperature();

    // ========================================================
    // SYSTEM ON/OFF
    // ========================================================

    bool systemON;

    if (current > 0.05) {

        systemON = true;

    } else {

        systemON = false;
    }

    // ========================================================
    // CURRENT TREND
    // ========================================================

    String currentTrend;

    if (
        current >
        previousCurrent +
        CURRENT_CHANGE
    ) {

        currentTrend =
            "INCREASING";

    } else if (
        current <
        previousCurrent -
        CURRENT_CHANGE
    ) {

        currentTrend =
            "DECREASING";

    } else {

        currentTrend =
            "STABLE";
    }

    // ========================================================
    // TEMPERATURE TREND
    // ========================================================

    String temperatureTrend;

    if (
        temperature >
        previousTemperature +
        TEMP_CHANGE
    ) {

        temperatureTrend =
            "INCREASING";

    } else if (
        temperature <
        previousTemperature -
        TEMP_CHANGE
    ) {

        temperatureTrend =
            "DECREASING";

    } else {

        temperatureTrend =
            "STABLE";
    }

    // ========================================================
    // LOAD STATUS
    // ========================================================

    String loadStatus;

    if (
        currentTrend ==
        "INCREASING"
    ) {

        loadStatus =
            "LOAD INCREASING";

    } else if (
        currentTrend ==
        "DECREASING"
    ) {

        loadStatus =
            "LOAD DECREASING";

    } else {

        loadStatus =
            "LOAD STABLE";
    }

    // ========================================================
    // FAN
    // ========================================================

    bool fanON = false;

    if (
        temperature >=
        FAN_ON_TEMP
    ) {

        fanON = true;

    } else if (
        temperature <=
        FAN_OFF_TEMP
    ) {

        fanON = false;
    }

    if (fanON) {

        digitalWrite(
            RELAY_PIN,
            LOW
        );

    } else {

        digitalWrite(
            RELAY_PIN,
            HIGH
        );
    }

    // ========================================================
    // PROTECTION STATUS
    // ========================================================

    String protectionStatus;

    if (
        temperature >=
        CRITICAL_TEMP
    ) {

        protectionStatus =
            "CRITICAL";

    } else if (
        temperature >=
        FAN_ON_TEMP
    ) {

        protectionStatus =
            "WARNING";

    } else {

        protectionStatus =
            "NORMAL";
    }

    // ========================================================
    // MOTOR STATUS
    // ========================================================

    String motorStatus;

    if (systemON) {

        motorStatus =
            "ON";

    } else {

        motorStatus =
            "OFF";
    }

    // ========================================================
    // MOTOR SPEED CONTROL
    // ========================================================

    updateMotor(
        systemON
    );

    // ========================================================
    // OLED
    // ========================================================

    updateOLED(
        temperature,
        batteryVoltage,
        current,
        fanON
    );

    // ========================================================
    // SERIAL MONITOR
    // ========================================================

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
        1
    );

    Serial.println(
        " km/h"
    );

    Serial.print(
        "Motor PWM       : "
    );

    Serial.println(
        motorPWM
    );

    Serial.println(
        "------------------------------------------"
    );

    // ========================================================
    // SEND TO RENDER
    // ========================================================

    unsigned long now =
        millis();

    if (
        now -
        lastSendTime >=
        SEND_INTERVAL
    ) {

        lastSendTime =
            now;

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

    // ========================================================
    // SAVE PREVIOUS VALUES
    // ========================================================

    previousCurrent =
        current;

    previousTemperature =
        temperature;

    delay(10);
}
