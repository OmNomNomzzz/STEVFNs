#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:16:24 2021

@author: aniqahsan
"""

from .EL_Demand import EL_Demand_Asset
from .HTH_Demand import HTH_Demand_Asset
from .CG import CG_Asset
from .EL_to_HTH import EL_to_HTH_Asset
from .RE import RE_Asset
from .BESS import BESS_Asset
from .EL_to_H2 import EL_to_H2_Asset
from .H2_to_EL import H2_to_EL_Asset
from .H2_Storage import H2_Storage_Asset
from .H2_to_HTH import H2_to_HTH_Asset
from .EL_Transport import EL_Transport_Asset
from .H2_Transport import H2_Transport_Asset
from .RE_PV import RE_PV_Asset
from .RE_WIND import RE_WIND_Asset

ASSET_DICT = {EL_Demand_Asset.asset_name: EL_Demand_Asset,
              HTH_Demand_Asset.asset_name: HTH_Demand_Asset,
              CG_Asset.asset_name: CG_Asset,
              EL_to_HTH_Asset.asset_name: EL_to_HTH_Asset,
              RE_Asset.asset_name: RE_Asset,
              BESS_Asset.asset_name: BESS_Asset,
              EL_to_H2_Asset.asset_name: EL_to_H2_Asset,
              H2_to_EL_Asset.asset_name: H2_to_EL_Asset,
              H2_Storage_Asset.asset_name: H2_Storage_Asset,
              H2_to_HTH_Asset.asset_name: H2_to_HTH_Asset,
              EL_Transport_Asset.asset_name: EL_Transport_Asset,
              H2_Transport_Asset.asset_name: H2_Transport_Asset,
              RE_PV_Asset.asset_name: RE_PV_Asset,
              RE_WIND_Asset.asset_name: RE_WIND_Asset,
              }
