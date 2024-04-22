"""
Thomas Vouk 20.01.2023
EVT Leoben
"""

import sys
import psycopg2 as ps
import pandas as pd

from queryConfigurations import query_configurations
from saveResults import resultDirectory

"""
For this calculation it is a must have, that the energy demand and supply is placed on the nodes of the node bus model.
It is also a must have, that every entry in the table USW_data is connected with the correct timeseries in the table timeseries 
and then this is connected with the timeseries id tho the ts_value table, where every timeseries is stored in one single table. 

It is also nessesary, that every entry in the usw_data table have the correct energy_carrier and an timestamp with the correct
calculation year. 

Then you can choose between the differenz szenarios, wich are shown in the bottom 
"""
def getTimeseriesMatrix(query_data):
    
    for q in query_data:
        
        main=q.get('main')
        sector=q.get('sector')
        location=q.get('location')
        year=q.get('year')
        powerFactor=q.get('powerFactor')  
        resolution=q.get('resolution')
        scenario=q.get('scenario')
        source=q.get('source')
        energy_carrier=q.get('energy_carrier')
        name=q.get('name')
        
        try:
            connection = ps.connect(database ="InfraTrans", 
                                    user = "thomas_vouk", 
                                    password = "V1o1u0k91", 
                                    host = "193.171.80.144", 
                                    port = "5432")
            cursor = connection.cursor()
            
            myQuery = 'SELECT to_char(zw."time",\'mm-dd HH24:MI\')AS "Zeitpunkt",\
                d."id" AS "USW_id",'+powerFactor+'*SUM(zw."value"*d."value") AS "Wert"\
                FROM "public"."ts_value" zw,"public"."USW_data" d\
                WHERE zw."id"=d."timeseries_id"\
                AND d."scenario" ='+scenario+'\
                AND zw."id" IN \
                (Select ts.id\
                FROM public.time_series ts\
                WHERE ts."NEA_main" '+main+'\
                and ts."nea_sector"'+sector+'\
                and ts."source"='+source+'\
                and ts.type=1 and\
                ts.resolution='+resolution+')\
                AND d."time" ='+year+'\
                AND d."energy_carrier" ='+energy_carrier+'\
                GROUP BY zw."time",d."id"\
                ORDER BY d."id"'
            
            cursor.execute(myQuery)
            mT = pd.read_sql(myQuery,connection)
            #mT = pd.read_sql_query(myQuery,connection)
            Energiewerte = cursor.fetchall()
            p=mT.pivot(index='Zeitpunkt', columns='USW_id',values='Wert')
            
            directory_path=resultDirectory()#Create result file directory if it doesen´t exist
            p.to_csv(f"{directory_path}"+energy_carrier+scenario+resolution+name+source+str(year[1:5])+".csv")#save file to result folder 
        
        except (Exception, ps.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    


def main():
    
    """
    This is just for testing the code above with an getTimeseriesMatrix
    """
    
    getTimeseriesMatrix([{'main': 'between 6 and 6', 'sector': 'between 0 and 0', 'location': 'between 2 and 399', 'year': "'2030-01-01 00:00:00'",
                          'powerFactor': '1', 'resolution': '1', 'scenario': "'NIP'", 'energy_carrier': '1','source': '1'}])


if __name__ == '__main__':

    sys.exit(main())

