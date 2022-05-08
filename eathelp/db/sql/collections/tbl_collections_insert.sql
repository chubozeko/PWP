USE `pwp_db`;

INSERT INTO collections (cookbook_id, recipe_id) VALUES
	(1, 1),
    (2, 1),
    (2, 2),
    (3, 2)
    AS new_entries
ON DUPLICATE KEY UPDATE
	cookbook_id = new_entries.cookbook_id,
	recipe_id = new_entries.recipe_id;