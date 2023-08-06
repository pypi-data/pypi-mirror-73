import unittest
import os
from pyieamods import pyieamods


class TestpyModsIEA(unittest.TestCase):

    def test_get_all(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        test_zip = os.path.join(dirname, 'sdbstxt.zip')
        res = pyieamods.allmods(test_zip)
        self.assertIn('PRODDAT', res)
        proddat = res['PRODDAT']
        self.assertIn('IEA.PROD.CRUDEOIL.AUSTRALI.OMRDEMB', proddat.columns)

        self.assertIn('CRUDEDAT', res)
        crudedat = res['CRUDEDAT']
        self.assertIn('IEA.CRUDE.AUSTRALI.CRNGFEED.CSNATTERT', crudedat.columns)

        self.assertIn('STOCKSDAT', res)
        stocksdat = res['STOCKSDAT']
        self.assertIn('IEA.STOCKS.INDUSTRY.CRNGFEED.AUSTRIA', stocksdat.columns)

        self.assertIn('SUMMARY', res)
        summary = res['SUMMARY']
        self.assertIn('IEA.SUMMARY.AMEDEM.FINAL', summary.columns)

        self.assertIn('SUPPLY', res)
        supply = res['SUPPLY']
        self.assertIn('IEA.SUPPLY.COND.AUSTRALIA', supply.columns)

        self.assertIn('NOECDDE', res)
        noedcdde = res['NOECDDE']
        self.assertIn('IEA.NOECDDE.BELARUS', noedcdde.columns)

        self.assertIn('OECDDE', res)
        oecdde = res['OECDDE']
        self.assertIn('IEA.OECDDE.JETANDKERO.AUSTRALI', oecdde.columns)
        self.assertEqual(oecdde['IEA.OECDDE.LPGETHANE.AUSTRALI']['2015-01'].iloc[0], 77.4722)


if __name__ == '__main__':
    unittest.main()


