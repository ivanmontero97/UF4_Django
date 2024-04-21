from django.urls import path
from MostrarDatosAlumnoProfesor import views

urlpatterns = [
    path('',views.index, name='index'),
    #Practica 1 a partir de aqui :
    path('centre/students/',views.getStudents, name ="students"),
    path('centre/student/<int:id>',views.getStudent, name ="student"),
    path('centre/teachers/',views.getTeachers, name="teachers"),
    path('centre/teachers/<int:id>/',views.getTeacher,name='teacher')

]