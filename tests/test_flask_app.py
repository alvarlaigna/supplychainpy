import logging
import os
import tempfile
import unittest

from supplychainpy.launch_reports import load_db
from supplychainpy.reporting.views import app
from supplychainpy.sample_data.config import ABS_FILE_PATH

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class TestFlaskReports(unittest.TestCase):

    def setUp(self):
        self.db_rs, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            load_db(file=ABS_FILE_PATH['COMPLETE_CSV_SM'])

    def tearDown(self):
        """Close database link and delete sqlite database"""
        os.close(self.db_rs)
        os.unlink(app.config['DATABASE'])
        app_dir = os.path.dirname(__file__, )
        rel_path = 'reporting.db'
        abs_file_path = os.path.abspath(os.path.join(app_dir, rel_path))
        os.remove(abs_file_path)

    def test_loaded_db(self):
        index_page = self.app.get('/')
        headings = [b'Top 10 Shortages', b'Classification Breakdown',  b'Top 10 Shortages']
        for heading in headings:
            assert heading in index_page.data

    def test_inventory_analysis_api(self):
        inventory_analysis = self.app.get('/api/inventory_analysis')
        headings = [b'abc_xyz_classification', b'average_orders',  b'currency']
        print(inventory_analysis.data)
        for heading in headings:
            assert heading in inventory_analysis.data

    #def test_launch_report(self):
    #    launcher = tk.Tk()
    #    spawn = SupplychainpyReporting(launcher)
    #    with self.assertRaises(ValueError):
    #        spawn.spawn_reports()




