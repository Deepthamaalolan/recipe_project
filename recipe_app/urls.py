# recipe_app/urls.py
from django.urls import path

from recipe_app import views
from .views import SignupView, LoginView, UpdateUserView, SignupViewAdmin, LoginViewAdmin, UpdateAdminView, UploadRecipeView, UpdateRecipeView,GetUserFavoritesView, SaveRecipeView, GenerateChatResponseView, home, about, contact, view_recipe, user_page, analytics, UserView, GetRecipeView
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('update_user/', UpdateUserView.as_view(), name='update_user'),
    path('admin/signup/', SignupViewAdmin.as_view(), name='admin_signup'),
    path('admin/login/', LoginViewAdmin.as_view(), name='admin_login'),
    path('admin/update_info/', UpdateAdminView.as_view(), name='admin_update_info'),
    path('admin/upload_recipe/', UploadRecipeView.as_view(), name='admin_upload_recipe'),
    path('admin/update_recipe/', UpdateRecipeView.as_view(), name='admin_update_recipe'),
    path('user/save_recipe/', SaveRecipeView.as_view(), name='user_save_recipe'),
    path('user/favorites/', GetUserFavoritesView.as_view(), name='get_user_fav'),
    path('generate_chat_response/', GenerateChatResponseView.as_view(), name='generate_chat_response'),
    path('home/', home, name='home'),
    path('user_profile/', UserView.as_view(), name = "user_profile"),
    path('view_recipe/', GetRecipeView.as_view(), name = "view_recipe"),
    path('about/', about, name='about'),
    #path('projects', views.projects, name='projects'),
    path('contact/', contact, name='contact'),
    path('view_recipe', view_recipe, name='view_recipe'),
    path('user_page/', user_page, name='user_page'),
    path('analytics/', analytics, name='analytics')
]
