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
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-04-10 15:11:39.349819','1','5-fluorouracil -ebewe 250mg/5ml i.v. vial',3,'',7,2),(2,'2023-04-10 15:11:39.368823','3','5-fluorouracil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(3,'2023-04-10 15:11:39.373823','5','5-fluorourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(4,'2023-04-10 15:11:39.376885','7','5-flusasdsaorourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(5,'2023-04-10 15:11:39.380884','9','5-flusasdsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(6,'2023-04-10 15:11:39.384899','11','5-flusasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(7,'2023-04-10 15:11:39.389827','19','5-flusasgrhejkremnrbhjsssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(8,'2023-04-10 15:11:39.393821','17','5-flusasssbnm,ssasdsadasdkjljkl -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(9,'2023-04-10 15:11:39.397879','15','5-flusasssbnm,sssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(10,'2023-04-10 15:11:39.401819','13','5-flusassssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(11,'2023-04-10 15:11:39.405845','8','abrammuaaaaaaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(12,'2023-04-10 15:11:39.408877','10','abrammuaaaaaIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(13,'2023-04-10 15:11:39.412840','12','abrammuaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(14,'2023-04-10 15:11:39.416821','18','abrammubnm,sssasssaaaaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(15,'2023-04-10 15:11:39.419824','16','abrammubnm,sssasssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(16,'2023-04-10 15:11:39.423845','2','abrammune 100 mg 50 capsules(n/a yet)',3,'',7,2),(17,'2023-04-10 15:11:39.426819','4','abrammune 1ssss00 mg 50 capsules(n/a yet)',3,'',7,2),(18,'2023-04-10 15:11:39.430845','6','abrammune 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(19,'2023-04-10 15:11:39.434822','20','abrammusssaerwesssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(20,'2023-04-10 15:11:39.437866','14','abrammusssasssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(21,'2023-04-10 16:00:44.499597','31','5-flusaaaasgrsssaadsadhejddkxxxremnrbhjsssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(22,'2023-04-10 16:00:44.507630','23','5-flusasgrhejddkremnrbhjsssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(23,'2023-04-10 16:00:44.510594','25','5-flusasgrhejddkxxxremnrbhjsssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(24,'2023-04-10 16:00:44.514595','21','5-flusasgrhejkremnrbhjsssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(25,'2023-04-10 16:00:44.519601','27','5-flusasgrsssahejddkxxxremnrbhjsssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(26,'2023-04-10 16:00:44.523595','29','5-flusasgrsssassshejddkxxxremnrbhjsssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(27,'2023-04-10 16:00:44.527595','24','abrammusssaerwddesssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(28,'2023-04-10 16:00:44.531597','26','abrammusssaerwddxxxesssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(29,'2023-04-10 16:00:44.536598','22','abrammusssaerwesssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(30,'2023-04-10 16:00:44.563600','28','abrammusssasssserwddxxxesssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(31,'2023-04-10 16:00:44.587597','32','abrammusssasssssssdadaerwddxxxesssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(32,'2023-04-10 16:00:44.669025','30','abrammusssassssssserwddxxxesssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(33,'2023-04-16 00:05:27.004498','1','try one',3,'',6,2),(34,'2023-04-16 00:05:27.048564','2','try two',3,'',6,2),(35,'2023-04-16 00:05:38.387406','21','anti tachycardia',3,'',8,2),(36,'2023-04-16 00:05:38.392408','19','antineoplastic',3,'',8,2),(37,'2023-04-16 00:05:38.397407','17','immunostimulant',3,'',8,2),(38,'2023-04-16 00:05:38.402706','22','immunosupggpressant',3,'',8,2),(39,'2023-04-16 00:05:38.407704','20','immunosuppressant',3,'',8,2),(40,'2023-04-16 00:05:38.412706','18','zinc supplement',3,'',8,2),(41,'2023-04-16 00:05:53.825206','33','5-flusaaaasgrsssaadsadhejddkxNBNNBNBNxxremnrbhjsssssasdSSSsaoSDSADSADDSDrourssssacil -ebewe 25ssss0mg/5ml i.v. vial',3,'',7,2),(42,'2023-04-16 00:05:53.873643','34','abrammusssasssssssdadaNMNMerwddxxxesssaaaaaSSSIOIPIaane 1ssss00 mg 50 casssspsules(n/a yet)',3,'',7,2),(43,'2023-04-16 00:35:26.591855','35','abimol 150mg/5ml 125ml syrup',3,'',7,2),(44,'2023-04-16 00:45:19.256904','36','abimol 500mg 20 tablets',3,'',7,2);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-16  6:19:39
