""" Provide bibtex/ris function"""
import base64
import requests
from IPython.display import HTML

import matplotlib.pyplot as plt
from IPython.core.pylabtools import print_figure

class Works:
    """ Works class """
    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def __str__(self):
        return "str"
    
    def _repr_markdown_(self):
        _authors = [
            f'[{au["author"]["display_name"]}]({au["author"]["id"]})'
            for au in self.data["authorships"]
        ]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and " + _authors[-1]

        title = self.data["title"]

        journal = f"[{self.data['host_venue']['display_name']}]({self.data['host_venue']['id']})"
        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [self.data["biblio"]["first_page"], self.data["biblio"]["last_page"]]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        oa = self.data["id"]

        # Citation counts by year
        years = [e["year"] for e in self.data["counts_by_year"]]
        counts = [e["cited_by_count"] for e in self.data["counts_by_year"]]

        fig, ax = plt.subplots()
        ax.bar(years, counts)
        ax.set_xlabel("year")
        ax.set_ylabel("citation count")
        data = print_figure(fig, "png")  # save figure in string
        plt.close(fig)

        b64 = base64.b64encode(data).decode("utf8")
        citefig = f"![img](data:image/png;base64,{b64})"

        s = f'{authors}, *{title}*, **{journal}**, {volume}{issue}{pages}, ({year}), {self.data["doi"]}. cited by: {citedby}. [Open Alex]({oa})'

        s += "<br>" + citefig
        return s

    def bibtex_str(self):
        """ bibtex """
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
            fields += [f'author={{{author["author"]["display_name"]}}}']
        fields += [f'year={self.data["publication_year"]}']
        fields += [f'title={{{self.data["title"]}}}']
        fields += [f'journal={{{self.data["host_venue"]["display_name"]}}}']
        fields += [f'volume={self.data["biblio"]["volume"]}']
        if self.data["biblio"]["issue"]:
            fields += [f'issue={self.data["biblio"]["issue"]}']

        fields += [
            f'pages={self.data["biblio"]["first_page"]}-{self.data["biblio"]["last_page"]}'
        ]

        fields += [f'doi={self.data["doi"]}\n}}']

        bibtex = ",\n".join(fields)

        return bibtex

    @property
    def bibtex(self):
        """ bibtex property """
        bibtexx = self.bibtex_str()
        bibtex64 = base64.b64encode(bibtexx.encode("utf-8")).decode("utf8")
        uri = f'<pre>{bibtexx}<pre><br><a href="data:text/plain;base64,{bibtex64}"' \
                'download="ris">Download bibtex</a>'

        return HTML(uri)

    def ris_str(self):
        """ ris """
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
        """ ris property"""
        riss = self.ris_str()
        ris64 = base64.b64encode(riss.encode('utf-8')).decode('utf8')
        uri = f'<pre>{riss}<pre><br><a href="data:text/plain;base64,{ris64}"' \
                'download="ris">Download RIS</a>'
        return HTML(uri)
