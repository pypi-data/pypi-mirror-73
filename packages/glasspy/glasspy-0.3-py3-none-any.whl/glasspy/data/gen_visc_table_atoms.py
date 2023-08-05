import numpy as np
import pandas as pd

import sys
sys.path.insert(0, "/data/Science/Projects/Git/glasspy")
from glasspy.data.load import sciglass

REMOVE_DUPES_DECIMAL = 3
ROUND_TEMPERATURE = 0
ROUND_VISCOSITY = 1

at_frac_columns = sciglass()['at_frac'].columns


### Temperaturas onde a viscosidade é um valor fixo
 
if 'data1' not in globals():
    Tviscos = np.arange(0, 13)

    dflst = []
    for logvisc in Tviscos:

        d = sciglass()

        d.dropna(subset=[('prop', f'T{logvisc}')], inplace=True)

        comp = d['at_frac'].copy()
        comp['T'] = d[('prop', f'T{logvisc}')]
        comp['log_visc'] = logvisc

        dflst.append(comp)

    data1 = pd.concat(dflst)


### Viscosidade onde a temperatura é um valor fixo

if 'data2' not in globals():
    viscoT = np.arange(0, 1700, 100) + 873

    dflst2 = []
    for T in viscoT:
        d = sciglass()

        if f'ViscosityAt{T}K' in d['prop'].columns:
            d.dropna(subset=[('prop', f'ViscosityAt{T}K')], inplace=True)

            comp = d['at_frac'].copy()
            comp['T'] = T
            comp['log_visc'] = d[('prop', f'ViscosityAt{T}K')]

            dflst2.append(comp)

    data2 = pd.concat(dflst2)


### Final dataset

data = pd.concat([data1, data2], sort=False)

print(f'Shape of data: {data.shape}')

data[at_frac_columns] = data[at_frac_columns].round(REMOVE_DUPES_DECIMAL)
data['T'] = data['T'].round(ROUND_TEMPERATURE)
grouped = data.groupby(list(at_frac_columns) + ['T'], sort=False)
data = grouped.median().reset_index()
# data['log_visc'] = data['log_visc'].round(ROUND_VISCOSITY)

print(f'Shape of data after dedupe: {data.shape}')

data.to_pickle('./data/viscosity_T.xz', protocol=-1)

print('done')

