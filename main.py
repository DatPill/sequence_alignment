from typing import Generator

from Bio import AlignIO
from Bio.Align import Alignment, MultipleSeqAlignment, PairwiseAligner
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# from parsing import create_parser
# from parsing.parsers import BasicParser


def main():
    # first_gene: BasicParser = create_parser()
    # first_sequence: Seq = first_gene.parse()
    # print(first_sequence)

    # second_gene: BasicParser = create_parser()
    # second_sequence: Seq = second_gene.parse()
    # print(second_sequence)

    input_filename: str = input('Укажите путь к файлу (с названием): ').strip('"')
    format: str = input('Укажите формат файла: ').lower().lstrip('.')

    output_filepath: str = input('Укажите папку, в которую необходимо сохранить файл с '
                                 'выравненными последовательностями: ').strip('"')
    output_filename: str = (input('Укажите имя файла с выравненными последовательностями: '))


    aligner: PairwiseAligner = PairwiseAligner(mode='global', match_score=1, mismatch_score=-1)

    alignments: Generator[MultipleSeqAlignment] = AlignIO.parse(input_filename, format)
    alignments: list[SeqRecord] = [record for alignment in alignments for record in alignment]



    for first_sequence_index in range(len(alignments)-1):
        for second_sequence_index in range(first_sequence_index+1, len(alignments)):
            first_sequence: Seq
            second_sequence: Seq
            first_sequence, second_sequence = alignments[first_sequence_index], alignments[second_sequence_index]

            alignment: Alignment
            for alignment in aligner.align(first_sequence, second_sequence):
                print('\n=== START ========================================================================')
                print(f"Score = {alignment.score}:")
                print(alignment)
                print('=== END ===========================================================================\n')

            with open(f'{output_filepath}/{output_filename}.txt', 'a') as file:
                file.write(f'=== START ========================================================================\n')
                file.write(f"Score = {alignment.score}:\n")
                file.write(f'{alignment}\n')
                file.write('=== END ===========================================================================\n\n')



if __name__ == '__main__':
    main()
