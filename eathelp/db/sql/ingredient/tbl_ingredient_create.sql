USE `pwp_db`;

DROP TABLE IF EXISTS `ingredient`;
CREATE TABLE IF NOT EXISTS `ingredient` (
	`ingredient_id` INT NOT NULL auto_increment,
    `name` NVARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (`ingredient_id`)
);