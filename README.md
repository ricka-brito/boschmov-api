# BOSCHmov
A Hackathon project to plan your routes with the bosch-bus

azure:
DATABASE_URL = mysql+mysqlconnector://BOSCHmov@data-boschmov:24INDUSTRIAconectada@data-boschmov.mariadb.database.azure.com:3306/boschmov
local:
DATABASE_URL = mysql+mysqlconnector://root@127.0.0.1:80/boschmov
SECRET_KEY = 238fa334079a3c0f3ae99f15




Dependencies for backend:
- fastapi
- pymysql
- sqlalchemy
- passlib
- python-jose
- bcrypt

+++++++++++++++++++Creation script of mysql databse:+++++++++++++++++++++

CREATE DATABASE `boschmov` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
CREATE TABLE `bus` (
   `lineNumber` varchar(45) NOT NULL,
   `departureTime` time NOT NULL,
   PRIMARY KEY (`lineNumber`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `adress` (
   `idAdress` int(11) NOT NULL AUTO_INCREMENT,
   `cep` varchar(255) NOT NULL,
   `houseNumber` int(11) DEFAULT NULL,
   `street` varchar(255) NOT NULL,
   `neighborhood` varchar(255) NOT NULL,
   `city` varchar(255) NOT NULL,
   PRIMARY KEY (`idAdress`)
 ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `busstop` (
   `idBusStop` int(11) NOT NULL AUTO_INCREMENT,
   `stopNumber` int(11) NOT NULL,
   `time` time NOT NULL,
   `idAdress` int(11) DEFAULT NULL,
   PRIMARY KEY (`idBusStop`),
   KEY `idAdress` (`idAdress`),
   CONSTRAINT `busstop_ibfk_1` FOREIGN KEY (`idAdress`) REFERENCES `adress` (`idAdress`)
 ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `busstop_bus` (
   `idBusStop` int(11) DEFAULT NULL,
   `idBusStop_Bus` int(11) NOT NULL AUTO_INCREMENT,
   `lineNumberBus` varchar(45) DEFAULT NULL,
   PRIMARY KEY (`idBusStop_Bus`),
   KEY `idBusStop` (`idBusStop`),
   KEY `busstop_bus_ibfk_3` (`lineNumberBus`),
   CONSTRAINT `busstop_bus_ibfk_2` FOREIGN KEY (`idBusStop`) REFERENCES `busstop` (`idBusStop`),
   CONSTRAINT `busstop_bus_ibfk_3` FOREIGN KEY (`lineNumberBus`) REFERENCES `bus` (`lineNumber`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `user` (
   `iduser` int(11) NOT NULL AUTO_INCREMENT,
   `name` varchar(255) NOT NULL,
   `edv` varchar(255) NOT NULL,
   `password` varchar(255) NOT NULL,
   `admin` tinyint(4) NOT NULL DEFAULT 0,
   PRIMARY KEY (`iduser`)
 ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

+++++++++++++++++++++++++Creation of first admin user+++++++++++++++++++++++++++

INSERT INTO `boschmov`.`user` (`iduser`, `name`, `edv`, `password`, `admin`) VALUES ('1', 'admin', '12345678', '$2a$12$KCeNGwls4U6P66ZvcWx50.zyUZn0lYK1npyfdS6I/UtzS0Sftkeqy', '1');