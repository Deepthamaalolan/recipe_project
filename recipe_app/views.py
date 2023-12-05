from django.shortcuts import render, get_object_or_404
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
from django.db.models.functions import Concat
from django.db.models import F, Value
from django.db import models


from .models import User
from .models import Admin, Recipe, Conversation
import json
import uuid
import requests

from django.shortcuts import HttpResponse, render
# import requests


# Create your views here.
def home(request):
    context = {'name': 'Web Weavers', 'course' : 'Web Systems'} 
    return render(request,'home.html',context)
def about(request):
    return render(request,'about.html')
#def projects(request):
    #return render(request,'projects.html')
def contact(request):
    return render(request,'contact.html')
#def view_recipe(request):
    #api_url = "https://api.example.com/data"
    
    # Make a request to the API
    #response = requests.get(api_url)
    
    # Check if the request was successful
    #if response.status_code == 200:
    #    data = response.json()
    #else:
    #    data = []

    #return render(request, 'view_recipe.html', {'api_data': data})
def view_recipe(request):
    return render(request,'view_recipe.html')
def user_page(request):
    return render(request,'user_page.html')
def analytics(request):
    return render(request,'analytics.html')
def login(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')
def adminportal(request):
    return render(request,'adminportal.html')
def adminprofile(request):
    return render(request,'adminprofile.html')

@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def post(self, request):
      
        # data = json.loads(request.body.decode('utf-8'))
        # print("data",data)
      
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        print("userId.................", user_id)
        if not user_id:
            return JsonResponse({'error': 'User ID not provided'}, status=400)

        user = get_object_or_404(User, userId=user_id)

        user_details = {
            'userId': user.userId,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'dietary_preferences': user.dietary_preferences,
            'meal_preferences': user.meal_preferences,
            'favorites': user.favorites,
        }

        return JsonResponse(user_details)

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return self.json_response({'error': 'Invalid JSON data'}, status=400)

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone_number = data.get('phone_number')
        dietary_preferences = data.get('dietary_preferences', "-")
        meal_preferences = data.get('meal_preferences', "-")
        # favorites = data.get('favorites', [])

        if not username or not password or not email:
            return self.json_response({'error': 'Username, password, and email are required'}, status=400)

        # Use get() to check for existing user
        existing_user = User.objects.filter(username=username).first() or User.objects.filter(email=email).first()
        if existing_user:
            return self.json_response({'error': 'Username or email already exists'}, status=400)

        hashed_password = make_password(password)
        user_id = str(uuid.uuid4())

        new_user = User(
            userId=user_id,
            username=username,
            password=hashed_password,
            email=email,
            phone_number=phone_number,
            dietary_preferences= dietary_preferences,
            meal_preferences= meal_preferences,
            # favorites= favorites
        )

        new_user.save()

        return self.json_response({'message': 'User created successfully', 'userId': user_id}, status=201)

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
            print("user admin", user.isadmin)
            return self.json_response({'message': 'Login successful', 'userId' : user.userId, 'isadmin': user.isadmin if hasattr(user, 'isadmin') else False}, status=200)
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
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print("data of the user", data)
        user_id = data.get('userId')

        if not user_id:
            return JsonResponse({'error': 'User ID not provided in headers'}, status=400)

        user = User.objects.filter(userId=str(user_id)).first()

        print("user found or not", user)

        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)

        favorites = user.favorites  # Assuming 'favorites' is a related field, use '.all()' to get all related objects

        if favorites:
            return JsonResponse({'favorites': favorites}, status=200)
        else:
            return JsonResponse({'message': 'User has not made any recipe favorite'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class GetRecipeView(View):
    def get(self, request):
        try:
            # Fetch the first 5 recipes from the Recipe model
            recipes = Recipe.objects.all()[:5]

            # Serialize the recipes
            serialized_recipes = []
            for recipe in recipes:
                serialized_recipes.append({
                    "dishName": recipe.dishName,
                    "ingredients": recipe.ingredients,
                    "steps": recipe.steps,
                    "created_at": recipe.created_at
                })

            # Return the serialized recipes in JSON format
            return JsonResponse({'recipes': serialized_recipes}, status=200)

        except Exception as e:
            # Handle exceptions or errors as needed
            return JsonResponse({'error': str(e)}, status=500)
    
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
        
@method_decorator(csrf_exempt, name='dispatch')
class GenerateChatResponseView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        user_id = data.get('userId')

        api_key = ''

        # conversation = data.get('conversation', [])

 
        question = data.get('question')

        print("question.............", question)

        self.save_history(question)

        existing_history = self.fetch_history()

        print("exisitng history........\n\n", existing_history)

        response = self.openai_chat_request(question, api_key, existing_history)

        assistant_reply = response['choices'][0]['message']['content']

        self.save_history(assistant_reply)

        return JsonResponse({'response': assistant_reply})

    def openai_chat_request(self, conversation, api_key, previous_conv):
        api_url = 'https://api.openai.com/v1/chat/completions'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }

        messages =[]

        messages.append({"role": "system", "content" :"You are a helpful assistant specializing in providing personalized cooking recipes. The user will provide specific ingredients along with their dietary preferences and meal preferences. Based on this information, you are tasked with recommending delicious recipes tailored to the user's preferences. For example, the user might say: What's a healthy recipe for dinner with chicken, broccoli, and quinoa? I prefer gluten-free options. Your responses should take into account the provided ingredients, the user's dietary preferences (such as gluten-free), and their meal preferences (e.g., dinner). Feel free to ask for clarification or additional details to ensure the recipes align perfectly with the user's needs. I will attach previous conversation as well." })

        # messages.append({"role": "system", "content": })
        for i in previous_conv:
            messages.append(i)

        # messages.append({"role": "user", "content": conversation})

        print("messages..................\n\n", messages)
        data = {
            'messages': messages,
            'model':'gpt-3.5-turbo-16k-0613'
        }

        response = requests.post(api_url, headers=headers, json=data)

        print("response from openAI", response.status_code, response.json())

        return response.json()
    
    def fetch_history(self):
        # Fetch all conversation history
        all_conversations = Conversation.objects.all()

        # Format messages alternatively
        formatted_messages = []
        for i, conversation in enumerate(all_conversations):
            role = 'user' if i % 2 == 0 else 'assistant'
            formatted_messages.append({'role': role, 'content': conversation.messages})

        return formatted_messages

    def save_history(self, new_message):
        # Create a new document for each message
        Conversation.objects.create(messages=new_message)