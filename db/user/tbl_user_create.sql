USE `pwp_db`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
	`user_id` INT NOT NULL auto_increment,
    `username` NVARCHAR(255) NOT NULL,
    PRIMARY KEY (`user_id`)
);