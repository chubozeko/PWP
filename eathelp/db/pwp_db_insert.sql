USE pwp_db;

INSERT INTO user (username) VALUES 
	('graham_norton'),
    ('harald_kumar'), 
    ('clark_kent'), 
    ('dr_steven_strange'), 
    ('optimus_prime')
    AS new_entries
ON DUPLICATE KEY UPDATE 
	username = new_entries.username;
    
INSERT INTO ingredient (name) VALUES 
	('Potato'),
    ('Egg'),
    ('Mayonnaise'),
    ('Milk'),
    ('Butter'),
    ('Salt'),
    ('Aromat Spice (Chilli Beef)'),
    ('Gingerbread Spice'),
    ('Sugar'),
    ('Beef Mince'),
    ('Onion'),
    ('Carrot'),
    ('Beans'),
    ('Garlic Paste'),
    ('Frozen Vegetables'),
    ('Corn Starch'),
    ('Beef Stock'),
    ('Grill Spice'),
    ('Tomato Sauce'),
    ('Tomato'),
    ('Sunflower Oil'),
    ('Black Pepper')
    AS new_entries
ON DUPLICATE KEY UPDATE 
	name = new_entries.name;

INSERT INTO recipe (recipe_name, prep_time, cooking_time, meal_type, calories, servings, creator_id, instructions) VALUES 
	('Mash', 10, 20, 'non-vegetarian', 780, 1, 1, 
    '1. Peel the potatoes and boil them for 20 minutes, or until they are soft. 
    2. Boil the eggs for 15 minutes.
    3. Mash the potatoes and put them in a bowl.
    4. Add the butter, milk and gingerbread spice to the mashed potatoes and mix them well.
    5. Mash the eggs and add the salt, black pepper and Aromat spice.
    6. Add the mashed eggs to the mashed potatoes and mix them well.
    7. Add the mayonnaise and sugar to the bowl and mix them well.
    8. Warm up the mash in the microwave if you wish to have it hot.'
    ),
    ('Minced Meat with Beans and Vegetables', 15, 20, 'non-vegetarian', 1265, 3, 2, 
    '1. Cut the onion into smaller pieces.
    2. Peel and grate the carrot.
    3. Grate the tomato to use for the sauce.
    4. Warm up the frozen vegetables.
    5. Create a spice mix by blending the salt, black pepper, Aromat chilli beef spice and grill spice.
    6. Add the oil to a pan over medium-high heat. Once the pan is hot, add the beef and cook it until it browns.
    7. Add the spice mix to the mince and stir it for a minute.
    8. Add the onion and garlic to the pan and allow it to cook for about a minute.
    9. Add the grated carrot to the pan and let it cook for another minute. Next, add the vegetables and beans to the pan and continue to stir and cook them for about 2 minutes.
    10. Reduce the heat to medium and start creating the sauce by adding the grated tomato, tomato sauce and crushed beef stock cube to the pan. Let it bubble for 2 minutes while gradually add some boiled water and corn starch to change the thickness of the sauce.
    11. Let it cook for another 3-5 minutes, or until the sauce is reduced and all the ingredients have fully cooked. Serve with pasta or rice.'
    )
    AS new_entries
ON DUPLICATE KEY UPDATE 
    recipe_name = new_entries.recipe_name,
    prep_time = new_entries.prep_time,
    cooking_time = new_entries.cooking_time,
    meal_type = new_entries.meal_type,
    calories = new_entries.calories,
    servings = new_entries.servings,
    creator_id = new_entries.creator_id,
    instructions = new_entries.instructions;
    
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

INSERT INTO cookbook (name, description, user_id) VALUES 
	('Showtime Cookbook', 'My favorite meals to eat before I go to work.', 1),
    ('Super Meals', 'Recipes for busy Superheroes', 3),
    ('Cookbook for Autobots', 'Meals that are out of this world.', 5)
    AS new_entries
ON DUPLICATE KEY UPDATE 
	name = new_entries.name,
    description = new_entries.description,
	user_id = new_entries.user_id;

INSERT INTO collections (cookbook_id, recipe_id) VALUES 
	(1, 1),
    (2, 1),
    (2, 2),
    (3, 2)
    AS new_entries
ON DUPLICATE KEY UPDATE 
	cookbook_id = new_entries.cookbook_id,
	recipe_id = new_entries.recipe_id;
    
-- INSERT INTO table1 (col1, col2) VALUES 
-- 	(''),(''),(''),(''),(''),(''),('')
--     AS new_entries
-- ON DUPLICATE KEY UPDATE 
-- 	col1 = new_entries.col1,
-- 	col2 = new_entries.col2
-- ;