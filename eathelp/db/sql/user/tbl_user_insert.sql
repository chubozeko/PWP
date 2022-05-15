USE `pwp_db`;

INSERT INTO user (username) VALUES
	('graham_norton'),
    ('harald_kumar'),
    ('clark_kent'),
    ('dr_steven_strange'),
    ('optimus_prime')
    AS new_entries
ON DUPLICATE KEY UPDATE
	username = new_entries.username;