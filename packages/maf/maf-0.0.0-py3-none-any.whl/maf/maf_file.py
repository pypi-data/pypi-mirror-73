import csv
import functools

from maf.gene import Gene


class MafFile:
    def __init__(self, path):
        self.path = path

    @property
    @functools.lru_cache()
    def genes(self):
        with open(self.path, "r") as file:
            maf = csv.DictReader(file, delimiter="\t")
            return [Gene(row) for row in maf]
