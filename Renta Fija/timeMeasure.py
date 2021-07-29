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

from abc import ABC
from abc import abstractmethod
import datetime as dt


class DayCountConvention(ABC):

    def __init__(self, businessDayConvention):
        self._businessDayConvention = businessDayConvention

    def adjust(self, unadjustedDate):
        return self._businessDayConvention.adjust(unadjustedDate)

    def timeMeasure(self, unadjustedStartDate, unadjustedEndDate):
        return self.adjust(unadjustedEndDate) - self.adjust(unadjustedStartDate)

    def timeMeasureNoAdjustment(self, unadjustedStartDate, unadjustedEndDate):
        return unadjustedEndDate - unadjustedStartDate

    @abstractmethod
    def yearFraction(self, unadjustedStartDate, unadjustedEndDate):
        pass


class DayCountConvention_Actual_365(DayCountConvention):

    def yearFraction(self, unadjustedStartDate, unadjustedEndDate):
        return self.timeMeasure(unadjustedStartDate, unadjustedEndDate).days / 365


class DayCountConvention_Actual_360(DayCountConvention):

    def yearFraction(self, unadjustedStartDate, unadjustedEndDate):
        return self.timeMeasure(unadjustedStartDate, unadjustedEndDate).days / 360


class DayCountConvention_30_360(DayCountConvention):

    def yearFraction(self, unadjustedStartDate, unadjustedEndDate):
        startDate = self.adjust(unadjustedStartDate)
        endDate = self.adjust(unadjustedEndDate)
        return (min(endDate.day, 30) + max(0, 30 - startDate.day)) / 360 + \
               max(0, endDate.month - startDate.month - 1) / 12 + \
               endDate.year - startDate.year


class DayCountConvention_Actual_Actual(DayCountConvention):

    def yearFraction(self, unadjustedStartDate, unadjustedEndDate):
        # No implemente la medida para este caso, entonces uso un proxy
        proxyMeasure = DayCountConvention_Actual_360(self._businessDayConvention)
        return proxyMeasure.yearFraction(unadjustedStartDate, unadjustedEndDate)


class DayCountConvention_Business_252(DayCountConvention):

    def yearFraction(self, unadjustedStartDate, unadjustedEndDate):
        numberOfDays = self.timeMeasureNoAdjustment(unadjustedStartDate, unadjustedEndDate).days
        numberOfBusinessDays = 0
        for d in range(numberOfDays):
            if self.isBusinessDay(unadjustedStartDate + dt.datetime.timedelta(d)):
                numberOfBusinessDays += 1
        return numberOfBusinessDays / 252

