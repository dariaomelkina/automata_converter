import sys

if __name__ == '__main__':
    # TODO: add checking of the argument provided
    input_file_path = sys.argv[1]

    transitions = dict()

    with open(input_file_path, "r") as input_file:
        size_of_Q, size_of_Sigma = [int(size) for size in input_file.readline().split()]

        index_of_initial_state = input_file.readline()
        list_of_indices_of_terminal_states = list(input_file.readline().split())[1:]

        for line in range(size_of_Sigma+1):
            element = input_file.readline().split()[0]
            transitions[element] = []
            for x in range(size_of_Q):
                row = input_file.readline().split()
                for y in range(size_of_Q):
                    if row[y] == "1":
                        transitions[element].append((x, y))

    print(transitions)