import ast
import json
from datetime import datetime
from decimal import Decimal
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_auth, logout
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .form import *
from .models import *


# Create your views here.
def home(request):
    cursor = connection.cursor()
    data = {}
    now = datetime.now()
    ano = now.year
    mes = now.month


    # Calcula o valor total da cesta básica do último mês com todos os dados
    text = "select evento_id, mes, ano, sum(preco) as preco from ( select ct.nome, avg(((cp.preco * ct.quantidade) / cs.quantidade)) as preco, cp.evento_id from cesta_pesquisa_preco as cp inner join cesta_produto as cs on cp.produto_id = cs.id inner join cesta_tipo as ct on cs.tipo_id = ct.id where cp.evento_id in ( select evento_id from ( select count(distinct(cc.tipo_id)) as qtdcesta, cp.evento_id from cesta_pesquisa_preco as cp inner join cesta_produto as cc on cp.produto_id = cc.id inner join cesta_tipo as ct on ct.id = cc.tipo_id where ct.cestabasica = 1 group by cp.evento_id ) as t where qtdcesta >= 12 ) and ct.cestabasica = 1 group by ct.nome, evento_id ) as ttt inner join cesta_evento as ct on evento_id = ct.id group by evento_id order by ano desc, mes desc limit 1"
    cursor.execute(text)
    tx =  cursor.fetchone()
    # data['cesta'] = tx[3]
    # mes = tx[1]
    # ano = tx [2]
    #
    #
    # # Calcula o valor dos produtos da cesta básica do último mês com todos os dados
    # text = "select ct.id, ct.nome, avg(((cp.preco*ct.quantidade)/cs.quantidade)) as preco, ct.imagem, ct.cestabasica from cesta_pesquisa_preco as cp inner join cesta_produto as cs on  cp.produto_id = cs.id inner join cesta_tipo as ct on cs.tipo_id = ct.id where cp.evento_id = (select id from cesta_evento where mes = %s and ano = %s) group by ct.nome" % ( mes, ano)
    # cursor.execute(text)
    # data['ProCesta'] = cursor.fetchall()
    #
    # if mes == 1:
    #     data['mes'] = 'Jan'
    # elif mes == 2:
    #     data['mes'] = 'Fev'
    # elif mes == 3:
    #     data['mes'] = 'Mar'
    # elif mes == 4:
    #     data['mes'] = 'Abr'
    # elif mes == 5:
    #     data['mes'] = 'Mai'
    # elif mes == 6:
    #     data['mes'] = 'Jun'
    # elif mes == 7:
    #     data['mes'] = 'Jul'
    # elif mes == 8:
    #     data['mes'] = 'Ago'
    # elif mes == 9:
    #     data['mes'] = 'Set'
    # elif mes == 10:
    #     data['mes'] = 'Out'
    # elif mes == 11:
    #     data['mes'] = 'Nov'
    # elif mes == 12:
    #     data['mes'] = 'Dez'
    # data['ano'] = ano

    return HttpResponse(tx)
    # return render(request, 'home.html', data)


def estatistica(request, id):
    cursor = connection.cursor()
    data = {}
    now = datetime.now()
    ano = now.year
    mes = now.month
    value = None
    titulo = None


    if (id == 0):
        text = "select 'Periodo Mensal', mes, ano, sum(preco) as preco from (select ct.nome, avg(((cp.preco*ct.quantidade)/cs.quantidade)) as preco, cp.evento_id from cesta_pesquisa_preco as cp inner join cesta_produto as cs on  cp.produto_id = cs.id inner join cesta_tipo as ct on cs.tipo_id = ct.id where cp.evento_id in (select evento_id from (select count(distinct(tipo_id)) as qtdcesta, evento_id from cesta_pesquisa_preco as cp inner join cesta_produto as cc on cp.produto_id = cc.id inner join cesta_tipo as ct on ct.id = cc.tipo_id  where ct.cestabasica = 1 group by evento_id) where qtdcesta >= 12) and ct.cestabasica =1  group by ct.nome, evento_id) inner join cesta_evento as ct on evento_id = ct.id group by evento_id order by ano desc, mes desc"
        cursor.execute(text)
        value = cursor.fetchall()
        data['Cesta'] = value
    else:
        text = "select (select nome from cesta_tipo where id = %s) as tipo, (select mes from cesta_evento where id = evento_id) as mes, (select ano from cesta_evento where id = evento_id) as ano, avg(preco) as preco from cesta_pesquisa_preco where produto_id in (select id from cesta_produto where tipo_id = %s) group by evento_id order by ano desc, mes desc" %(id, id)
        cursor.execute(text)
        value = cursor.fetchall()
        data['Cesta'] = value

    ma = {}
    pc = {}
    count = 0
    for cat, mes, ano, preco in value:
        titulo = cat
        if count < 12:
            ma[count] = str(mes)+"/"+str(ano)
            pc[count] = preco
        count = count+1

    data['ma'] = ma
    data['pc'] = pc
    data['titulo'] = titulo
    # return HttpResponse(data['tree'])
    return render(request, 'estatistica.html', data)

def relatorio(request):
    cursor = connection.cursor()
    data = {}

    text = "select * from cesta_evento where id in (select distinct(evento_id) from cesta_pesquisa_preco) order by ano desc, mes desc"
    cursor.execute(text)
    value = cursor.fetchall()
    data['meses'] = value

    text = "select ct.nome, evento_id, avg(preco) as preco from cesta_pesquisa_preco as cpp inner join cesta_produto as cp on cpp.produto_id = cp.id inner join cesta_tipo as ct on cp.tipo_id = ct.id group by cpp.evento_id,ct.id order by ct.nome"
    cursor.execute(text)
    value = cursor.fetchall()
    data['categoria'] = value

    text = "select evento_id, sum(preco) as preco from (select ct.nome, avg(((cp.preco*ct.quantidade)/cs.quantidade)) as preco, cp.evento_id from cesta_pesquisa_preco as cp inner join cesta_produto as cs on  cp.produto_id = cs.id inner join cesta_tipo as ct on cs.tipo_id = ct.id where cp.evento_id in (select evento_id from (select count(distinct(tipo_id)) as qtdcesta, evento_id from cesta_pesquisa_preco as cp inner join cesta_produto as cc on cp.produto_id = cc.id inner join cesta_tipo as ct on ct.id = cc.tipo_id  where ct.cestabasica = 1 group by evento_id) where qtdcesta >= 12) and ct.cestabasica =1  group by ct.nome, evento_id) inner join cesta_evento as ct on evento_id = ct.id group by evento_id"
    cursor.execute(text)
    value = cursor.fetchall()
    data['cesta'] = value

    return render(request, 'relatorio.html', data)


def entrar(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        return redirect('/cestabasica/index')


@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('user')
        password = request.POST.get('pass')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return redirect('/cestabasica/index')
        else:
            messages.error(request, "erro")
    return redirect('/cestabasica/login')


@login_required(login_url='/cestabasica/login')
def index(request):
    data = {}
    data['eventos'] = evento.objects.all()
    return render(request, 'index.html', data)


@login_required(login_url='/cestabasica/login')
def dados(request, mes, ano):
    data = {}
    cursor = connection.cursor()
    text = "select id from cesta_evento where mes = '%s' and ano = '%s'" % (mes, ano)
    cursor.execute(text)
    id = cursor.fetchone()
    if(id is None):
        text = "insert into cesta_evento(mes, ano) values('%s','%s')" % (mes, ano)
        cursor.execute(text)
        text = "select id from cesta_evento where mes = '%s' and ano = '%s'" % (mes, ano)
        cursor.execute(text)
        id = cursor.fetchone()
    data['id'] = "%s" % id
    # data['eventos'] = pesquisa_preco.objects.filter(evento_id=id)


    data['estabelecimento'] = estabelecimento.objects.all()
    # return HttpResponse(id)
    return render(request, 'data.html', data)


@login_required(login_url='/cestabasica/login')
def lista(request, evento, super):
    data = {}
    cursor = connection.cursor()
    data['evento'] = evento;
    data['sup'] = super;
    # data['eventos'] = pesquisa_preco.objects.filter(Q(evento_id=pk) & Q(categoria_id=id))
    text = "select * from cesta_pesquisa_preco as cpp inner join cesta_evento as ce on cpp.evento_id = ce.id inner join cesta_produto as cp on cpp.produto_id = cp.id where evento_id ='%s' and estabelecimento_id = '%s'"  % (evento,super)
    data['pesquisa'] = pesquisa_preco.objects.raw(text)

    text = "select (mes||'/'||ano) as dia from cesta_evento where id = %s" %evento
    cursor.execute(text)
    data['mes_ano'] = "%s" % cursor.fetchone()

    text = "select nome from cesta_estabelecimento where id = %s" % super
    cursor.execute(text)
    data['estabelecimento'] = "%s" % cursor.fetchone()
    # data['eventos'] = tipo.objects.all()
    # data['cat'] = categoria.objects.all()
    # return HttpResponse(str(text)+str(data['eventos']))
    # return HttpResponse(data['mes_ano'])
    data['tipos'] = tipo.objects.all()
    data['produto'] = produto.objects.all()
    data['categoria'] = categoria.objects.all()
    return render(request, 'lista.html', data)


@login_required(login_url='/cestabasica/login')
def updados(request, id, pk):
    data = {}
    data['id'] = pk;
    preco = pesquisa_preco.objects.get(id=id)
    form = PrecoForm(request.POST or None, instance=preco)
    if form.is_valid():
        form.save()
        # return redirect('/da')
        text = "/data/%s" % (pk)
        return redirect(text)
    data['form'] = form
    # return HttpResponse(form)
    return render(request, 'updata.html', data)

@login_required(login_url='/cestabasica/login')
def requestprod(request, produto, evento, estabelecimeto, preco, div, boo):
    data = {}
    # data['evento'] = evento;
    # data['sup'] = estabelecimeto;
    data['div'] = div;

    cursor = connection.cursor()
    # text = "select * from cesta_pesquisa_preco where estabelecimento_id = %s and evento_id = %s and produto_id = %s" % (estabelecimeto, evento, produto)
    # cursor.execute(text)
    # existe = "%s" % cursor.fetchone()
    prod = 0
    data['prod'] = "Erro ao efetuar operação"

    # data['url'] = "/%s/%s/0/2" % (evento,estabelecimento)
    if(boo == 1):

        text = "select count(*) from cesta_pesquisa_preco where estabelecimento_id = '%s' and evento_id = '%s' and produto_id ='%s'" % (estabelecimeto, evento, produto)
        cursor.execute(text)
        igual = cursor.fetchone()
        igual = int(igual [0])
        # igual = int(igual)
        if(igual > 0):
            return HttpResponse("true")

        text = "insert into cesta_pesquisa_preco (preco, estabelecimento_id, evento_id, produto_id) values ('%s',%s,%s,%s)" % (preco, estabelecimeto, evento, produto)
        cursor.execute(text)

        text = "select tipo_id from cesta_produto where id = %s" % produto
        cursor.execute(text)
        prod = produto
        produto = "%s" % cursor.fetchone()
        text = "select * from cesta_pesquisa_preco as cpp inner join cesta_produto as cp on cpp.produto_id = cp.id  where estabelecimento_id =%s and evento_id = %s  and cpp.id != '%s' and tipo_id = (select tipo_id from cesta_produto where tipo_id = %s);" % (
            estabelecimeto, evento, prod, produto)
        data['prod'] = pesquisa_preco.objects.raw(text)

    elif(boo == 2):
        text = "select tipo_id from cesta_pesquisa_preco as cpp inner join cesta_produto as cp on cpp.produto_id = cp.id where cpp.id = %s" % produto
        cursor.execute(text)
        prod = produto
        # text = "delete from cesta_pesquisa_preco where id = '%s'" % produto
        # cursor.execute(text)
        pesquisa_preco.objects.filter(id=produto).delete()
        produto = "%s" % cursor.fetchone()
        text = "select * from cesta_pesquisa_preco as cpp inner join cesta_produto as cp on cpp.produto_id = cp.id  where estabelecimento_id =%s and evento_id = %s  and cpp.id != '%s' and tipo_id = (select tipo_id from cesta_produto where tipo_id = %s);" % (
        estabelecimeto, evento, prod, produto)
        data['prod'] = pesquisa_preco.objects.raw(text)




    # return HttpResponse(div)
    return render(request, 'request.html', data)


@login_required(login_url='/cestabasica/login')
def cadevento(request, id, pk):
    data = {}
    data['id'] = pk;
    # preco = pesquisa_preco.objects.get(id=id)
    form = PrecoFormCad(request.POST or None)
    if form.is_valid():
        form.save()
        # return redirect('/da')
        text = "/lista/%s/%s" % (id, pk)
        return redirect(text)
    data['form'] = form
    # form.initial['produto'] = id
    form.initial['evento'] = pk
    # form.fields['produto'].widget = forms.HiddenInput()
    form.fields['evento'].widget = forms.HiddenInput()
    # form.fields["produto"] = models.forms.ModelMultipleChoiceField(queryset=someData.objects.filter(tipo=id))
    form.fields['produto'] = forms.ModelChoiceField(produto.objects.filter(tipo_id=id))
    # return HttpResponse(form)
    return render(request, 'cadeventos.html', data)


def sair(request):
    logout(request)
    return redirect('/cestabasica/')


def api(request):
    cursor = connection.cursor()
    data = {}

    text = "select * from cesta_evento where id in (select distinct(evento_id) from cesta_pesquisa_preco) order by ano desc, mes desc"
    cursor.execute(text)
    value = cursor.fetchall()
    data['meses'] = value

    text = "select ct.nome, evento_id, avg(preco) as preco from cesta_pesquisa_preco as cpp inner join cesta_produto as cp on cpp.produto_id = cp.id inner join cesta_tipo as ct on cp.tipo_id = ct.id group by cpp.evento_id,ct.id order by ct.nome"
    cursor.execute(text)
    value = cursor.fetchall()
    data['categoria'] = value

    text = "select evento_id, sum(preco) as preco from (select ct.nome, avg(((cp.preco*ct.quantidade)/cs.quantidade)) as preco, cp.evento_id from cesta_pesquisa_preco as cp inner join cesta_produto as cs on  cp.produto_id = cs.id inner join cesta_tipo as ct on cs.tipo_id = ct.id where cp.evento_id in (select evento_id from (select count(distinct(tipo_id)) as qtdcesta, evento_id from cesta_pesquisa_preco as cp inner join cesta_produto as cc on cp.produto_id = cc.id inner join cesta_tipo as ct on ct.id = cc.tipo_id  where ct.cestabasica = 1 group by evento_id) where qtdcesta >= 12) and ct.cestabasica =1  group by ct.nome, evento_id) inner join cesta_evento as ct on evento_id = ct.id group by evento_id"
    cursor.execute(text)
    value = cursor.fetchall()
    data['cesta'] = value

    var = '{"produto": {'
    # var = var[:-1]
    for eventoid, mes, ano in data['meses']:
        var = '%s "%s-%s": {' % (var, mes, ano)
        for produto, evento, preco in data['categoria']:
            if evento == eventoid:
                var = '%s "%s":%s,' % (var, produto, preco)
        var = var[:-1]
        var = '%s },' % var
    var = var[:-1]
    var = '%s }' % var
    var = '%s ,"cesta":{  ' % var
    for eventoid, mes, ano in data['meses']:
        # var = '%s ' % (var, mes, ano)
        for evento, valor in data['cesta']:
            if evento == eventoid:
                var = '%s "%s-%s": %s,' % (var, mes, ano, valor)
        # var = var[:-1]
        # var = '%s,' % var
    var = var[:-1]
    var = '%s }}' % var

    return HttpResponse(var)