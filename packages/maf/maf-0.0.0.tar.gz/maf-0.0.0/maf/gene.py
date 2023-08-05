class Gene:
    def __init__(self, maf_fields):
        self.maf_fields = maf_fields

    @property
    def hugo_symbol(self):
        return self.maf_fields["Hugo_Symbol"]

    @property
    def chromosome(self):
        return self.maf_fields["Chromosome"]
