import sys


# TODO: add terminal states checking and converting

def parse(input_file_path):
    with open(input_file_path, "r") as input_file:
        size_of_q, size_of_sigma = [int(size) for size in input_file.readline().split()]

        index_of_initial_state = int(input_file.readline().split()[0])
        set_of_indices_of_terminal_states = \
            set(int(term) for term in list(input_file.readline().split())[1:])

        transitions = dict()
        for i in range(size_of_q):
            transitions[i] = {}

        set_of_elements = set()
        for line in range(size_of_sigma + 1):
            element = input_file.readline().split()[0]
            set_of_elements.add(element)

            for x in range(size_of_q):
                row = input_file.readline().split()
                for y in range(size_of_q):
                    if row[y] == "1":
                        if element not in transitions[x]:
                            transitions[x][element] = set()
                        transitions[x][element].add(y)

    return {"initial": {index_of_initial_state},
            "terminal": set_of_indices_of_terminal_states,
            "transitions": transitions,
            "elements": set_of_elements}


def epsilon_nfa_to_nfa(automata):
    prev = automata["transitions"]
    flag = 1
    new = {}
    while flag:
        new = {}
        flag = 0
        for state in prev:
            new[state] = {}
            for transition in prev[state].items():
                if transition[0] == '\\e':
                    for new_state in transition[1]:
                        new[state] = merge(new[state], prev[new_state])
                    flag = 1
                elif transition[0] not in new[state]:
                    new[state][transition[0]] = transition[1]
                else:
                    new[state][transition[0]].add(transition[1])
        prev = new
    automata["transitions"] = new
    return automata


def nfa_to_dfa(automata):
    prev = prepare_for_dfa(automata["transitions"])
    flag = 1
    new = {}
    while flag:
        new = {}
        flag = 0
        for state in prev:
            temp = set()  # Holds new possible states
            entries = find_entries(state, new)
            if entries:
                for entry in entries:
                    new[entry] = merge(new[entry], prev[state])
                    temp = temp | set(tuple(i) for i in new[entry].values())
            else:
                new[state] = prev[state]
                temp = temp | set(tuple(i) for i in new[state].values())

            for key in temp:
                other_entries = find_entries(key, new)
                if not other_entries:
                    new[tuple(key)] = {}
                    if set(key) not in list(set(i) for i in prev):
                        flag = 1
                else:
                    for entry in other_entries:
                        if len(entry) < len(key):
                            if set(key) not in list(set(i) for i in new):
                                new[tuple(key)] = {}
                                if set(key) not in list(set(i) for i in prev):
                                    flag = 1
                            new[tuple(key)] = merge(new[tuple(key)], new[entry])
                            del new[entry]
                        elif len(entry) > len(key):
                            new[entry] = merge(new[entry], new[tuple(key)])
                            del new[tuple(key)]

        prev = new
    automata["transitions"] = new
    return automata


def dfa_to_cdfa(automata):
    absorbing_state = "absorbing"
    flag = 0
    for state in automata["transitions"]:
        for element in automata["elements"] - {'\\e'}:
            if element not in automata["transitions"][state]:
                flag = 1
                automata["transitions"][state][element] = {absorbing_state}
    if flag:
        automata["transitions"][(absorbing_state,)] = {}
        for element in automata["elements"] - {'\\e'}:
            automata["transitions"][(absorbing_state,)][element] = {absorbing_state}
    return automata


def merge(dict1, dict2):
    for transition in dict2.items():
        if transition[0] in dict1:
            dict1[transition[0]] | set(transition[1])
        else:
            dict1[transition[0]] = transition[1]
    return dict1


def find_entries(state, dct):
    entries = set()
    for key in dct:
        if set(state) & set(key):
            entries.add(key)
    return entries


def prepare_for_dfa(dct):
    new_dct = {}
    for i in dct.items():
        new_dct[(i[0],)] = i[1]
    return new_dct


if __name__ == '__main__':
    # TODO: add checking of the argument provided
    given_file_path = sys.argv[1]

    # Parsing file to get automata represented as a list:
    automata = parse(given_file_path)

    # Epsilon-NFA to NFA:
    automata = epsilon_nfa_to_nfa(automata)

    # NFA to DFA:
    automata = nfa_to_dfa(automata)

    # DFA to cDFA:
    automata = dfa_to_cdfa(automata)

    # Results:
    # TODO: write results to a file

    for i in automata["transitions"]:
        print(f"{i}    " + str(automata["transitions"][i]))
