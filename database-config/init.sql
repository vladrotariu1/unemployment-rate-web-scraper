CREATE TABLE total_unemployment (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    month VARCHAR(30) NOT NULL,
    year VARCHAR(30) NOT NULL,
    county VARCHAR(50),
    total INT NOT NULL,
    women INT NOT NULL,
    men INT NOT NULL,
    under_25 INT NOT NULL,
    25_to_29 INT NOT NULL,
    30_to_39 INT NOT NULL,
    40_to_49 INT NOT NULL,
    50_to_55 INT NOT NULL,
    greater_55 INT NOT NULL
);