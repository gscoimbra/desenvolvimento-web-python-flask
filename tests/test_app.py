import sys
import os
import unittest
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class FlaskTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

        cls.db = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="api2-python",
            user="postgres",
            password="root"
        )
        cls.cursor = cls.db.cursor()
        cls.cursor.execute("DROP TABLE IF EXISTS usuarios")
        cls.cursor.execute('''
            CREATE TABLE usuarios (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        cls.db.commit()

    def setUp(self):
        self.cursor.execute("DELETE FROM usuarios")
        self.db.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.db.close()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_route_get(self):
        response = self.client.get('/cadastrar')
        self.assertEqual(response.status_code, 200)

    def test_cadastrar_route_post(self):
        response = self.client.post('/cadastrar', data=dict(nome='Teste', email='teste@email.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Teste', response.data)

    def test_editar_route(self):
        self.client.post('/cadastrar', data=dict(nome='Editar', email='editar@email.com'), follow_redirects=True)

        self.cursor.execute("SELECT id FROM usuarios WHERE nome = %s", ('Editar',))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        user_id = result[0]

        response = self.client.post(f'/editar/{user_id}', data=dict(nome='Editado', email='editado@email.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Editado', response.data)


if __name__ == '__main__':
    unittest.main()
