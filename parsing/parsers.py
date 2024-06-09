import asyncio


from Bio import Entrez, SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature


class BasicParser:
    def __init__(
            self,
            ncbi_id: int = None,
            organism: str = None,
            gene: str = None,
            entries: int = 1
        ):

        # TODO: validate on initialization
        self._ncbi_id = f'txid{ncbi_id}' if ncbi_id else None
        self._organism = f'"{organism}"' if organism else None
        self.gene = gene
        self.entries = entries

    @property
    def ncbi_id(self):
        return self._ncbi_id.lstrip('txid')
    @ncbi_id.setter
    def ncbi_id(self, value):
        if self.ncbi_id_valid(value):
            self._ncbi_id = f'txid{value}'
        else:
            raise ValueError("NCBI ID must be a positive integer.")

    @property
    def organism(self):
        return self._organism.strip('"')
    @organism.setter
    def organism(self, value):
        if self.organism_valid(value):
            self._organism = value.strip()
        else:
            raise ValueError("Incorrect organism name.")

    @staticmethod
    def organism_valid(organism_name: str) -> bool:
        if isinstance(organism_name, str) and ' ' in organism_name:
            return True
        return False

    @staticmethod
    def ncbi_id_valid(ncbi_id: int) -> bool:
        if isinstance(ncbi_id, int) and ncbi_id > 0:
            return True
        return False

    def parse(self) -> Seq | None:
        Entrez.email = 'Test@example.com'
        organism = self._ncbi_id if self._ncbi_id is not None else self._organism   # TODO: if bot are None

        handle = Entrez.esearch(
            db='nuccore',
            term=f'{organism}[Organism] AND RefSeq[Filter] AND {self.gene}[All Fields] NOT WGS[Filter] NOT plasmid[All Fields]',
            retmax=self.entries
        )
        record = Entrez.read(handle)

        gene_sequence = ''

        for id in record['IdList']:
            handle = Entrez.efetch(db='nuccore', id=id, rettype='gbwithparts', retmode='text')
            genomes = SeqIO.parse(handle, 'genbank')

            genome: SeqRecord
            for genome in genomes:

                gene: SeqFeature
                for gene in genome.features:

                    if 'gene' in gene.qualifiers:

                        if self.gene in gene.qualifiers['gene'][0]:  # TODO
                            start = gene.location.start
                            end = gene.location.end
                            # gene_sequence = Seq(genome.seq[start:end])
                            gene_sequence += f'>{self.gene}GI:{id}|{genome.description}\n{genome.seq[start:end]}\n'
                            break

        return gene_sequence
