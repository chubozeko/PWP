USE `pwp_db`;

DROP TABLE IF EXISTS `cookbook_recipes`;
CREATE TABLE IF NOT EXISTS `cookbook_recipes` (
    `cookbook_id` int NOT NULL,
    `recipe_id` INT NOT NULL,
--    PRIMARY KEY (`col_id`)
    CONSTRAINT `fk_col_cookbook_id` FOREIGN KEY (`cookbook_id`) REFERENCES `cookbook` (`cookbook_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_col_recipe_id` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`recipe_id`) ON DELETE CASCADE ON UPDATE CASCADE
);