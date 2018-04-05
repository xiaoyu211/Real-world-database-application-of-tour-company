Xiaoyu Wang  xw2419
Yuhao Pan    yp2391

postreSQL: xw2419


1): CREATE COMPOSITE TYPE
CREATE TYPE address_type AS(
street_address VARCHAR, 
city VARCHAR,
state VARCHAR, 
zip VARCHAR);

CREATE TABLE address (
address_id serial, 
address_struct address_type, 
cid VARCHAR(20), 
primary key(address_id), 
foreign key(cid) references customer (cid) ON DELETE CASCADE);

We create a composite type of address as a new entity to our design. To the tour companies, it is necessary to know the demographic of the customer in order to provide better service and design new tour packages tailoring to it. 


QUERY: print all information who lived in the NYC
SELECT address_id,(address_struct).street_address,
(address_struct).city,
(address_struct).state,
(address_struct).zip
FROM address 
WHERE (address_struct).city= 'NEW YORK';

2): add arrays column ‘languages’ to table ‘tour_guide’
ALTER TABLE tour_guide ADD COLUMN languages text[];

We add a new attribute of language speaking to the tour_guide table. It makes perfect that since most of the tour guides should speak more than one language. The reason we made language as a entity is that we did’t know there exists a array type. Therefore, we decided to delete the language entity and make it as an attribute. 
We didn’t delete the language yet, since our project 1.3 was still on progress of grading. We will definitely update that in the future. 

QUERY: select any tour guide who speaks ‘Chinese’.
SELECT * FROM tour_guide WHERE 'Chinese' = ANY (languages);


3): add text column ‘attraction’ to table ‘tour_atrraction’
ALTER TABLE tour_attraction ADD COLUMN attraction text;


We add a new attribute of attractions to tour_attraction table. Before the updating, the attraction table only contains the information of location of the attraction instead of the name of the attraction. In the real world, tour packages will include both the attraction names and the locations. Therefore, customers can pick those that they are most interested. 

QUERY: print attraction information which contain word ‘Grand Canyon’.
SELECT A.tid, A.destination 
FROM tour_attraction A 
WHERE to_tsvector('english', attraction) @@ to_tsquery('english','Grand & Canyon');