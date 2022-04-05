USE `pwp_db`;

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