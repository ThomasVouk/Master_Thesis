import oemof.solph as solph

from Tools.fill_model_v4 import fill_energysystem
from Tools.oemof_system_plot import oemof_network_plot
import pandas as pd

#dataname='UpHy II_InputFile_2030_v11_daylieAvg'
#dataname='UpHy II_InputFile_2030_v11_4h'
#dataname='UpHy II_InputFile_2030_v11_2h_b'
dataname= 'Transition_Input_TV_2040_v1'
esysd_filename = dataname+'.xlsx'

#insert function, which ask you, if you want to translate the input File into an file

datetimeindex = pd.date_range('01/01/2040', periods=8760, freq='h')

#datetimeindex = pd.date_range('01/01/2030', periods=4380,freq='2H')
#datetimeindex = pd.date_range('01/01/2030', periods=365, freq='d')

esys = solph.EnergySystem(timeindex=datetimeindex,infer_last_interval=False)
esys = fill_energysystem(esys, esysd_filename)


#nt = oemof_network_plot(esys, dataname+'.html') #OEMOF-Network visualisation
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