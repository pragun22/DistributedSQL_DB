-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: Lonely
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Attributes`
--

DROP TABLE IF EXISTS `Attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Attributes` (
  `id` int NOT NULL,
  `AttributeName` varchar(255) NOT NULL,
  `RelationName` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Attributes`
--

LOCK TABLES `Attributes` WRITE;
/*!40000 ALTER TABLE `Attributes` DISABLE KEYS */;
INSERT INTO `Attributes` VALUES (1,'Id','Supplier'),(2,'ContanctNumber','Supplier'),(3,'ContactName','Supplier'),(4,'CompanyName','Supplier'),(5,'Email','Supplier'),(6,'Phone','Supplier'),(7,'City','Supplier'),(8,'Address','Supplier'),(9,'PostalCode','Supplier'),(10,'Id','Category'),(11,'Name','Category'),(12,'Decription','Category'),(13,'Id','Products'),(14,'Name','Products'),(15,'Decription','Products'),(16,'Quantity','Products'),(17,'Price','Products'),(18,'SupplierId','Products'),(19,'CategoryId','Products');
/*!40000 ALTER TABLE `Attributes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Category`
--

DROP TABLE IF EXISTS `Category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Category` (
  `Id` int unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Description` mediumtext NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Category`
--

LOCK TABLES `Category` WRITE;
/*!40000 ALTER TABLE `Category` DISABLE KEYS */;
INSERT INTO `Category` VALUES (1,'Mens','Mens Category for Clothing');
/*!40000 ALTER TABLE `Category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DHorFragment`
--

DROP TABLE IF EXISTS `DHorFragment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DHorFragment` (
  `FragmentId` int NOT NULL,
  `AttributeId` int NOT NULL,
  `Right_Table_FragmentId` int NOT NULL,
  PRIMARY KEY (`FragmentId`,`AttributeId`),
  KEY `AttributeId` (`AttributeId`),
  KEY `Right_Table_FragmentId` (`Right_Table_FragmentId`),
  CONSTRAINT `DHorFragment_ibfk_1` FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`),
  CONSTRAINT `DHorFragment_ibfk_2` FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`),
  CONSTRAINT `DHorFragment_ibfk_3` FOREIGN KEY (`Right_Table_FragmentId`) REFERENCES `HorFragment` (`FragmentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DHorFragment`
--

LOCK TABLES `DHorFragment` WRITE;
/*!40000 ALTER TABLE `DHorFragment` DISABLE KEYS */;
INSERT INTO `DHorFragment` VALUES (1,13,1),(1,14,1),(1,15,1),(1,16,1),(1,17,1),(1,18,1),(1,19,1),(2,13,2),(2,14,2),(2,15,2),(2,16,2),(2,17,2),(2,18,2),(2,19,2),(3,13,3),(3,14,3),(3,15,3),(3,16,3),(3,17,3),(3,18,3),(3,19,3);
/*!40000 ALTER TABLE `DHorFragment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fragments`
--

DROP TABLE IF EXISTS `Fragments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Fragments` (
  `id` int NOT NULL,
  `SiteId` int NOT NULL,
  `FragmentType` varchar(255) NOT NULL,
  `RelationName` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `SiteId` (`SiteId`),
  CONSTRAINT `Fragments_ibfk_1` FOREIGN KEY (`SiteId`) REFERENCES `Site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fragments`
--

LOCK TABLES `Fragments` WRITE;
/*!40000 ALTER TABLE `Fragments` DISABLE KEYS */;
INSERT INTO `Fragments` VALUES (1,1,'Hor','Category'),(2,2,'Hor','Category'),(3,3,'Hor','Category'),(4,1,'Ver','Supplier'),(5,2,'Ver','Supplier'),(6,1,'DHor','Product'),(7,2,'DHor','Product'),(8,3,'DHor','Product');
/*!40000 ALTER TABLE `Fragments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HorFragment`
--

DROP TABLE IF EXISTS `HorFragment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HorFragment` (
  `FragmentId` int NOT NULL,
  `AttributeId` int NOT NULL,
  `condition` varchar(255) NOT NULL,
  PRIMARY KEY (`FragmentId`,`AttributeId`),
  KEY `AttributeId` (`AttributeId`),
  CONSTRAINT `HorFragment_ibfk_1` FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`),
  CONSTRAINT `HorFragment_ibfk_2` FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HorFragment`
--

LOCK TABLES `HorFragment` WRITE;
/*!40000 ALTER TABLE `HorFragment` DISABLE KEYS */;
INSERT INTO `HorFragment` VALUES (1,10,'Men'),(1,11,'Men'),(1,12,'Men'),(2,10,'Women'),(2,11,'Women'),(2,12,'Women'),(3,10,'Children'),(3,11,'Children'),(3,12,'Children');
/*!40000 ALTER TABLE `HorFragment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product` (
  `Id` int NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Description` text NOT NULL,
  `Quantity` int NOT NULL,
  `Price` int NOT NULL,
  `SupplierId` int NOT NULL,
  `CategoryId` int NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product`
--

LOCK TABLES `Product` WRITE;
/*!40000 ALTER TABLE `Product` DISABLE KEYS */;
/*!40000 ALTER TABLE `Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Site`
--

DROP TABLE IF EXISTS `Site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Site` (
  `id` int NOT NULL,
  `IP/BindAddress` varchar(255) NOT NULL,
  `Port` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Site`
--

LOCK TABLES `Site` WRITE;
/*!40000 ALTER TABLE `Site` DISABLE KEYS */;
INSERT INTO `Site` VALUES (1,'10.3.5.212',22),(2,'10.3.5.211',22),(3,'10.3.5.208',22);
/*!40000 ALTER TABLE `Site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Supplier`
--

DROP TABLE IF EXISTS `Supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Supplier` (
  `Id` int unsigned NOT NULL AUTO_INCREMENT,
  `ContactNumber` varchar(10) NOT NULL,
  `ContactName` varchar(30) NOT NULL,
  `CompanyName` varchar(30) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Supplier`
--

LOCK TABLES `Supplier` WRITE;
/*!40000 ALTER TABLE `Supplier` DISABLE KEYS */;
INSERT INTO `Supplier` VALUES (1,'9345678231','Surya Kumar','Wilson Pvt Ltd'),(2,'9345678232','Akshay Singh','Sam Pvt Ltd'),(3,'9345678233','Rahul Kumar','Singh seeb & co'),(4,'8845678233','Mayank D','kethces & co'),(5,'8985678233','DV j','Pubb corp');
/*!40000 ALTER TABLE `Supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VerFragment`
--

DROP TABLE IF EXISTS `VerFragment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VerFragment` (
  `FragmentId` int NOT NULL,
  `AttributeId` int NOT NULL,
  PRIMARY KEY (`FragmentId`,`AttributeId`),
  KEY `AttributeId` (`AttributeId`),
  CONSTRAINT `VerFragment_ibfk_1` FOREIGN KEY (`FragmentId`) REFERENCES `Fragments` (`id`),
  CONSTRAINT `VerFragment_ibfk_2` FOREIGN KEY (`AttributeId`) REFERENCES `Attributes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VerFragment`
--

LOCK TABLES `VerFragment` WRITE;
/*!40000 ALTER TABLE `VerFragment` DISABLE KEYS */;
INSERT INTO `VerFragment` VALUES (1,1),(2,1),(1,2),(1,3),(1,4),(2,5),(2,6),(2,7),(2,8),(2,9);
/*!40000 ALTER TABLE `VerFragment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-19 21:48:32
