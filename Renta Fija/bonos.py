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


import numpy as np
import pandas as pd
import datetime as dt


class Cashflow():

    # Deberiamos agregar una moneda, pero no voy a considerar FX
    def __init__(self, date, amount):
        self._date = date
        self._amount = amount

    # Dia del cashflow (pasado o futuro)
    @property
    def date(self):
        return self._date

    @property
    def amount(self):
        return self._amount


class CurvaDeDescuentoContinua():

    # Deberiamos agregar una moneda, pero no voy a considerar FX
    def __init__(self, tasaRiskFree, businessDayConvention):
        self._tasaRiskFree = tasaRiskFree
        self._businessDayConvention = businessDayConvention

    @property
    def discountFactor(self, asOfDate, paymentDate):
        timeMeasure = self._businessDayConvention.timeMeasure(asOfDate, paymentDate)
        return np.exp(-self._tasaRiskFree * timeMeasure)


class BonoDeCuponFijo():

    bps = 0.0001

    @property
    def cashflows(self):
        if (self._cashflows is None): # Lazy initialization
            # Agrego los cupones
            self._cashflows = [Cashflow(date, self.couponAmount) for date in self.settlementDates]
            # Agrego el repago del principal
            self._cashflows[-1] = Cashflow(self._expiryDate, self._cashflows[-1].amount + self._principal)
        return self._cashflows

    @property
    def couponAmount(self):
        if (self._couponAmount is None): # Lazy initialization
            self._couponAmount = self._principal * self.couponRatesInBasisPoints
        return self._couponAmount

    @property
    def couponRatesInBasisPoints(self):
        if (self._couponRatesInBasisPoints is None): # Lazy initialization
            self._couponRatesInBasisPoints = self._couponRate * self.bps
        return self._couponRatesInBasisPoints

    @property
    def settlementDates(self):
        # Hay que remover la primer fecha del schedule porque no hay flujo ese dia
        if (self._settlementDates is None): # Lazy initialization
            self._settlementDates = self.schedule.tolist()
            if (len(self._settlementDates) > 0):
                self._settlementDates.remove(self._settlementDates[0])
        return self._settlementDates

    @property
    def schedule(self):
        return self._schedule

    def __init__(self, startDate, expiryDate, frequency, couponRate, principal):
        self._startDate = startDate
        self._expiryDate = expiryDate
        self._frequency = frequency
        self._couponRate = couponRate
        self._principal = principal
        self._schedule = pd.date_range(start=startDate, end=expiryDate, freq=frequency).to_pydatetime()
        # Es recomendable fail fast... por ejemplo inicializar los cashflows aca, como hice para el schedule  
        self._cashflows = None      
        self._couponAmount = None
        self._couponRatesInBasisPoints = None
        self._settlementDates = None


class ValuadorDeBono():

    def __init__(self, bono, curvaDeDescuento):
        self._bono = bono
        self._curvaDeDescuento = curvaDeDescuento

    def netPresentValue(self, asOfDate):
        cashflowsFuturos = self.cahflowsFuturos(asOfDate)
        if (len(cashflowsFuturos) < 1):
            return 0
        discountFactor = self._curvaDeDescuento.discountFactor(asOfDate, cashflowsFuturos[0].date)
        cahflowsDescontados = [c.amount * self._curvaDeDescuento.discountFactor(asOfDate, c.date) for c in cashflowsFuturos]
        npv = sum(cahflowsDescontados)
        return npv

    def cahflowsFuturos(self, asOfDate):
        return [c for c in self._bono.cashflows if c.date > asOfDate]

