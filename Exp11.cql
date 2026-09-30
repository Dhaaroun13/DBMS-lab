cqlsh> CREATE KEYSPACE library WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };

cqlsh> USE library;

cqlsh:library> CREATE TABLE authors ( AuthorID int PRIMARY KEY, FirstName text, LastName text );

cqlsh:library> INSERT INTO authors (AuthorID, FirstName, LastName) VALUES (1, 'George', 'Orwell');
cqlsh:library> INSERT INTO authors (AuthorID, FirstName, LastName) VALUES (2, 'Aldous', 'Huxley');
cqlsh:library> INSERT INTO authors (AuthorID, FirstName, LastName) VALUES (3, 'J.K.', 'Rowling');

cqlsh:library> SELECT * FROM authors;

 authorid | firstname | lastname
----------+-----------+----------
        1 |    George |   Orwell
        2 |    Aldous |   Huxley
        3 |      J.K. |  Rowling

(3 rows)

cqlsh:library> UPDATE authors SET LastName = 'Smith' WHERE AuthorID = 1;

cqlsh:library> SELECT * FROM authors WHERE AuthorID = 1;

 authorid | firstname | lastname
----------+-----------+----------
        1 |    George |    Smith

(1 rows)

cqlsh:library> DELETE FROM authors WHERE AuthorID = 1;

cqlsh:library> SELECT * FROM authors WHERE AuthorID = 1;

 authorid | firstname | lastname
----------+-----------+----------

(0 rows)