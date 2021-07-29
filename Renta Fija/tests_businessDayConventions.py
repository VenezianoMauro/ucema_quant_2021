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
from timeMeasure import *
import datetime as dt
import unittest

#Notas: 
# deberia haber un solo Assert por test
# cada test deberia nombrarse con el resultado esperado

class Test_BusinessDayConventions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.calendario = calendars.CalendarArgentina()
        cls.diaLaborable = dt.datetime(2020, 8, 28)
        cls.diaFeriado = dt.datetime(2020, 7, 9)
        cls.diaDeFinDeSemana = dt.datetime(2020, 10, 31)
        cls.diaFeriadoEnUSA = dt.datetime(2019, 7, 4)

    def test_UnadjustedBusinessDay(self):

        # test setup
        bdc = businessDayConvention.Unadjusted(self.calendario)

        # Asserts sobre el calendario
        self.assertTrue(self.calendario.isBusinessDay(self.diaLaborable), "Esperaba que fuera dia laborable")
        self.assertFalse(self.calendario.isHoliday(self.diaLaborable), "Esperaba que fuera dia laborable")
        self.assertTrue(self.calendario.isHoliday(self.diaFeriado), "Esperaba que fuera un feriado")
        self.assertTrue(self.calendario.isBusinessDay(self.diaFeriadoEnUSA), "Esperaba que fuera dia laborable")

        # Asserts sobre la convencion de dias laborables
        self.assertTrue(bdc.isBusinessDay(self.diaLaborable), "Esperaba que fuera dia laborable")
        self.assertTrue(bdc.isBusinessDay(self.diaFeriadoEnUSA), "Esperaba que fuera dia laborable")

        # Hagamos fallar algunos tests
        self.assertEqual(bdc.nextDay(self.diaLaborable), self.diaLaborable)
        self.assertEqual(bdc.adjust(self.diaLaborable), self.diaLaborable)

    def test_FollowingBusinessDay(self):

        # test setup
        bdc = businessDayConvention.Following(self.calendario)

        # Asserts sobre la convencion de dias laborables
        # Hagamos fallar algunos tests
        self.assertEqual(bdc.adjust(self.diaLaborable), self.diaLaborable)
        #self.assertEqual(bdc.adjust(self.diaFeriado), self.diaFeriado)

    def test_ModifiedFollowingBusinessDay(self):

        # test setup
        bdc = businessDayConvention.ModifiedFollowing(self.calendario)

        # Asserts sobre la convencion de dias laborables
        # Hagamos fallar algunos tests
        #self.assertEqual(bdc.adjust(self.diaDeFinDeSemana), self.diaDeFinDeSemana)
        


if __name__ == '__main__':
    unittest.main()

