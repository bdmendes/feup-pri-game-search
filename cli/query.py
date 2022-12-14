from urllib.request import urlopen
from urllib.parse import urlencode
from pydoc import pager


SOLR_QUERY_URL = "http://127.0.0.1:8983/solr/games_tuned/query"


class Query:
    def __init__(self, query, *, qop="AND", bf="", fq="", qf="", def_type="edismax", rows=10):
        self.query = query
        self.qop = qop
        self.bf = bf
        self.fq = fq
        self.qf = qf
        self.def_type = def_type
        self.rows = rows

    def __str__(self):
        return f"Query: {self.query}"

    def url(self):
        query_fields = {
            "q": self.query,
            "q.op": self.qop,
            "defType": self.def_type,
            "bf": self.bf,
            "fq": self.fq,
            "qf": self.qf,
            "rows": self.rows
        }
        return f"{SOLR_QUERY_URL}?{urlencode(query_fields)}"

    def ui_url(self):
        return self.url().replace("/solr/", "/solr/#/")

    def results(self):
        connection = urlopen(f"{self.url()}&wt=python")
        response = eval(connection.read())
        return response['response']['docs'], response['response']['numFound']


class GameQuery(Query):
    def __init__(self, query, *, rows=10):
        super().__init__(query, qop="OR",
                         qf="Genres^4 ResponseName^3 WikiData^2 PromotionalDescription", def_type="edismax", rows=rows)
        self.bf = self.generate_boost_function()
        self.qop = self.generate_qop()

    def generate_boost_function(self):
        # dark magic here; heuristics to determine the boost function according to the query
        # return m2 default for now
        return "sum(sum(mul(0.5,Metacritic),mul(10,log(SteamSpyPlayersEstimate))),mul(15,log(RecommendationCount)))"

    def generate_qop(self):
        # dark magic; heuristics to determine the q.op according to the query
        # return OR for now
        return "OR"

    def print_results_in_pager(self):
        res = ""
        results, num_found = self.results()
        res += f"Query: {self.query}\n"
        res += f"bf: {self.bf}\n"
        res += f"q.op: {self.qop}\n"
        res += f"Found {num_found} results\n\n"
        res += "==============================================\n\n"
        for result in results:
            res += GameQuery.stringify_doc(result) + "\n"
        res += "==============================================\n\n"
        res += f"URL: {self.ui_url()}\n"
        pager(res)

    @staticmethod
    def stringify_doc(doc):
        res = ""
        for key in ["ResponseName", "Genres", "WikiData", "PromotionalDescription",
                    "ReleaseDate", "RecommendationCount", "SteamSpyPlayersEstimate",
                    "IsFree", "Categories", "Platforms", "Metacritic"]:
            if key not in doc:
                continue
            if type(doc[key]) == list:
                res += f"{key}: {', '.join(doc[key])}\n"
                continue
            if isinstance(doc[key], str) and len(doc[key]) > 200:
                res += f"{key}: {doc[key][:200]}...\n"
                continue
            res += f"{key}: {doc[key]}\n"
        return res
