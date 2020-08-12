from sport.apps.core.models import Serie


class Stats:
    def __init__(self, user):
        self.stats = {}
        self.series = Serie.objects.filter(user=user)
        self.user_exos = None

    def all(self):
        self.get_n_sceances()
        self.get_mean_exercice_per_sceance()

    def get_n_sceances(self):
        self.stats['n_sceances'] = len(set([s.get_date() for s in self.series]))
        return self.stats['n_sceances']

    def get_mean_exercice_per_sceance(self):
        if 'n_sceances' not in self.stats:
            self.get_n_sceances()

        l = [(s.get_date(), s.exercice_id) for s in self.series]

        # map: (date, (exo, ...))
        d = {}
        for e in l:
            _date, exo = e
            if _date not in d:
                d[_date] = []
            d[_date].append(exo)

        dd = {}
        for k, v in d.items():
            dd[k] = {}
            for elem in v:
                print(elem)
                if elem not in dd[k]:
                    dd[k][elem] = 0
                dd[k][elem] += 1
        ddd = {}
        for k, v in dd.items():
            ddd[k] = len(v)

        mean = 0
        for k, v in ddd.items():
            mean += v
        mean /= len(ddd)

        self.stats['mean_exercice_per_sceance'] = mean
        return self.stats['mean_exercice_per_sceance']

    def get_sceance_length(self, exo_id):
        if 'n_sceances' not in self.stats:
            self.get_n_sceances()

