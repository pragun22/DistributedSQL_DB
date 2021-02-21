CREATE TABLE `Supplier` (
  `id` int PRIMARY KEY,
  `ContactNumber` int,
  `Contactname` varchar(256),
  `CompanyName` varchar(256),
  `Email` varchar(256),
  `Address` varchar(256),
  `City` varchar(256),
  `PostalCode` int
);

CREATE TABLE `Category` (
  `Id` int PRIMARY KEY AUTO_INCREMENT,
  `Name` varchar(256),
  `Description` varchar(256)
);

CREATE TABLE `Product` (
  `id` int PRIMARY KEY,
  `SupplierId` int,
  `CategoryId` int,
  `Price` int,
  `Quantity` int,
  `Name` varchar(256),
  `Description` text,
);

ALTER TABLE `products` ADD FOREIGN KEY (`SupplierId`) REFERENCES `Supplier` (`id`);

ALTER TABLE `Category` ADD FOREIGN KEY (`Id`) REFERENCES `products` (`CategoryId`);

CREATE UNIQUE INDEX `products_index_0` ON `products` (`id`);
