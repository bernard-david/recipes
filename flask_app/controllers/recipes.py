from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/recipes/new")
def new_recipe():
    if "user_id" in session:
        return render_template("create_recipe.html")
    
    flash("You need to log in before creating a recipe!")
    return redirect("/")

@app.route("/recipes/create", methods=["POST"])
def create_recipe():
    if not "user_id" in session:
        flash("You must login first!")
        return redirect("/")

    if Recipe.validate_recipe(request.form):
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date": request.form["date"],
            "under_30": request.form["under_30"],
            "user_id": session["user_id"]
        }
        Recipe.create(data)
        print("SUCCESS!!!!")
        return redirect("/dashboard")
    print("FAILED!!!!")
    return redirect("/recipes/new")

@app.route("/recipes/<int:recipe_id>")
def one_recipe(recipe_id):
    if not "user_id" in session:
        flash("You must login first!")
        return redirect("/")

    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)

    if recipe == False:
        return redirect("/dashboard")
    
    return render_template("show_recipe.html", recipe = recipe)

@app.route("/recipes/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    if not "user_id" in session:
        flash("You must login first!")
        return redirect("/")

    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)

    if recipe == False:
        return redirect('/dashboard')
    if recipe.user_id.id != session['user_id']:
        return redirect('/dashboard')


    return render_template("edit_recipe.html", recipe = recipe)

@app.route("/recipes/<int:recipe_id>/update", methods=["POST"])
def update_recipe(recipe_id):
    print("I MADE IT TO THE ROUTE")
    if Recipe.validate_recipe(request.form):
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date": request.form["date"],
            "under_30": request.form["under_30"],
            "recipe_id": recipe_id
        }
        Recipe.update_recipe(data)
        print("SUCCESS")
        return redirect("/dashboard")
    print("FAIL")
    return redirect(f"/recipes/{recipe_id}/edit")

@app.route("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)

    if recipe == False:
        return redirect('/dashboard')
    if recipe.user_id.id != session['user_id']:
        return redirect('/dashboard')

    Recipe.delete_recipe(data)
    return redirect('/dashboard')