# Copyright 2020 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


demande_inspection_schema ={
    'type': 'object',
    'required': ['nom_etablissement', 'adresse', 'ville', 'date_visite_client', 'nom_client', 'prenom_client', 'plainte'],
    'properties': {
        'id': {
            'type': 'number'
        },
        'nom_etablissement': {
            'type': 'string'
        },
        'adresse': {
            'type': 'string'
        },
        'ville': {
            'type': 'string'
        },
        'date_visite_client': {
            'type': 'string'
        },
        'nom_client': {
            'type': 'string'
        },
        'prenom_client': {
            'type': 'string'
        },
        'plainte': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}

{
"nom_etablsmnt":"TTT2222555",
"proprietaire":"rue TTT2225555 ",
"adresse":"Montréal2555",
"ville":"montreal",
"statut":"ouvert",
"nbr_infraction_etablsmnt":5
}

maj_etablissement_schema ={
    'type': 'object',
    'properties': {
        'nom_etablsmnt': {
            'type': 'string'
        },
        'proprietaire': {
            'type': 'string'
        },
        'adresse': {
            'type': 'string'
        },
        'ville': {
            'type': 'string'
        },
        'statut': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}

create_user_schema={
    'type': 'object',
    'properties': {
        'nom': {
            'type': 'string'
        },
        'prenom': {
            'type': 'string'
        },
        'courriel': {
            'type': 'string',
            'format': 'email'
        },
        'etablissement_a_surveiller': {
            'type': 'array', 
            'items': {
                'type': 'string'
            }
        },
        'mot_de_passe': {
            'type': 'string'
        }
    },
    "required": ["nom", "prenom", "courriel", "etablissement_a_surveiller", "mot_de_passe"],
    "additionalProperties": False
}

schema = {
    "type": "object",
    "properties": {
        "nom": {"type": "string"},
        "prenom": {"type": "string"},
        "courriel": {"type": "string", "format": "email"},
        "etablissement_a_surveiller": {"type": "array", "items": {"type": "string"}},
        "mot_de_passe": {"type": "string"}
    },
    "required": ["nom", "prenom", "courriel", "etablissement_a_surveiller", "mot_de_passe"],
    "additionalProperties": False
}
