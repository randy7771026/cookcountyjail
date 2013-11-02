#
# Tests the web API wiring to class that provides daily population changes
# functionality.
#

from json import loads
from random import randint

from ccj.app import app
from helper import flatten_dpc_dict, safe_remove_file


class Test_DailyPopulationChanges_API:

    def setup_method(self, method):
        app.testing = True
        self._tmp_file = app.config['DPC_PATH']
        safe_remove_file(self._tmp_file)
        self.client = app.test_client()

    def teardown_method(self, method):
        safe_remove_file(self._tmp_file)

    def test_fetch_with_nothing_stored_returns_empty_array(self):
        expected = '[]'
        result = self.client.get('/daily_population_changes')
        assert result.status_code == 200
        assert result.data == expected

    def test_post_with_one_entry_should_store_result(self):
        expected = [
            {
                'Date': '2013-10-30',
                'Males': {
                    'Booked': {'AS': str(randint(0, 101))}
                }
            }
        ]
        result = self.client.post('/daily_population_changes',
                                  data=flatten_dpc_dict(expected[0]))
        assert result.status_code == 201

        result = self.client.get('/daily_population_changes')
        assert loads(result.data, encoding='ASCII') == expected

    def test_external_post_fails(self):

        data = {
            'Date': '2013-10-30',
            'Males': {
                'Booked': {'As': str(randint(0, 101))}
            }
        }

        result = self.client.post('/daily_population_changes',
                                  data=flatten_dpc_dict(data),
                                  environ_overrides={'REMOTE_ADDR': '127.0.0.2'})
        assert result.status_code == 401
