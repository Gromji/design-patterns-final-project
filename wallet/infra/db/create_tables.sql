CREATE TABLE Users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Email TEXT UNIQUE,
    API_key TEXT UNIQUE
);

CREATE TABLE Wallets (
    Address TEXT PRIMARY KEY,
    Amount REAL,
    User_ID INTEGER,
    FOREIGN KEY (User_ID) REFERENCES Users(ID)
);

CREATE TABLE Transactions (
    UUID TEXT PRIMARY KEY,
    From_Address TEXT,
    To_Address TEXT,
    Amount REAL,
    Fee REAL,
    FOREIGN KEY (From_Address) REFERENCES Wallets(Address),
    FOREIGN KEY (To_Address) REFERENCES Wallets(Address)
);

CREATE TABLE AdminKeys (
    API_Key TEXT PRIMARY KEY
);
