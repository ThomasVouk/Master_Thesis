# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:13:44 2023

@author: Thomas Vouk
"""
import sys

from Query import Dienstleistungen_v2 as dl
from Query import pkw_v2 as p
from Query import Top_down_industry_v2_gas as ind
from Query import Top_down_industry_v2_gas as indg
from Query import households_v1 

from Query import LNF_v2 as lnf
from Query import SNF_v1 as snf

from Query import company as c
from Query import company_gas as cg
from Query import households_heat_pump as hp



def calculate(cases):
    
    for case in cases:
        
        user=case.get('User')
        initial_data =case.get('Initial_data')
        energy_carrier=case.get('Energy_carrier')
        scenario=case.get('Scenario')
        reference_year=case.get('Reference year')
        calculate_year=case.get('Calculate year')
        resolution=case.get('Resolution')
        target=case.get('Target')
        creation_time=case.get('Creation_time')
        comment=case.get('Comment')
        
        true_keys = [key for key, value in case.items() if value == True]
        
        print(true_keys)
        
        
        
        
        
        
        print()
        e_carrier=['1']
        #e_carrier=['4','2']
        
        scenario=["'NIP'",]
        
        """
        Calculate Scenario (The reference year is at the moment part of the query and is for all of the data 2019 
        except for the transportation, there it is 2020 after TU Graz)
        """
        
        #year=["'2030-01-01 00:00:00'","'2040-01-01 00:00:00'",]
        year=["'2020-01-01 00:00:00'",]
        #year=["'2025-01-01 00:00:00'","'2030-01-01 00:00:00'","'2035-01-01 00:00:00'","'2040-01-01 00:00:00'","'2045-01-01 00:00:00'","'2050-01-01 00:00:00'"] 
        #Calculate Year
        
        source={'State':'state','Country':'country'}
        #Dataframe for the datasource of the regionalization prozess for example state or country
        
        goal={'USW':'USW','Municipality':'municipality'} 
        
        country={'Austria':'1',}#This is for the future modul to get a Drop down menue for the user
        state={'UpperAustria':'4',}#This is for the future modul to get Drop down menues for the users 
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
                    
                    #industrie=ind.top_down_industry(s, "'2020-01-01 00:00:00'", y,'2',e,'country','1','USW',"'NEFI'","'2'",'ch4')#Industrie verortung elektrisch Energie
                    #industrie=ind.top_down_industry(s, "'2020-01-01 00:00:00'", y,'1','1','country','1','USW',"'NEFI'","'1'",'electricity')
                    #H=h.calcHousehold(s, y,'1','country','1','USW')#Households elektrische Energie
                    
                    #SNF=snf.calcSNF(s, y,'1','country','1','municipality')#SNF und LNF berechnung für elektrische Energie
                    
                    
                    #LNF=lnf.calcLNF(s, y,'1','country','1','district')#SNF und LNF berechnung für elektrische Energie
                    #LKW=lkw.calcSNF_LNF(s, y,'2')#SNF und LNF berechnung für elektrische Energie
                    
                    #company=cg.calcCompany(s, "'2019-01-01 00:00:00'", y,e,'country','1','USW',"'NEFI'")#Unternehmen Regionalisierung elektrisch Energie
                    
                    #Hp=hp.calcHouseholdHeatPump(s, y,'9','country','1','USW')#Berechnung Wärmepumpen für Haushalte elektrisch
                    
                    #DL_G0_g=dlg.calcDienstleistungen(s, "'2019-01-01 00:00:00'", y,'2' )#DL_G0_g(Scenario,Bezugsjahr;Berechnungsjahr,Energieträger=(2=CH4) )
                    #industrie_g=indg.top_down_industry(s, "'2019-01-01 00:00:00'", y,'2')#Industrie verortung CH4
                    #H_g=hg.calcHousehold(s, y,'2')#Households CH4
                    #PKW_g=p.calcPKW(s, "'2020-01-01 00:00:00'", y,'2')#PKW CH4
                    company=c.calcCompany(s, "'2020-01-01 00:00:00'", y,e,e,'country','1','USW',"'NEFI'")#Unternehmen Regionalisierung CH4
                    #LKW_g=lkw.calcSNF_LNF(s, y,'2')#SNF und LNF berechnung für CH4
                
        #print(Hp)
        #print(DL_G0)



            
    """
    
    return 
    



def main():
    
    
    case=[{'User': 'Unknown_User', 'Initial_data': 'state', 'Energy carrier': 'electricity', 'Scenario': 'NIP',
           'Reference year': '2020', 'Calculation year': '2030', 'Resolution': '1H', 'Target': 'USW-district',
           'Creation_time': '2024-01-09T13:28:02', 'Comment': '', 'Car': True, 'Light duty truck': True,
           'Heavy duty truck': True, 'Industry Top-down': False, 'Industrie Bottom-Up': False, 'Households H0': False,
           'Households heatpumps': False, 'Services': False, 'Services heatpumps': False,
           'Locomotiv': False, 'Compressor station': False}]
    
    calculate(case)
    
    

    
    print('Calculation is done!')

if __name__ == '__main__':

    sys.exit(main())