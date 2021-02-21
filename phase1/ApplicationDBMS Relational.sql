CREATE TABLE `Supplier` (
  `id` int PRIMARY KEY,
  `ContactNumber` int,
  `Contactname` string,
  `CompanyName` string,
  `Email` string,
  `Address` string,
  `City` string,
  `PostalCode` int
);

CREATE TABLE `Category` (
  `Id` int PRIMARY KEY AUTO_INCREMENT,
  `Name` string,
  `Description` string
);

CREATE TABLE `products` (
  `id` int PRIMARY KEY,
  `SupplierId` int,
  `CategoryId` int,
  `Price` int,
  `Quantity` int,
  `Name` string,
  `Description` string
);

ALTER TABLE `products` ADD FOREIGN KEY (`SupplierId`) REFERENCES `Supplier` (`id`);

ALTER TABLE `Category` ADD FOREIGN KEY (`Id`) REFERENCES `products` (`CategoryId`);

CREATE UNIQUE INDEX `products_index_0` ON `products` (`id`);
