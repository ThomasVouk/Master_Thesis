# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:13:44 2023

@author: Thomas Vouk
"""
import sys
#import Dienstleistungen_v2 as dl
#import Dienstleistungen_gas as dlg
#import pkw_v2 as p
import Top_down_industry_v2_gas as ind
#import Top_down_industry_v2_gas as indg
#import households_v1 as h
#import households_gas as hg
#import LNF_v2 as lnf
#import SNF_v1 as snf
import SNF_LNF_v2 as snf
import company as c
import company_gas as cg
#import households_heat_pump as hp


def main():
    
    
    #Calculate electricity demand --> energy_carrier = 1
    #Calculate electricity demand for heat pumps --> energy carrier = 9
    
    #scenario=["'E_AG_ISB'","'E_AG_SK'","'E_AG_Trend'","'E_AG_WAM'",]
    #scenario=["'E_AG_ISB'","'E_AG_WAM'",]
    
    #scenario=["'E_AG_ISB'",]
    
    
    #scenario=["'NEFI_ZEM'","'NEFI_POI'"]
    #scenario=["'NEFI_POI'"]
    scenario=["'NIP'"]
    
   
    e_carrier=['1']
    #e_carrier=['4','2']
    
    #scenario=["'NIP'",]
    
    """
    Calculate Scenario (The reference year is at the moment part of the query and is for all of the data 2019 
    except for the transportation, there it is 2020 after TU Graz)
    """
    
    year=["'2030-01-01 00:00:00'","'2040-01-01 00:00:00'",]
    #year=["'2025-01-01 00:00:00'",]
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
    #print(DL_G0)
    
    print('Calculation is done!')

if __name__ == '__main__':

    sys.exit(main())