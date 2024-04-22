# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:29:51 2023

@author: Thomas Vouk
"""
import psycopg2 as ps
import pandas as pd

def calcSNF_LNF(scenario,calc_year, e_carrier):
    year=calc_year[1:5]
    try:
        connection = ps.connect(database="InfraTrans",
                                user="postgres",
                                password="1evt!Met?OG1",
                                host="193.171.80.232",
                                port="5432")
        cursor = connection.cursor()
        myQuery = 'Select "Verschneidung"."USW",\
                    sum("lkw"."SNF"*"Verschneidung"."Bezirk_Anteil") as SNF,\
                    sum("lkw"."LNF"*"Verschneidung"."Bezirk_Anteil") as "LNF" FROM\
                    (SELECT d.id as "BKZ",\
                    0.5*(Select s.value\
                    From public.state_data s\
                    where s.nea_sec=24\
                    and s.time='+calc_year+'\
                    and s.state =4\
                    and s.e_carrier='+e_carrier+'\
                    and s.project ='+scenario+')*\
                    d."SNF_lokal"/\
                    (Select sum(d1."SNF_lokal")\
                    	FROM public.district_data d1\
                    	where d1.time = '+calc_year+'\
                    	and d1.id between 400 and 500	\
                    )+0.5*(Select s.value\
                    From public.state_data s\
                    where s.nea_sec=24\
                    and s.time='+calc_year+'\
                    and s.state =4\
                    and s.e_carrier='+e_carrier+'\
                    and s.project ='+scenario+')*\
                    d."SNF_fern"/\
                    (Select sum(d2."SNF_fern")\
                    	FROM public.district_data d2\
                    	where d2.time = '+calc_year+'\
                    	and d2.id between 400 and 500\
                    ) as "SNF",\
                    (Select s.value\
                    From public.state_data s\
                    where s.nea_sec=25\
                    and s.time='+calc_year+'\
                    and s.state =4\
                    and s.e_carrier='+e_carrier+'\
                    and s.project ='+scenario+')*\
                    d."LNF"/(Select sum(d3."LNF")\
                    	FROM public.district_data d3\
                    	where d3.time = '+calc_year+'\
                    	and d3.id between 400 and 500)as "LNF"\
                    FROM public.district_data d\
                    where d.time = '+calc_year+'\
                    and d.id between 400 and 500)as "lkw"\
                    	join(select s."id" as "BKZ",\
                    		u."id" as "USW",\
                    		ST_Area(ST_INTERSECTION(u."polygon", s."polygon"))/ST_AREA(s."polygon") as "Bezirk_Anteil"\
                    		from public."USW" u, public."district_gis" s\
                    		WHERE s."id" between 400 and 500\
                    		and ST_Overlaps(u."polygon", s."polygon")\
                    		UNION ALL\
                    		select s."id" as "BKZ",u."id",\
                    		ST_Area(ST_INTERSECTION(u."polygon", s."polygon"))/ST_AREA(s."polygon") as "Bezirk_Anteil"\
                    		from public."USW" u, public."district_gis" s\
                    		WHERE s."id" between 400 and 500\
                    		and ((ST_Contains(u."polygon", s."polygon") = True)or (ST_Contains(s."polygon", u."polygon") = True)))as "Verschneidung"\
                    	on "Verschneidung"."BKZ"=lkw."BKZ"\
                    	group by 1'

        cursor.execute(myQuery)
        mT = pd.read_sql(myQuery, connection)
        Energiewerte = cursor.fetchall()
        #p = mT.pivot(index='Zeitpunkt', columns='USW_id', values='Wert')
        mT.to_csv(f"LKW{scenario}{year}.csv",index=False)

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
