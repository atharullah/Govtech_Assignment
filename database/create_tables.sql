CREATE TABLE item (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    manufacturer_name VARCHAR(255) NOT NULL,
    cost NUMERIC(10,2) NOT NULL,
    weight_kg NUMERIC(10,2) NOT NULL
);

CREATE TABLE member_transaction (
    transaction_id SERIAL PRIMARY KEY,
    membership_id VARCHAR(255) NOT NULL,
    item_id INTEGER NOT NULL,
    total_price NUMERIC(10,2) NOT NULL,
    total_weight_kg NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (membership_id) REFERENCES member(membership_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);

CREATE TABLE member (
    membership_id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    mobile_no VARCHAR(8) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    above_18 BOOLEAN NOT NULL
);
