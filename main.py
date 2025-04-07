
import pandas as pd
import sqlite3
from datetime import datetime
from random import randint, random,choice


def read_patients():
  # Create SQLite connection
  conn = sqlite3.connect('patients.db')

  conn.close()


