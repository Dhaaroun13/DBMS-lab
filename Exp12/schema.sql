CREATE TABLE IF NOT EXISTS account (
    accno   INTEGER PRIMARY KEY,
    cname   TEXT    NOT NULL,
    balance REAL    NOT NULL DEFAULT 0 CHECK (balance >= 0)
);

INSERT INTO account (cname, accno, balance) VALUES ('Mathi', 1234, 10000);

SELECT * FROM account;
