CREATE TABLE `car` (
  `vin` int(11) NOT NULL,
  `msrp` int(11) DEFAULT NULL,
  `cost` int(11) DEFAULT NULL,
  `make` text,
  `model` text,
  `year` int(11) DEFAULT NULL,
  `owner` text,
  PRIMARY KEY (`vin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into car (vin, msrp,cost,make,model,year,owner)
values 
	(100, 25000, 20000, "Honda", "Accord", 2012, "Jon"),
	(101, 25000, 20000, "Honda", "Accord", 2012, "none"),
	(102, 25000, 20000, "Honda", "Accord", 2012, "none"),
	(103, 22000, 17000, "Honda", "Civic", 2012, "Jon"),
	(104, 22000, 17000, "Honda", "Civic", 2012, "Jon"),
	(105, 22000, 17000, "Honda", "Civic", 2012, "none");
	(106, 40000, 32000, "Subaru", "STI", 2014, "Mike"),
	(107, 25000, 20000, "Audi", "S4", 2014, "Casey"),
	(108, 25000, 20000, "Honda", "Civic", 2012, "none");
	



CREATE TABLE `customer` (
  `name` text,
  `email` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `sale` (
  `cust` text,
  `vin` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `ds` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `service` (
  `name` text,
  `price` int(11) DEFAULT NULL,
  `dur` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
