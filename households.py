# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:29:51 2023

@author: Thomas Vouk
"""
import psycopg2 as ps
import pandas as pd

"""

Households are calculatet based on the WAM-Scenario from the Project InfraTrans2040 --> and also based on the Timeseries, which was used there!

"""

def calcHousehold(scenario,calc_year, e_carrier):
    year=calc_year[1:5]
    try:
        connection = ps.connect(database="InfraTrans",
                                user="postgres",
                                password="1evt!Met?OG1",
                                host="193.171.80.232",
                                port="5432")
        cursor = connection.cursor()
        myQuery = 'SELECT u.id as "usw",'+scenario+' as "scenario",'+calc_year+' as "time",'+e_carrier+' as "energy_carrier",u.timeseries_id as "timeseries_id",\
                (select s.value\
	            From public."state_data" s\
	            where s.NEA_sec = 14\
	            and s.time = '+calc_year+'\
	            and s.project='+scenario+'\
	            and s.e_carrier= '+e_carrier+')\
                *sum(u.value/\
                (select sum(u1.value) FROM public."USW_data" u1\
                where u1.timeseries_id = 832\
	            and u1.energy_carrier = 1\
	            and u1.scenario=\'WAM\'\
	            and u1.time ='+calc_year+'\
	            and u1.id between 3000 and 4000)\
                ) as "value",u.name as "name"\
                FROM public."USW_data" u\
                where u.timeseries_id = 832\
                and u.energy_carrier = 1\
                and u.scenario= \'WAM\'\
                and u.time ='+calc_year+'\
                and u.id between 3000 and 4000\
                group by 1,2,3,4,5,7'

        cursor.execute(myQuery)
        mT = pd.read_sql(myQuery, connection)
        Energiewerte = cursor.fetchall()
        #p = mT.pivot(index='Zeitpunkt', columns='USW_id', values='Wert')
        mT.to_csv(f"Households{scenario}{year}{e_carrier}.csv",index=False)

    except (Exception, ps.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        mT= 'error'

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return mT
