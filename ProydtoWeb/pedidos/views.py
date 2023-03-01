from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from flask import redirect

from pedidos.models import Pedido, LineaPedido
from carro.carro import Carro

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
# Create your views here.

@login_required(login_url="/autentication/logear")
def procesar_pedido(request):
    pedido=Pedido.objects.create(user=request.user)
    carro=Carro(request)
    lineas_pedido=list()
    for key, value in carro.carro.items():
        lineas_pedido.append(LineaPedido(

            producto_id=key,
            cantidad=value["cantidad"],
            user=request.user,
            pedido=pedido
        ))
    #insert into
    LineaPedido.objects.bulk_create(lineas_pedido)

    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        nombreusuario=request.user.username,
        emailususario=request.user.email
    )
    messages.success(request,"El pedido se ha creado correctamente")
    return redirect("../")

def enviar_mail(**kwargs):
    asunto="Gracias por el pedido"
    mensaje=render_to_string("emails/pedidos.html",{

        "pedido":kwargs.get("pedido"),
        "lineas_pedido":kwargs.get("lineas_pedido"),
        "nombreusuario":kwargs.get("nombreusuario")
    })

    mensaje_texto=strip_tags(mensaje)
    from_email="chaqquererj@gmail.com"
    #to=kwargs.get("emailususario")
    to="joseChaqquereRea@outlook.com"

    sendEmail(asunto, mensaje_texto,from_email,[to],html_message=mensaje)