from crur.models import Register
import json, os
from django.conf import settings
from django.urls import reverse


class GenerateHTML:

    @classmethod
    def generate(cls, register: Register, permission: int):
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

        register.html = html
        return register