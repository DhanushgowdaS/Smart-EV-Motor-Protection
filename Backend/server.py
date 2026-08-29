from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime


# ============================================================
# FASTAPI APPLICATION
# ============================================================

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

    fan: bool

    status: str

    system: bool

    current_trend: str

    temperature_trend: str

    load_status: str

    motor_status: str


# ============================================================
# LATEST DATA
# ============================================================

latest_data = {

    "voltage": 0.0,

    "current": 0.0,

    "temperature": 0.0,

    "fan": False,

    "status": "NORMAL",

    "system": False,

    "current_trend": "STABLE",

    "temperature_trend": "STABLE",

    "load_status": "LOAD STABLE",

    "motor_status": "OFF",

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
# GET LATEST DATA
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

        "system": "EV Motor Protection API",

        "status": "running"

    }
