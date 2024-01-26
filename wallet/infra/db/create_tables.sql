CREATE TABLE Users (
    ID TEXT PRIMARY KEY,
    Email TEXT UNIQUE,
    API_key TEXT UNIQUE
);

CREATE TABLE Wallets (
    Address TEXT PRIMARY KEY,
    Amount INTEGER,
    User_ID TEXT,
    FOREIGN KEY (User_ID) REFERENCES Users(ID)
);

CREATE TABLE Transactions (
    UUID TEXT PRIMARY KEY,
    From_Address TEXT,
    To_Address TEXT,
    Amount INTEGER,
    Fee INTEGER,
    FOREIGN KEY (From_Address) REFERENCES Wallets(Address),
    FOREIGN KEY (To_Address) REFERENCES Wallets(Address)
);

CREATE TABLE AdminKeys (
    API_Key TEXT PRIMARY KEY
);
