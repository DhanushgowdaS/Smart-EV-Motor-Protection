# 🚗 Smart EV Motor Temperature & Overload Protection System

An ESP32-based intelligent EV motor protection system designed to monitor motor temperature, motor current, overload conditions, cooling system, and obstacle detection in real time. The system automatically protects the motor from overheating and overload while providing a professional dashboard for live monitoring.

---

# 📖 Project Overview

Electric vehicle motors are subjected to varying loads during operation. High mechanical load increases motor current, which causes the motor windings to heat up. Continuous overheating may damage the motor and reduce its lifespan.

This project continuously monitors motor temperature and motor current using sensors connected to an ESP32. Based on predefined protection levels, the system automatically activates the cooling fan, provides warnings, and shuts down the motor if the temperature exceeds safe operating limits.

Additionally, the system integrates three ultrasonic sensors for obstacle detection. When the vehicle is operating above a predefined speed threshold, obstacles are detected and the motor speed is automatically reduced or stopped to improve safety.

The complete system can be monitored through an OLED display as well as a modern web-based dashboard.

---

# 🎯 Objectives

- Monitor motor temperature continuously.
- Detect motor overload using current sensing.
- Automatically activate the cooling fan.
- Protect the motor from overheating.
- Stop the motor during critical conditions.
- Display live parameters on OLED.
- Monitor the complete system through a web dashboard.
- Detect front, left and right obstacles.
- Automatically reduce speed or stop the motor during obstacle detection.
- Demonstrate an intelligent EV motor protection system.

---

# ⚙️ Features

✅ Real-time Motor Temperature Monitoring

✅ Real-time Motor Current Monitoring

✅ Automatic Cooling Fan Control

✅ Multi-Level Protection System

✅ Emergency Motor Shutdown

✅ OLED Live Display

✅ ESP32 Web Dashboard

✅ Obstacle Detection

✅ Automatic Speed Reduction

✅ Battery Voltage Monitoring

✅ Warning Buzzer

✅ Visual Status Indicators

---

# 🛠 Hardware Components

- ESP32 DevKit V1
- DC Geared Motor
- L298N Motor Driver
- ACS712 Current Sensor
- DS18B20 Temperature Sensor
- 12V Cooling Fan
- MOSFET Module
- 0.96" OLED Display
- Active Buzzer
- LEDs
- Push Buttons
- Three HC-SR04 Ultrasonic Sensors
- 12V Battery / Adapter
- Wooden Chassis
- Connecting Wires

---

# 🖥 Dashboard Parameters

The web dashboard displays:

- Motor Temperature
- Motor Current
- Motor Speed
- Battery Voltage
- Cooling Fan Status
- Protection Status
- Obstacle Detection Status
- System Health
- Warning Notifications

---

# 🛡 Protection Levels

| Level | Condition | Action |
|--------|-----------|--------|
| Level 1 | Normal | Motor runs normally |
| Level 2 | Load Detected | Monitor motor |
| Level 3 | High Temperature | Cooling Fan ON |
| Level 4 | Critical | Warning Display |
| Level 5 | Maximum Temperature | Motor Shutdown |

---

# 🚧 Obstacle Detection

Three ultrasonic sensors are used.

- Front Sensor
- Left Sensor
- Right Sensor

When the vehicle speed is above the predefined limit, the ESP32 continuously checks for nearby obstacles.

If an obstacle is detected:

- Motor speed reduces.
- Warning is displayed.
- Motor stops if necessary.

---

# 📊 System Workflow

```
Power ON
      │
      ▼
Read Sensors
      │
      ▼
Measure Current
      │
Measure Temperature
      │
Obstacle Detection
      │
      ▼
Protection Decision
      │
      ▼
Update Dashboard
      │
      ▼
Run / Cool / Warn / Stop
```

---

# 📁 Project Structure

```
Smart-EV-Motor-Protection/
│
├── firmware/
├── web_dashboard/
├── docs/
├── hardware/
├── images/
└── README.md
```

---

# 🔮 Future Enhancements

- Cloud Data Logging
- Mobile Application
- Battery Health Monitoring
- GPS Tracking
- Motor RPM Measurement
- Predictive Maintenance using AI
- MQTT Integration

---

# 👨‍💻 Developed Using

- ESP32
- Arduino IDE
- HTML
- CSS
- JavaScript
- OLED Graphics
- Embedded C++

---

# 📄 License

This project is developed for educational and research purposes.

---

# ⭐ Repository

If you find this project useful, consider giving this repository a ⭐.
