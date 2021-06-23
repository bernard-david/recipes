from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_30)s, %(user_id)s);"
        return connectToMySQL('recipes_schema').query_db( query, data )
    
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('recipes_schema').query_db(query)

        recipes = []

        for result in results:
            recipe = cls(result)
            user_data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            recipe.user_id = User(user_data)
            recipes.append(recipe)

        return recipes

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)

        if len(results) == 0:
            print("No recipe with that id.")
            return False
        
        else:
            result = results[0]
            recipe = cls(result)
            user_data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
            recipe.user_id = User(user_data)
            return recipe

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date=%(date)s, under_30=%(under_30)s  WHERE id = %(recipe_id)s;"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 3:
            is_valid = False
            flash("Name of recipe must be at least 3 characters long.")

        if len(data['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters long.")

        if len(data['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters long.")

        if not data['date']:
            is_valid = False
            flash("Please select a date.")

        return is_valid
    