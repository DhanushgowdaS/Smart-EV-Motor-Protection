from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="EV Motor Protection API"
)


# ============================================================
# DATA MODEL
# ============================================================

class SensorData(BaseModel):

    voltage: float

    current: float

    temperature: float

    current_trend: str

    temperature_trend: str

    load_status: str

    motor_status: str

    fan: bool


# ============================================================
# LATEST DATA
# ============================================================

latest_data = {

    "voltage": 0.0,

    "current": 0.0,

    "temperature": 0.0,

    "current_trend": "STABLE",

    "temperature_trend": "STABLE",

    "load_status": "NORMAL",

    "motor_status": "NORMAL",

    "fan": False,

    "timestamp": None
}


# ============================================================
# RECEIVE ESP32 DATA
# ============================================================

@app.post("/data")
def receive_data(data: SensorData):

    global latest_data

    latest_data = data.model_dump()

    latest_data["timestamp"] = (
        datetime.now().isoformat()
    )

    return {

        "success": True,

        "message": "Data received"

    }


# ============================================================
# STREAMLIT GETS LATEST DATA
# ============================================================

@app.get("/data")
def get_data():

    return latest_data


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {

        "system":
        "EV Motor Protection API",

        "status":
        "running"

    }
