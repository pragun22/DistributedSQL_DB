CREATE TABLE `Fragments` (
  `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `SiteId` int NOT NULL,
  `FragmentType` varchar(255) NOT NULL,
  `RelationName` varchar(255) NOT NULL
);

CREATE TABLE `Site` (
  `Id` int  NOT NULL PRIMARY KEY,
  `IP/BindAddress` varchar(255) NOT NULL,
  `Port` int NOT NULL
);

CREATE TABLE `Attributes` (
  `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `AttributeName` varchar(255) NOT NULL,
  `RelationName` varchar(255) NOT NULL
);

CREATE TABLE `HorFragment` (
  `FragmentId` int NOT NULL,
  `AttributeId` int NOT NULL,
  `condition` varchar(255) NOT NULL,
  PRIMARY KEY (`FragmentId`, `AttributeId`)
);

CREATE TABLE `VerFragment` (
  `FragmentId` int NOT NULL,
  `AttributeId` int NOT NULL,
  PRIMARY KEY (`FragmentId`, `AttributeId`)
);

CREATE TABLE `DHorFragment` (
  `FragmentId` int NOT NULL,
  `AttributeId` int NOT NULL,
  `condition` varchar(256) NOT NULL,
  `Right_Table_FragmentId` int NOT NULL,
  PRIMARY KEY (`FragmentId`, `AttributeId`)
);

ALTER TABLE `HorFragment` ADD FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`);

ALTER TABLE `VerFragment` ADD FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`);

ALTER TABLE `DHorFragment` ADD FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`);

ALTER TABLE `HorFragment` ADD FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`);

ALTER TABLE `VerFragment` ADD FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`);

ALTER TABLE `DHorFragment` ADD FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`);

ALTER TABLE `Fragments` ADD FOREIGN KEY (`SiteId`) REFERENCES `Site` (`Id`);

ALTER TABLE `DHorFragment` ADD FOREIGN KEY (`Right_Table_FragmentId`) REFERENCES `HorFragment` (`FragmentId`);

