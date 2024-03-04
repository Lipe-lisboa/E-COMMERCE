from django.urls import path 
from perfil.views import views_perfil

app_name = "perfil"
urlpatterns = [
    path('',views_perfil.Criar.as_view(), name='criar'),
    path('atualizar/',views_perfil.Criar.as_view(), name='atualizar'),
    path('login/',views_perfil.Login.as_view() ,name='login'),
    path('logout/',views_perfil.Logout.as_view() , name='logout')
]
