import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

def connect_db() -> psycopg2.connect:
  """Function to connect to Heroku database, returns connection."""

  load_dotenv()
  connection = psycopg2.connect(
    database=os.getenv("H_DATABASE"),
    user=os.getenv("H_USER"),
    password=os.getenv("H_PASSWORD"),
    host=os.getenv("H_HOST"),
    port=os.getenv("H_PORT")
  )
  return connection

def create_table() -> None:
  """Function to create table to store predictions."""
  
  con = connect_db()
  cur = con.cursor()
  cur.execute("""
  CREATE TABLE IF NOT EXISTS objects(
    id serial PRIMARY KEY,
    neighborhood VARCHAR(255),
    rooms INT,
    area_m2 FLOAT,
    floor INT,
    max_floors INT,
    year INT,
    build_material VARCHAR(255),
    heating_type VARCHAR(255),
    condition VARCHAR(255),
    prediction FLOAT
  );
  """)
  con.commit()
  cur.close()

def data_to_db(input_df: dict, pred: list) -> None:
  """
  Function to upload prediction results to heroku database.
  :param input_df: input DataFrame for linear regression.
  :param pred: prediction values.
  """
  con = connect_db()
  cur = con.cursor()

  input_df = pd.DataFrame(input_df)
  input_df["pred"] = pred
  records = list(input_df.to_records(index=False))
  for row in records:
    (
      neighborhood, 
      rooms, 
      area_m2, 
      floor, 
      max_floors, 
      year, 
      build_material, 
      heating_type, 
      condition, 
      pred
    ) = row
    insert_this = f"INSERT INTO objects(neighborhood, rooms, area_m2, floor, \
      max_floors, year, build_material, heating_type, condition, pred) \
      VALUES('{neighborhood}', '{rooms}', '{area_m2}', '{floor}', '{max_floors}', \
      '{year}', '{build_material}', '{heating_type}', '{condition}', '{pred}')"
    cur.execute(insert_this)

  con.commit()
  cur.close()


def last10(input_df: pd.DataFrame, pred: list) -> dict:
  """Function to get last 10 predictions, returns dictionary."""
  
  con = connect_db()
  cur = con.cursor()

  cur.execute("""
    SELECT * FROM objects ORDER BY id DESC LIMIT 10;
  """)
  history10 = cur.fetchall()
  
  last10 = [
    {
      "neighborhood": row[0], 
      "rooms": row[1], 
      "area_m2": row[2], 
      "floor": row[3], 
      "max_floors": row[4], 
      "year": row[5], 
      "build_material": row[6], 
      "heating_type": row[7], 
      "condition": row[8], 
      "pred": row[9]
    } for row in history10
  ]
  con.commit()
  cur.close()
  return last10









