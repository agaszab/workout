-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: workout
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `series`
--

DROP TABLE IF EXISTS `series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `series` (
  `ids` int NOT NULL AUTO_INCREMENT,
  `id_exercise` int DEFAULT NULL,
  `number_sets` mediumint DEFAULT NULL,
  `number_repeats` varchar(20) COLLATE utf8mb3_polish_ci DEFAULT NULL,
  `weight` varchar(45) COLLATE utf8mb3_polish_ci DEFAULT NULL,
  `superseries` tinyint DEFAULT '0',
  `set` int DEFAULT '0',
  PRIMARY KEY (`ids`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_polish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `series`
--

LOCK TABLES `series` WRITE;
/*!40000 ALTER TABLE `series` DISABLE KEYS */;
INSERT INTO `series` VALUES (1,1,4,'20,18,15,12','15',0,NULL),(2,2,5,'max','20',0,NULL),(6,4,4,'10-12','3-4',0,NULL),(7,3,5,'15, max','5, 7.5',0,NULL),(8,5,4,'12','20',0,NULL),(9,6,5,'20, 15, 12, 10, 8','4, 5, 6, 7, 8',0,NULL),(10,7,4,'10-12','progress od 30',0,NULL),(11,9,4,'15, 12, 10, 10','8',0,NULL),(12,10,4,'10-12','progres',0,NULL),(13,11,4,'20','bez, 2.5, 5, 7.5',0,NULL),(14,12,3,'20','15',1,1),(15,13,3,'20','25',1,1),(16,14,3,'od szyby do drzwix2','bez',1,1),(17,15,3,'20','30',1,2),(18,16,3,'20','30',1,2),(19,18,5,'bez, bez, 5, 5, 5','15, 15, max',0,NULL),(20,19,5,'12, 10-12','7, 9 lub 10',0,NULL),(21,20,4,'20-30','bez',0,NULL),(22,21,3,'20','bez',0,NULL),(23,22,3,'20','bez',0,NULL);
/*!40000 ALTER TABLE `series` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-09 16:00:04
