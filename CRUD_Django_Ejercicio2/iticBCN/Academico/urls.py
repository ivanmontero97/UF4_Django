from django.urls import path
from Academico import views
from django.contrib import admin
from Academico.views import *

urlpatterns = [
    path('',FormListView.as_view(),name='gestion_usuarios'),
    path('centre/students/',StudentsView.as_view(), name ="students"),
    path('centre/teachers/',TeachersView.as_view(), name="teachers"),
    path('centre/editUser/<int:pk>', views.editSubjects, name ="edit"),
    path('creacionUsuario',views.processUserCreation, name="creacionUsuario"),
    path('delete/user/<int:pk>',views.deleteUser,name="deleteUser"),
    path('update/user/<int:pk>',views.updateUser,name="updateUser"),
    path('delete/user/<int:pk>/subject/<int:pkSubject>', views.deleteRelationalSubject, name="deleteRelationalSubject"),
    path('add/user/<int:pk>/subject/<int:pkSubject>', views.addRelationalSubject, name="addRelationalSubject")
]