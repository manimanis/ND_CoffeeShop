import os
import unittest
from flask_sqlalchemy import SQLAlchemy

from src.api import create_app
from src.database.models import setup_db, db_drop_and_create_all, Drink


BARISTER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNsV1ZCaFkw' \
                 'VzVfYTNseEZ1QldLWiJ9.eyJpc3MiOiJodHRwczovL21hbmlhbmlzLmV' \
                 '1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTkxODJkN2Q4OWRlZTB' \
                 'iZGQxN2NiMDIiLCJhdWQiOiJ1ZGFjaXR5X2NvZmZlZV9zaG9wX2FwaSI' \
                 'sImlhdCI6MTU4NjYyMjcyOSwiZXhwIjoxNTg2NzA5MTI4LCJhenAiOiJ' \
                 '4ckJiSzJ4TVlNNnRhS3pTUDFteTFzNTI2dDhucnlGYSIsInNjb3BlIjo' \
                 'iIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.kne' \
                 'DFpaOY3IYpP0zES42V6A4gqInCmZj-SgudZB9ZPh_RP3A7rFFEHXtlwT' \
                 'l0_glJGFCfGLpT89GKaEZkNk-X2zNmEszdjCBSZSSruTiWhhl-9SaL1R' \
                 'oqI94imJJ_2KTl-9zX3Op1DbJiS_CCiYYsdoEMwf5_kTxu6fOJcbT_mX' \
                 'N2fFyA0ou2ZhyGTs4fIh4MJAFbJ0CfLEOOjsGbPxgO6DPvzK_PmnbZh8' \
                 '28Mwz2hgMCEYWbIVAxFBNcGnfOqsnW-sjhUowMSrPqM9qwg4AUIqQpgp' \
                 '_1JcXTEfitlBSXjgmvmI7Ox3lP1pKUlsPH3iAkBmbpxc1VyVED2Wk9zPLJg'
MANAGER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNsV1ZCaFkwV' \
                'zVfYTNseEZ1QldLWiJ9.eyJpc3MiOiJodHRwczovL21hbmlhbmlzLmV1L' \
                'mF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTk4Mzc0MT' \
                'A1NjMyMzc3OTc0NCIsImF1ZCI6WyJ1ZGFjaXR5X2NvZmZlZV9zaG9wX2F' \
                'waSIsImh0dHBzOi8vbWFuaWFuaXMuZXUuYXV0aDAuY29tL3VzZXJpbmZv' \
                'Il0sImlhdCI6MTU4NjYyMTg2MCwiZXhwIjoxNTg2NzA4MjU5LCJhenAiO' \
                'iJ4ckJiSzJ4TVlNNnRhS3pTUDFteTFzNTI2dDhucnlGYSIsInNjb3BlIj' \
                'oib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWx' \
                'ldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlu' \
                'a3MiLCJwb3N0OmRyaW5rcyJdfQ.LtsdkIzHsCDU6Ifddsm38RTXe9qCxk' \
                'RlvqY5gcu0_iuyphbw-FElQbOg0OSretcVx57aSyYAiDA7K9EmxaBASXl' \
                '_O9rbA2dGveGNqOURZlPd-3y3ro5w41W0zGolN37xiUsr9O77Pc8q3ag_' \
                'JjyqxUVnrjueslTeykhyLFdJyW4geQDbYQ6VA60tMvl_fy974bwy0nwFC' \
                'cdBFCbk3bfa0E0X391zvN0lhdenuqGTpr0o4jwvIbMXbEHFJYuPj9G4hq' \
                'un0KgSJhCxMYbPOT98O7wV1a36Pp6smh6KJj4M6n3ivNItNE1iOcb4XyF' \
                'h5LeBxj8rB11LnZ7pX_LdSvRNMQ'


class DrinkTestCase(unittest.TestCase):
    """This class represents the Drink resource test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        database_filename = "src/test_database.db"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "sqlite:///{}" \
            .format(os.path.join(project_dir, database_filename))

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def drink_data_common_form(self, data):
        """Test if the drink data are in the common form to long and short"""
        self.assertTrue(data['success'])
        self.assertTrue('drinks' in data)
        self.assertGreater(len(data['drinks']), 0)
        for drink in data['drinks']:
            self.assertTrue('id' in drink)
            self.assertTrue('title' in drink)
            self.assertTrue('recipe' in drink)

            for part in drink['recipe']:
                self.assertIn('parts', part)
                self.assertIn('color', part)

    def drink_data_is_in_short_form(self, data):
        """To be in the short form the recipe data must not include names"""
        self.drink_data_common_form(data)
        for drink in data['drinks']:
            for part in drink['recipe']:
                self.assertNotIn('name', part)

    def drink_data_is_in_long_form(self, data):
        """To be in the short form the recipe data include names"""
        self.drink_data_common_form(data)
        for drink in data['drinks']:
            for part in drink['recipe']:
                self.assertIn('name', part)

    # Regular user tests ------------------------------------------------------
    def test_user_fetch_drinks(self):
        """Every user can get list of drinks in their short form"""
        res = self.client().get('/drinks')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.drink_data_is_in_short_form(data)

    def test_user_fetch_drinks_details(self):
        """Without role user doesn't have access to drinks details"""
        res = self.client().get('/drinks-detail')
        self.assertEqual(res.status_code, 401)

    def test_user_insert_drink(self):
        """Normal user cannot insert drinks"""
        res = self.client().post('/drinks', json={
            'title': 'New Drink',
            'recipe': {
                'name': 'part1',
                'color': 'white',
                'parts': 2
            }
        })
        self.assertEqual(res.status_code, 401)

    def test_user_update_drink(self):
        """Normal user cannot update drinks"""
        res = self.client().patch('/drinks/1', json={
            'title': 'New Drink',
            'recipe': {
                'name': 'part1',
                'color': 'white',
                'parts': 2
            }
        })
        self.assertEqual(res.status_code, 401)

    def test_user_fetch_delete_drink(self):
        """Normal user cannot delete drinks"""
        res = self.client().delete('/drinks/1')
        self.assertEqual(res.status_code, 401)

    # Barister user tests -----------------------------------------------------
    def test_barister_fetch_drinks(self):
        """Barrister can view list of drinks"""
        res = self.client().get('/drinks',
                                headers={
                                    'Authorization': f'Bearer {BARISTER_TOKEN}'
                                })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.drink_data_is_in_short_form(data)

    def test_barister_fetch_drinks_details(self):
        """Barrister can view drinks details"""
        res = self.client().get('/drinks-detail',
                                headers={
                                    'Authorization': f'Bearer {BARISTER_TOKEN}'
                                })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.drink_data_is_in_long_form(data)

    def test_barister_insert_drink(self):
        """Barrister cannot insert new drinks"""
        res = self.client().post('/drinks',
                                 json={
                                     'title': 'New Drink',
                                     'recipe': {
                                         'name': 'part1',
                                         'color': 'white',
                                         'parts': 2
                                     }
                                 },
                                 headers={
                                     'Authorization':
                                         f'Bearer {BARISTER_TOKEN}'
                                 })
        self.assertEqual(res.status_code, 403)

    def test_barister_update_drink(self):
        """Barrister cannot update existing drinks"""
        res = self.client().patch('/drinks/1',
                                  json={
                                      'title': 'New Drink',
                                      'recipe': {
                                          'name': 'part1',
                                          'color': 'white',
                                          'parts': 2
                                      }
                                  },
                                  headers={
                                      'Authorization':
                                          f'Bearer {BARISTER_TOKEN}'
                                  })
        self.assertEqual(res.status_code, 403)

    def test_barister_fetch_delete_drink(self):
        """Barrister cannot delete drinks"""
        res = self.client().delete('/drinks/1',
                                   headers={
                                       'Authorization':
                                           f'Bearer {BARISTER_TOKEN}'
                                   })
        self.assertEqual(res.status_code, 403)

    # Manager user tests -----------------------------------------------------
    def test_manager_fetch_drinks(self):
        """Manager can view list of drinks"""
        res = self.client().get('/drinks',
                                headers={
                                    'Authorization': f'Bearer {MANAGER_TOKEN}'
                                })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.drink_data_is_in_short_form(data)

    def test_manager_fetch_drinks_details(self):
        """Manager can view drinks details"""
        res = self.client().get('/drinks-detail',
                                headers={
                                    'Authorization': f'Bearer {MANAGER_TOKEN}'
                                })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.drink_data_is_in_long_form(data)

    def test_manager_insert_drink(self):
        """Manager can insert new drinks"""
        res = self.client().post('/drinks',
                                 json={
                                     'title': 'New Drink',
                                     'recipe': {
                                         'name': 'part1',
                                         'color': 'white',
                                         'parts': 2
                                     }
                                 },
                                 headers={
                                     'Authorization':
                                         f'Bearer {MANAGER_TOKEN}'
                                 })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.drink_data_is_in_long_form(data)

    def test_manager_insert_drink_missing_fields(self):
        """Manager cannot insert partial data"""
        data = {
            'title': 'New Drink',
            'recipe': {
                'name': 'part1',
                'color': 'white',
                'parts': 2
            }
        }
        for k in data.keys():
            res = self.client().post('/drinks',
                                     json={k: data[k]},
                                     headers={
                                         'Authorization':
                                             f'Bearer {MANAGER_TOKEN}'
                                     })
            self.assertEqual(res.status_code, 422)

    def test_manager_insert_duplicate_drinks(self):
        """Manager cannot insert duplicate drinks"""
        data = Drink.query.first().long()
        del data['id']
        res = self.client().post('/drinks',
                                 json=data,
                                 headers={
                                     'Authorization':
                                         f'Bearer {MANAGER_TOKEN}'
                                 })
        self.assertEqual(res.status_code, 422)

    def test_manager_update_drink(self):
        """Manager can update existing drinks"""
        res = self.client().patch('/drinks/1',
                                  json={
                                      'title': 'New Drink',
                                      'recipe': {
                                          'name': 'part1',
                                          'color': 'white',
                                          'parts': 2
                                      }
                                  },
                                  headers={
                                      'Authorization':
                                          f'Bearer {MANAGER_TOKEN}'
                                  })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.drink_data_is_in_long_form(data)

    def test_manager_update_inexistant_drink(self):
        """Manager cannot delete inexistant drinks"""
        # Get the last drink
        drink = (Drink
                 .query
                 .order_by(Drink.id.desc())
                 .first()
                 .short())
        drink_id = drink['id'] + 1
        res = self.client().patch(f'/drinks/{drink_id}',
                                  json={
                                      'title': 'New Drink',
                                      'recipe': {
                                          'name': 'part1',
                                          'color': 'white',
                                          'parts': 2
                                      }
                                  },
                                  headers={
                                      'Authorization':
                                          f'Bearer {MANAGER_TOKEN}'
                                  })
        self.assertEqual(res.status_code, 404)

    def test_manager_fetch_delete_drink(self):
        """Manager can delete existing drinks"""
        res = self.client().delete('/drinks/1',
                                   headers={
                                       'Authorization':
                                           f'Bearer {MANAGER_TOKEN}'
                                   })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['delete'], 1)

    def test_manager_fetch_delete_inexistant_drink(self):
        """Manager cannot delete inexistant drinks"""
        # Get the last drink
        drink = (Drink
                 .query
                 .order_by(Drink.id.desc())
                 .first()
                 .short())
        drink_id = drink['id'] + 1
        res = self.client().delete(f'/drinks/{drink_id}',
                                   headers={
                                       'Authorization':
                                           f'Bearer {MANAGER_TOKEN}'
                                   })
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()

