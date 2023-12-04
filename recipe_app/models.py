from django.db import models
from django.contrib.postgres.fields import ArrayField
import json

class User(models.Model):
    userId = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dietary_preferences = ArrayField(models.CharField(max_length=255), default=list)
    meal_preferences = ArrayField(models.CharField(max_length=255), default=list)
    favorites = ArrayField(models.CharField(max_length=255), default=list)

    def save(self, *args, **kwargs):
        # Call the original save method to save the user
        super().save(*args, **kwargs)

        # Convert lists to strings before saving to MongoDB
        self.dietary_preferences = json.dumps(self.dietary_preferences)
        self.meal_preferences = json.dumps(self.meal_preferences)
        self.favorites = json.dumps(self.favorites)

        # Convert strings back to lists after saving
        if self.dietary_preferences:
            self.dietary_preferences = json.loads(self.dietary_preferences)
        if self.meal_preferences:
            self.meal_preferences = json.loads(self.meal_preferences)
        if self.favorites:
            self.favorites = json.loads(self.favorites)

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

