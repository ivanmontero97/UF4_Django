from django.http import HttpResponse 
from django.shortcuts import render
from django.template import loader
# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

# Practica 1 a partir de aqui :

#Array estudiantes
students= [
        {"id":1, "nombre":"Paco" , "apellido":"Romero","edad":15,"rol":"Student","curso":"DAW2A"},
        {"id":2, "nombre":"Luis" , "apellido":"Arena","edad":19,"rol":"Student","curso":"DAW2B"},
        {"id":3, "nombre":"Marta" , "apellido":"Playa","edad":20,"rol":"Student","curso":"DAW2C"},
        {"id":4, "nombre":"Julia" , "apellido":"Carol","edad":21,"rol":"Student","curso":"DAW2A"},
        {"id":5, "nombre":"Smithers" , "apellido":"Puertas","edad":34,"rol":"Student","curso":"DAW2A"}
        ]
def getStudents(request):
    return render(request,'students.html',{"students":students})
def getStudent(request,id):
    students_obj = None
    for x in students:
        if x["id"]==id:
            students_obj=x
    return render(request,'student.html',{'student':students_obj})

#Array profesores
teachers= [
        {"id":1, "nombre":"Robert" , "apellido":"Deniro","edad":41,"rol":"Profesor","curso":"DAW2A"},
        {"id":2, "nombre":"Campi" , "apellido":"Ñon","edad":91,"rol":"Profesor","curso":"DAW2B"},
        {"id":3, "nombre":"Elver" , "apellido":"Sinto","edad":24,"rol":"Profesor","curso":"DAW2C"},
        {"id":4, "nombre":"Julia" , "apellido":"Roberts","edad":54,"rol":"Profesor","curso":"DAW2A"},
        {"id":5, "nombre":"Alejandro" , "apellido":"Sanz","edad":43,"rol":"Profesor","curso":"DAW2A"},
    ]
#Funciones del array profesor
def getTeachers(request):
    return render(request,'teachers.html',{"teachers":teachers})
def getTeacher(request,id):
    teacher_obj = None
    for x in teachers:
        if x["id"]==id:
            teacher_obj=x
    return render(request,'teacher.html',{'profesor':teacher_obj})