import unittest
from pathlib import Path
import mrpsolver as mrps

mod_path = Path(__file__).parent
TEST_IMF_CSV = (mod_path / 'sample_files/sample_imf.csv').resolve()
TEST_IMF_JSON = (mod_path / 'sample_files/sample_imf.json').resolve()
TEST_MPS_CSV = (mod_path / 'sample_files/sample_mps.csv').resolve()
TEST_MPS_JSON = (mod_path / 'sample_files/sample_mps_by_part.json').resolve()
TEST_BOM_CSV = (mod_path / 'sample_files/sample_bom.csv').resolve()
TEST_BOM_JSON = (mod_path / 'sample_files/sample_bom.json').resolve()

VERIFIED_MRP = {
    'a': [50.0, 190.0, 1400.0, 810.0, 1500.0, 600.0, 200.0, 0.0, 0.0, 0.0],
    'b': [0.0, 0.0, 0.0, 0.0, 100.0, 0.0, 100.0, 0.0, 0.0, 0.0],
    'c': [1350.0, 600.0, 1950.0, 600.0, 450.0, 0.0, 450.0, 0.0, 0.0, 0.0],
    'd': [0.0, 200.0, 100.0, 200.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'e': [0.0, 1400.0, 800.0, 1400.0, 600.0, 200.0, 0.0, 0.0, 0.0, 0.0],
    'f': [0.0, 0.0, 0.0, 3300.0, 0.0, 3300.0, 0.0, 0.0, 0.0, 0.0],
    'g': [0.0, 0.0, 150.0, 100.0, 200.0, 100.0, 0.0, 0.0, 0.0, 0.0],
    'x': [0.0, 0.0, 0.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0],
    'y': [0.0, 0.0, 0.0, 0.0, 150.0, 100.0, 200.0, 100.0, 0.0, 0.0]
}

VERIFIED_AVAILABLE = {
    'a': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'b': [100.0, 100.0, 100.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'c': [235.0, 183.0, 218.0, 140.0, 230.0, 220.0, 110.0, 110.0, 160.0, 160.0],
    'd': [0.0, 0.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0],
    'e': [450.0, 260.0, 260.0, 250.0, 150.0, 150.0, 150.0, 150.0, 150.0, 150.0],
    'f': [500.0, 500.0, 500.0, 500.0, 300.0, 300.0, 100.0, 100.0, 100.0, 100.0],
    'g': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'x': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'y': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}

class ImportTests(unittest.TestCase):
    def test_imf_import(self):
        (csv_solver := mrps.Solver()).load_imf(TEST_IMF_CSV)
        (json_solver := mrps.Solver()).load_imf(TEST_IMF_JSON)
        part_a = mrps.Part(id='a', oh=0, alloc=0, ss=0, lt=2, ls=1, sr={3: 100})
        part_c = mrps.Part(id='c', oh=500, alloc=225, ss=100, lt=2, ls=150, sr={2: 100, 4:100})
        self.assertEqual(part_a, csv_solver.all_parts['a'])
        self.assertEqual(part_a, json_solver.all_parts['a'])
        self.assertEqual(part_c, csv_solver.all_parts['c'])
        self.assertEqual(part_c, json_solver.all_parts['c'])

    def test_mps_import(self):
        (csv_solver := mrps.Solver()).load_imf(TEST_IMF_CSV)
        (json_solver := mrps.Solver()).load_imf(TEST_IMF_JSON)
        csv_solver.load_mps(TEST_MPS_CSV, listed_by='part')
        json_solver.load_mps(TEST_MPS_JSON, listed_by='part')
        part_a = mrps.Part(id='a', oh=0, alloc=0, ss=0, lt=2, ls=1, sr={3: 100}, mps={1: 0, 2: 0, 3: 0, 4: 90, 5: 100, 6: 110, 7: 100, 8: 0, 9: 0, 10: 0})
        part_c = mrps.Part(id='c', oh=500, alloc=225, ss=100, lt=2, ls=150, sr={2: 100, 4:100}, mps={1: 0})
        self.assertEqual(part_a, csv_solver.all_parts['a'])
        self.assertEqual(part_a, json_solver.all_parts['a'])
        self.assertEqual(part_c, csv_solver.all_parts['c'])
        self.assertEqual(part_c, json_solver.all_parts['c'])
        self.assertEqual(csv_solver.total_periods(), 10)
        self.assertEqual(json_solver.total_periods(), 10)

    def test_bom_import(self):
        (csv_solver := mrps.Solver()).load_imf(TEST_IMF_CSV)
        (json_solver := mrps.Solver()).load_imf(TEST_IMF_JSON)
        csv_solver.load_mps(TEST_MPS_CSV, listed_by='part')
        json_solver.load_mps(TEST_MPS_JSON, listed_by='part')
        csv_solver.load_bom(TEST_BOM_CSV)
        json_solver.load_bom(TEST_BOM_JSON)
        part_x = csv_solver.all_parts['x']
        part_y = json_solver.all_parts['y']
        part_g = json_solver.all_parts['g']
        part_a = mrps.Part(id='a', oh=0, alloc=0, ss=0, lt=2, ls=1, sr={3: 100}, mps={1: 0, 2:0, 3: 0, 4: 90, 5: 100, 6: 110, 7: 100, 8: 0, 9: 0, 10: 0}, bom={'c': 0.8, 'e': 1.0}, parents=[part_x, part_y, part_g], rem_parents=3)
        part_a_j = mrps.Part(id='a', oh=0, alloc=0, ss=0, lt=2, ls=1, sr={3: 100}, mps={1: 0, 2:0, 3: 0, 4: 90, 5: 100, 6: 110, 7: 100, 8: 0, 9: 0, 10: 0}, bom={'c': 0.8, 'e': 1}, parents=[part_x, part_y, part_g], rem_parents=3)
        self.assertEqual(part_a, csv_solver.all_parts['a'])
        self.assertEqual(part_a_j, json_solver.all_parts['a'])

class ProcessingTests(unittest.TestCase):
    (sample_solver := mrps.Solver()).load_imf(TEST_IMF_JSON)
    sample_solver.load_mps(TEST_MPS_JSON, listed_by='part')
    sample_solver.load_bom(TEST_BOM_JSON)
    def test_solve_result(self):
        test_mrp, test_avail = self.sample_solver.solve()
        self.assertEqual(VERIFIED_MRP, test_mrp)
        self.assertEqual(VERIFIED_AVAILABLE, test_avail)



if __name__ == '__main__':
    unittest.main()