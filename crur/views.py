from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Register, Archive, Setting
from .controler.generate_html import GenerateHTML
from controller.request import RequestWhatsapp, RequestCommands
import json, re, threading
from django.contrib.auth import authenticate, login
from django.contrib import messages

def global_context(request, context):
    context['is_auth'] = request.user.username
    return context

def index(request):
    return render(request, 'crur.html', context=global_context(request, {}))

def crur_open(request):
    return render(request, 'crur_open.html', context=global_context(request, {}))

def crur_term(request):
    return render(request, 'crur_term.html', context=global_context(request, {}))

def crur_check(request, term=None):
    context = {'term': term}
    if term:
        context['registers'] = Register.objects.filter(identifier=term)
    return render(request, 'crur_check.html', context=global_context(request, context))

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('response')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'crur_login.html')


@csrf_exempt
def crur_response(request, term=None):
    if request.method == "GET":
        if not request.user.is_staff:
            return redirect('crur_login')
        
        nivel_acess = None
        try:
            nivel_acess = int(request.user.field_extra)
        except:
            messages.error(request, 'Nivel de acesso não definido')
            return redirect('crur')
        
        context = {'term': term, 'all': Register.objects.count()}
        registers = None

        if not term:
            match nivel_acess:
                case 1:
                    registers = Register.objects.filter(status='analise')
                    if not registers:
                        registers = Register.objects.filter(status='deferido')
                case 2:
                    registers = Register.objects.filter(status="deferido", auth=False)
                    if registers:
                        term = 'notauth'
                    else:
                        registers = Register.objects.filter(auth=True)
                        if registers:
                            term = 'auth'
        else:
            match term:
                case 'notauth':
                    registers = Register.objects.filter(status="deferido", auth=False)
                case 'auth':
                    registers = Register.objects.filter(auth=True)
                case 'all':
                    registers = Register.objects.all()
                case _:
                    registers = Register.objects.filter(identifier=term)
                    if not registers:
                        registers = Register.objects.filter(status=term)
        

        if not registers:
            registers = Register.objects.all()

        try:
            context['filter'] = int(term)
        except:
            pass

        context['count'] = registers.count()
        context['registers'] = [GenerateHTML.generate(r, nivel_acess) for r in registers]
        return render(request, 'crur_response.html', context=global_context(request, context))


    
    elif request.method == "POST":
        pk = request.POST.get('pk')
        response = request.POST.get('response')
        select = request.POST.get('select')
        register = Register.objects.get(pk=pk)
        register.status = select
        register.response = response
        register.save()

        if not register.auth:
            if select == "indefirido":
                message_wpp = f"*MENSAGEM AUTOMATICA (NÃO RESPONDA)*\n A resposta da solicitação de cópia do boletim de atendimento samu foi atualizado, para acompanhar acesse https://atendimentocrur.cisbaf.org.br/check/{register.identifier}"
                threading.Thread(target=RequestWhatsapp.notification_wpp, args=(register.identifier, message_wpp)).start()
        else:
            message_wpp = f"*MENSAGEM AUTOMATICA (NÃO RESPONDA)*\n A resposta da solicitação de cópia do boletim de atendimento samu foi atualizado, para acompanhar acesse https://atendimentocrur.cisbaf.org.br/check/{register.identifier}"
            threading.Thread(target=RequestWhatsapp.notification_wpp, args=(register.identifier, message_wpp)).start()
        
        return redirect('response')
    
def authorizar(request, pk):
    register = Register.objects.get(pk=pk)
    register.auth = True
    register.save()
    message_wpp = f"*MENSAGEM AUTOMATICA (NÃO RESPONDA)*\n A resposta da solicitação de cópia do boletim de atendimento samu foi atualizado, para acompanhar acesse https://atendimentocrur.cisbaf.org.br/check/{register.identifier}"
    threading.Thread(target=RequestWhatsapp.notification_wpp, args=(register.identifier, message_wpp)).start()
    url = RequestCommands.get_previous_url(request)
    if url:
        return redirect(url)
    
    return redirect('crur')

@csrf_exempt
def archives(request, pk):
    if request.method == "POST":
        desc = request.POST.get('desc')
        file = request.FILES['file']
        register = Register.objects.get(pk=pk)
        register.response_attachments.add(Archive.objects.create(name=desc, archive=file))
        return JsonResponse({"message": 'successs'}, status=200)
    if request.method == "PUT":
        Archive.objects.get(pk=pk).delete()
        return JsonResponse({"message": 'successs'}, status=200)

    return JsonResponse({"msg": "not foi possivel processar sua requisição"}, status=400)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data_json_str = request.POST.get('data_json')
            data_json = json.loads(data_json_str)
            identifier = data_json['Dados do solicitante']['Celular']
            identifier = re.sub(r'\D', '', identifier)
            register_instance = Register(identifier=identifier, data_json=data_json_str)
            register_instance.save()
            images = []
            for i in range(3):
                try:
                    file = request.FILES[f'file{i}']
                    name = str(file.name).split('-DIV-')[0].replace('_', ' ')
                    images.append(Archive.objects.create(name=name, archive=file))
                except:
                    pass
            register_instance.archives.set(images)
            settings = Setting.objects.first()
            message_return = f"Solicitação realizada! para acompanhar a solicitação acesse o menu de acompanhamento e utilize o numero de celular do solicitante, com o final *********{identifier[-4:]}\n O prazo de resposta é de 7 dias!"
            message_wpp = f"*MENSAGEM AUTOMATICA (NÃO RESPONDA)*\n Nova solicitação no atendimento crur, para acompanhar acesse https://atendimentocrur.cisbaf.org.br/response/{identifier}"
            threading.Thread(target=RequestWhatsapp.notification_wpp, args=(settings.number_contact, message_wpp)).start()

            return JsonResponse({"message": message_return, "identifier": identifier})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
 
    return JsonResponse({"erorr": "not foi possivel processar sua requisição"})
        
