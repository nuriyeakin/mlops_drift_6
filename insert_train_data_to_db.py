import pandas as pd
from sqlalchemy.sql import text as sa_text
from database import engine
from models import HepsiburadaTrain
from sqlmodel import Session

# read data
df = pd.read_csv("https://raw.githubusercontent.com/KuserOguzHan/mlops_1/main/hepsiburada.csv.csv")
print(df.head())

# Truncate table with sqlalchemy
with Session(engine) as session:
    session.execute(sa_text(''' TRUNCATE TABLE hepsiburadatrain  '''))
    session.commit()

# Insert training data
records_to_insert = []

for df_idx, line in df.iterrows():
    records_to_insert.append(
                    HepsiburadaTrain(memory=line[1],
                    ram=line[2],
                    screen_size=line[3],
                    power=line[4],
                    front_camera=line[5],
                    rc1=line[6],
                    rc3=line[7],
                    rc5=line[8],
                    rc7=line[9],
                    price=line[10]
                    )
    )

session.bulk_save_objects(records_to_insert)
session.commit()
# Ends database insertion

    