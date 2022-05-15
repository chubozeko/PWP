USE `pwp_db`;

INSERT INTO cookbook (name, description, user_id) VALUES
	('Showtime Cookbook', 'My favorite meals to eat before I go to work.', 1),
    ('Super Meals', 'Recipes for busy Superheroes', 3),
    ('Cookbook for Autobots', 'Meals that are out of this world.', 5)
    AS new_entries
ON DUPLICATE KEY UPDATE
	name = new_entries.name,
    description = new_entries.description,
	user_id = new_entries.user_id;