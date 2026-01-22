from django.db import models

class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='servicio', null=True)
    visible = models.BooleanField(default=True, verbose_name="¿Mostrar en la pagina web?")

    class Meta:
        verbose_name_plural = "Servicios"
    
    def __str__(self):
        return self.nombre

class Formulario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido= models.CharField(max_length=30)
    empresa = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField() 
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name="Tipo de servicios")
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de envío")
    estado = models.BooleanField(default=False, verbose_name="¿Formulario revisado?")

    class Meta:
        verbose_name = "Formulario de Contactos"
        verbose_name_plural = "Bandeja de Entrada" 
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.empresa} - {self.correo}"


class Galeria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    imagen = models.ImageField(upload_to='galeria', null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, verbose_name="Tipo de servicio")

    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Galeria de trabajos"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre} - {self.servicio}"
