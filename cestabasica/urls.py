"""cestabasica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cestabasica.cesta.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('cestabasica/admin/', admin.site.urls),
    path('cestabasica/', home),
    path('cestabasica/login', entrar),
    path('cestabasica/login/submit', submit_login),
    path('cestabasica/index', index),
    path('cestabasica/logout', sair),
    path('cestabasica/data/<int:mes>/<ano>', dados),
    path('cestabasica/estatistica/<int:id>/', estatistica),
    path('cestabasica/lista/<int:evento>/<int:super>', lista),
    path('cestabasica/request/<int:produto>/<int:evento>/<int:estabelecimeto>/<str:preco>/<str:div>/<int:boo>', requestprod),
    path('cestabasica/cad/<int:id>/<int:pk>', cadevento),
    path('cestabasica/updata/<int:id>/<int:pk>', updados),
    path('cestabasica/relatorio', relatorio),
    path('cestabasica/api', csrf_exempt(api)),
    path('cestabasica/produto/<int:id>', csrf_exempt(produt)),
]
