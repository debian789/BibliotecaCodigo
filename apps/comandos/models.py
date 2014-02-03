#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from apps.elementos_comunes.models import *

class mdl_comandos(models.Model):
	nombre 		 = models.CharField(max_length=500,verbose_name="Nombre")
	descripcion  = models.TextField(verbose_name="Descripción",blank=True)
	comando 	 = models.CharField(max_length=500,verbose_name="Comando",blank=False,null=False)
	#lenguaje     = models.ForeignKey(mdl_lenguaje,blank=False)
	usuario      = models.ForeignKey(User)
	favorito    = models.BooleanField(default=False,blank=False)
	fechaIngreso = models.DateField(auto_now = True)
	estado       = models.BooleanField(default = True)
	

	class Meta:
		verbose_name = ('Comando')
		verbose_name_plural = ('Comandos')

	def __unicode__(self):
		return self.nombre
