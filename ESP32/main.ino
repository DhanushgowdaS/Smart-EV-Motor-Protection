#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <math.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ============================================================
// WIFI
// ============================================================

const char* WIFI_SSID = "Admin";
const char* WIFI_PASSWORD = "password";

const char* SERVER_URL =
    "https://smart-ev-motor-protection.onrender.com/data";

// ============================================================
// PIN DEFINITIONS
// ============================================================

const int VOLTAGE_PIN = 34;
const int CURRENT_PIN = 35;
const int TEMP_PIN = 4;
const int RELAY_PIN = 13;

const int MOTOR_PWM_PIN = 17;

// ============================================================
// ULTRASONIC PINS
// ============================================================

// FRONT
#define FRONT_TRIG 14
#define FRONT_ECHO 27

// LEFT
#define LEFT_TRIG 26
#define LEFT_ECHO 25

// RIGHT
#define RIGHT_TRIG 33
#define RIGHT_ECHO 32

// ============================================================
// ULTRASONIC SETTINGS
// ============================================================

#define ULTRASONIC_TIMEOUT 10000
#define ACCIDENT_DISTANCE 30.0

// ============================================================
// OLED
// ============================================================

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

// ============================================================
// TEMPERATURE SENSOR
// ============================================================

OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

// ============================================================
// SENSOR CALIBRATION
// ============================================================

const float CURRENT_ZERO = 2.5605;
const float CURRENT_SENSITIVITY = 0.066;

const float VOLTAGE_RATIO = 5.0;

// ============================================================
// TREND SETTINGS
// ============================================================

const float CURRENT_CHANGE = 0.03;
const float TEMP_CHANGE = 0.3;

// ============================================================
// FAN
// ============================================================

const float FAN_ON_TEMP = 31.0;
const float FAN_OFF_TEMP = 30.0;

// ============================================================
// PROTECTION
// ============================================================

const float CRITICAL_TEMP = 35.0;

// ============================================================
// MOTOR
// ============================================================

const float MAX_SPEED = 45.0;

const int PWM_MAX = 255;

// 0 -> 255 in approximately 5 seconds
const unsigned long ACCELERATION_TIME = 5000;

// 255 -> 0 in approximately 7 seconds
const unsigned long DECELERATION_TIME = 7000;

// ============================================================
// RENDER
// ============================================================

const unsigned long SEND_INTERVAL = 100;

unsigned long lastSendTime = 0;

// ============================================================
// GLOBAL VARIABLES
// ============================================================

float baseCurrent = 0;
float previousCurrent = 0;
float previousTemperature = 0;

float speed = 0.0;
int motorPWM = 0;

unsigned long motorRampStart = 0;

float speedAtStop = 0;

bool lastSystemState = false;

// ============================================================
// ACCIDENT LOCK
// ============================================================

// IMPORTANT:
// This variable is NEVER reset in software.
//
// It becomes false again only after ESP32 restart.
//
// volatile is used because the ultrasonic task modifies it.
volatile bool accidentDetected = false;

// ============================================================
// ULTRASONIC DISTANCES
// ============================================================

volatile float frontDistance = -1;
volatile float leftDistance = -1;
volatile float rightDistance = -1;

// ============================================================
// MOTOR EMERGENCY STOP
// ============================================================

void emergencyMotorStop() {

    speed = 0.0;

    motorPWM = 0;

    analogWrite(
        MOTOR_PWM_PIN,
        0
    );

    lastSystemState = false;
}

// ============================================================
// READ ULTRASONIC DISTANCE
// ============================================================

float readDistance(
    int trigPin,
    int echoPin
) {

    digitalWrite(
        trigPin,
        LOW
    );

    delayMicroseconds(2);

    digitalWrite(
        trigPin,
        HIGH
    );

    delayMicroseconds(10);

    digitalWrite(
        trigPin,
        LOW
    );

    unsigned long duration =
        pulseIn(
            echoPin,
            HIGH,
            ULTRASONIC_TIMEOUT
        );

    if (duration == 0) {
        return -1;
    }

    float distance =
        (duration * 0.0343) / 2.0;

    return distance;
}

// ============================================================
// ULTRASONIC SAFETY TASK
// ============================================================
//
// This runs independently from the main loop.
//
// Therefore the 500-sample current measurement,
// temperature reading, WiFi communication etc.
// will NOT stop ultrasonic monitoring.
//

void ultrasonicSafetyTask(void *parameter) {

    while (true) {

        // ====================================================
        // IF ACCIDENT ALREADY DETECTED
        // ====================================================

        if (accidentDetected) {

            // Keep motor OFF forever
            emergencyMotorStop();

            // Do not clear accidentDetected.
            // It stays locked until ESP32 restart.

            vTaskDelay(
                pdMS_TO_TICKS(5)
            );

            continue;
        }

        // ====================================================
        // FRONT SENSOR
        // ====================================================

        frontDistance =
            readDistance(
                FRONT_TRIG,
                FRONT_ECHO
            );

        if (
            frontDistance > 0 &&
            frontDistance < ACCIDENT_DISTANCE
        ) {

            accidentDetected = true;

            emergencyMotorStop();

            Serial.println();
            Serial.println(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            );

            Serial.println(
                "ACCIDENT DETECTED - FRONT"
            );

            Serial.print(
                "Front Distance: "
            );

            Serial.print(
                frontDistance,
                1
            );

            Serial.println(
                " cm"
            );

            Serial.println(
                "MOTOR EMERGENCY STOP"
            );

            Serial.println(
                "SYSTEM LOCKED"
            );

            Serial.println(
                "RESTART ESP32 TO RESET"
            );

            Serial.println(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            );

            continue;
        }

        // Small gap before next ultrasonic pulse
        vTaskDelay(
            pdMS_TO_TICKS(1)
        );

        // ====================================================
        // LEFT SENSOR
        // ====================================================

        leftDistance =
            readDistance(
                LEFT_TRIG,
                LEFT_ECHO
            );

        if (
            leftDistance > 0 &&
            leftDistance < ACCIDENT_DISTANCE
        ) {

            accidentDetected = true;

            emergencyMotorStop();

            Serial.println();
            Serial.println(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            );

            Serial.println(
                "ACCIDENT DETECTED - LEFT"
            );

            Serial.print(
                "Left Distance: "
            );

            Serial.print(
                leftDistance,
                1
            );

            Serial.println(
                " cm"
            );

            Serial.println(
                "MOTOR EMERGENCY STOP"
            );

            Serial.println(
                "SYSTEM LOCKED"
            );

            Serial.println(
                "RESTART ESP32 TO RESET"
            );

            Serial.println(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            );

            continue;
        }

        vTaskDelay(
            pdMS_TO_TICKS(1)
        );

        // ====================================================
        // RIGHT SENSOR
        // ====================================================

        rightDistance =
            readDistance(
                RIGHT_TRIG,
                RIGHT_ECHO
            );

        if (
            rightDistance > 0 &&
            rightDistance < ACCIDENT_DISTANCE
        ) {

            accidentDetected = true;

            emergencyMotorStop();

            Serial.println();
            Serial.println(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            );

            Serial.println(
                "ACCIDENT DETECTED - RIGHT"
            );

            Serial.print(
                "Right Distance: "
            );

            Serial.print(
                rightDistance,
                1
            );

            Serial.println(
                " cm"
            );

            Serial.println(
                "MOTOR EMERGENCY STOP"
            );

            Serial.println(
                "SYSTEM LOCKED"
            );

            Serial.println(
                "RESTART ESP32 TO RESET"
            );

            Serial.println(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            );

            continue;
        }

        // ====================================================
        // VERY SHORT LOOP DELAY
        // ====================================================

        vTaskDelay(
            pdMS_TO_TICKS(2)
        );
    }
}

// ============================================================
// NORMAL OLED
// ============================================================

void updateNormalOLED(
    float temperature,
    float voltage,
    float current,
    bool fanON
) {

    if (!oledOK) {
        return;
    }

    display.clearDisplay();

    display.setTextColor(
        SSD1306_WHITE
    );

    display.setTextSize(1);

    // --------------------------------------------------------
    // TEMPERATURE
    // --------------------------------------------------------

    display.setCursor(
        40,
        2
    );

    display.print(
        "TEMP: "
    );

    display.print(
        temperature,
        1
    );

    display.print(
        "C"
    );

    // --------------------------------------------------------
    // VOLTAGE
    // --------------------------------------------------------

    display.setCursor(
        0,
        22
    );

    display.print(
        "V: "
    );

    display.print(
        voltage,
        2
    );

    display.print(
        " V"
    );

    // --------------------------------------------------------
    // CURRENT
    // --------------------------------------------------------

    display.setCursor(
        68,
        22
    );

    display.print(
        "A: "
    );

    display.print(
        current,
        2
    );

    display.print(
        " A"
    );

    // --------------------------------------------------------
    // FAN
    // --------------------------------------------------------

    display.setCursor(
        43,
        44
    );

    display.print(
        "FAN: "
    );

    if (fanON) {

        display.print(
            "ON"
        );

    } else {

        display.print(
            "OFF"
        );
    }

    display.display();
}

// ============================================================
// ACCIDENT OLED
// ============================================================
//
// Once accidentDetected becomes true,
// this function displays ONLY the accident message.
//

void updateAccidentOLED() {

    if (!oledOK) {
        return;
    }

    display.clearDisplay();

    display.setTextColor(
        SSD1306_WHITE
    );

    // Large text
    display.setTextSize(2);

    display.setCursor(
        10,
        10
    );

    display.println(
        "ACCIDENT"
    );

    display.setCursor(
        16,
        38
    );

    display.println(
        "DETECTED"
    );

    display.display();
}

// ============================================================
// MOTOR SPEED CONTROL
// ============================================================

void updateMotor(
    bool systemON
) {

    // --------------------------------------------------------
    // ACCIDENT OVERRIDES EVERYTHING
    // --------------------------------------------------------

    if (accidentDetected) {

        emergencyMotorStop();

        return;
    }

    unsigned long now =
        millis();

    // ========================================================
    // SYSTEM JUST TURNED ON
    // ========================================================

    if (
        systemON &&
        !lastSystemState
    ) {

        motorRampStart =
            now;

        speed = 0.0;
    }

    // ========================================================
    // SYSTEM JUST TURNED OFF
    // ========================================================

    if (
        !systemON &&
        lastSystemState
    ) {

        motorRampStart =
            now;

        speedAtStop =
            speed;
    }

    // ========================================================
    // ACCELERATION
    // ========================================================

    if (systemON) {

        unsigned long elapsed =
            now -
            motorRampStart;

        if (
            elapsed >=
            ACCELERATION_TIME
        ) {

            speed =
                MAX_SPEED;

        } else {

            speed =
                (
                    (float)elapsed /
                    (float)ACCELERATION_TIME
                ) *
                MAX_SPEED;
        }
    }

    // ========================================================
    // DECELERATION
    // ========================================================

    else {

        unsigned long elapsed =
            now -
            motorRampStart;

        if (
            speedAtStop <=
            0.0
        ) {

            speed =
                0.0;

        } else if (
            elapsed >=
            DECELERATION_TIME
        ) {

            speed =
                0.0;

        } else {

            speed =
                speedAtStop *
                (
                    1.0 -
                    (
                        (float)elapsed /
                        (float)DECELERATION_TIME
                    )
                );
        }
    }

    // ========================================================
    // SPEED TO PWM
    // ========================================================

    motorPWM =
        (int)(
            (speed / MAX_SPEED) *
            PWM_MAX
        );

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

    lastSystemState =
        systemON;
}

// ============================================================
// CURRENT SENSOR
// ============================================================

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

        delayMicroseconds(
            100
        );
    }

    float sensorVoltage =
        (sum / samples) /
        1000.0;

    float current =
        (
            sensorVoltage -
            CURRENT_ZERO
        ) /
        CURRENT_SENSITIVITY;

    current =
        fabs(current);

    if (
        current < 0.03
    ) {

        current =
            0;
    }

    return current;
}

// ============================================================
// VOLTAGE SENSOR
// ============================================================

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

        delayMicroseconds(
            100
        );
    }

    float sensorVoltage =
        (sum / samples) /
        1000.0;

    float actualVoltage =
        sensorVoltage *
        VOLTAGE_RATIO;

    return actualVoltage;
}

// ============================================================
// TEMPERATURE SENSOR
// ============================================================

float readTemperature() {

    sensors.requestTemperatures();

    float temperature =
        sensors.getTempCByIndex(
            0
        );

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

    if (
        WiFi.status() !=
        WL_CONNECTED
    ) {

        Serial.println(
            "WiFi disconnected!"
        );

        return;
    }

    HTTPClient http;

    http.begin(
        SERVER_URL
    );

    http.addHeader(
        "Content-Type",
        "application/json"
    );

    String jsonData =
        "{"
        "\"voltage\":" +
        String(
            voltage,
            2
        ) +

        ",\"current\":" +
        String(
            current,
            2
        ) +

        ",\"temperature\":" +
        String(
            temperature,
            2
        ) +

        ",\"fan\":" +
        String(
            fanON
                ? "true"
                : "false"
        ) +

        ",\"status\":\"" +
        status +
        "\"" +

        ",\"system\":" +
        String(
            systemON
                ? "true"
                : "false"
        ) +

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
        String(
            currentSpeed,
            1
        ) +

        "}";

    Serial.println();
    Serial.println(
        "Sending data:"
    );

    Serial.println(
        jsonData
    );

    int responseCode =
        http.POST(
            jsonData
        );

    Serial.print(
        "HTTP Response Code: "
    );

    Serial.println(
        responseCode
    );

    if (
        responseCode > 0
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

    http.end();
}

// ============================================================
// SETUP
// ============================================================

void setup() {

    Serial.begin(
        115200
    );

    // ========================================================
    // ADC
    // ========================================================

    analogReadResolution(
        12
    );

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
    // ULTRASONIC
    // ========================================================

    pinMode(
        FRONT_TRIG,
        OUTPUT
    );

    pinMode(
        FRONT_ECHO,
        INPUT
    );

    pinMode(
        LEFT_TRIG,
        OUTPUT
    );

    pinMode(
        LEFT_ECHO,
        INPUT
    );

    pinMode(
        RIGHT_TRIG,
        OUTPUT
    );

    pinMode(
        RIGHT_ECHO,
        INPUT
    );

    digitalWrite(
        FRONT_TRIG,
        LOW
    );

    digitalWrite(
        LEFT_TRIG,
        LOW
    );

    digitalWrite(
        RIGHT_TRIG,
        LOW
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

        oledOK =
            true;

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

        delay(
            1500
        );

        display.clearDisplay();

        display.display();

    } else {

        oledOK =
            false;

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

    // Relay OFF
    digitalWrite(
        RELAY_PIN,
        HIGH
    );

    delay(
        2000
    );

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

    double currentSum =
        0;

    for (
        int i = 0;
        i < 2000;
        i++
    ) {

        currentSum +=
            analogReadMilliVolts(
                CURRENT_PIN
            );

        delayMicroseconds(
            100
        );
    }

    float currentVoltage =
        (currentSum / 2000.0) /
        1000.0;

    baseCurrent =
        fabs(
            (
                currentVoltage -
                CURRENT_ZERO
            ) /
            CURRENT_SENSITIVITY
        );

    previousCurrent =
        baseCurrent;

    // ========================================================
    // INITIAL TEMPERATURE
    // ========================================================

    sensors.requestTemperatures();

    previousTemperature =
        sensors.getTempCByIndex(
            0
        );

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
        WiFi.status() !=
        WL_CONNECTED
    ) {

        delay(
            500
        );

        Serial.print(
            "."
        );
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

    // ========================================================
    // START ULTRASONIC SAFETY TASK
    // ========================================================

    Serial.println(
        "Starting ultrasonic safety monitoring..."
    );

    xTaskCreatePinnedToCore(
        ultrasonicSafetyTask,
        "UltrasonicSafety",
        4096,
        NULL,
        3,
        NULL,
        0
    );

    Serial.println(
        "Ultrasonic safety monitoring ACTIVE"
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
// MAIN LOOP
// ============================================================

void loop() {

    // ========================================================
    // ACCIDENT HAS HIGHEST PRIORITY
    // ========================================================

    if (accidentDetected) {

        // Keep motor OFF
        emergencyMotorStop();

        // OLED ONLY SHOWS ACCIDENT
        updateAccidentOLED();

        // ----------------------------------------------------
        // We still send/update sensor data below so dashboard
        // can receive ACCIDENT DETECTED.
        // ----------------------------------------------------
    }

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

    if (
        current > 0.05
    ) {

        systemON =
            true;

    } else {

        systemON =
            false;
    }

    // ========================================================
    // ACCIDENT OVERRIDES SYSTEM STATE
    // ========================================================

    if (accidentDetected) {

        systemON =
            false;
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

    bool fanON =
        false;

    if (
        temperature >=
        FAN_ON_TEMP
    ) {

        fanON =
            true;

    } else if (
        temperature <=
        FAN_OFF_TEMP
    ) {

        fanON =
            false;
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

    // ACCIDENT HAS HIGHEST PRIORITY
    if (accidentDetected) {

        protectionStatus =
            "ACCIDENT DETECTED";

    } else if (
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

    if (
        accidentDetected
    ) {

        motorStatus =
            "OFF";

    } else if (
        systemON
    ) {

        motorStatus =
            "ON";

    } else {

        motorStatus =
            "OFF";
    }

    // ========================================================
    // MOTOR SPEED CONTROL
    // ========================================================

    if (accidentDetected) {

        emergencyMotorStop();

    } else {

        updateMotor(
            systemON
        );
    }

    // ========================================================
    // OLED
    // ========================================================

    if (accidentDetected) {

        // ONLY ACCIDENT MESSAGE
        updateAccidentOLED();

    } else {

        // NORMAL DISPLAY
        updateNormalOLED(
            temperature,
            batteryVoltage,
            current,
            fanON
        );
    }

    // ========================================================
    // SERIAL MONITOR
    // ========================================================

    Serial.println();

    Serial.println(
        "------------------------------------------"
    );

    // --------------------------------------------------------
    // ACCIDENT INFORMATION
    // --------------------------------------------------------

    if (accidentDetected) {

        Serial.println(
            "!!! ACCIDENT DETECTED !!!"
        );

        Serial.println(
            "SYSTEM LOCKED"
        );

        Serial.println(
            "MOTOR OFF"
        );

        Serial.println(
            "Restart ESP32 to reset"
        );

        Serial.println();

        Serial.print(
            "Front Distance : "
        );

        Serial.print(
            frontDistance,
            1
        );

        Serial.println(
            " cm"
        );

        Serial.print(
            "Left Distance  : "
        );

        Serial.print(
            leftDistance,
            1
        );

        Serial.println(
            " cm"
        );

        Serial.print(
            "Right Distance : "
        );

        Serial.print(
            rightDistance,
            1
        );

        Serial.println(
            " cm"
        );

    } else {

        // ----------------------------------------------------
        // NORMAL INFORMATION
        // ----------------------------------------------------

        Serial.print(
            "System : "
        );

        if (systemON) {

            Serial.println(
                "ON"
            );

        } else {

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

        } else {

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
    }

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

    delay(
        5
    );
}
