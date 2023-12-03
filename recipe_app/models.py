from django.db import models

class User(models.Model):
    userId = models.CharField(max_length=100, unique=True)  # Assuming 36 is the length of your UUID strings
    username = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dietary_preferences = models.JSONField(default=list)
    meal_preferences = models.JSONField(default=list)
    favorites = models.JSONField(default=list)

class Admin(models.Model):
    admin_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

class Recipe(models.Model):
    admin_id = models.CharField(max_length=255)
    recipe_id = models.CharField(max_length=100, unique=True)
    dishName = models.CharField(max_length=255)
    ingredients = models.JSONField(default=list)
    steps = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    conversation_id = models.CharField(max_length=255)
    userId = models.CharField(max_length=100, unique=True)
    messages = models.JSONField(default=list)

