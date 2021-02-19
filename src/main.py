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

    return [index_of_initial_state, list_of_indices_of_terminal_states,
            element_transitions, state_transitions]


def get_normal_delta_representation(transitions):
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
    # TODO: add list of initial states
    # First, we will change index of initial state to a list of indexes, so algorithm can work
    # fa[0] = [fa[0]]

    if '\\e' in fa[2]:
        for transition in fa[2]['\\e']:
            start_state = transition[0]
            end_state = transition[1]

            # if start_state in fa[0]:
            #     fa[0].append(end_state)

            if end_state in fa[1]:
                fa[1].append(start_state)

            for end_transition in fa[3][end_state]:
                if '\\e' not in end_transition:
                    fa[3][start_state].append(end_transition)
                fa[2][end_transition[0]].append((start_state, end_transition[1]))

        del fa[2]['\\e']

    for element in fa[3]:
        for transition in fa[3][element]:
            if '\\e' in transition:
                fa[3][element].remove(transition)
    return fa


if __name__ == '__main__':
    # TODO: add checking of the argument provided
    given_file_path = sys.argv[1]

    # Parsing file to get automata represented as a list:
    # [index of initial state, list of indices of terminal states,
    #  transitions: element:[(pair of states), ....]
    #  state transitions: {state:[(element1,state1), (element1, state2), ...]} ]
    automata = parse(given_file_path)

    # If we have epsilon-NFA, convert it to NFA:
    automata = epsilon_nfa_to_nfa(automata)

    # Convert automata to DFA:
    # Initially new Q is empty, I suppose
    new_element_transitions = dict()
    new_state_transitions = dict()
    q = []
    new_delta = dict()

    # костильний метод для отримання переходів,
    # приберу його коли буду нормально парсити, а не як зараз:/
    delta = get_normal_delta_representation(automata[3])
    # for i in delta.items():
    #     print(i)

    q.append((automata[0],))

    for state in q:
        new_delta[state] = dict()

        for element in state:
            for transition in delta[element]:
                transition_state_set = delta[element][transition]
                if transition not in new_delta[state]:
                    new_delta[state][transition] = transition_state_set
                else:
                    new_delta[state][transition].union(transition_state_set)
                new_state = tuple(transition_state_set)
                # for other_state in q:
                #     if element in state:
                #         new_delta[state][transition].union(new_delta[other_state][element])
                if new_state not in q:
                    q.append(new_state)
    print(f"     {'  '.join(list(str(i) for i in range(len(automata[2]))))}")
    for i in new_delta:
        print(f"{i}   {'  '.join(list(str(i) for i in range(len(new_delta))))}")
