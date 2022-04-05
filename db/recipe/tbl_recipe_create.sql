USE `pwp_db`;

DROP TABLE IF EXISTS `recipe`;
CREATE TABLE IF NOT EXISTS `recipe` (
    `recipe_id` INT NOT NULL AUTO_INCREMENT,
    `recipe_name` VARCHAR(50) NOT NULL,
    `prep_time` INT NOT NULL,
    `cooking_time` INT NOT NULL,
    `meal_type` ENUM ('vegetarian', 'non-vegetarian') NOT NULL,
    `calories` VARCHAR(50) NOT NULL,
    `servings` VARCHAR(50) NOT NULL,
    `instructions` VARCHAR(500) NOT NULL,
    `creator_id` INT NOT NULL,
    PRIMARY KEY (`recipe_id`),
    CONSTRAINT `fk_r_user_id` FOREIGN KEY (`creator_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);
