import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

import unittest
import psycopg2

class ConnTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_db_connection(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                dbname="api2-python",
                user="postgres",
                password="root"
            )
            conn.close()
        except Exception as e:
            self.fail(f"Falha na conexão com o banco: {e}")

if __name__ == "__main__":
    unittest.main()
