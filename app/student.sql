CREATE DATABASE IF NOT EXISTS student;

USE student;

CREATE TABLE IF NOT EXISTS student (
  srn VARCHAR(20),
  name VARCHAR(255),
  age VARCHAR(5),
  PRIMARY KEY (srn)
);

INSERT INTO student VALUES("1","Sam","21");