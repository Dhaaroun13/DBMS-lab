SQL> Create table customer(id int PRIMARY KEY,Name varchar(30),age int,address varchar(100),salary int);

Table created.

SQL> Insert into customer values(1,'ezhil',23,'aaa',20000);

1 row created.

SQL> Insert into customer values(2,'aarthi',24,'bbb',30000);

1 row created.

SQL> Insert into customer values(3,'sumathi',21,'ccc',35000);

1 row created.

SQL> Insert into customer values(4,'viji',24,'ddd',40000);

1 row created.


SQL> Insert into customer values(5,'priya',21,'eee',43000);

1 row created.


SQL> select*from customer;

        ID NAME                                  AGE
---------- ------------------------------ ----------
ADDRESS
--------------------------------------------------------------------------------
    SALARY
----------
         1 ezhil                                  23
aaa
     20000

         2 aarthi                                 24
bbb
     30000

        ID NAME                                  AGE
---------- ------------------------------ ----------
ADDRESS
--------------------------------------------------------------------------------
    SALARY
----------

         3 sumathi                                21
ccc
     35000

         4 viji                                   24
ddd

        ID NAME                                  AGE
---------- ------------------------------ ----------
ADDRESS
--------------------------------------------------------------------------------
    SALARY
----------
     40000

         5 priya                                  21
eee
     43000




SQL> SET SERVEROUTPUT ON;
SQL>
SQL> DECLARE
  2 c_id    customer.id%TYPE := 5;
  3 c_name  customer.name%TYPE;
  4 c_addr  customer.address%TYPE;
  5
  6  BEGIN
  7  SELECT name, address
  8      INTO c_name, c_addr
  9      FROM customer
 10      WHERE id = c_id;
 11
 12      DBMS_OUTPUT.PUT_LINE('name: ' || c_name);
 13      DBMS_OUTPUT.PUT_LINE('address: ' || c_addr);
 14
 15  EXCEPTION
 16      WHEN NO_DATA_FOUND THEN
 17          DBMS_OUTPUT.PUT_LINE('no such customer!');
 18
 19      WHEN OTHERS THEN
 20          DBMS_OUTPUT.PUT_LINE('error!');
 21
 22  END;
 23  /
name: priya
address: eee

PL/SQL procedure successfully completed.


SQL> DECLARE
  2      c_id    customer.id%TYPE := -6;
  3      c_name  customer.name%TYPE;
  4      c_addr  customer.address%TYPE;
  5
  6      ex_invalid_id EXCEPTION;
  7
  8  BEGIN
  9      IF c_id <= 0 THEN
 10          RAISE ex_invalid_id;
 11      ELSE
 12          SELECT name, address
 13          INTO c_name, c_addr
 14          FROM customer
 15          WHERE id = c_id;
 16
 17          DBMS_OUTPUT.PUT_LINE('Name: ' || c_name);
 18          DBMS_OUTPUT.PUT_LINE('Address: ' || c_addr);
 19      END IF;
 20
 21  EXCEPTION
 22      WHEN ex_invalid_id THEN
 23          DBMS_OUTPUT.PUT_LINE('ID must be greater than zero!');
 24
 25      WHEN NO_DATA_FOUND THEN
 26          DBMS_OUTPUT.PUT_LINE('No such customer!');
 27
 28      WHEN OTHERS THEN
 29          DBMS_OUTPUT.PUT_LINE('Error!');
 30
 31  END;
 32  /
ID must be greater than zero!

PL/SQL procedure successfully completed.



SQL>