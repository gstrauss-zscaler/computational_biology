from typing import Callable
from Consts import Choice

class LocalAlignment:
    __sequence_1: str # The first sequence
    __sequence_2: str # The second sequence
    __score_function: Callable[[str, str, Choice], int] # The score function
    __score_matrix: list[list[int]] # A matrix of size n*m of the scores
    __pointer_matrix: list[list[tuple[int, int] | None]] # A matrix of size n*m of the pointer to the previous choice.
    __choice_matrix: list[list[Choice]] # A matrix of size n*m of the choices made (if equal we will show substitution)

    def __init__(self, sequence_1: str, sequence_2: str, score_function: Callable[[str, str, Choice], int]):
        """
        Initialize the object to allow for easy use,
        We are intializing the matrixs to allow us to call the functions out of the box.
        """

        self.__sequence_1 = sequence_1
        self.__sequence_2 = sequence_2
        self.__score_function = score_function
        self.__score_matrix = [[0 for _ in range(len(self.__sequence_1) + 1)] for _ in range(len(self.__sequence_2) + 1)]
        self.__pointer_matrix = [[None for _ in range(len(self.__sequence_1) + 1)] for _ in range(len(self.__sequence_2) + 1)]
        self.__choice_matrix = [[Choice.NONE for _ in range(len(self.__sequence_1) + 1)] for _ in range(len(self.__sequence_2) + 1)]
        self._fill_matrixs_cells()

    def get_score_matrix(self) -> list[list[int]]:
        """
        Returns the score matrix for local alignment.
        """
        return self.__score_matrix

    def get_pointer_matrix(self) -> list[list[tuple[int, int] | None]]:
        """
        Returns the pointer to the previous cell in the sequence of choices or None if its the end.
        """

        return self.__pointer_matrix
    
    def get_choice_matrix(self) -> list[list[Choice]]:
        return self.__choice_matrix

    def get_maximum_alignment_path(self) -> list[tuple[int, int]]:
        """
        Returns a possible maximum alignment path.
        """

        last_cell = self._get_maximum_alignment_cell()
        result_path = [last_cell]
        self._trace_back_path_from_cell(last_cell[0], last_cell[1], result_path)

        # We traced back the path, so we need to reverse it
        return list(reversed(result_path))

    def get_aligments(self) -> tuple[str, str]:
        alignment_path = self.get_maximum_alignment_path()
        aligned_1 = ""
        aligned_2 = ""
        for alignment in alignment_path:
            aligned_chars = self._get_aligned_values(alignment)
            aligned_1 += aligned_chars[0]
            aligned_2 += aligned_chars[1]
        
        return aligned_1, aligned_2

    ### private:
    def _calculate_possible_choices(self, index_1: int, index_2: int) -> dict[Choice, int]:
        """
        For a given cell, calculates all the given options of choices and their scores.
        """

        if 0 == index_1 == index_2:
            # In (0, 0) we have no options
            return {
                        Choice.NONE: 0
                    }
        
        if 0 == index_1:
            # In (0, a) we only have one choice
            return {
                        Choice.NONE: 0,
                        Choice.GAP_RIGHT: self.__score_matrix[index_2 - 1][index_1] + self.__score_function(None, self.__sequence_2[index_2 - 1], Choice.GAP_RIGHT)
                    }


        if 0 == index_2:
            # In (a, 0) we only have one choice
            return {
                        Choice.NONE: 0,
                        Choice.GAP_DOWN: self.__score_matrix[index_2][index_1 - 1] + self.__score_function(self.__sequence_1[index_1 - 1], None, Choice.GAP_DOWN)
                    }
        
        # The index in the sequences are actually one less then in the matrix.
        index_1 = index_1 - 1
        index_2 = index_2 - 1

        return {
                    # A long form of: map choice to previous cell score + the cost of the choice.
                    Choice.NONE: 0,
                    Choice.SUBSTITUTION: self.__score_matrix[index_2][index_1] + self.__score_function(self.__sequence_1[index_1], self.__sequence_2[index_2], Choice.SUBSTITUTION),
                    Choice.GAP_RIGHT: self.__score_matrix[index_2][index_1 + 1] + self.__score_function(self.__sequence_1[index_1], self.__sequence_2[index_2], Choice.GAP_RIGHT),
                    Choice.GAP_DOWN: self.__score_matrix[index_2 + 1][index_1] + self.__score_function(self.__sequence_1[index_1], self.__sequence_2[index_2], Choice.GAP_DOWN)
                }
        
    def _calculate_optimal_choice(self, index_1: int, index_2: int) -> Choice:
        """
        For a given cell returns one of the best options of the cell.
        """

        options = self._calculate_possible_choices(index_1, index_2)
        optimal_choice = max(options, key=options.get)
        if 0 == options.get(optimal_choice):
            return Choice.NONE # If we reach 0 we should always choose NONE.

        return optimal_choice

    def _fill_pointer_matrix_cell(self, index_1: int, index_2: int, optimal_choice: Choice) -> None:
        """
        Fill the cell at (index_2, index_1) in the pointer matrix with the optimal choice.
        """
        
        if Choice.SUBSTITUTION == optimal_choice:
            self.__pointer_matrix[index_2][index_1] = (index_2 - 1, index_1 - 1)
        
        if Choice.GAP_RIGHT == optimal_choice:
            self.__pointer_matrix[index_2][index_1] = (index_2 - 1, index_1)
        
        if Choice.GAP_DOWN == optimal_choice:
            self.__pointer_matrix[index_2][index_1] = (index_2, index_1 - 1)

        if Choice.NONE == optimal_choice:
            self.__pointer_matrix[index_2][index_1] = None
            return
        
        # We have a bug where if the previous cell is 0 we don't want to point to it, because we are the start.
        x, y = self.__pointer_matrix[index_2][index_1]
        if 0 == self.__score_matrix[x][y]:
            self.__pointer_matrix[index_2][index_1] = None
        

    def _fill_score_matrix_cell(self, index_1: int, index_2: int, optimal_choice: Choice) -> None:
        """
        Fill the cell at (index_2, index_1) in the score matrix with the optimal choice.
        """

        score = self.__score_function(self.__sequence_1[index_1 - 1], self.__sequence_2[index_2 - 1], optimal_choice)
        
        if Choice.SUBSTITUTION == optimal_choice:
            self.__score_matrix[index_2][index_1] = self.__score_matrix[index_2 - 1][index_1 - 1] + score
        
        if Choice.GAP_RIGHT == optimal_choice:
            self.__score_matrix[index_2][index_1] = self.__score_matrix[index_2 - 1][index_1] + score
        
        if Choice.GAP_DOWN == optimal_choice:
            self.__score_matrix[index_2][index_1] = self.__score_matrix[index_2][index_1 - 1] + score

        if Choice.NONE == optimal_choice:
            self.__score_matrix[index_2][index_1] = 0

    def _fill_choice_matrix_cell(self, index_1: int, index_2: int, optimal_choice: Choice) -> None:
        self.__choice_matrix[index_2][index_1] = optimal_choice

    def _fill_matrixs_cell(self, index_1: int, index_2: int) -> None:
        """
        Fill all the matrixs in the cell (index_2, index_1)
        """

        optimal_choice = self._calculate_optimal_choice(index_1, index_2)
        self._fill_score_matrix_cell(index_1, index_2, optimal_choice)
        self._fill_pointer_matrix_cell(index_1, index_2, optimal_choice)
        self._fill_choice_matrix_cell(index_1, index_2, optimal_choice)
    
    def _fill_matrixs_cells(self) -> None:
        """
        Fill all the matrixs.
        """

        for i in range(len(self.__sequence_1) + 1):
            for j in range(len(self.__sequence_2) + 1):
                self._fill_matrixs_cell(i, j)

    def _get_maximum_alignment_cell(self) -> tuple[int, int]:
        """
        Finds the max score location.
        """

        # For a more clean code
        matrix = self.__score_matrix
        return max(((i, j) for i, row in enumerate(matrix) for j, column in enumerate(row)), key=lambda p: matrix[p[0]][p[1]])

    def _find_previous_cell(self, row: int, column: int) -> tuple[int, int] | None:
        """
        Finds the previous cell in the sequence.
        """

        return self.__pointer_matrix[row][column]

    def _trace_back_path_from_cell(self, row: int, column: int, result_path: list[tuple[int, int]]) -> None:
        """
        Recursively fills result_path with all the cells in an optimal alignment sequence.
        """
        
        previous_cell = self._find_previous_cell(row, column)
        if None == previous_cell:
            return
        
        result_path.append(previous_cell)
        return self._trace_back_path_from_cell(previous_cell[0], previous_cell[1], result_path)

    def _get_aligned_values(self, alignment: tuple[int, int]) -> tuple[str, str]:
        """
        Converting from alignemnts to strings
        """

        choice = self.__choice_matrix[alignment[0]][alignment[1]]
        
        if Choice.SUBSTITUTION == choice:
            return self.__sequence_1[alignment[1] - 1], self.__sequence_1[alignment[1] - 1]

        if Choice.GAP_RIGHT:
            return "-", self.__sequence_2[alignment[0] - 1]
        
        if Choice.GAP_DOWN:
            return self.__sequence_1[alignment[1] - 1], "-"
        
        raise RuntimeError("We shouldn't have Choice.NONE in pointer matrix other then start of sequences.")