# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:13:44 2023

@author: Thomas Vouk
"""

import sys
import pandas as pd

"""
import Dienstleistungen_v2 as dl
import services_Hp as s_Hp
import pkw_v2 as p
import Top_down_industry_v2_gas as ind
import Top_down_industry_v2_gas as indg
import households_v1 as h
#import households_gas as hg
import LNF_v2 as lnf
import SNF_v1 as snf
import company as c
import company_gas as cg
import households_heat_pump as hp
import psycopg2 as ps


This are the timeseries_ids for different technologies

timeseries={'car':'844 and 844',
            'Heavy duty truck': '846 and 846',
            'Light duty truck': '845 and 845',
            'Locomotiv': '36 and 36',
            'H0 households': '832 and 832',
            'Households heatpumps': '36 and 433',
            'Services': '833 and 833',
            'Services heatpumps': '434 and 831',
            'Photovoltaik': '880 and 1277',
            'Wind': '1278 and 1675',
            'Hydro <10MW': '1677 and 1677',
            'Hydro >10MW': '1678 and 1766', 
            'Biomass': '1676 and 1676'}
"""

def query_configurations(data_cases):
    
    query_Data_list=[]
    for d in data_cases:
        
        """
        First define the parameter out of the data_cases for the query input. 
        
        """
        name=''
        NEA_Main=[]
        NEA_Sector=[]
        location=[]
        user=d.get('User')
        s=d.get('Scenario')
        scenario=f"'{s}'"
        source=d.get('Initial_data')
        source_tsdata={"Unknown":'0',"PV_GIS":'1',"RenewableNinja":'2',"GanyMed":'3',"SigLinde":'4',"MerritOrderOptimizer":'5',}
        
        ts_source_input=d.get('Timeseries_Source')
        ts_source=source_tsdata.get(ts_source_input)
        
        if d.get('Energy carrier')=='electricity':
            e_carrier='1'
        
        if d.get('Energy carrier')=='CH4':
            e_carrier='2'
            
        ref_year=f"'{d.get('Reference year')}-01-01 00:00:00'"
        calc_year=f"'{d.get('Calculation year')}-01-01 00:00:00'"
        
        if d.get('Resolution')=='1H':
            resolution='1'#Resoltution 1 means 1hour Resolution
            power_Factor='1'
        else:
            resolution='2'#Resoltution 2 means 15Min Resolution
            power_Factor='4'
        
        if d.get('Target')=='USW-district':
            
            goal='USW'
        else:
            goal='district'
            
            
        if (d.get('Industry')==True and e_carrier =='1'):#Calculate company Spatial Resolution
            NEA_Main.append('1')
            NEA_Sector.append('1')#Start Sektor of Industry
            NEA_Sector.append('13')#End Sektor of Industry
            location.append('between 1 and 399')
            name+='_Industry'

        if d.get('H0 households')==True:#Calculate households Spatial Resolution
            NEA_Main.append('3')
            NEA_Sector.append('14')
            location.append('between 1 and 1')
            name+='_H0'
            
        if d.get('Households heatpumps')==True:#Calculate spatial resolution for heatpumps_households 
            NEA_Main.append('3')
            NEA_Sector.append('14')
            location.append('between 2 and 399')
            name+='_HpH0'

        if d.get('Services')==True:#Calculate spatial resolution for heatpumps_households 
            NEA_Main.append('4')
            NEA_Sector.append('15')
            location.append('between 1 and 1')
            name+='_G0'
            
        if d.get('Services heatpumps')==True:#Calculate spatial resolution for heatpumps_households
            NEA_Main.append('4')
            NEA_Sector.append('15')
            location.append('between 2 and 399')
            name+='_HpG0'

        if d.get('Locomotiv')==True:#Calculate Industry-Top-Down Spatial Resolution
            NEA_Main.append('2')
            NEA_Sector.append('17')
            location.append('between 1 and 1')
            name+='_Locomotiv'        

        if d.get('Car')==True:
            NEA_Main.append('2')
            NEA_Sector.append('23')
            location.append('between 1 and 399')
            name+='_Car'
        
        if d.get('Light duty truck')==True:
            NEA_Main.append('2')
            NEA_Sector.append('25')
            location.append('between 1 and 399')
            name+='_Ldt'
        
        if d.get('Heavy duty truck')==True:#SNF Lokal and SNF long distance mixture (actual 96 to 4 %)
            NEA_Main.append('2')
            NEA_Sector.append('24')
            location.append('between 1 and 399')
            name+='_Hdt'
          

        if d.get('Photovoltaik')==True:#Calculate spatial resolution for pv
            NEA_Main.append('6')
            NEA_Sector.append('0')
            location.append('between 2 and 399')
            name+='_PV'

        if d.get('Wind')==True:#Calculate spatial resolution for heatpumps_households
            NEA_Main.append('7')
            NEA_Sector.append('0')
            location.append('between 2 and 399')
            name+='_Wind'

        if d.get('Hydro <10MW')==True:#Calculate spatial resolution for heatpumps_households
            NEA_Main.append('8')
            NEA_Sector.append('0')
            location.append('between 1 and 1')
            name+='_SmallHydro'

        if d.get('Hydro >10MW')==True:#Calculate spatial resolution for heatpumps_households
            NEA_Main.append('9')
            NEA_Sector.append('0')
            location.append('between 1 and 1')
            name+='_BigHydro'

        if d.get('Biomass')==True:#Calculate spatial resolution for heatpumps_households
            NEA_Main.append('10')
            NEA_Sector.append('0 ')
            location.append('between 1 and 1')
            name+='_Biomass'

        """
        
        Delete duplicates from Input Elemetns for SQL-queries
        
        """
        
        #NEA_Main_output=list(pd.unique(NEA_Main))
        #NEA_sector_output=list(pd.unique(NEA_Sector))
        #locations_list=list(pd.unique(location))
        locations_list=list(set(location))
        
        if len(NEA_Main)>1:
            NEA_Main=[f'between {NEA_Main[0]} and {NEA_Main[-1]}']
        else: 
            NEA_Main=[f'between {NEA_Main[0]} and {NEA_Main[-1]}']
        
        if len(NEA_Sector)>1:
            NEA_Sector=[f'between {NEA_Sector[0]} and {NEA_Sector[-1]}']
        else:
            NEA_Sector=[f'between {NEA_Sector[0]} and {NEA_Sector[-1]}']
            
        if (('between 2 and 399') in locations_list) and ('between 1 and 1') in locations_list:
            locations_list=['between 1 and 399']
            
        
        query_Data={'main':NEA_Main[0],'sector': NEA_Sector[0],
                    'location': locations_list[0],'year':calc_year,'powerFactor':power_Factor,
                    'resolution':resolution,'scenario': scenario,'energy_carrier':e_carrier,'name':name,'source':ts_source}
        query_Data_list.append(query_Data)
        
    #print(query_Data_list)
    return query_Data_list

def main():
    
    """
    This is just for testing the code above with an calculation_case_set. In this example there are just one case!
    """
    
    query_configurations([{'User': 'TV', 'Initial_data': 'USW-district', 'Reference year': '2019', 'Calculation year': '2030',
                           'Resolution': '1H', 'Scenario': 'NIP', 'Energy carrier': 'electricity','Timeseries_Source':'PV_GIS', 'Creation_time': '2024-03-21T15:42:20',
                           'Comment': '', 'Car': False, 'Heavy duty truck': False, 'Light duty truck': False, 'Locomotiv': False,
                           'Industry': False, 'H0 households': False, 'Households heatpumps': False, 'Services': False,
                           'Services heatpumps': False, 'Photovoltaik': True, 'Wind': False, 'Hydro <10MW': False,
                           'Hydro >10MW': False, 'Biomass': False}])

    
if __name__ == '__main__':

    sys.exit(main())