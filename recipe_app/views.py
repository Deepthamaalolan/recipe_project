from django.shortcuts import render
# recipe_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator

from .models import User
from .models import Admin, Recipe
import json
import uuid

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone_number = data.get('phone_number')
        dietary_preferences = data.get('dietary_preferences', [])
        meal_preferences = data.get('meal_preferences', [])
        favorites = data.get('favorites', [])

        if not username or not password or not email:
            return self.json_response({'error': 'Username, password, and email are required'}, status=400)

        all_users = User.objects.all()

        # Print users to the console
        for user in all_users:
            print(f'Username: {user.username}, Email: {user.email}')

        existing_user = User.objects.filter(username=username) or User.objects.filter(email=email)
        if existing_user:
            return self.json_response({'error': 'Username or email already exists'}, status=400)

        hashed_password = make_password(password)
        user_id = str(uuid.uuid4())

        new_user = User.objects.create(
            userId=user_id,
            username=username,
            password=hashed_password,
            email=email,
            phone_number=phone_number,
            dietary_preferences=dietary_preferences,
            meal_preferences=meal_preferences,
            favorites=favorites
        )

        return self.json_response({'message': 'User created successfully'}, status=201)

    def json_response(self, data, status=200):
        return JsonResponse(data, status=status)

    def get_json_data(self, request):
        return request.POST if request.method == 'POST' else {}

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return self.json_response({'error': 'Username and password are required'}, status=400)

        user = User.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            return self.json_response({'message': 'Login successful'}, status=200)
        else:
            return self.json_response({'error': 'Invalid username or password'}, status=401)
    def json_response(self, data, status=200):
        return JsonResponse(data, status=status)

    def get_json_data(self, request):
        return request.POST if request.method == 'POST' else {}
    
@method_decorator(csrf_exempt, name='dispatch')  
class UpdateUserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def put(self, request):
        data = json.loads(request.body.decode('utf-8'))

        user_id = data.get('userId')

        print("user_id", user_id)

        if not user_id:
            return JsonResponse({'error': 'Provide userId for updating'}, status=400)
        
        existing_user = User.objects.filter(userId=str(user_id)).first()
        if not existing_user:
            return JsonResponse({'error': 'User not found'}, status=404)

        excluded_fields = ['username', 'userId', 'email']
        update_data = {key: value for key, value in data.items() if key not in excluded_fields}

        User.objects.filter(userId=str(user_id)).update(**update_data)

        return JsonResponse({'message': 'User information updated successfully'}, status=200)
    
@method_decorator(csrf_exempt, name='dispatch')
class SignupViewAdmin(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        full_name = data.get('full_name')
        phone_number = data.get('phone_number')
        email = data.get('email')

        if not username or not password or not email:
            return self.json_response({'error': 'Admin Username, password, and email are required'}, status=400)

        all_admins = Admin.objects.all()

        for user in all_admins:
            print(f'Username: {user.username}, Email: {user.email}')

        existing_user = Admin.objects.filter(username=username) or Admin.objects.filter(email=email)
        if existing_user:
            return self.json_response({'error': 'Admin Username or email already exists'}, status=400)

        hashed_password = make_password(password)
        admin_id = str(uuid.uuid4())

        new_user = Admin.objects.create(
            admin_id=admin_id,
            username=username,
            password=hashed_password,
            email=email,
            phone_number=phone_number,
            full_name =full_name
        )

        return self.json_response({'message': 'Admin User created successfully'}, status=201)

    def json_response(self, data, status=200):
        return JsonResponse(data, status=status)

    def get_json_data(self, request):
        return request.POST if request.method == 'POST' else {}
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginViewAdmin(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return self.json_response({'error': 'Username and password are required'}, status=400)

        user = Admin.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            return self.json_response({'message': 'Login successful'}, status=200)
        else:
            return self.json_response({'error': 'Invalid username or password'}, status=401)
    def json_response(self, data, status=200):
        return JsonResponse(data, status=status)

    def get_json_data(self, request):
        return request.POST if request.method == 'POST' else {}
    
@method_decorator(csrf_exempt, name='dispatch')  
class UpdateAdminView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def put(self, request):
        data = json.loads(request.body.decode('utf-8'))

        admin_id = data.get('admin_id')

        if not admin_id:
            return JsonResponse({'error': 'Provide userId for updating'}, status=400)
        
        existing_user = Admin.objects.filter(admin_id=str(admin_id)).first()
        if not existing_user:
            return JsonResponse({'error': 'Admin not found'}, status=404)

        excluded_fields = ['username', 'admin_id', 'email']
        update_data = {key: value for key, value in data.items() if key not in excluded_fields}

        Admin.objects.filter(admin_id=str(admin_id)).update(**update_data)

        return JsonResponse({'message': 'Admin information updated successfully'}, status=200)
    
@method_decorator(csrf_exempt, name='dispatch')
class UploadRecipeView(View):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        admin_id = data.get('adminId')
        dish_name = data.get('dishName')
        ingredients = data.get('ingredients', [])
        steps = data.get('steps', [])
        recipe_id = str(uuid.uuid4())

        if not admin_id or not dish_name:
            return JsonResponse({'error': 'AdminId and dishName are required'}, status=400)

        new_recipe = Recipe.objects.create(
            admin_id=admin_id,
            recipe_id=recipe_id,
            dishName=dish_name,
            ingredients=ingredients,
            steps=steps
        )

        return JsonResponse({'message': 'Recipe uploaded successfully'}, status=201)
    

@method_decorator(csrf_exempt, name='dispatch')
class UpdateRecipeView(View):
    def put(self, request):
        data = json.loads(request.body.decode('utf-8'))

        admin_id = data.get('admin_id')
        recipe_id = data.get('recipe_id')
        dish_name = data.get('dishName')
        excluded_fields = ['admin_id', 'recipe_id', 'dishName']  # Add fields you want to exclude from update

        if not admin_id or not recipe_id or not dish_name:
            return JsonResponse({'error': 'AdminId, recipeId, and dishName are required'}, status=400)

        existing_recipe = Recipe.objects.filter(recipe_id=str(recipe_id), admin_id=str(admin_id)).first()

        if not existing_recipe:
            return JsonResponse({'error': 'Recipe not found for the given AdminId and recipeId'}, status=404)

        update_data = {key: value for key, value in data.items() if key not in excluded_fields}

        Recipe.objects.filter(recipe_id=str(recipe_id), admin_id=str(admin_id)).update(**update_data)

        return JsonResponse({'message': 'Recipe information updated successfully'}, status=200)
    

@method_decorator(csrf_exempt, name='dispatch')
class GetUserFavoritesView(View):
    def get(self, request):
        data = json.loads(request.body.decode('utf-8'))

        user_id = data.get('userId')

        if not user_id:
            return JsonResponse({'error': 'User ID not provided in headers'}, status=400)

        user = User.objects.filter(userId=str(user_id)).first()

        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)

        if user:
            favorites = user.favorites

            if favorites:
                return JsonResponse({'favorites': favorites}, status=200)
            else:
                return JsonResponse({'message': 'User has not made any recipe favorite'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class SaveRecipeView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        user_id = data.get('userId')

        if not user_id:
            return JsonResponse({'error': 'User ID not provided in headers'}, status=400)

        user = User.objects.filter(userId=str(user_id)).first()

        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)

        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return JsonResponse({'error': 'Recipe ID not provided in the request'}, status=400)
        
        recipe = Recipe.objects.filter(recipe_id=recipe_id).first()

        if not recipe:
            return JsonResponse({'error': 'Recipe not found'}, status=404)

        if user.favorites is None:
            user.favorites = []
        
        if recipe_id not in user.favorites:
            # Update the User collection using update method
            User.objects.filter(userId=str(user_id)).update(favorites=user.favorites + [recipe_id])
            return JsonResponse({'message': 'Recipe saved to favorites successfully'}, status=201)
        else:
            return JsonResponse({'error': 'Recipe already in favorites'}, status=400)

