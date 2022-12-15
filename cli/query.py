import os
from urllib.request import urlopen
from urllib.parse import urlencode
from pydoc import pager

SOLR_QUERY_URL = "http://127.0.0.1:8983/solr/games_tuned/query"
SOLR_MLT_URL = "http://127.0.0.1:8983/solr/games_tuned/mlt"

script_dir = os.path.dirname(__file__)
rel_path = "gamer_dict.txt"
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as f:
    GAMER_DICT = [line.rstrip().lower() for line in f]


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

    def url(self, baseUrl):
        query_fields = {
            "q": self.query,
            "q.op": self.qop,
            "defType": self.def_type,
            "bf": self.bf,
            "fq": self.fq,
            "qf": self.qf,
            "rows": self.rows
        }
        return f"{baseUrl}?{urlencode(query_fields)}"

    def query_url(self):
        return f"{self.url(SOLR_QUERY_URL)}&wt=python"

    def mlt_url(self, query):
        query_fields = {
            "q": query,
            "q.op": self.qop,
            "defType": self.def_type,
            "bf": self.bf,
            "fq": self.fq,
            "qf": self.qf,
            "mlt.fl": "WikiData,PromotionalDescription" + (",EntityWikiData" if "EntityWikiData" in self.qf else ""),
            "mlt.qf": self.qf
        }
        return f"{SOLR_MLT_URL}?{urlencode(query_fields)}&wt=python"

    def ui_url(self):
        return self.url(SOLR_QUERY_URL).replace("/solr/", "/solr/#/")

    def results(self):
        query_connection = urlopen(self.query_url())
        query_response = eval(query_connection.read())
        mlt_results = {}
        for item in query_response['response']['docs']:
            mlt_connection = urlopen(self.mlt_url(item["ResponseName"]))
            mlt_response = eval(mlt_connection.read())
            mlt_results[item["ResponseName"]] = [i['ResponseName'] for i in mlt_response['response']['docs']]
        return query_response['response']['docs'], query_response['response']['numFound'], mlt_results


class GameQuery(Query):
    def __init__(self, query, *, rows=10, use_bf=True, use_entities_data=False, use_gamer_profile=False):
        qf = "ResponseName^4 Genres^3 WikiData^2 PromotionalDescription"
        if use_entities_data:
            qf += " EntityWikiData"

        super().__init__(query, qop="OR", qf=qf, def_type="edismax", rows=rows)

        if use_bf:
            gamer_dict_occurences, self.bf = self.generate_boost_function(
                use_gamer_profile=use_gamer_profile)
        else:
            gamer_dict_occurences = False

        self.qop = self.generate_qop(gamer_dict_occurences)

    def generate_boost_function(self, *, use_gamer_profile):
        # STANDARD COEFFICIENTS
        # Metacritic ranges from 0 to 100: 0.5 * 100 = 50
        # SteamSpyPlayersEstimate ranges from 0 to about 10000000: 10 * log(10000000) = 23.02585092994046
        # RecommendationCount ranges from 0 to about 100000: 15 * log(100000) = 17.26941802993629
        # 50 + 23.02585092994046 + 17.26941802993629 = 90.29526895987675
        # Dividing by 5 gives a boost function that ranges from 1 to 36
        # Query fields are boosted by 4+3+2+1+1 = 11 * len(query.split())

        # COEFFICIENT CALCULATION BASED ON THE USER'S PROFILE
        metacritic_coefficient = 0.5
        steamspy_coefficient = 10
        recommendation_coefficient = 15

        gamer_dict_occurences = 0
        if use_gamer_profile:
            # if the query contains entries from the gamer dictionary, boost recommendation count and decrease steamspy
            lower_query_split = self.query.lower().split()
            for entry in GAMER_DICT:
                for word in entry.lower().split():
                    if word in lower_query_split:
                        gamer_dict_occurences += 1
                        break

            recommendation_coefficient += gamer_dict_occurences * 3
            if gamer_dict_occurences > 0:
                steamspy_coefficient -= gamer_dict_occurences * 3
                metacritic_coefficient += gamer_dict_occurences * 0.1
            if steamspy_coefficient < 0:
                steamspy_coefficient = 0

            # boost metacritic as long as the query length increases
            metacritic_coefficient += len(self.query.split()) * 0.05

        return gamer_dict_occurences, f"div(sum(sum(mul({metacritic_coefficient},Metacritic),mul({steamspy_coefficient},log(SteamSpyPlayersEstimate))),mul({recommendation_coefficient},log(RecommendationCount))),5)"

    def generate_qop(self, gamer_dict_occurences):
        return "AND" if gamer_dict_occurences >= 2 else "OR"

    def print_results_in_pager(self):
        res = ""
        results, num_found, mlt_results = self.results()
        res += f"Query: {self.query}\n"
        res += f"bf: {self.bf}\n"
        res += f"q.op: {self.qop}\n"
        res += f"Found {num_found} results\n\n"
        res += "==============================================\n\n"
        for result in results:
            res += GameQuery.stringify_doc(result)
            res += f"Related results: {', '.join(mlt_results[result['ResponseName']])}" + "\n\n"
        res += "==============================================\n\n"
        res += f"URL: {self.ui_url()}\n"
        pager(res)

    @staticmethod
    def stringify_doc(doc):
        res = ""
        for key in ["ResponseName", "Genres", "WikiData", "PromotionalDescription",
                    "ReleaseDate", "RecommendationCount", "SteamSpyPlayersEstimate",
                    "Metacritic"]:
            if key not in doc:
                continue
            if key == "PromotionalDescription" and "WikiData" in doc and doc["WikiData"] != "":
                continue
            if type(doc[key]) == list:
                res += f"{key}: {', '.join(doc[key])}\n"
                continue
            if isinstance(doc[key], str) and len(doc[key]) > 500:
                res += f"{key}: {doc[key][:500]}...\n"
                continue
            res += f"{key}: {doc[key]}\n"
        return res
