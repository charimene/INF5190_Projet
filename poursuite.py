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


class Poursuite:
    def __init__(self, id, date_poursuite, date_jugement, motif, montant, id_etablsmnt):
        self.id = id
        self.date_poursuite = date_poursuite
        self.date_jugement = date_jugement
        self.motif = motif
        self.montant = montant
        self.id_etablsmnt = id_etablsmnt
    
    def asDictionary(self):
        return {"id": self.id,
                "date_poursuite": self.date_poursuite,
                "date_jugement": self.date_jugement,
                "description": self.motif,
                "montant": self.montant,
                "id_etablissement": self.id_etablsmnt}