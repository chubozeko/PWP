USE `pwp_db`;

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
