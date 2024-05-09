from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self): #Metodo toString del modelo 
        return self.name
    class Meta: #Sirve para establecer los metadatos del modelo
        verbose_name='Subject'
        verbose_name_plural='Subjects'
        db_table='subject'
        ordering=['name']    

class User(models.Model):
    name=models.CharField(max_length=100,verbose_name="Nombre")
    surname=models.CharField(max_length=100,verbose_name="Apellidos")
    rol=models.ForeignKey(Rol,on_delete=models.CASCADE)
    #, el parámetro through se utiliza en el campo ManyToManyField para especificar el nombre de una tabla intermedia personalizada que se utilizará 
    #para representar la relación muchos a muchos entre dos modelos.Define el nombre de la tabla intermedia.
    subject = models.ManyToManyField(Subject, through='relationalUserSubject')    
    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'
        db_table='user'
        ordering=['name']

#Seria en el modelo entidad-relacion podría ser una entidad debil, ya que establece una relación 1-1 con la tabla Users
class relationalUserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
    class Meta:
        #unique_together es una opción de la clase Meta que te permite especificar que la combinación de ciertos campos debe ser única en la base de datos
        unique_together = ('user', 'subject')