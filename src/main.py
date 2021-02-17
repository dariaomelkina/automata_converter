import sys


def parse(input_file_path):
    # TODO: create some kind of object to hold these transitions
    element_transitions = dict()  # element: (start_state, end_state)
    state_transitions = dict()  # start_state: (element, end_state)
    with open(input_file_path, "r") as input_file:
        size_of_q, size_of_sigma = [int(size) for size in input_file.readline().split()]

        index_of_initial_state = int(input_file.readline().split()[0])
        list_of_indices_of_terminal_states = \
            [int(term) for term in list(input_file.readline().split())[1:]]

        for line in range(size_of_sigma + 1):
            element = input_file.readline().split()[0]
            element_transitions[element] = []

            for x in range(size_of_q):
                row = input_file.readline().split()

                if x not in state_transitions:
                    state_transitions[x] = []

                for y in range(size_of_q):
                    if row[y] == "1":
                        element_transitions[element].append((x, y))
                        state_transitions[x].append((element, y))

    return index_of_initial_state, list_of_indices_of_terminal_states, element_transitions, state_transitions


if __name__ == '__main__':
    # TODO: add checking of the argument provided
    given_file_path = sys.argv[1]

    # Parsing file to get automata represented as a list:
    # [index of initial state, list of indices of terminal states,
    #  transitions: element:[(pair of states), ....]]
    automata = parse(given_file_path)

    # If we have epsilon-NFA, convert it to NFA:
    if '\\e' in automata[2]:
        for transition in automata[2]['\\e']:
            start_state = transition[0]
            end_state = transition[1]
            # TODO: додати перевірку чи виходимо з початкового стану, тоді і наступний стан зробити початковим
            if end_state in automata[1]:
                automata[1].append(start_state)

            for end_transition in automata[3][end_state]:
                automata[3][start_state].append(end_transition)
                automata[2][end_transition[0]].append((start_state, end_transition[1]))

        del automata[2]['\\e']

    print(automata)