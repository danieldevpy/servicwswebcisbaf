from crur.models import Register
import json, os
from django.conf import settings
from django.urls import reverse


class GenerateHTML:

    @classmethod
    def generate(cls, register: Register, permission: int):
        file = register.response_attachments.first()
        element_file = ''
        delete = ''
        if file:
            if permission == 1:
                delete = f'<a href="/admin/crur/archive/{file.pk}/delete/" target="_blank">Deletar Arquivo</a>'
            if permission == 1 or permission == 2:
                element_file = f'<a href="{file.archive.url}" target="_blank">Visualizar Arquivo</a> {delete}'
            else:
                if register.auth:
                    element_file = f'<a href="{file.archive.url}" target="_blank">Visualizar Arquivo</a> {delete}'
                else:
                    element_file = f'<label>Aguardando autorização para liberação do documento</label>'
        html = ''
        data_json = json.loads(register.data_json)
        for key in data_json:
            html += f"""
                <h5>{key}</h5>
                <div class="d-flex flex-column m-3">
            """
            for field, value in data_json[key].items():
                html += f"""
                    <label><b>{field}:</b> {value}</label>
                """
            html += "</div>"
        html += f"""
        <hr>
        <h5>Anexos</h5>
        <div class="d-flex flex-row flex-wrap">
        """
        
        for archive in register.archives.all():
            path = os.path.join(settings.MEDIA_URL, str(archive))
            name = str(archive).split('/')[1]
            html += f"""
           <div class="card">
            <div class="card-body">
                <h5 class="card-title">{archive.name}</h5>
                <p class="card-text">{name}</p>
                <a href="{path}" target="_blank" class="btn btn-primary">Visualizar</a>
            </div>
            </div>
            """
        r = ''
        if register.response:
            r = register.response

        html += f"""
        </div>
        <hr>
        <form action="{reverse('response')}" method="POST" enctype="multipart/form-data" class="d-flex flex-column" style="gap:10px;">
            <input name="pk" value="{register.pk}" style="display:none;">
            <h5>Resposta da Solicitação</h5>

            {element_file if file else f'<div class="mb-3"><label for="file{register.pk}" class="form-label">Anexo Resposta</label> <input name="file" class="form-control" type="file" id="file{register.pk}"/></div>'}
            
            <textarea class="form-control" name="response" rows="4" {'readonly' if permission != 1 else ''}>{r}</textarea>
            <select name="select" class="form-select form-control" {'readonly' if permission != 1 else ''}>
        """

        for options in register._meta.get_field('status').choices:
            if register.status == options[0]:
                html += f'<option value="{options[0]}" selected>{options[1]}</option>'
            else:
                html += f'<option value="{options[0]}">{options[1]}</option>'

        
        btn_auth = ''
        if permission == 2:
            if register.status != "analise":
                if not register.auth:
                    btn_auth = f'<a href="{reverse("authorize", args=[register.pk])}" class="btn btn-success">Autorizar</a>'
                else:
                    btn_auth = '<h6>O relatório foi autorizado!</h6>'
            else:
                btn_auth = '<h6>Aguardando Analise</h6>'
            
        html += f"""
            </select>
            {'<input type="submit" value="Atualizar" class="btn btn-primary">' if permission == 1 else ''}
            { btn_auth }
        </form>
        """

        register.html = html
        return register