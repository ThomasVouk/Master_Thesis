# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:29:51 2023

@author: Thomas Vouk
"""
import psycopg2 as ps
import pandas as pd

def calcPKW(scenario, ref_year, calc_year, e_carrier,source,country,target):
    
    year=calc_year[1:5]#für die Ausgabe in der CSV-Datei relevant
    
    try:
        connection = ps.connect(database="InfraTrans",
                                user="thomas_vouk",
                                password="V1o1u0k91",
                                host="193.171.80.144",
                                port="5432")
        cursor = connection.cursor()
        myQuery = 'Select data.usw as "usw",data.scenario as"scenario",data.time as "time",\
                    data.energy_carrier as "energy_carrier",ts_nea.id as "timeseries_id", data.value as "value",ts_nea.name as "name"\
                        \
                    FROM (Select "Verschneidung"."USW" as "usw",'+scenario+' as "scenario",to_char(pkw.time,\'yyyy-mm-dd HH24:MI\') as "time",\
                    \''+e_carrier+'\' as "energy_carrier",\
                    sum("pkw"."PKW_Anteil"*"Verschneidung"."Bezirk_Anteil")as "value",\'PKW\' as "name"\
                    FROM\
                    (Select d.id as "BKZ","resident".res_time as "time",\
		            sum((\
                    Select s.value\
		            From public.'+source+'_data s\
		            where s.nea_sec=23\
		            and s.time='+calc_year+'\
		            and s.id ='+country+'\
		            and s.e_carrier= '+e_carrier+'\
		            and s.project ='+scenario+'\
		            )*(d."PKW"/d.resident)*resident."res30"/\
                    (Select sum((d."PKW"/d.resident)*resident."res30")\
	                as "pkw_2030_ele"\
		            FROM public.district_data d\
		            join\
                    (Select d.id as "id",d.time as "time",d.resident as "res30"\
			        FROM public.district_data d\
			        where d.time = '+calc_year+'\
			        and d.id between 400 and 500\
		            ) as resident\
		            on resident.id=d.id\
		            where d.time = '+ref_year+'\
		            and d.id between 400 and 500\
		            ))\
                    as "PKW_Anteil"\
                    FROM \
	                public.district_data d\
	                join\
                    (\
                    Select d.id as "id",d.time as "res_time",\
		            d.resident as "res30"\
		            FROM public.district_data d\
		            where d.time = '+calc_year+'\
		            and d.id between 400 and 500\
	                ) as resident\
	                on resident.id=d.id\
	                where d.time = '+ref_year+'\
	                and d.id between 400 and 500\
	                group by 1,2)\
	                as "pkw"\
	                join\
                    (\
		            select s."id" as "BKZ",\
		            u."id" as "USW",\
		            ST_Area(ST_INTERSECTION(u."polygon", s."polygon"))/ST_AREA(s."polygon") as "Bezirk_Anteil"\
		            from public."USW" u, public."district_gis" s\
		            WHERE s."id" between 400 and 500\
		            and ST_Overlaps(u."polygon", s."polygon")\
                  UNION ALL \
                  select s."id" as "BKZ",\
		            u."id",\
		            ST_Area(ST_INTERSECTION(u."polygon", s."polygon"))/ST_AREA(s."polygon") as "Bezirk_Anteil"\
		            from public."USW" u, public."district_gis" s\
		            WHERE s."id" between 400 and 500\
		            and ((ST_Contains(u."polygon", s."polygon") = True)or (ST_Contains(s."polygon", u."polygon") = True))\
		            )\
		            as "Verschneidung"\
	                on "Verschneidung"."BKZ"=pkw."BKZ"\
	                group by 1,2,3,4,6) as "data"\
                    join(Select ts.id as "id", ns.name as "name", ns.id as "ids" From public."time_series" ts\
                         join public."NEA_sector" ns \
                        on ts."nea_sector"=ns.id\
                    where ts.id between 832 and 2100 \
                        and ts.type =3 and ns.id=23)as "ts_nea"\
                    on data."name"=ts_nea.name\
                    where ts_nea.id between 832 and 2100 \
                        and ts_nea.ids=23'
        cursor.execute(myQuery)
        mT = pd.read_sql(myQuery, connection)
        Energiewerte = cursor.fetchall()
        #p = mT.pivot(index='Zeitpunkt', columns='USW_id', values='Wert')
        mT.to_csv(f"PKW{scenario}{year}.csv",index=False)

    except (Exception, ps.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        mT = 'error'

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return mT
