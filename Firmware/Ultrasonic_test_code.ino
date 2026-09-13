// ============================================================
// 3-ULTRASONIC SENSOR TEST
// ============================================================

// FRONT
#define FRONT_TRIG 15
#define FRONT_ECHO 14

// LEFT
#define LEFT_TRIG 26
#define LEFT_ECHO 25

// RIGHT
#define RIGHT_TRIG 33
#define RIGHT_ECHO 32

// Maximum time to wait for echo
#define ULTRASONIC_TIMEOUT 30000


// ============================================================
// READ ULTRASONIC DISTANCE
// ============================================================

float readDistance(int trigPin, int echoPin)
{
    // Make sure trigger is LOW
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    // Send 10 microsecond trigger pulse
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Measure echo pulse
    unsigned long duration =
        pulseIn(
            echoPin,
            HIGH,
            ULTRASONIC_TIMEOUT
        );

    // No echo received
    if (duration == 0)
    {
        return -1;
    }

    // Calculate distance in cm
    float distance =
        (duration * 0.0343) / 2.0;

    return distance;
}


// ============================================================
// SETUP
// ============================================================

void setup()
{
    Serial.begin(115200);

    // --------------------------------------------------------
    // FRONT
    // --------------------------------------------------------

    pinMode(FRONT_TRIG, OUTPUT);
    pinMode(FRONT_ECHO, INPUT);

    // --------------------------------------------------------
    // LEFT
    // --------------------------------------------------------

    pinMode(LEFT_TRIG, OUTPUT);
    pinMode(LEFT_ECHO, INPUT);

    // --------------------------------------------------------
    // RIGHT
    // --------------------------------------------------------

    pinMode(RIGHT_TRIG, OUTPUT);
    pinMode(RIGHT_ECHO, INPUT);

    // Keep all trigger pins LOW
    digitalWrite(FRONT_TRIG, LOW);
    digitalWrite(LEFT_TRIG, LOW);
    digitalWrite(RIGHT_TRIG, LOW);

    Serial.println();
    Serial.println("======================================");
    Serial.println("     3 ULTRASONIC SENSOR TEST");
    Serial.println("======================================");

    Serial.println();
    Serial.println("Pin Configuration:");
    Serial.println("Front : TRIG = GPIO15 | ECHO = GPIO14");
    Serial.println("Left  : TRIG = GPIO26 | ECHO = GPIO25");
    Serial.println("Right : TRIG = GPIO33 | ECHO = GPIO32");

    Serial.println();
    Serial.println("Starting test...");
    Serial.println();
}


// ============================================================
// LOOP
// ============================================================

void loop()
{
    // --------------------------------------------------------
    // FRONT SENSOR
    // --------------------------------------------------------

    float frontDistance =
        readDistance(
            FRONT_TRIG,
            FRONT_ECHO
        );

    // Small delay to prevent ultrasonic interference
    delay(50);


    // --------------------------------------------------------
    // LEFT SENSOR
    // --------------------------------------------------------

    float leftDistance =
        readDistance(
            LEFT_TRIG,
            LEFT_ECHO
        );

    delay(50);


    // --------------------------------------------------------
    // RIGHT SENSOR
    // --------------------------------------------------------

    float rightDistance =
        readDistance(
            RIGHT_TRIG,
            RIGHT_ECHO
        );


    // ========================================================
    // PRINT RESULTS
    // ========================================================

    Serial.println("--------------------------------------");

    // FRONT
    Serial.print("FRONT : ");

    if (frontDistance < 0)
    {
        Serial.println("NO ECHO");
    }
    else
    {
        Serial.print(frontDistance, 1);
        Serial.println(" cm");
    }


    // LEFT
    Serial.print("LEFT  : ");

    if (leftDistance < 0)
    {
        Serial.println("NO ECHO");
    }
    else
    {
        Serial.print(leftDistance, 1);
        Serial.println(" cm");
    }


    // RIGHT
    Serial.print("RIGHT : ");

    if (rightDistance < 0)
    {
        Serial.println("NO ECHO");
    }
    else
    {
        Serial.print(rightDistance, 1);
        Serial.println(" cm");
    }

    Serial.println("--------------------------------------");

    delay(500);
}
