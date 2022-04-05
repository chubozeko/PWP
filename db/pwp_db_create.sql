CREATE DATABASE IF NOT EXISTS `pwp_db`;
USE `pwp_db`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
	`user_id` INT NOT NULL auto_increment,
    `username` NVARCHAR(255) NOT NULL,
    PRIMARY KEY (`user_id`)
);

DROP TABLE IF EXISTS `ingredient`;
CREATE TABLE IF NOT EXISTS `ingredient` (
	`ingredient_id` INT NOT NULL auto_increment,
    `name` NVARCHAR(255) NOT NULL,
    PRIMARY KEY (`ingredient_id`)
);

DROP TABLE IF EXISTS `recipe`;
CREATE TABLE IF NOT EXISTS `recipe` (
    `recipe_id` INT NOT NULL AUTO_INCREMENT,
    `recipe_name` VARCHAR(50) NOT NULL,
    `prep_time` INT NOT NULL,
    `cooking_time` INT NOT NULL,
    `meal_type` ENUM ('vegetarian', 'non-vegetarian') NOT NULL,
    `calories` INT NOT NULL,
    `servings` INT NOT NULL,
    `instructions` VARCHAR(2000) NOT NULL,
    `creator_id` INT NOT NULL,
    PRIMARY KEY (`recipe_id`),
    CONSTRAINT `fk_r_user_id` FOREIGN KEY (`creator_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS `recipe_ingredient`;
CREATE TABLE IF NOT EXISTS `recipe_ingredient` (
	`rec_ing_id` INT NOT NULL auto_increment,
    `recipe_id` INT NOT NULL,
    `ingredient_id` INT NOT NULL,
    `amount` DOUBLE NOT NULL,
	`unit` NVARCHAR(255) NOT NULL,
    PRIMARY KEY (`rec_ing_id`),
    CONSTRAINT fk_ri_ingredient_id FOREIGN KEY (`ingredient_id`) references ingredient(`ingredient_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ri_recipe_id FOREIGN KEY (`recipe_id`) REFERENCES recipe(`recipe_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS `cookbook`;
CREATE TABLE IF NOT EXISTS `cookbook` (
    `cookbook_id` int NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `description` VARCHAR(200) NOT NULL,
    `user_id` INT NOT NULL,
    PRIMARY KEY (`cookbook_id`),
    CONSTRAINT `fk_cb_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS `collections`;
CREATE TABLE IF NOT EXISTS `collections` (
    `cookbook_id` int NOT NULL,
    `recipe_id` INT NOT NULL,
    CONSTRAINT `fk_col_cookbook_id` FOREIGN KEY (`cookbook_id`) REFERENCES `cookbook` (`cookbook_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_col_recipe_id` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

-- SET foreign_key_checks = 0;
-- SET foreign_key_checks = 1;