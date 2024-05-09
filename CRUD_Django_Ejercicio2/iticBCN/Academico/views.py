from django.http import HttpResponse 
from django.shortcuts import render,redirect
from django.template import loader
from Academico.models import *
from django.views.generic import ListView #Es necesario importar esto para las vistas basadas

#Este ejercicio lo haremos con vistas basadas en modelos

#En el caso de vistas basadas en clases, generalmente se elige un modelo principal para la vista 
#y se agregan datos adicionales de otros modelos al contexto según sea necesario.
class FormListView(ListView):
    model=Subject #Lo primero será indicar el modelo en el que se va a basar la vista
    template_name='form.html' #La plantilla a renderizar

    # def get_queryset(self): #Elegimos que datos queremos enviarle del modelo
    #     return Subject.objects.all()
    #Para enviar información adicional y no solamente el modelo Subject se debe utilizar get_context_data
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs) #Es un diccionario con todos los datos que se estan enviando a la pagina
        #Como es un diccionario podemos pasarles datos.
        context['roles']=Rol.objects.all()
        return context
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    rol = user.rol.id
    user.delete()  # Usar user.delete() para eliminar el usuario
    if rol == 1:
        return redirect('teachers')
    return redirect('students')
 
def updateUser(request, pk):
    # Obtener el usuario que se desea actualizar
    user = User.objects.get(id=pk)
    
    user.name = request.POST['nombre']
    user.surname = request.POST['apellido']
    user.rol_id = request.POST['rol']
    user.save()

    if(user.rol == 1):
        return redirect('students')
    return redirect('teachers')
    
def processUserCreation(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        rolSelected = request.POST['rol']

        asignaturas_seleccionadas = []
        for key, value in request.POST.items():
            if key.startswith('subject_'):
                asignatura_id = value  # Obtenemos el ID de la asignatura del nombre del checkbox
                asignaturas_seleccionadas.append(int(asignatura_id))

        rolObject = Rol.objects.get(id=rolSelected)
        usuario = User.objects.create(name=nombre, surname=apellido, rol=rolObject)

        for subject_id in asignaturas_seleccionadas:
            subject = Subject.objects.get(id=subject_id)
            relationalUserSubject.objects.create(user=usuario, subject_id=subject_id)

        if usuario.rol_id == 2:
            return redirect('centre/students/')
        else:
            return redirect('centre/teachers/')



class StudentsView(ListView):
    model=User 
    template_name='students.html'
    def get_queryset(self): 
        return User.objects.filter(rol=2) #Filtramos por solo aquellos que sean estudiantes (1 id del rol estudiante)
 
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs) #Es un diccionario con todos los datos que se estan enviando a la pagina
        #Como es un diccionario podemos pasarles datos.
        students = User.objects.filter(rol=2)
        context['subjectsByUser']=relationalUserSubject.objects.filter(user_id__in=students)
        return context

class TeachersView(ListView):
    model=User 
    template_name='teachers.html'
    def get_queryset(self): 
        return User.objects.filter(rol=1) #Filtramos por solo aquellos que sean estudiantes (1 id del rol estudiante)
 
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs) #Es un diccionario con todos los datos que se estan enviando a la pagina
        #Como es un diccionario podemos pasarles datos.
        teachers = User.objects.filter(rol=1)
        context['subjectsByUser']=relationalUserSubject.objects.filter(user_id__in=teachers)
        return context
    
def editSubjects(request, pk):
    # Obtener el usuario específico
    user = User.objects.get(id=pk)
    
    # Obtener todas las asignaturas asociadas al usuario
    userSubjects = relationalUserSubject.objects.filter(user_id=user.id)
    user_subject_ids = [relational.subject_id for relational in userSubjects]
    
    # Obtener todas las asignaturas que no están asociadas al usuario
    notUserSubjects = Subject.objects.exclude(id__in=user_subject_ids)

    # Obtener los nombres de las asignaturas asociadas al usuario 
    user_subject_names = [user_subject.subject.name for user_subject in userSubjects]
    # Obtener los nombres de las asignaturas no asociadas al usuario 
    not_user_subject_names = [not_user_subject.name for not_user_subject in notUserSubjects]
    rol= Rol.objects.all()

    print("Asignaturas asociadas al usuario:")
    for subject_name in user_subject_names:
        print(subject_name)

    print("\nAsignaturas no asociadas al usuario:")
    for subject_name in not_user_subject_names:
        print(subject_name)
    data = {
        'user': user, 
        'subjects': userSubjects,
        'not_user_subjects': notUserSubjects,
        'rol':rol
    }
    return render(request, 'editSubjects.html', {'data': data})

from django.shortcuts import redirect, get_object_or_404
from .models import relationalUserSubject

from django.shortcuts import redirect, get_object_or_404
from .models import relationalUserSubject

def deleteRelationalSubject(request, pk, pkSubject):
    # Buscar la instancia de relationalUserSubject por los IDs proporcionados
    relational_subject = get_object_or_404(relationalUserSubject, user_id=pk, subject_id=pkSubject) 
    # Obtener el ID del usuario antes de eliminar la asignatura
    user_id = relational_subject.user.id
    # Eliminar la instancia de relationalUserSubject
    relational_subject.delete()
    # Redireccionar a la vista edit con el ID del usuario
    return redirect('edit', pk=user_id)

def addRelationalSubject(request, pk, pkSubject):
    # Buscar el usuario y la asignatura correspondientes
    user = get_object_or_404(User, id=pk)
    subject = get_object_or_404(Subject, id=pkSubject)
    # Verificar si la relación ya existe
    existing_relation = relationalUserSubject.objects.filter(user=user, subject=subject).exists()
    # Si la relación no existe, agregar la asignatura al usuario
    if not existing_relation:
        relationalUserSubject.objects.create(user=user, subject=subject)
    user_id=user.id
    return redirect('edit', pk=user_id)

