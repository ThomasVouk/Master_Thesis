import oemof.solph as solph

from Tools.fill_model_v4 import fill_energysystem
from Tools.oemof_system_plot import oemof_network_plot
import pandas as pd

#dataname='UpHy II_InputFile_2030_v11_daylieAvg'
#dataname='UpHy II_InputFile_2030_v11_4h'
#dataname='UpHy II_InputFile_2030_v11_2h_b'
dataname= 'KWEinsatz_v34_NIP2030_baseCase'
esysd_filename = dataname+'.xlsx'

#insert function, which ask you, if you want to translate the input File into an file

datetimeindex = pd.date_range('01/01/2030', periods=8760, freq='H')

#datetimeindex = pd.date_range('01/01/2030', periods=4380,freq='2H')
#datetimeindex = pd.date_range('01/01/2030', periods=365, freq='d')

esys = solph.EnergySystem(timeindex=datetimeindex,infer_last_interval=False)
esys = fill_energysystem(esys, esysd_filename)


nt = oemof_network_plot(esys, dataname+'.html') #OEMOF-Network visualisation

#"""
BatteryStorage = solph.GenericStorage(
    label="BatteryStorage",
    inputs={esys.entities[0]: solph.Flow(nominal_value=5855, variable_costs=0.001)},
    outputs={esys.entities[0]: solph.Flow(nominal_value=5855, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=29275, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.99)

#######################################################################

UpperStoragePS1 = solph.GenericStorage(
    label="UpperStoragePS1",
    inputs={esys.entities[39]: solph.Flow(variable_costs=0.001)},
    outputs={esys.entities[47]: solph.Flow(nominal_value=2279, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=394374, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.89)

UpperStoragePS2 = solph.GenericStorage(
    label="UpperStoragePS2",
    inputs={esys.entities[40]: solph.Flow(variable_costs=0.001)},
    outputs={esys.entities[48]: solph.Flow(nominal_value=1669, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=348919, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.89)

UpperStoragePS3 = solph.GenericStorage(
    label="UpperStoragePS3",
    inputs={esys.entities[41]: solph.Flow(variable_costs=0.001)},
    outputs={esys.entities[49]: solph.Flow(nominal_value=1731, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=568858, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.89)

UpperStoragePS4 = solph.GenericStorage(
    label="UpperStoragePS4",
    inputs={esys.entities[42]: solph.Flow(variable_costs=0.001)},
    outputs={esys.entities[50]: solph.Flow(nominal_value=50, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=32469, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.89)

#######################################################################

LowerStoragePS1 = solph.GenericStorage(
    label="LowerStoragePS1",
    inputs={esys.entities[51]: solph.Flow(variable_costs=0.001)},
    outputs={esys.entities[43]: solph.Flow(nominal_value=2279, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=10671, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.89)

LowerStoragePS2 = solph.GenericStorage(
    label="LowerStoragePS2",
    inputs={esys.entities[52]: solph.Flow(variable_costs=0.001)},
    outputs={esys.entities[44]: solph.Flow(nominal_value=1669, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=18618, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.89)

LowerStoragePS3 = solph.GenericStorage(
    label="LowerStoragePS3",
    inputs={esys.entities[53]: solph.Flow(variable_costs=0.001)},
    outputs={esys.entities[45]: solph.Flow(nominal_value=1731, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=109070, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.89)

LowerStoragePS4 = solph.GenericStorage(
    label="LowerStoragePS4",
    inputs={esys.entities[54]: solph.Flow(variable_costs=0.001)},
    outputs={esys.entities[46]: solph.Flow(nominal_value=50, variable_costs=0.001)},
    loss_rate=0, nominal_storage_capacity=32447, initial_storage_level=0.5, balanced=True,
    inflow_conversion_factor=1, outflow_conversion_factor=0.89)

#######################################################################

Electrolysis = solph.Sink(
    label="Electrolysis",
    inputs={esys.entities[0]: solph.Flow(nominal_value=0, summed_min=2272.341111, variable_costs=0.1)})

PtH = solph.Sink(
    label="PtH",
    inputs={esys.entities[0]: solph.Flow(nominal_value=0, summed_min=1531.640306, variable_costs=0.1)})

XtP = solph.Source(
    label="XtP",
    outputs={esys.entities[0]: solph.Flow(nominal_value=0, summed_min=2831.856369, variable_costs=10000)})

esys.add(UpperStoragePS1)
esys.add(UpperStoragePS2)
esys.add(UpperStoragePS3)
esys.add(UpperStoragePS4)
esys.add(LowerStoragePS1)
esys.add(LowerStoragePS2)
esys.add(LowerStoragePS3)
esys.add(LowerStoragePS4)
esys.add(BatteryStorage)
esys.add(Electrolysis)
esys.add(PtH)
esys.add(XtP)


#"""


model = solph.Model(esys)

model.solve(solver='gurobi') #Write here other keyword arguments --> weighted etc.

# with open('fill_model_example.pickle', 'wb') as f:
#     pickle.dump(model, f)

results = solph.processing.results(model)
list = []
for ob in results.keys():
    list.append(ob)

result_frame = pd.DataFrame()

for ob in list:
    new_df = results[ob]['sequences']
    label = 'VON: ' + ob[0].label
    if hasattr(ob[1], 'label'):
        label = 'VON: ' + ob[0].label + '   ' + 'ZU: ' + ob[1].label
        new_df = new_df.rename(columns={new_df.columns[0]: label})
        result_frame = pd.concat([result_frame, new_df], axis=1)

result_frame.to_excel(dataname+'_results.xlsx')