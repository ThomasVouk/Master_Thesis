# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:29:51 2023

@author: Thomas Vouk
"""
import psycopg2 as ps
import pandas as pd

"""
comments: There must be a change, that you can choose between the typ of timeseries 1 = electricity 1h; 3 = electricity 15min
            There must be also a change for all USW- Areas and not just for upper austria, but the rest must be the same!!
            Probably there must be a change for the USW-Areas to overlapp it with districts, which are smaller than a single municipality!

"""


def top_down_industry(scenario, ref_year, calc_year, e_carrier):
    year=calc_year[1:5]
    try:
        connection = ps.connect(database="InfraTrans",
                                user="postgres",
                                password="1evt!Met?OG1",
                                host="193.171.80.232",
                                port="5432")
        cursor = connection.cursor()
        myQuery = 'Select data.usw as "usw",data.scenario as"scenario",data.time as "time",\
                    data.energy_carrier as "energy_carrier",ts_nea.id as "timeseries_id", data.value as "value",ts_nea.name as "name"\
                        \
                    FROM (SELECT "Verschneidung"."USW" as "usw",s.project as "scenario",\
                    to_char(s.time,\'yyyy-mm-dd HH24:MI\')as "time" ,s.e_carrier as "energy_carrier",\
                    sum(coalesce(s.value-company_demand."Verbrauch",s.value)*m_rel."Mitarbeiter_relativ"*"Verschneidung"."Gemeinde_Anteil")\
                    as "value",s.nea_sec as "nea_sector"\
                        \
                    From public.state_data s\
                    full join(\
	                SELECT c.nea_sector as "nea_sec",\
	                sum(cd.electricity*NEA."Wachstumsrate") as "Verbrauch",NEA.time as "time"\
	                From\
	                (SELECT s.nea_sec, s1.time as "time", s.e_carrier as "e_carrier", s1.value/s.value as "Wachstumsrate"\
	                From public.state_data s\
	                join public.state_data s1\
	                on s1.nea_sec=s.nea_sec\
	                and s1.time ='+calc_year+'\
	                and s.time ='+ref_year+'\
                   and s.project = '+scenario+'\
                   and s1.project = '+scenario+'\
   	                and s.e_carrier = '+e_carrier+'\
                   and s1.e_carrier = '+e_carrier+'\
	                ) AS NEA,\
                        \
                    public.company c\
	                join public.company_data cd\
	                on c.id =cd."company_id"\
	                where c.usw_id between 3000 and 4000\
	                and NEA.nea_sec=c.nea_sector\
	                and cd.project = \'E_AG_ISZ\'\
                   and NEA.e_carrier='+e_carrier+'\
	                Group by c.nea_sector,NEA.time)\
                    as company_demand\
                    on company_demand.nea_sec=s.nea_sec,\
                        public."NEA_sector",\
	                (SELECT\
	                oa."NEA_sector" as "nea_sec",\
	                e."GKZ" as "GKZ",\
	                sum(e.employee) as "m_abs",\
	                sum(e.employee/nea_mitarbeiter."Mitarbeiter") as "Mitarbeiter_relativ"\
	                FROM public.employee e\
	                join public."OENACE_Abteilung" oa\
                    on e."oenace_Abt"=oa.id,\
		            (SELECT\
		            oa."NEA_sector" as "nea_sec",\
		            sum(e.employee) as "Mitarbeiter"\
		            FROM public.employee e\
		            join public."OENACE_Abteilung" oa\
                    on e."oenace_Abt"=oa.id\
		            where oa."NEA_main"=1\
                    and e."GKZ" between 40000 and 50000\
                    group by 1)as nea_mitarbeiter\
	                where oa."NEA_main"=1\
	                and e."GKZ" between 40000 and 50000\
	                and nea_mitarbeiter."nea_sec"=oa."NEA_sector"\
	                group by 1,2)as m_rel\
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
	                ) as "Verschneidung"\
	                on "Verschneidung"."GKZ"=m_rel."GKZ"\
                    where s.time ='+calc_year+'\
                    and s.nea_sec <14\
                    and m_rel.nea_sec=s.nea_sec\
                    and s.project='+scenario+'\
                    and s.e_carrier = '+e_carrier+'\
                    group by 1,2,3,4,6\
                    order by 1) as "data"\
                    join(Select ts.id as "id", ns.name as "name", ns.id as "ids" From public."time_series" ts\
                         join public."NEA_sector" ns \
                        on ts."nea_sector"=ns.id\
                    where ts.id between 832 and 2100 \
                        and ts.type =3 and ns.id<14)as "ts_nea"\
                    on data."nea_sector"=ts_nea.ids\
                    where ts_nea.id between 832 and 2100 \
                        and ts_nea.ids<14'
    

        cursor.execute(myQuery)
        mT = pd.read_sql(myQuery, connection)
        Energiewerte = cursor.fetchall()
        #p = mT.pivot(index='Zeitpunkt', columns='USW_id', values='Wert')\
        mT.to_csv(f"TD_Industry{scenario}{year}.csv",index=False)

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
