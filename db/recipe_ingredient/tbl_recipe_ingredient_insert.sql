USE `pwp_db`;

INSERT INTO recipe_ingredient (recipe_id, ingredient_id, amount, unit) VALUES
	(1, 1, 0.5,''),
    (1, 2, 3,''),
    (1, 3, 2,'TABLESPOON'),
    (1, 4, 1,'TABLESPOON'),
    (1, 5, 0.5,'TEASPOON'),
    (1, 6, 0.25,'TEASPOON'),
    (1, 22, 0.25,'TEASPOON'),
    (1, 7, 0.25,'TEASPOON'),
    (1, 8, 0.25,'TEASPOON'),
    (1, 9, 1,'TABLESPOON'),
    (2, 10, 200,'GRAMS'),
    (2, 11, 0.5,''),
    (2, 12, 1,''),
    (2, 13, 100,'GRAMS'),
    (2, 14, 0.5,'TEASPOON'),
    (2, 15, 100,'GRAMS'),
    (2, 16, 1,'TABLESPOON'),
    (2, 17, 10,'GRAMS'),
    (2, 6, 0.5,'TEASPOON'),
    (2, 22, 0.5,'TEASPOON'),
    (2, 7, 0.5,'TEASPOON'),
    (2, 18, 0.5,'TEASPOON'),
    (2, 19, 0.5,'CUP'),
    (2, 20, 1,''),
    (2, 21, 1,'TABLESPOON')
    AS new_entries
ON DUPLICATE KEY UPDATE
	recipe_id = new_entries.recipe_id,
    ingredient_id = new_entries.ingredient_id,
    amount = new_entries.amount,
	unit = new_entries.unit;