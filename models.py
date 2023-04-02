from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Hepsiburada(SQLModel, table=True):
    dataID: Optional[int] = Field(default=None, primary_key=True)
    memory: float
    ram: float
    screen_size: float
    power:float
    front_camera:float
    rc1: float
    rc3: float
    rc5: float
    rc7: float
    prediction: float
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str



class HepsiburadaTrain(SQLModel, table=True):
    dataID: Optional[int] = Field(default=None, primary_key=True)
    memory: float
    ram: float
    screen_size: float
    power:float
    front_camera:float
    rc1: float
    rc3: float
    rc5: float
    rc7: float
    price: float



class HepsiburadaInput(SQLModel):
    memory: float
    ram: float
    screen_size: float
    power:float
    front_camera:float
    rc1:float
    rc3:float
    rc5:float
    rc7:float

    class Config:
        schema_extra = {
            "example": {
                "memory": 128.0,
                "ram": 8.0,
                "screen_size": 6.40,
                "power": 4310.0,
                "front_camera": 32.0,
                "rc1": 48.0,
                "rc3": 8.0 ,
                "rc5": 2.0,
                "rc7": 2.0,

            }
        }


class HepsiburadaDriftInput(SQLModel):
    n_days_before: int

    class Config:
        schema_extra = {
            "example": {
                "n_days_before": 5,
            }
        }