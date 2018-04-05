CREATE TABLE Customers(
    cid VARCHAR(20) NOT NULL,
    cname VARCHAR(20),
    age INTEGER CHECK (age >0),
    gender VARCHAR(1) CHECK (gender =‘F’ or gender =‘M’),
    phone INTEGER,
    PRIMARY KEY (cid)
);

CREATE TABLE Travel_Company (
    tcid VARCHAR(20) NOT NULL,
    tcname VARCHAR(20),
    rate FLOAT CHECK (rate > 0),
    state VARCHAR(2),
    phone VARCHAR(20),
    PRIMARY KEY (tcid)
);

CREATE TABLE Tour_Package (
    tid VARCHAR(20) NOT NULL,
    price FLOAT CHECK (price >0),
    rate FLOAT CHECK (rate > 0),
    tcid VARCHAR(20) NOT NULL,
    PRIMARY KEY (tid),
    FOREIGN KEY(tcid) REFERENCES Travel_company (tcid) ON DELETE CASCADE
);

CREATE TABLE Groups (
    gid VARCHAR(20) NOT NULL,
    gname VARCHAR(20),
    capacity INTEGER CHECK (capacity > 0),
    tid VARCHAR(20) NOT NULL,
    PRIMARY KEY (gid),
    FOREIGN KEY(tid) REFERENCES Tour_package (tid) ON DELETE CASCADE
);


CREATE TABLE Tour_Guide (
    tgid VARCHAR(20) NOT NULL,
    tgname VARCHAR(20),
    gender VARCHAR(1)CHECK (gender =‘F’ or gender =‘M’),
    exp INTEGER CHECK (exp > 0),
    rate FLOAT CHECK (rate > 0),
    tcid VARCHAR(20) NOT NULL,
    PRIMARY KEY (tgid),
    FOREIGN KEY(tcid) REFERENCES Travel_company (tcid) ON DELETE CASCADE
);

CREATE TABLE TG_Language (
    tlname VARCHAR(20) NOT NULL,
    tgid VARCHAR(20),
    PRIMARY KEY (tlname,tgid),
    FOREIGN KEY(tgid) REFERENCES Tour_guide (tgid) ON DELETE CASCADE
    
);

CREATE TABLE Tour_Attraction (
    aid VARCHAR(20),
    destination VARCHAR(225),
    PRIMARY KEY (aid),
    tid VARCHAR(20),
    FOREIGN KEY(tid) REFERENCES Tour_Package (tid) ON DELETE CASCADE
);

CREATE TABLE Joins (
    cid VARCHAR(20),
    gid VARCHAR(20),
    jdate DATE,
    PRIMARY KEY (cid,gid),
    FOREIGN KEY(cid) REFERENCES Customers (cid) ON DELETE CASCADE,
    FOREIGN KEY(gid) REFERENCES Groups (gid) ON DELETE CASCADE
);

