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

import businessDayConvention
import calendars
import timeMeasure
import unittest
import datetime as dt

#Notas: 
# deberia haber un solo Assert por test
# cada test deberia nombrarse con el resultado esperado

class Test_TimeMeasure(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.calendario = calendars.CalendarArgentina()
        cls.diaLaborable = dt.datetime(2020, 8, 28)
        cls.diaFeriado = dt.datetime(2020, 7, 9)
        cls.ejemploT1 = dt.datetime(2019, 1, 1)
        cls.ejemploT2 = dt.datetime(2019, 6, 17)

    def test_ModifiedFollowingBusinessDay(self):

        delta = 0.000001

        # test setup
        bdc = businessDayConvention.ModifiedFollowing(self.calendario)
        dcc_30_360 = timeMeasure.DayCountConvention_30_360(bdc)
        dcc_Actual_Actual = timeMeasure.DayCountConvention_Actual_Actual(bdc)
        dcc_Actual_360 = timeMeasure.DayCountConvention_Actual_360(bdc)
        dcc_Actual_365 = timeMeasure.DayCountConvention_Actual_365(bdc)

        # Asserts sobre la convencion de dias laborables
        self.assertAlmostEqual(0.458333333, dcc_30_360.yearFraction(self.ejemploT1, self.ejemploT2), delta=delta)
        self.assertAlmostEqual(0.46, dcc_Actual_Actual.yearFraction(self.ejemploT1, self.ejemploT2), delta=0.01) # Al usar un proxy la tolerancia es mayor
        self.assertAlmostEqual(0.461111111, dcc_Actual_360.yearFraction(self.ejemploT1, self.ejemploT2), delta=delta)
        self.assertAlmostEqual(0.454794520, dcc_Actual_365.yearFraction(self.ejemploT1, self.ejemploT2), delta=delta)


if __name__ == '__main__':
    unittest.main()

