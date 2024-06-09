from .parsers import BasicParser

def create_parser() -> BasicParser:
    valid_organism = False

    while not valid_organism:
        organism_or_id: str = input('Введите название организма или идентификационный номер из БД Taxonomy NCBI: ')
        organism: str = None
        ncbi_id: int = None

        if organism_or_id.isdigit():
            ncbi_id = int(organism_or_id)
            valid_organism = True
        elif ' ' in organism_or_id:
            organism = organism_or_id
            valid_organism = True
        else:
            print('\nВведено некорректное название или номер организма. Попробуйте ещё раз.')

    gene: str = input('Введите название гена: ')
    return BasicParser(ncbi_id=ncbi_id, organism=organism, gene=gene)
