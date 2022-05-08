USE `pwp_db`;

DROP TABLE IF EXISTS `cookbook`;
CREATE TABLE IF NOT EXISTS `cookbook` (
    `cookbook_id` int NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `description` VARCHAR(200) NOT NULL,
    `user_id` INT NOT NULL,
    PRIMARY KEY (`cookbook_id`),
    CONSTRAINT `fk_cb_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);