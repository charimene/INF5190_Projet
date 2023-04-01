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