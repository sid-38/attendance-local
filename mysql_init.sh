mysql -u root -pletmein -h 127.0.0.1 -P 3307 << EOF
DROP DATABASE nitc;
CREATE DATABASE nitc;
use nitc;
CREATE TABLE user(tid int PRIMARY KEY AUTO_INCREMENT, id varchar(10), b varchar(255));
CREATE TABLE rollcall(slno int PRIMARY KEY AUTO_INCREMENT, id varchar(10), date varchar(12), time varchar(12));
EOF