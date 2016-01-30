.echo on 
.mode column
.header on

.output Task3.log
--12
select name as Country_name, population/2 as Half_population from Country limit 10;
--13
select name as Country_name, country as Country_code, province as Province_name, population as Population, elevation as Elevation, latitude as Latitude, longitude as Longitude
from City
where name = 'Manchester';
--14 
select name as City_name
from City
where name like 'Man%';
--15
select country.name as Country_name, organization.name as Organization_name
from country, organization, religion, isMember
where country.code = religion.country and religion.name = 'Buddhist' and organization.established > '1994-12-01' and isMember.country = Country.code and isMember.organization = Organization.abbreviation;
--16
select country.name as Country, ifnull(numbers.times, 0) as Numbers
from Country country left outer join (select island.country,count(*) as times from geo_island island group by island.country) numbers 
on numbers.country=country.code;

