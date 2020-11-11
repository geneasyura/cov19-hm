#!/usr/bin/python3
# coding: utf-8

import math

class AirRegistance:
    def __init__(self):
        self.R   = 2e-7 # 半径 [m]
        self.L   = self.R * 2 # 直径 [m]
        self.Fd  = None # 空気抵抗力 [N]
        self.eta = None # 空気粘性率 [kg/ms]
        self.rho = None # 空気密度 [kg/m^3]
        self.v   = 0.80 # 球体速度 [m/s]
        self.Re  = None # レイルズ数
        self.Cd  = None # 抗力係数

    def _calc_rho(self, t, P, M):
        a = 0.0034856447
        b = 272.48
        c = 0.378
        d = 100 * 6.1078
        x = (7.5 * t)/(t + 237.3)
        rho = (a*(P/(t+b))) * (1-M*c*((d*10**x)/(P)))
        return rho

    def _calc_Cd(self, Re):
        Cd = 24/Re + \
            (26*(Re/5.0)) / (1+(Re/5.0)**1.52) + \
            (0.411*(Re/263000)**(-7.94)) / (1+(Re/263000)**(-8)) + \
            ((Re**0.80) / 461000)
        return Cd

    def _calc_Fd(self):
        Fd = 0.5 * self.Cd * self.rho * math.pi * \
            self.R**2 * self.v**2
        return Fd

    def calc(self, t, P, rh):
        K = t + 273.15
        self.eta = 1.487 * 1e-6 * ((K**1.5)/(K+117))
        self.rho = self._calc_rho(t, P, rh/100.0)
        #print("eta:{}, rho:{}".format(self.eta, self.rho))
        self.Re = (self.v * self.rho * self.L) / self.eta
        self.Cd = self._calc_Cd(self.Re)
        #print("Re:{} Cd:{}".format(self.Re, self.Cd))
        self.Fd = self._calc_Fd()
        #print("Fd:{}".format(self.Fd))
        return self.Fd
