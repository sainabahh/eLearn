from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash_screen, name='splash'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('course_list/', views.course_list_view, name='course_list'),  
    path('select_course/', views.select_course, name='select_course'),
    path('video/<int:video_id>/', views.video_screen, name='video_screen'),
]
