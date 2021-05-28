from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle
import logging

app.config["TESTING"] =True

class FlaskTests(TestCase):

    def test_show_score(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle</h1>', html)
            self.assertIn('board', session)


    def test_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["H","E","L","L","O"],
                                            ["H","E","L","L","O"],
                                            ["H","E","L","L","O"],
                                            ["H","E","L","L","O"],
                                            ["H","E","L","L","O"]]

            res1 = client.get('/guess?guess=bat')
            code1 = res1.json['result']
            self.assertEqual(res1.status_code, 200)
            self.assertEqual(code1, "not-on-board")

            res2 = client.get('/guess?guess=lllll')
            code2 = res2.json['result']
            self.assertEqual(res2.status_code, 200)
            self.assertEqual(code2, "not-word")

            res3 = client.get('/guess?guess=hello')
            code3 = res3.json['result']
            self.assertEqual(res3.status_code, 200)
            self.assertEqual(code3, "ok")


    def test_end(self):
        with app.test_client() as client:
            res1 = client.post('/end', json = {"score" : 10})

            self.assertEqual(res1.status_code, 200)
            self.assertEqual(res1.json["games_played"], 1)
            self.assertEqual(res1.json["high_score"], 10)

            with client.session_transaction() as change_session:
                change_session['games_played'] = 20
                change_session['high_score'] = 100

            res2 = client.post('/end', json = {"score" : 10})

            self.assertEqual(res2.status_code, 200)
            self.assertEqual(res2.json["games_played"], 21)
            self.assertEqual(res2.json["high_score"], 100)

