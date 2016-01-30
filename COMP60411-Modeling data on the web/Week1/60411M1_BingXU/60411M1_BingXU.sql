create table people
(
ID smallint primary key,
first_name varchar(255),
last_name varchar(255),
company varchar(255),
address varchar(255),
city varchar(255),
country varchar(255),
postal varchar(255),
email varchar(255),
web varchar(255)
);

create table phone
(
personID varchar(255),
number varchar (255) primary key,
foreign key(personID) references people(ID)
);
