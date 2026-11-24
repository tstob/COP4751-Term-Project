-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: job_tracker
-- ------------------------------------------------------
-- Server version	9.4.0
CREATE DATABASE IF NOT EXISTS job_tracker;
USE job_tracker;
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
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (1,1,'2025-01-16','Offer Accepted','v2.1',1,NULL,NULL,NULL,'2026-09-21 23:15:16',NULL),(2,3,'2025-01-13','Interview Completed','v2.1',1,NULL,NULL,NULL,'2026-09-21 23:15:16','{\"feedback\": \"Strong technical skills, good communication\", \"next_steps\": \"Offer extended!\", \"interviewers\": [\"Sarah Johnson\", \"Mike Chen\", \"David Brown\"], \"offer_amount\": 85000, \"interview_rounds\": 2, \"technical_questions\": [\"SQL joins\", \"Python basics\", \"API design\"]}'),(3,4,'2025-01-09','Interview Completed','v2.0',0,NULL,NULL,NULL,'2026-09-21 23:15:16',NULL),(4,5,'2025-01-15','Applied','v2.1',1,NULL,NULL,NULL,'2026-09-21 23:15:16',NULL),(5,7,'2025-01-12','Phone Screen','v2.1',1,NULL,NULL,NULL,'2026-09-21 23:15:16','{\"feedback\": \"Needs more experience with cloud platforms\", \"interviewers\": [\"Emily Williams\"], \"interview_rounds\": 1, \"technical_questions\": [\"Database normalization\", \"Transaction isolation\"]}'),(6,6,'2026-10-03','Applied','v3.0',1,NULL,NULL,NULL,'2026-10-03 22:58:52',NULL);
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES (1,'Tech Solutions Inc','Technology','www.techsolutions.com','Miami','Florida',NULL,'2026-09-21 23:04:31'),(2,'Data Analytics Corp','Data Science','www.dataanalytics.com','Austin','Texas',NULL,'2026-09-21 23:04:31'),(3,'Cloud Systems LLC','Cloud Computing','www.cloudsystems.com','Seattle','Washington',NULL,'2026-09-21 23:04:31'),(4,'Digital Innovations','Software','www.digitalinnovations.com','San Francisco','California','Applied to Senior Developer position on 2026-10-03','2026-09-21 23:04:31'),(5,'Smart Tech Group','AI/ML','www.smarttech.com','Boston','Massachusetts',NULL,'2026-09-21 23:04:31'),(7,'New Tech Corp','Technology',NULL,'Denver','Colorado',NULL,'2026-10-03 22:27:28');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
INSERT INTO `contacts` VALUES (1,1,'Sarah','Johnson','sjohnson@techsolutions.com',NULL,'HR Manager',NULL,NULL,'2026-09-21 23:21:34'),(2,2,'Michael','Chen','mchen@dataanalytics.com',NULL,'Technical Recruiter',NULL,NULL,'2026-09-21 23:21:34'),(3,3,'Emily','Williams','ewilliams@cloudsystems.com',NULL,'Hiring Manager',NULL,NULL,'2026-09-21 23:21:34'),(4,4,'David','Brown',NULL,NULL,'Senior Developer',NULL,NULL,'2026-09-21 23:21:34'),(5,5,'Lisa','Garcia','lgarcia@smarttech.com',NULL,'Talent Acquisition',NULL,NULL,'2026-09-21 23:21:34'),(7,4,'Robert','Kim','rkim@digitalinnovations.com',NULL,'Engineering Manager',NULL,NULL,'2026-10-03 23:01:38');
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,1,'Software Developer',NULL,70000.00,90000.00,'Full-time',NULL,'2025-01-15',1,'2026-09-21 23:12:54','{\"education\": \"Bachelor in CS or related field\", \"remote_option\": true, \"required_skills\": [\"Python\", \"SQL\", \"Git\"], \"experience_years\": 2, \"preferred_skills\": [\"Flask\", \"Docker\", \"AWS\"]}'),(2,1,'Database Administrator',NULL,75000.00,95000.00,'Full-time',NULL,'2025-01-10',1,'2026-09-21 23:12:54',NULL),(3,2,'Data Analyst',NULL,65000.00,85000.00,'Full-time',NULL,'2025-01-12',1,'2026-09-21 23:12:54','{\"education\": \"Bachelor degree\", \"remote_option\": false, \"required_skills\": [\"SQL\", \"Excel\", \"Tableau\"], \"experience_years\": 1, \"preferred_skills\": [\"Python\", \"R\"]}'),(4,3,'Cloud Engineer',NULL,80000.00,100000.00,'Full-time',NULL,'2025-01-08',1,'2026-09-21 23:12:54',NULL),(5,4,'Junior Developer',NULL,55000.00,70000.00,'Full-time',NULL,'2025-01-14',1,'2026-09-21 23:12:54',NULL),(6,4,'Senior Developer',NULL,95000.00,120000.00,'Full-time',NULL,'2025-01-14',1,'2026-09-21 23:12:54',NULL),(7,5,'ML Engineer',NULL,90000.00,115000.00,'Full-time',NULL,'2025-01-11',1,'2026-09-21 23:12:54',NULL),(8,1,'QA Engineer',NULL,60000.00,80000.00,'Full-time',NULL,'2025-01-05',1,'2026-09-29 03:07:07',NULL),(9,2,'Business Analyst',NULL,65000.00,85000.00,'Full-time',NULL,'2025-01-06',1,'2026-09-29 03:07:07',NULL),(10,2,'Data Scientist',NULL,85000.00,110000.00,'Full-time',NULL,'2025-01-07',1,'2026-09-29 03:07:07',NULL),(11,3,'DevOps Engineer',NULL,80000.00,105000.00,'Full-time',NULL,'2025-01-08',1,'2026-09-29 03:07:07',NULL),(12,3,'Security Analyst',NULL,75000.00,95000.00,'Full-time',NULL,'2025-01-09',1,'2026-09-29 03:07:07',NULL),(13,4,'UI/UX Designer',NULL,60000.00,80000.00,'Full-time',NULL,'2025-01-10',1,'2026-09-29 03:07:07',NULL),(14,5,'Product Manager',NULL,90000.00,120000.00,'Full-time',NULL,'2025-01-11',1,'2026-09-29 03:07:07',NULL),(15,1,'Technical Writer',NULL,55000.00,75000.00,'Contract',NULL,'2025-01-12',1,'2026-09-29 03:07:07',NULL),(16,2,'Intern - Data',NULL,30000.00,40000.00,'Internship',NULL,'2025-01-13',1,'2026-09-29 03:07:07',NULL),(17,4,'Intern - Development',NULL,32000.00,42000.00,'Internship',NULL,'2025-01-14',1,'2026-09-29 03:07:07',NULL),(18,7,'Software Architect',NULL,120000.00,150000.00,'Full-time',NULL,NULL,1,'2026-10-03 22:28:09',NULL);
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-22 20:23:11
