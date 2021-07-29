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


import datetime as dt

class Calendar():
# From Wiki: A calendar is a system of organizing days for social, religious, commercial or administrative purposes. 
# This is done by giving names to periods of time, typically days, weeks, months and years.
# The Gregorian calendar is the de facto international standard and is used almost everywhere in the world for civil purposes.

    def __init__(self, isoweekends, nonRecurringHolidays, recurringHolidays):
        self._isoWeekends = isoweekends
        self._recurringHolidays = recurringHolidays  
        self._nonRecurringHolidays = nonRecurringHolidays

    def isBusinessDay(self, aDate):
        return self.isWeekDay(aDate) and self.isNotHoliday(aDate)

    def isWeekDay(self, aDate):
        return not self.isWeekend(aDate)

    def isWeekend(self, aDate):
        # Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.
        return aDate.isoweekday() in self._isoWeekends

    def isHoliday(self, aDate):
        return aDate in self._nonRecurringHolidays or \
                (aDate.month, aDate.day) in self._recurringHolidays

    def isNotHoliday(self, aDate):
        return not self.isHoliday(aDate)

    def getBusinessDays(self, aDateList):
        # Por performance se puede persistir esta lista
        return [d for d in aDateList if self.isBusinessDay(d)]


class CalendarArgentina():

    _isoWeekends = [6, 7] 

    # Enorme simplificacion, e.g. desde cuando aplica la recurrencia?
    # Que pasa si un an~o se mueve un feriado recurrente, por fines turisticos por ejemplo?
    # La solucion mas sencilla, y rapida de corregir es tener un archivo plano de 
    # texto con todos los feriados de los proximos 100 an~os... 
    _recurringHolidays = [(1, 1),   # An~o nuevo
                          (3, 24),  # Día Nacional de la Memoria por la Verdad y la Justicia.
                          (5, 1),   # Dia del trabajo  
                          (5, 25),  # Revolucion de Mayo
                          (6, 20),  # Dia de la bandera
                          (7, 9),   # Dia de la independencia
                          (8, 17),  # Paso a la Inmortalidad del Gral. José de San Martín.
                          (10, 12), # Día del Respeto a la Diversidad Cultural.
                          (12, 8),  # Dia de la virgen
                          (12, 25), # Navidad
                         ]
    _nonRecurringHolidays = [dt.datetime(2020, 7, 10), # Viernes Santo
                             dt.datetime(2020, 2, 24), # Carnaval
                             dt.datetime(2020, 2, 24), # Carnaval
                             dt.datetime(2020, 7, 10), # Feriado puente
                             dt.datetime(2020, 12, 7), # Feriado puente
                            ]

    def __init__(self):
        self._aCalendar = Calendar(self._isoWeekends, self._nonRecurringHolidays, self._recurringHolidays)

    def isBusinessDay(self, aDate):
        return self._aCalendar.isBusinessDay(aDate)

    def isWeekDay(self, aDate):
        return self._aCalendar.isWeekDay(aDate)

    def isHoliday(self, aDate):
        return self._aCalendar.isHoliday(aDate)

    def isNotHoliday(self, aDate):
        return self._aCalendar.isNotHoliday(aDate)

    def isWeekDay(self, aDate):
        return self._aCalendar.isWeekDay(aDate)

    def isWeekend(self, aDate):
        # Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.
        return aDate.isoweekday() in self._isoWeekends
