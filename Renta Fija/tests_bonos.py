# MIT License

# Copyright (c) 2020 Hernan Reisin

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bonos import *
from timeMeasure import *
import datetime as dt
import unittest

class Test_BonoDeCuponFijo(unittest.TestCase):

    def zercoCouponBond(self):
        startDate = dt.datetime(2010, 1, 15)
        expiryDate = dt.datetime(2030, 1, 15)
        # Las frecuencias de date_range en pandas
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
        # Q: month start frequency
        # SMS: semi-month start frequency (1st and 15th)
        frequency = '20Y'
        couponRate = 0 # en bps, 1 bps = 0.01%
        principal = 100
        bono = BonoDeCuponFijo(startDate, expiryDate, frequency, couponRate, principal)
        return bono

    def bonoDeCuponFijo(self):
        startDate = dt.datetime(2010, 1, 15)
        expiryDate = dt.datetime(2030, 1, 15)
        # Las frecuencias de date_range en pandas
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
        # Q: month start frequency
        # SMS: semi-month start frequency (1st and 15th)
        frequency = '12SMS'
        couponRate = 500 # en bps, 1 bps = 0.01%
        principal = 100
        bono = BonoDeCuponFijo(startDate, expiryDate, frequency, couponRate, principal)
        return bono

    def test_BonoDeCuponFijo(self):
        # test setup
        bono = self.bonoDeCuponFijo()
        # afirmaciones
        self.assertEqual(bono.couponAmount, 5)
        self.assertEqual(bono.couponRatesInBasisPoints, 0.05)
        self.assertEqual(len(bono.schedule), 41)
        self.assertEqual(bono.schedule[0], dt.datetime(2010, 1, 15))
        self.assertEqual(bono.schedule[-1], dt.datetime(2030, 1, 15))
        self.assertEqual(len(bono.settlementDates), 40)
        self.assertEqual(bono.settlementDates[0], dt.datetime(2010, 7, 15))
        self.assertEqual(len(bono.cashflows), 40)


    def testZeroCouponBond(self):

        # test setup
        bono = self.zercoCouponBond()
        
        # dcc = DayCountConvention_Actual_365()
        # curvaDeDescuento = CurvaDeDescuentoContinua(0.05)
        # diaDeValuacion = dt.datetime(2020, 8, 31)
        # pricer = ValuadorDeBono(bono, curvaDeDescuento)

        # cashflowsFuturos = pricer.cahflowsFuturos(diaDeValuacion)

        # npv = pricer.netPresentValue(diaDeValuacion)

if __name__ == '__main__':
    unittest.main()
