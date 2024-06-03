class BasicParser:
    _entries = 1

    def __init__(self, ncbi_id: int = None, organism: str = None, gene: str = None):
        self._ncbi_id = f'txid{ncbi_id}' if ncbi_id else None
        self._organism = f'"{organism}"' if organism else None

    @property
    def ncbi_id(self):
        return self._ncbi_id.lstrip('txid')

    @ncbi_id.setter
    def ncbi_id(self, value):
        if isinstance(value, int) and value > 0:
            self._ncbi_id = f'txid{value}'
        else:
            raise ValueError("NCBI ID must be a positive integer.")

    @property
    def organism(self):
        return self._organism.strip('"')

    @organism.setter
    def organism(self, value):
        if isinstance(value, str) and value.strip():
            self._organism = value
        else:
            raise ValueError("Organism name must be a non-empty string.")
