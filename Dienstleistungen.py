# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:29:51 2023

@author: Thomas Vouk
"""
import psycopg2 as ps
import pandas as pd
from saveResults import resultDirectory

def calcDienstleistungen(scenario, ref_year, calc_year, e_carrier):
    year=calc_year[1:5]
    try:
        connection = ps.connect(database="InfraTrans",
                                user="thomas_vouk",
                                password="V1o1u0k91",
                                host="193.171.80.144",
                                port="5432")
        cursor = connection.cursor()
        myQuery = 'SELECT "Verschneidung"."USW",\
                od.time,\
                sum("Verschneidung"."Gemeinde_Anteil"*m_nace."m_rel"*od.rel_ele*\
    				(SELECT s.value FROM public.state_data s\
    				where s.state=4\
    				and s.time = '+calc_year+'\
    				and s.nea_sec=15\
    				and s.e_carrier ='+e_carrier+'\
    				and s.project='+scenario+')) as "Verbrauch_DL"\
    				FROM public.oenace_ab_data od\
    				join public."OENACE_Abteilung" oa\
    				on oa.id= od.id,\
    				(SELECT e."oenace_Abt" as "abt",\
    				e."GKZ",\
    				e.employee/ms_sum.s_m as "m_rel"\
    				FROM public.employee e\
    				join public."OENACE_Abteilung" oa\
    				on e."oenace_Abt"=oa.id,\
    				(SELECT e."oenace_Abt" as "abt",\
    				sum(e.employee) as "s_m"\
    				FROM public.employee e\
    				join public."OENACE_Abteilung" oa\
    				on e."oenace_Abt"=oa.id\
    				where oa."NEA_main"=3\
    				and e."GKZ" between 40000 and 50000\
    				group by 1\
    				)as "ms_sum"\
    				where oa."NEA_main"=3\
    				and ms_sum.abt=e."oenace_Abt"\
    				and e."GKZ" between 40000 and 50000\
    				)as "m_nace"\
    				join\
    				(select s."id" as "GKZ",\
    				u."id" as "USW",\
    				ST_Area(ST_INTERSECTION(u."polygon", s."polygon"))/ST_AREA(s."polygon") as "Gemeinde_Anteil"\
    				from public."USW" u, public."municipality_gis" s\
    				WHERE u."id" between 2000 and 9000\
    				and s."id" between 40000 and 50000\
    				and ST_Overlaps(u."polygon", s."polygon")\
    				UNION ALL\
    				select s."id",\
    				u."id",\
    				ST_Contains(u."polygon", s."polygon")::int as "Gemeinde_Anteil"\
    				from public."USW" u, public."municipality_gis" s\
    				WHERE u."id" between 2000 and 9000\
    				and s."id" between 40000 and 50000\
    				and (ST_Contains(u."polygon", s."polygon") = True)\
    				)as "Verschneidung"\
    				on "Verschneidung"."GKZ"=m_nace."GKZ"\
    				where od.time = '+calc_year+'\
    				and m_nace."abt"=od.id\
    				and oa."NEA_main"=3\
    				group by 1,2\
    				order by 1'

        cursor.execute(myQuery)
        mT = pd.read_sql(myQuery, connection)
        Energiewerte = cursor.fetchall()
        directory_path=resultDirectory()
       
        mT.to_csv(f"{directory_path}Dl{scenario}{year}{e_carrier}.csv")

    except (Exception, ps.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        mT='error'

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return mT
