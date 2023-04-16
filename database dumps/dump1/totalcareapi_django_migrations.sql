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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-04-10 05:00:38.587131'),(2,'contenttypes','0002_remove_content_type_name','2023-04-10 05:00:40.801123'),(3,'auth','0001_initial','2023-04-10 05:00:55.947724'),(4,'auth','0002_alter_permission_name_max_length','2023-04-10 05:00:58.138192'),(5,'auth','0003_alter_user_email_max_length','2023-04-10 05:00:58.150176'),(6,'auth','0004_alter_user_username_opts','2023-04-10 05:00:58.162177'),(7,'auth','0005_alter_user_last_login_null','2023-04-10 05:00:58.175175'),(8,'auth','0006_require_contenttypes_0002','2023-04-10 05:00:58.180176'),(9,'auth','0007_alter_validators_add_error_messages','2023-04-10 05:00:58.192176'),(10,'auth','0008_alter_user_username_max_length','2023-04-10 05:00:58.201175'),(11,'auth','0009_alter_user_last_name_max_length','2023-04-10 05:00:58.215182'),(12,'auth','0010_alter_group_name_max_length','2023-04-10 05:00:58.289175'),(13,'auth','0011_update_proxy_permissions','2023-04-10 05:00:58.304180'),(14,'auth','0012_alter_user_first_name_max_length','2023-04-10 05:00:58.316177'),(15,'core','0001_initial','2023-04-10 05:00:58.856178'),(16,'admin','0001_initial','2023-04-10 05:00:59.077173'),(17,'admin','0002_logentry_remove_auto_add','2023-04-10 05:00:59.090175'),(18,'admin','0003_logentry_add_action_flag_choices','2023-04-10 05:00:59.106183'),(19,'medicines','0001_initial','2023-04-10 05:00:59.613174'),(20,'medicines','0002_alter_drug_name_alter_medicine_name_and_more','2023-04-10 05:00:59.698178'),(21,'medicines','0003_alter_medicine_drug','2023-04-10 05:00:59.709196'),(22,'medicines','0004_alter_medicine_parcode','2023-04-10 05:00:59.796175'),(23,'medicines','0005_alter_medicine_price','2023-04-10 05:00:59.802173'),(24,'medicines','0006_alter_medicine_drug','2023-04-10 05:00:59.811175'),(25,'core','0002_doctor_medicationprofile_alter_user_profile_type_and_more','2023-04-10 05:01:00.529195'),(26,'core','0003_remove_patient_medicationprofile_and_more','2023-04-10 05:01:00.719177'),(27,'core','0004_delete_medicationprofile','2023-04-10 05:01:00.762176'),(28,'guardian','0001_initial','2023-04-10 05:01:01.707173'),(29,'guardian','0002_generic_permissions_index','2023-04-10 05:01:01.788179'),(30,'medicines','0007_alter_medicine_drug','2023-04-10 05:01:01.806179'),(31,'medicines','0008_alter_medicine_drug','2023-04-10 05:01:01.815176'),(32,'medicines','0009_category_remove_medicine_category_image_and_more','2023-04-10 05:01:02.407174'),(33,'sessions','0001_initial','2023-04-10 05:01:02.461175'),(34,'users','0001_initial','2023-04-10 05:01:02.742176'),(35,'medicines','0010_remove_image_category_category_category_and_more','2023-04-10 05:39:31.381238'),(36,'medicines','0011_alter_medicine_category','2023-04-10 05:39:31.487241'),(37,'medicines','0012_rename_category_category_image','2023-04-10 05:41:38.306870'),(38,'medicines','0013_image_category_alter_category_image_and_more','2023-04-10 06:10:48.301052');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-16  6:19:44
