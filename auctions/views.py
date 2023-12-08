from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .models import *


def index(request):
    listings = Listado.objects.all()


    return render(request, "auctions/index.html", {
        "listings": listings,
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def crearlistado(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]

        # Obtener el usuario autenticado actualmente
        autor = request.user

        # Crear un nuevo Listado con el usuario actual como autor
        listado = Listado.objects.create(
            titulo=title,
            descripcion=description,
            oferta_inicial=starting_bid,
            url_imagen=image_url,
            categoria=category,
            autorListado=autor
        )

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/crearlistado.html")


def mostrar_detalle_listado(request, listado_id):
    listado = get_object_or_404(Listado, pk=listado_id)
    comentarios = Comentario.objects.filter(listado=listado)
    pujas = Oferta.objects.filter(listado=listado)
    
    oferta_mas_alta = pujas.aggregate(Max('monto_oferta'))['monto_oferta__max']
    
    oferta_mas_alta_instance = Oferta.objects.filter(listado=listado, monto_oferta=oferta_mas_alta).first()
    postor_oferta_mas_alta = oferta_mas_alta_instance.postor if oferta_mas_alta_instance else None
    
    sigue_listado = False  
    if request.user.is_authenticated:
        sigue_listado = ListaSeguimiento.objects.filter(listado=listado, seguidor=request.user).exists()

    return render(request, "auctions/verlistado.html", {
        "listado": listado,
        "sigue_listado": sigue_listado,
        "comentarios": comentarios,
        "pujas": pujas,
        "oferta_mas_alta": oferta_mas_alta,
        "postor_oferta_mas_alta": postor_oferta_mas_alta,
        "user": request.user  # Asegúrate de pasar 'user' a la plantilla
    })


@login_required
def seguir_listado(request, listado_id):
    listado = Listado.objects.get(pk=listado_id)
    usuario = request.user

    
    if ListaSeguimiento.objects.filter(listado=listado, seguidor=usuario).exists():
        seguimiento = ListaSeguimiento.objects.get(listado=listado, seguidor=usuario)


      
        
        return HttpResponseRedirect(reverse("index"))
    else:
        
        seguimiento = ListaSeguimiento(listado=listado, seguidor=usuario)
        seguimiento.save()

     
        return HttpResponseRedirect(reverse("index"))

@login_required
def dejar_seguir_listado(request, listado_id):
    listado = Listado.objects.get(pk=listado_id)
    usuario = request.user
    seguimiento = ListaSeguimiento.objects.get(listado=listado, seguidor=usuario)
    seguimiento.delete()
    return HttpResponseRedirect(reverse("index"))

@login_required
def crearcomentario(request, listado_id):

    if request.method == "POST":

        comment = request.POST["comment"]
        listado = Listado.objects.get(pk=listado_id)
        autor = request.user

        comentario = Comentario(texto= comment, comentarista= autor, listado= listado)

        comentario.save()



        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/verlistado.html")


@login_required
def haceroferta(request, listado_id):
    if request.method == "POST":
        offer = float(request.POST["oferta"])
        listado = Listado.objects.get(pk=listado_id)
        autor = request.user

        oferta_mas_alta_actual = listado.ofertas.aggregate(Max('monto_oferta'))['monto_oferta__max']

        if oferta_mas_alta_actual is None:
            oferta_mas_alta_actual = listado.oferta_inicial

        if offer > listado.oferta_inicial and offer > oferta_mas_alta_actual:
            oferta = Oferta(monto_oferta=offer, postor=autor, listado=listado)
            oferta.save()

            return JsonResponse({'success': True, 'message': 'Oferta realizada correctamente'})
        else:
            return JsonResponse({'success': False, 'message': 'La oferta debe ser mayor que la oferta inicial y la oferta más alta actual.'}, status=400)

    return render(request, "auctions/verlistado.html")@login_required
def MiListaSeguimiento(request):
    seguimientos = ListaSeguimiento.objects.filter(seguidor=request.user)
    listados_seguidos = [seguimiento.listado for seguimiento in seguimientos]

    return render(request, "auctions/mislistas.html", {
        "listados_seguidos": listados_seguidos
    })

@login_required
def cerrar_subasta(request, listado_id):
    listado = Listado.objects.get(pk=listado_id)

    if request.user == listado.autorListado:
        listado.subasta_cerrada = True
        listado.save()
        # Puedes redirigir a una página de confirmación o a donde sea necesario
        # En este ejemplo, redirigimos a la página del listado nuevamente
        return HttpResponseRedirect(reverse("mostrar_detalle_listado", args=(listado_id,)))

    # En caso de que el usuario no sea el propietario, puedes mostrar un mensaje de error o redirigirlo a otra página
    return HttpResponse("No tienes permiso para cerrar esta subasta.")