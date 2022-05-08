USE `pwp_db`;

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