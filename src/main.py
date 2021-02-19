import sys


# TODO: implement adequate parsing, not a parody that I have now
def parse(input_file_path):
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

    return [index_of_initial_state, list_of_indices_of_terminal_states, element_transitions, state_transitions]


def get_normal_q_representation(transitions):
    """
    :param transitions: {state:[(element1,state1), (element1, state2), ...]}
    :return: {state:{element:(state1, state2, ...), ...}
    """
    adequate_q = dict()
    for state in transitions:
        adequate_q[state] = dict()
        for transition in transitions[state]:
            if transition[0] in adequate_q[state]:  # element
                adequate_q[state][transition[0]].add(transition[1])
            else:
                adequate_q[state][transition[0]] = {transition[1]}
    return adequate_q


def epsilon_nfa_to_nfa(fa):
    # First, we will change index of initial state to a list of indexes, so algorithm can work
    fa[0] = [fa[0]]

    if '\\e' in fa[2]:
        for transition in fa[2]['\\e']:
            start_state = transition[0]
            end_state = transition[1]

            if start_state in fa[0]:
                fa[0].append(end_state)

            if end_state in fa[1]:
                fa[1].append(start_state)

            for end_transition in fa[3][end_state]:
                fa[3][start_state].append(end_transition)
                fa[2][end_transition[0]].append((start_state, end_transition[1]))

        del automata[2]['\\e']
    return fa


if __name__ == '__main__':
    # TODO: add checking of the argument provided
    given_file_path = sys.argv[1]

    # Parsing file to get automata represented as a list:
    # [index of initial state, list of indices of terminal states,
    #  transitions: element:[(pair of states), ....]
    #  state transitions: ]
    automata = parse(given_file_path)

    # If we have epsilon-NFA, convert it to NFA:
    automata = epsilon_nfa_to_nfa(automata)

    # Convert automata to DFA:
    # Initially new Q is empty
    new_element_transitions = dict()
    new_state_transitions = dict()

    # костильний метод для отримання переходів,
    # приберу його коли буду нормально парсити, а не як зараз:/
    q = get_normal_q_representation(automata[3])
    print(q)
