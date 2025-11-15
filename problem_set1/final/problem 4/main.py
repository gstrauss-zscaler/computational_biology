from pandas import DataFrame

from LocalAlignment import LocalAlignment
from ScoreFunctions import default_score_function

def main():
    SEQUENCE_1 = "CCCATAGGTGCGGTAGCC"
    SEQUENCE_2 = "ATAAGGCATTGACCGTATTGCCAA"

    alignment = LocalAlignment(SEQUENCE_1, SEQUENCE_2, default_score_function)

    # Print score matrix
    print(DataFrame(alignment.get_score_matrix()))

    # Print maximum alignment path
    print(alignment.get_maximum_alignment_path())

    # Print alignmet
    aligned_sequences = alignment.get_aligments()
    print(aligned_sequences[0])
    print(aligned_sequences[1])
    

if "__main__" == __name__:
    main()