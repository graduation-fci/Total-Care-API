-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: totalcareapi
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `users_medicationprofile_medicine`
--

DROP TABLE IF EXISTS `users_medicationprofile_medicine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_medicationprofile_medicine` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `medicationprofile_id` bigint NOT NULL,
  `medicine_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_medicationprofile__medicationprofile_id_med_ec5cd55b_uniq` (`medicationprofile_id`,`medicine_id`),
  KEY `users_medicationprof_medicine_id_bb009076_fk_medicines` (`medicine_id`),
  CONSTRAINT `users_medicationprof_medicationprofile_id_2aa388c7_fk_users_med` FOREIGN KEY (`medicationprofile_id`) REFERENCES `users_medicationprofile` (`id`),
  CONSTRAINT `users_medicationprof_medicine_id_bb009076_fk_medicines` FOREIGN KEY (`medicine_id`) REFERENCES `medicines_medicine` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_medicationprofile_medicine`
--

LOCK TABLES `users_medicationprofile_medicine` WRITE;
/*!40000 ALTER TABLE `users_medicationprofile_medicine` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_medicationprofile_medicine` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-16  6:19:48
