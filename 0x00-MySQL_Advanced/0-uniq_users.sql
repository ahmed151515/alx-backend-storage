-- solve task
CREATE TABLE IF NOT EXISTS users (
    id int not NULL AUTO_INCREMENT,
    email varchar(255) not NULL,
    name varchar(255),
    UNIQUE (email),
    PRIMARY KEY (id)
)