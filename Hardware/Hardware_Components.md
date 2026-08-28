# 🔧 Hardware Components

This project is a prototype **EV Motor Protection and Monitoring System**.
It monitors motor current, motor temperature, and battery voltage.
When the motor temperature becomes high, a cooling fan is automatically
activated through a relay.

## 📦 Components Used

| No. | Component | Quantity | Purpose / Use |
|-----|-----------|----------|---------------|
| 1 | ESP32 DevKit | 1 | Main controller. Reads all sensors, processes the data, controls the relay/fan, and can send data through Wi-Fi. |
| 2 | ACS712 30A Current Sensor | 1 | Measures the current consumed by the motor and detects changes in motor load. |
| 3 | Voltage Sensor Module (0–25V) | 1 | Measures the battery/motor supply voltage and sends a scaled voltage signal to the ESP32. |
| 4 | DS18B20 Temperature Sensor | 1 | Measures the motor temperature and helps detect overheating. |
| 5 | 4.7kΩ Resistor | 1 | Pull-up resistor required for reliable communication between the DS18B20 and ESP32. |
| 6 | L298N Motor Driver | 1 | Controls the motor and allows the ESP32 to control the motor direction/speed. |
| 7 | DC Motor | 1 | Used as the prototype EV motor/load for testing the protection system. |
| 8 | Relay Module | 1 | Electrically switches the cooling fan ON/OFF based on the motor temperature. |
| 9 | DC Cooling Fan | 1 | Cools the motor when the temperature reaches the protection threshold. |
| 10 | Battery | 1 | Provides power to the motor and the prototype system. |
| 11 | Jumper Wires | As required | Used to make electrical connections between the ESP32, sensors, relay, and other components. |
| 12 | Breadboard / Prototype Board | 1 | Used to assemble and test the circuit without permanent soldering. |
| 13 | Multimeter | 1 | Used for testing and verifying voltage, current, continuity, and circuit connections. |

---

# ⚡ Sensor Connections

| Component | ESP32 Pin | Function |
|-----------|-----------|----------|
| Voltage Sensor OUT | GPIO 34 | Battery voltage measurement |
| ACS712 OUT | GPIO 35 | Motor current measurement |
| DS18B20 DATA | GPIO 4 | Motor temperature measurement |
| Relay IN | GPIO 13 | Cooling fan control |

---

# 🌡️ Temperature Sensor

The DS18B20 is used to monitor the temperature of the motor.

A **4.7kΩ pull-up resistor** is connected between the DATA pin and 3.3V.

Connections:

    DS18B20 VCC  → ESP32 3.3V
    DS18B20 GND  → ESP32 GND
    DS18B20 DATA → ESP32 GPIO 4

    4.7kΩ resistor:
    DATA → 3.3V

---

# ⚡ Current Sensor

The ACS712-30A measures the current consumed by the motor.

The current sensor is connected **in series with the motor power path**.

The ESP32 reads the ACS712 output voltage through:

    ACS712 OUT → ESP32 GPIO 35

The system uses the current variation to identify changes in motor load.

---

# 🔋 Voltage Sensor

The voltage sensor module measures the battery voltage.

    Voltage Sensor OUT → ESP32 GPIO 34

The ESP32 converts the sensor output into the actual battery voltage.

---

# 🌀 Cooling Fan

A relay is used to control the cooling fan.

    ESP32 GPIO 13 → Relay IN

The relay is configured as an **active-LOW relay**.

    HIGH → Fan OFF
    LOW  → Fan ON

The fan is activated when the motor temperature reaches the configured
protection temperature.

---

# ⚙️ Motor Driver

The L298N motor driver is used to control the DC motor.

The ESP32 provides the control signals to the L298N, while the motor
receives its required power through the motor driver.

The motor driver allows the prototype to simulate different motor loads
during testing.

---

# 🔄 System Working

    Battery
       │
       ├──────────────→ Motor Driver → DC Motor
       │
       └──────────────→ Monitoring Circuit
                              │
              ┌───────────────┼────────────────┐
              │               │                │
        Voltage Sensor    ACS712-30A        DS18B20
              │               │                │
              └───────────────┼────────────────┘
                              │
                            ESP32
                              │
                         Relay Module
                              │
                         Cooling Fan

The ESP32 continuously monitors:

- Battery voltage
- Motor current
- Motor temperature
- Current variation
- Temperature variation
- Cooling fan status

When the motor load increases, the motor may consume more current.
If the motor temperature also rises and reaches the configured
protection level, the ESP32 activates the cooling fan automatically.

---

# 🎯 Project Objective

The main objective of this prototype is to demonstrate a **motor
overload and overheating protection system**.

The system monitors changes in motor current and temperature and
automatically activates a cooling fan when the motor temperature becomes
too high.

This concept can be further developed for **EV motor protection systems**
to help prevent motor overheating and potential damage.
