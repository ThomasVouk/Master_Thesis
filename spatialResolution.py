# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:13:44 2023

@author: Thomas Vouk
"""
import sys
from Query import Dienstleistungen_v2 as dl
from Query import services_Hp as s_Hp
from Query import pkw_v2 as p
from Query import Top_down_industry_v2_gas as ind
from Query import Top_down_industry_v2_gas as indg
from Query import households_v1 as h
#import households_gas as hg
from Query import LNF_v2 as lnf
from Query import SNF_v1 as snf
from Query import company as c
from Query import company_gas as cg
from Query import households_heat_pump as hp
import psycopg2 as ps


def calculateSpatial(data_cases):
    
    for d in data_cases:
        
        user=d.get('User')
        s_ref=d.get('Reference_Scenario')
        scenario_ref=f"'{s_ref}'"

        s_calc=d.get('Calculate_Scenario')
        scenario_calc=f"'{s_calc}'"

        source=d.get('Initial_data')
        if d.get('Energy carrier')=='electricity':
            e_carrier='1'
        
        if d.get('Energy carrier')=='CH4':
            e_carrier='2'

        if d.get('Energy carrier')=='district heat':
            e_carrier='3'

        if d.get('Energy carrier')=='hydrogen':
            e_carrier='4'



            
        ref_year=f"'{d.get('Reference year')}-01-01 00:00:00'"
        calc_year=f"'{d.get('Calculation year')}-01-01 00:00:00'"
        
        if d.get('Resolution')=='1H':
            resolution='1'#Resoltution 1 means 1hour Resolution
        else:
            resolution='2'#Resoltution 2 means 15Min Resolution
        
        if d.get('Target')=='USW-district':
            
            goal='USW'
        else:
            goal='district'
        
        

        if d.get('Car')==True:#Calculate vehicle Spatial Resolution
            car=p.calcPKW(scenario_ref, ref_year, calc_year,e_carrier,source,'1',resolution,goal)#PKW 
            
          
        if d.get('Light duty truck')==True:
            l_d_truck=lnf.calcLNF(scenario_ref,calc_year, e_carrier,source,'1',goal) # 1 stands for Austria --> for future Projects here could be other numbers for other Countries 
        
        if d.get('Heavy duty truck')==True:#SNF Lokal and SNF long distance mixture (actual 96 to 4 %)
            h_d_truck=snf.calcSNF(scenario_ref,calc_year, e_carrier,source,'1',resolution,goal) # 1 stands for Austria --> for future Projects here could be other numbers for other Countries 
        
        if d.get('Industry Top-down')==True:#Calculate Industry-Top-Down Spatial Resolution
            
            if e_carrier=='1':
                industrie=ind.top_down_industry(scenario_ref, ref_year,scenario_calc, calc_year,e_carrier,source,'1',goal,"'NEFI'","'1'")
            
            else:
                
                 industrie=indg.top_down_industry(scenario_ref, ref_year,scenario_calc, calc_year,e_carrier,e_carrier,source,'1',goal,"'NEFI'","'2'",'ch4')
    
        """
        #Spatial resolution industry, first one is for energy_carrier ref_year, the secound "1" is for the country 1=Austria, InfraTrans is for the Steakholder_research
        The "2" is for gas timeseries.
        The ch4 means, that the gas timeseries are connected with the energy values.
        """
        
        if (d.get('Industrie Bottom-Up')==True and e_carrier =='1'):#Calculate company Spatial Resolution
            company=c.calcCompany(scenario_ref, ref_year,scenario_calc, calc_year,e_carrier,e_carrier,source,'1',goal,"'NEFI'")

        if (d.get('Industrie Bottom-Up')==True and e_carrier =='2'):#Calculate company_Gas Spatial Resolution
            
            company=cg.calcCompanyGas(scenario_ref, ref_year,scenario_calc, calc_year,e_carrier,e_carrier,source,'1',goal,"'NEFI'")
        
        if d.get('Households H0')==True:#Calculate households Spatial Resolution
            H=h.calcHousehold(scenario_ref, calc_year,ref_year,e_carrier,source,'1',goal)#Households 
        
        if d.get('Households heatpumps')==True:#Calculate spatial resolution for heatpumps_households 
            Hp=hp.calcHouseholdHeatPump(scenario_ref, calc_year,'9',source,'1',goal)#calculate heatpumps for households
        
        if d.get('Services')==True:#Calculate spatial resolution for heatpumps_households 
            DL_G0=dl.calcDienstleistungen(scenario_ref, ref_year, calc_year, e_carrier, source,'1', goal)#DL_Strom(login_data,Scenario,Bezugsjahr;Berechnungsjahr,Energieträger=(1=elektrische Energie), )
        
        if d.get('Services heatpumps')==True:#Calculate spatial resolution for heatpumps_households
            e_carrier='9'
            DL_WP=s_Hp.calcHp(scenario_ref, ref_year, calc_year,e_carrier,source,'1',goal,resolution )#'1' Means the country -> 1 Stands for Austria
        
        """
        
        scenario=["'NEFI_POI'"]
        e_carrier=['2']
        #e_carrier=['4','2']
        
        #scenario=["'NIP'",]
        
        
        Calculate Scenario (The reference year is at the moment part of the Query and is for all of the data 2019 
        except for the transportation, there it is 2020 after TU Graz)
        
        
        #year=["'2030-01-01 00:00:00'","'2040-01-01 00:00:00'",]
        year=["'2025-01-01 00:00:00'",]
        #year=["'2025-01-01 00:00:00'","'2030-01-01 00:00:00'","'2035-01-01 00:00:00'","'2040-01-01 00:00:00'","'2045-01-01 00:00:00'","'2050-01-01 00:00:00'"] 
        #Calculate Year
        
        
        source={'State':'state','Country':'country'}
        #Dataframe for the datasource of the regionalization prozess for example state or country
        
        #goal={'USW':'USW','Municipality':'municipality'} 
        goal={'USW':'USW'}
        
        country={'Austria':'1',}#This is for the future modul to get a Drop down menue for the user
        #state={'UpperAustria':'4',}#This is for the future modul to get Drop down menues for the users 
        #Dataframe for the desired result of the regionalization prozess for example nodes of the "Node-Branch-Modell or Municipality
        
        for e in e_carrier:
            for s in scenario:
                for y in year:
            
                    #DL_WP=dl.calcDienstleistungen(s, "'2019-01-01 00:00:00'", y,'1','country','1','USW' )#DL_Wärmepumpen (Scenario,Bezugsjahr;Berechnungsjahr,Energieträger=9(Strom für WP))
                    
                    #DL_G0=dl.calcDienstleistungen(s, "'2019-01-01 00:00:00'", y,'1','country','1','USW' )#DL_Strom(Scenario,Bezugsjahr;Berechnungsjahr,Energieträger=(1=elektrische Energie) )
                    #DL_G0=dl.calcDienstleistungen(s, "'2019-01-01 00:00:00'", y,'2','country','1','USW' )
                    #PKW=p.calcPKW(s, "'2020-01-01 00:00:00'", y,'4')#PKW elektrisch
                    
                    #PKW=p.calcPKW(s, "'2020-01-01 00:00:00'", y,'1','country','1','municipality')#PKW elektrisch
                    #PKW=p.calcPKW(s, "'2020-01-01 00:00:00'", y,'1','country','1','municipality')#PKW elektrisch
                    
                    #industrie=ind.top_down_industry(s, "'2020-01-01 00:00:00'", y,'4',e,'country','1','USW',"'NEFI'","'2'",'hydrogen')#Industrie verortung elektrisch Energie
                    industrie=ind.top_down_industry(s, "'2019-01-01 00:00:00'", y,'2',e,'country','1','USW',"'NEFI'","'2'",'ch4')#Industrie verortung CH4
                    #industrie=ind.top_down_industry(s, "'2020-01-01 00:00:00'", y,'1','1','country','1','USW',"'NEFI'","'1'",'electricity')
                    #H=h.calcHousehold(s, y,'1','country','1','USW')#Households elektrische Energie
                    
                    #SNF=snf.calcSNF_LNF(s, y,'4','country','1','municipality')#SNF und LNF berechnung für elektrische Energie
                    #SNF=snf.calcSNF_LNF(s, y,'4','country','1')#SNF und LNF berechnung für elektrische Energie
                    
                    #LNF=lnf.calcLNF(s, y,'1','country','1','district')#SNF und LNF berechnung für elektrische Energie
                    #LKW=lkw.calcSNF_LNF(s, y,'2')#SNF und LNF berechnung für elektrische Energie
                    
                    #company=cg.calcCompany(s, "'2019-01-01 00:00:00'", y,e,'country','1','USW',"'NEFI'")#Unternehmen Regionalisierung elektrisch Energie
                    #company=cg.calcCompany(s, "'2019-01-01 00:00:00'", y,e,'country','1','USW',"'InfraTrans'")#Unternehmen Regionalisierung elektrisch Energie
                    #Hp=hp.calcHouseholdHeatPump(s, y,'9','country','1','USW')#Berechnung Wärmepumpen für Haushalte elektrisch
                    
                    #DL_G0_g=dlg.calcDienstleistungen(s, "'2019-01-01 00:00:00'", y,'2' )#DL_G0_g(Scenario,Bezugsjahr;Berechnungsjahr,Energieträger=(2=CH4) )
                    #industrie_g=indg.top_down_industry(s, "'2019-01-01 00:00:00'", y,'2')#Industrie verortung CH4
                    #H_g=hg.calcHousehold(s, y,'2')#Households CH4
                    #PKW_g=p.calcPKW(s, "'2020-01-01 00:00:00'", y,'2')#PKW CH4
                    #company=c.calcCompany(s, "'2019-01-01 00:00:00'", y,e,e,'country','1','USW',"'NEFI'")#Unternehmen Regionalisierung CH4
                    #company=c.calcCompany(s, "'2019-01-01 00:00:00'", y,e,e,'country','1','USW',"'NEFI'")#Unternehmen Regionalisierung CH4
                    #LKW_g=lkw.calcSNF_LNF(s, y,'2')#SNF und LNF berechnung für CH4
        
        #print(Hp)
        #print(car)
        """
        #print('Calculation is done!')

def main():
    
    """
    This is just for testing the code above with an calculation_case_set. In this example there are just one case!
    """
    
    calculateSpatial([{'User': 'Unknown_User', 'Initial_data': 'country', 'Energy carrier': 'electricity',
                       'Reference_Scenario': 'NIP', 'Reference year': '2020', 'Calculation year': '2030',
                       'Resolution': '1H', 'Target': 'USW-district', 'Creation_time': '2024-03-14T11:34:05',
                       'Comment': '', 'Car': False, 'Light duty truck': False, 'Heavy duty truck': False,
                       'Industry Top-down': False, 'Industrie Bottom-Up': False, 'Households H0': False,
                       'Households heatpumps': False, 'Services': False, 'Services heatpumps': True,
                       'Locomotiv': False, 'Compressor station': False}])


if __name__ == '__main__':

    sys.exit(main())