-- Task3.sql

-- Sen Zheng

-- set echoing on

.echo on 

-- set spooling out: note the suffix

.output task3.log

--

.timer on
.print Q1
select C.name from country C,geo_sea S where C.code=S.country;
.print Q2
select name from lake union select name from river union select name from sea;
.print Q3
select avg(length) from river;
.print Q4
select distinct C.name from country C,geo_island I where C.code=I.country group by C.code having count(distinct(island)) >10;
.print Q5
select R.length from geo_river GR,river R where GR.country='GB' and GR.river=R.name;
.print Q6
select C.name,sum(length) from country C,(select distinct GR.river,GR.country,length from geo_river GR,river R where GR.river=R.name) as CL where CL.country=C.code group by code order by sum(length) desc limit 10;
.print Q7
select * from City where name = 'Manchester';
.print Q8
select name from City where name like 'Man%';
.print Q9
select C.name,O.name from isMember iM,Country C,Religion R,Organization O where O.abbreviation=iM.organization and iM.country=C.code and C.code=R.country and R.name='Buddhist' and O.established > '1994-12-01';
.print Q10
select C.name,ifnull(t1.count1,0) from Country C left outer join (select gi.country,count(*) as count1 from geo_island gi group by gi.country) t1 on t1.country=C.code limit 20;

