""" Provide bibtex/ris function"""
import base64
import requests
from IPython.display import HTML

class Works:
    """ Works class """
    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def __str__(self):
        return "str"

    @property
    def bibtex(self):
        """ bibtex property """
        fields = []
        if self.data["type"] == "journal-article":
            authors = []
            for author in self.data["authorships"]:
                lastname = author["author"]["display_name"].split()[-1]
                year = self.data["publication_year"]
                authors += [f"{lastname}{year}"]
            fields += ["@article{" + " ".join(authors)]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'author={author["author"]["display_name"]}']
        fields += [f'year={self.data["publication_year"]}']
        fields += [f'title={self.data["title"]}']
        fields += [f'journal={self.data["host_venue"]["display_name"]}']
        fields += [f'volume={self.data["biblio"]["volume"]}']
        if self.data["biblio"]["issue"]:
            fields += [f'issue={self.data["biblio"]["issue"]}']

        fields += [
            f'pages={self.data["biblio"]["first_page"]}-{self.data["biblio"]["last_page"]}'
        ]

        fields += [f'doi={self.data["doi"]}\n}}']

        ris = ",\n".join(fields)
        ris64 = base64.b64encode(ris.encode("utf-8")).decode("utf8")
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,{ris64}"' \
                'download="ris">Download RIS</a>'

        return HTML(uri)
    
    def _ris(self):
        """ ris property """
        fields = []
        if self.data['type'] == 'journal-article':
            fields += ['TY  - JOUR']
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data['authorships']:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data['biblio']['issue']:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ['ER  -']

        ris = '\n'.join(fields)

        return ris
        
    @property
    def ris(self):
        riss = self._ris()
        ris64 = base64.b64encode(riss.encode('utf-8')).decode('utf8')
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,{ris64}"' \
                'download="ris">Download RIS</a>'
        return HTML(uri)

    