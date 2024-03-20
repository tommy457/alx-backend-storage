-- Script that creates a table named users.

CREATE TABLE IF NOT EXISTS  users(
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    email VARCHAR(256) UNIQUE NOT NULL,
    name VARCHAR(256)
);
