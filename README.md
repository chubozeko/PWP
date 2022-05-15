# PWP SPRING 2022
# PROJECT NAME
# Group information
* Student 1. Chubo Zeko (czeko21@student.oulu.fi)
* Student 2. David Ochia (dochia21@student.oulu.fi)
* Student 3. Hamza Abdalla (habdalla20@student.oulu.fi)
* Student 4. Sehrish Khan (Sehrish.-@student.oulu.fi)

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

---
# Project Layout
Last updated: 10/05/2022

```
PWP/
├── home.md
├── meetings.md
├── README.md
├── requirements.txt
├── setup.py
├── eathelp/ 
│   ├── __init__.py
│   ├── api.py
│   ├── models.py
│   ├── README.md
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── cookbook.py
│   │   ├── ingredient.py
│   │   ├── recipe.py
│   │   └── recipe_ingredient.py
│   ├── db/
│   │   ├── load_database.py
│   │   ├── pwp_db_create.sql
│   │   ├── pwp_db_insert.sql
│   │   ├── README.md
│   │   └── sql/
│   │       ├── pwp_db_dump.sql
│   │       ├── collections/
│   │       │   ├── tbl_collections_create.sql
│   │       │   └── tbl_collections_insert.sql
│   │       ├── cookbook/
│   │       │   ├── tbl_cookbook_create.sql
│   │       │   └── tbl_cookbook_insert.sql
│   │       ├── ingredient/
│   │       │   ├── tbl_ingredient_create.sql
│   │       │   └── tbl_ingredient_insert.sql
│   │       ├── recipe/
│   │       │   ├── tbl_recipe_create.sql
│   │       │   └── tbl_recipe_insert.sql
│   │       ├── recipe-ingredient/
│   │       │   ├── tbl_recipe_ingredient_create.sql
│   │       │   └── tbl_recipe_ingredient_insert.sql
│   │       └── user/
│   │           ├── tbl_user_create.sql
│   │           └── tbl_user_insert.sql
│   └── static/
├── tests/
│   ├── README.md
│   └── dummy_data/
│       └── requests/
│           ├── request_recipe_0.json
│           ├── request_recipe_1.json
│           ├── request_recipe_2.json
│           └── request_recipe_3.json
└── client/
    └── README.md
```

