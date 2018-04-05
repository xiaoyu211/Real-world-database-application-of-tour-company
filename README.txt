PostgreSQL account: xw2419

URL: http://40.114.89.48:8111 


Parts unchanged from Project 1.1

As from 1.1, we keep the Customer, Tour Package, Groups, Attraction, Tour Company, Tour Guide, Language as entity sets. We also have Join as a relationship set that associate Customer and Groups.

Changes From Project 1.1 

1. We cancel the aggregation part that treats customer-buys-tour package as one relationship set to connect with Join. 

We followed the suggestion from the feedback of the project 1.1.

2. we cancel the Buy relationship set in order to make the design more concise. 

3. We delete the address entity since it is not necessary. 

4. we add user name (UNIQUE) and password as attributes of Customer entity in order to make the login feature to work. 



Interesting parts:

1. A visitor can visit the website by entering the “Visit the page as guest”. Then the visitor can view the front page and what can one do in the front page, e.g. search the tour package information by destination, looking for tour companies. However, only the membership can interact with the website and data in the database. By clicking the New Membership Registration, a visitor can register an account and the information will be insert into the Customer table. After login into the website, a visitor can view his/her information by entering Member Profile. The page will show the visitor’s basic information by accessing the Customer table. It will also access the Join’s table to check if the user is already in a group or not. If he/she indeed joined a group, the page will show the information as well. 

2. The search page using destination is quite interesting. A user can view all the destination and by searching them, a tour package id and associated tour companies will be represented. The page first shows all the attraction names by extract the attraction names from the database, then the customer will be able to search one of them. The input of the page will be used to find the associated attraction in the database. Based on the attraction, it will go back to find the associated tour packages. Based on the tour packages, it will also find the tour companies. After all the operations, the result will show the tour package id, tour company. It also shows the information of the associated groups of the tour packages.

