from django.db import models
from datetime import datetime
from django.urls import reverse

class Setting(models.Model):
    number_contact = models.CharField("Numero para receber solicitações", max_length=200)

    def __str__(self) -> str:
        return 'Configurações'
    
    
class Archive(models.Model):
    name = models.CharField('Identificador do Arquivo', max_length=100, blank=True)
    archive = models.FileField(upload_to='crur/')
    
    def __str__(self) -> str:
        return self.archive.name


class Register(models.Model):
    identifier = models.CharField('Identificador', max_length=100)
    data_json = models.CharField('Dados em JSON', max_length=1000)
    archives = models.ManyToManyField(Archive, related_name='register_archives')
    status = models.CharField(
        max_length=100, 
        default="analise", 
        choices=(
            ("analise", "Em analise"), 
            ("deferido", "Deferido"), 
            ("indeferido", "Indeferido")
        )
    )
    response_attachments = models.ManyToManyField(Archive, related_name='register_response_attachments', blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    date = models.DateTimeField('Data', default=datetime.now, blank=True, null=True)
    auth = models.BooleanField(default=False)
    html = None

    def __str__(self) -> str:
        return self.identifier