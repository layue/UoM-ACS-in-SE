.timer on
.echo on
.output week2.log

-- 1
select City.name from City cross join Country;
select City.name from City join Country;

-- 2
select name from City where City.population between 1000 and 20000000;
create index index_pop on City(population);
select name from City where City.population between 1000 and 20000000;

-- 3
select name from City where name like 'Man%';
select name from City where name >= 'Man' and name <= 'Manz';
