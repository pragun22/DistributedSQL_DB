CREATE TABLE `Fragments` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `SiteId` int,
  `FragmentType` varchar(255),
  `RelationName` varchar(255)
);

CREATE TABLE `Site` (
  `Id` int PRIMARY KEY AUTO_INCREMENT,
  `IP/BindAddress` varchar(255),
  `Port` int
);

CREATE TABLE `Attributes` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `AttributeName` varchar(255),
  `RelationName` varchar(255)
);

CREATE TABLE `Horizontal-Fragment` (
  `FragmentId` int,
  `AttributeId` int,
  `condition` varchar(255),
  PRIMARY KEY (`FragmentId`, `AttributeId`)
);

CREATE TABLE `Vertical-Fragment` (
  `FragmentId` int,
  `AttributeId` int,
  PRIMARY KEY (`FragmentId`, `AttributeId`)
);

CREATE TABLE `Derived-Horizontal-Fragment` (
  `FragmentId` int,
  `AttributeId` int,
  `condition` int,
  `Right_Table_FragmentId` int,
  PRIMARY KEY (`FragmentId`, `AttributeId`)
);

ALTER TABLE `Horizontal-Fragment` ADD FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`);

ALTER TABLE `Vertical-Fragment` ADD FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`);

ALTER TABLE `Derived-Horizontal-Fragment` ADD FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`);

ALTER TABLE `Horizontal-Fragment` ADD FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`);

ALTER TABLE `Vertical-Fragment` ADD FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`);

ALTER TABLE `Derived-Horizontal-Fragment` ADD FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`);

ALTER TABLE `Site` ADD FOREIGN KEY (`Id`) REFERENCES `Fragments` (`SiteId`);

ALTER TABLE `Horizontal-Fragment` ADD FOREIGN KEY (`FragmentId`) REFERENCES `Derived-Horizontal-Fragment` (`Right_Table_FragmentId`);

