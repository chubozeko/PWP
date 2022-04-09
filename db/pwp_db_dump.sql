-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: pwp_db
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `collections`
--

DROP TABLE IF EXISTS `collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collections` (
  `cookbook_id` int NOT NULL,
  `recipe_id` int NOT NULL,
  KEY `fk_col_cookbook_id` (`cookbook_id`),
  KEY `fk_col_recipe_id` (`recipe_id`),
  CONSTRAINT `fk_col_cookbook_id` FOREIGN KEY (`cookbook_id`) REFERENCES `cookbook` (`cookbook_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_col_recipe_id` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collections`
--

LOCK TABLES `collections` WRITE;
/*!40000 ALTER TABLE `collections` DISABLE KEYS */;
INSERT INTO `collections` VALUES (1,1),(2,1),(2,2),(3,2);
/*!40000 ALTER TABLE `collections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cookbook`
--

DROP TABLE IF EXISTS `cookbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cookbook` (
  `cookbook_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(200) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`cookbook_id`),
  KEY `fk_cb_user_id` (`user_id`),
  CONSTRAINT `fk_cb_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cookbook`
--

LOCK TABLES `cookbook` WRITE;
/*!40000 ALTER TABLE `cookbook` DISABLE KEYS */;
INSERT INTO `cookbook` VALUES (1,'Showtime Cookbook','My favorite meals to eat before I go to work.',1),(2,'Super Meals','Recipes for busy Superheroes',3),(3,'Cookbook for Autobots','Meals that are out of this world.',5);
/*!40000 ALTER TABLE `cookbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredient`
--

DROP TABLE IF EXISTS `ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredient` (
  `ingredient_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient`
--

LOCK TABLES `ingredient` WRITE;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
INSERT INTO `ingredient` VALUES (1,'Potato'),(2,'Egg'),(3,'Mayonnaise'),(4,'Milk'),(5,'Butter'),(6,'Salt'),(7,'Aromat Spice (Chilli Beef)'),(8,'Gingerbread Spice'),(9,'Sugar'),(10,'Beef Mince'),(11,'Onion'),(12,'Carrot'),(13,'Beans'),(14,'Garlic Paste'),(15,'Frozen Vegetables'),(16,'Corn Starch'),(17,'Beef Stock'),(18,'Grill Spice'),(19,'Tomato Sauce'),(20,'Tomato'),(21,'Sunflower Oil'),(22,'Black Pepper');
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe`
--

DROP TABLE IF EXISTS `recipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe` (
  `recipe_id` int NOT NULL AUTO_INCREMENT,
  `recipe_name` varchar(50) NOT NULL,
  `prep_time` int NOT NULL,
  `cooking_time` int NOT NULL,
  `meal_type` enum('vegetarian','non-vegetarian') NOT NULL,
  `calories` int NOT NULL,
  `servings` int NOT NULL,
  `instructions` varchar(2000) NOT NULL,
  `creator_id` int NOT NULL,
  PRIMARY KEY (`recipe_id`),
  KEY `fk_r_user_id` (`creator_id`),
  CONSTRAINT `fk_r_user_id` FOREIGN KEY (`creator_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe`
--

LOCK TABLES `recipe` WRITE;
/*!40000 ALTER TABLE `recipe` DISABLE KEYS */;
INSERT INTO `recipe` VALUES (1,'Mash',10,20,'non-vegetarian',780,1,'1. Peel the potatoes and boil them for 20 minutes, or until they are soft. \n    2. Boil the eggs for 15 minutes.\n    3. Mash the potatoes and put them in a bowl.\n    4. Add the butter, milk and gingerbread spice to the mashed potatoes and mix them well.\n    5. Mash the eggs and add the salt, black pepper and Aromat spice.\n    6. Add the mashed eggs to the mashed potatoes and mix them well.\n    7. Add the mayonnaise and sugar to the bowl and mix them well.\n    8. Warm up the mash in the microwave if you wish to have it hot.',1),(2,'Minced Meat with Beans and Vegetables',15,20,'non-vegetarian',1265,3,'1. Cut the onion into smaller pieces.\n    2. Peel and grate the carrot.\n    3. Grate the tomato to use for the sauce.\n    4. Warm up the frozen vegetables.\n    5. Create a spice mix by blending the salt, black pepper, Aromat chilli beef spice and grill spice.\n    6. Add the oil to a pan over medium-high heat. Once the pan is hot, add the beef and cook it until it browns.\n    7. Add the spice mix to the mince and stir it for a minute.\n    8. Add the onion and garlic to the pan and allow it to cook for about a minute.\n    9. Add the grated carrot to the pan and let it cook for another minute. Next, add the vegetables and beans to the pan and continue to stir and cook them for about 2 minutes.\n    10. Reduce the heat to medium and start creating the sauce by adding the grated tomato, tomato sauce and crushed beef stock cube to the pan. Let it bubble for 2 minutes while gradually add some boiled water and corn starch to change the thickness of the sauce.\n    11. Let it cook for another 3-5 minutes, or until the sauce is reduced and all the ingredients have fully cooked. Serve with pasta or rice.',2);
/*!40000 ALTER TABLE `recipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe_ingredient`
--

DROP TABLE IF EXISTS `recipe_ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe_ingredient` (
  `rec_ing_id` int NOT NULL AUTO_INCREMENT,
  `recipe_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  `amount` double NOT NULL,
  `unit` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`rec_ing_id`),
  KEY `fk_ri_ingredient_id` (`ingredient_id`),
  KEY `fk_ri_recipe_id` (`recipe_id`),
  CONSTRAINT `fk_ri_ingredient_id` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`ingredient_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_ri_recipe_id` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe_ingredient`
--

LOCK TABLES `recipe_ingredient` WRITE;
/*!40000 ALTER TABLE `recipe_ingredient` DISABLE KEYS */;
INSERT INTO `recipe_ingredient` VALUES (1,1,1,0.5,''),(2,1,2,3,''),(3,1,3,2,'TABLESPOON'),(4,1,4,1,'TABLESPOON'),(5,1,5,0.5,'TEASPOON'),(6,1,6,0.25,'TEASPOON'),(7,1,22,0.25,'TEASPOON'),(8,1,7,0.25,'TEASPOON'),(9,1,8,0.25,'TEASPOON'),(10,1,9,1,'TABLESPOON'),(11,2,10,200,'GRAMS'),(12,2,11,0.5,''),(13,2,12,1,''),(14,2,13,100,'GRAMS'),(15,2,14,0.5,'TEASPOON'),(16,2,15,100,'GRAMS'),(17,2,16,1,'TABLESPOON'),(18,2,17,10,'GRAMS'),(19,2,6,0.5,'TEASPOON'),(20,2,22,0.5,'TEASPOON'),(21,2,7,0.5,'TEASPOON'),(22,2,18,0.5,'TEASPOON'),(23,2,19,0.5,'CUP'),(24,2,20,1,''),(25,2,21,1,'TABLESPOON');
/*!40000 ALTER TABLE `recipe_ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'graham_norton'),(2,'harald_kumar'),(3,'clark_kent'),(4,'dr_steven_strange'),(5,'optimus_prime');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-05 21:16:42
