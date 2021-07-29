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

class BusinessDayConvention(ABC):

    def __init__(self, calendar):
        self._calendar = calendar

    @abstractmethod
    def adjust(self, aDate):
        pass

    def isBusinessDay(self, aDate):
        return self._calendar.isBusinessDay(aDate)

    def isBusinessDay(self, aDate):
        return self._calendar.isBusinessDay(aDate)

    def nextDay(self, aDate):
        return aDate + dt.timedelta(days=1)

    def previustDay(self, aDate):
        return aDate - dt.timedelta(days=1)


class Unadjusted(BusinessDayConvention):

    def adjust(self, aDate):
        return aDate


class Following(BusinessDayConvention):

    def adjust(self, aDate):
        if self._calendar.isBusinessDay(aDate):
            return aDate
        else:
            return self.adjust(self.nextDay(aDate))


class Previus(BusinessDayConvention):

    def adjust(self, aDate):
        if self._calendar.isBusinessDay(aDate):
            return aDate
        else:
            return self.adjust(self.previustDay(aDate))


class ModifiedFollowing(BusinessDayConvention):

    def adjust(self, aDate):
        nextBusinessDate = Following(self._calendar).adjust(aDate)
        if (nextBusinessDate.month == aDate.month):
            return nextBusinessDate
        else:
            return Previus(self._calendar).adjust(aDate)


class ModifiedPrevius(BusinessDayConvention):

    def adjust(self, aDate):
        previousBusinessDate = Previus(self._calendar).adjust(aDate)
        if (previousBusinessDate.month == aDate.month):
            return previousBusinessDate
        else:
            return Following(self._calendar).adjust(aDate)


class EndOfMonth(BusinessDayConvention):
# De https://quant.opengamma.io/Interest-Rate-Instruments-and-Market-Conventions.pdf
# Where the start date of a period is on the final business day of a particular calendar month, the end
# date is on the final business day of the end month

    def adjust(self, aDate):
        # Que tiene de malo este modelo???
        return aDate

