from django.shortcuts import render_to_response,get_object_or_404,render
from django.template import RequestContext
from django.contrib.auth.models import User
from apps.codigos.models import *
from models import *
from forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.views.generic import ListView

def view_inicio_sesion(request):
	if request.user.is_authenticated():
		usuario = User.objects.select_related().get(id=request.user.id)
		codigos = mdl_codigos.objects.select_related().filter(usuario=usuario)
		favoritos = mdl_favoritos.objects.select_related().filter(codigo=codigos)
		ultimoCodigo = mdl_codigos.objects.select_related().filter(usuario=usuario)[:10]
		contexto = {"favoritos":favoritos,"codigos":ultimoCodigo}
		return render(request,"inicioSesion.html",contexto)

def view_inicio(request):
	return render(request,'index.html')

def view_salir(request):
	logout(request)
	return HttpResponseRedirect('/')

def view_ingresar(request):
	mensaje=""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/comandos')
		#return HttpResponseRedirect('/inicioSesion')

	else:
		if request.method == "POST":
			form = loginForm(request.POST)
			if form.is_valid():
				username= form.cleaned_data['userName']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/comandos')
					#return HttpResponseRedirect('/inicioSesion')

				else:
					mensaje = "usuario y password incorrectos "

		form = loginForm()
		contexto = {'form':form,'mensaje':mensaje}
		print mensaje
		return render(request,'login.html',contexto)

def view_agregar_favoritos(request,id_codigo):
	if request.user.is_authenticated():
		usuario   = User.objects.select_related().get(id=request.user.id)
		codigo    = mdl_codigos.objects.get(id=id_codigo,usuario=usuario)
		datosTemp = mdl_favoritos.objects.create(codigo=codigo)
		datosTemp.save()
		codigo.favorito = True 
		codigo.save()

		codigos = mdl_codigos.objects.all()
		contexto = {"codigos":codigos}
		return render(request,'codigos.html',contexto)

def view_quitar_favorito(request,id_codigo):
	if request.user.is_authenticated():
		codigo = mdl_codigos.objects.get(id=id_codigo)
		datos = mdl_favoritos.objects.filter(codigo=codigo).delete()
		#datos.save()
		codigo.favorito = False
		codigo.save()

		codigos = mdl_codigos.objects.all()
		contexto = {"codigos":codigos}
		return render(request,'codigos.html',contexto)

def view_quitar_favorito_principal(request,id_codigo):
	if request.user.is_authenticated():
		codigo = mdl_codigos.objects.get(id=id_codigo)
		datos = mdl_favoritos.objects.filter(codigo=codigo).delete()
		codigo.favorito = False
		codigo.save()
		usuario = User.objects.select_related().get(id=request.user.id)
		codigos = mdl_codigos.objects.select_related().filter(usuario=usuario)
		favoritos = mdl_favoritos.objects.select_related().filter(codigo=codigos)
		ultimoCodigo = mdl_codigos.objects.select_related().filter(usuario=usuario)[:10]
		#codigos = mdl_codigos.objects.all()[:2]
		#codigo
		contexto = {"favoritos":favoritos,"codigos":ultimoCodigo}
		return render(request,"inicioSesion.html",contexto)

def view_agregar_proyecto_favoritos(request,id_proyecto):
	if request.user.is_authenticated():
		usuario   = User.objects.select_related().get(id=request.user.id)
		proyecto  = mdl_proyectos.objects.get(id=id_proyecto,usuario=usuario)
		#datosTemp = mdl_

