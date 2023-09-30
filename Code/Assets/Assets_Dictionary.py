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
from .EL_to_NH3 import EL_to_NH3_Asset
from .NH3_to_EL import NH3_to_EL_Asset
from .NH3_Storage import NH3_Storage_Asset
from .NH3_to_HTH import NH3_to_HTH_Asset
from .EL_Transport import EL_Transport_Asset
from .NH3_Transport import NH3_Transport_Asset
from .RE_PV import RE_PV_Asset
from .RE_WIND import RE_WIND_Asset
from .RE_max import RE_max_Asset
from .EL_Demand_UM import EL_Demand_UM_Asset
from .EL_Demand_Constant import EL_Demand_Constant_Asset
from .RE_PV_Constant import RE_PV_Constant_Asset
from .RE_WIND_Constant import RE_WIND_Constant_Asset
from .CO2_Budget import CO2_Budget_Asset

ASSET_DICT = {EL_Demand_Asset.asset_name: EL_Demand_Asset,
              HTH_Demand_Asset.asset_name: HTH_Demand_Asset,
              CG_Asset.asset_name: CG_Asset,
              EL_to_HTH_Asset.asset_name: EL_to_HTH_Asset,
              RE_Asset.asset_name: RE_Asset,
              BESS_Asset.asset_name: BESS_Asset,
              EL_to_NH3_Asset.asset_name: EL_to_NH3_Asset,
              NH3_to_EL_Asset.asset_name: NH3_to_EL_Asset,
              NH3_Storage_Asset.asset_name: NH3_Storage_Asset,
              NH3_to_HTH_Asset.asset_name: NH3_to_HTH_Asset,
              EL_Transport_Asset.asset_name: EL_Transport_Asset,
              NH3_Transport_Asset.asset_name: NH3_Transport_Asset,
              RE_PV_Asset.asset_name: RE_PV_Asset,
              RE_WIND_Asset.asset_name: RE_WIND_Asset,
              RE_max_Asset.asset_name: RE_max_Asset,
              EL_Demand_UM_Asset.asset_name: EL_Demand_UM_Asset,
              EL_Demand_Constant_Asset.asset_name: EL_Demand_Constant_Asset,
              RE_PV_Constant_Asset.asset_name: RE_PV_Constant_Asset,
              RE_WIND_Constant_Asset.asset_name: RE_WIND_Constant_Asset,
              CO2_Budget_Asset.asset_name: CO2_Budget_Asset,
              }
