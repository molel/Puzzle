from random import choice


class State:
    directions = {
        "left": -1,
        "right": 1,
        "up": -3,
        "down": 3,
    }

    def __init__(self, current_state, final_state, depth):
        self.current_state = current_state
        self.final_state = final_state
        self.depth = depth
        self.manhattan_distance = self.calculate_manhattan_distance()
        self.z_index = current_state.find("0")

    def get_current_state(self):
        return self.current_state

    def get_final_state(self):
        return self.final_state

    def get_manhattan_distance(self):
        return self.manhattan_distance

    def get_depth(self):
        return self.depth

    def get_z_index(self):
        return self.z_index

    def compare(self):
        return self.get_current_state() == self.get_final_state()

    def is_solvable(self):
        start_state_is_odd = self.count_inversions() % 2 == 1
        final_state_is_odd = self.count_inversions(start=False) % 2 == 1
        return start_state_is_odd == final_state_is_odd

    def calculate_manhattan_distance(self):
        distance = 0
        for i in range(len(self.get_current_state())):
            x1 = i % 3
            y1 = i // 3
            for j in range(len(self.get_final_state())):
                if self.get_current_state()[i] == self.get_final_state()[j]:
                    x2 = j % 3
                    y2 = j // 3
                    distance += abs(x2 - x1) + abs(y2 - y1)
        return distance

    def count_inversions(self, start=True):
        count = 0
        state = self.get_current_state() if start else self.get_final_state()
        for i in range(len(state)):
            for j in range(len(state)):
                first_element = state[i]
                second_element = state[j]
                if first_element == "0" or second_element == "0":
                    continue
                elif second_element < first_element:
                    count += 1
        return count

    @staticmethod
    def swap(string, index1, index2):
        string = list(string)
        string[index1], string[index2] = string[index2], string[index1]
        return "".join(string)

    @staticmethod
    def find_minimal_state(states):
        min_distance = min([state.get_manhattan_distance() for state in states])
        result = []
        for state in states:
            if state.get_manhattan_distance() == min_distance:
                result.append(state)
        return choice(result)

    def change_current_state(self, state):
        self.current_state = state.get_current_state()
        self.final_state = state.get_final_state()
        self.depth = state.get_depth()
        self.manhattan_distance = state.get_manhattan_distance()
        self.z_index = state.get_z_index()

    @staticmethod
    def rollback_state(states, target_state):
        for state in reversed(states):
            if state != target_state:
                states.pop(-1)
            else:
                break

    def move(self, direction):
        if direction == "left" and self.get_z_index() % 3 != 0 or \
                direction == "right" and self.get_z_index() % 3 != 2 or \
                direction == "up" and self.get_z_index() > 2 or \
                direction == "down" and self.get_z_index() < 6:
            new_state = self.swap(self.get_current_state(), self.z_index,
                                  self.z_index + State.directions[direction])
            return State(new_state, self.final_state, self.get_depth() + 1)
        else:
            return

    def get_new_states(self, open_states):
        new_states = []
        for direction in State.directions.keys():
            new_state = self.move(direction)
            if new_state and new_state.get_current_state() not in open_states:
                new_states.append(new_state)
        return new_states

    def path(self, current_path, open_states):
        if not self.compare():
            new_states = self.get_new_states(open_states)
            if len(new_states) == 0:
                self.rollback_state(current_path, current_path[-2])
            else:
                next_state = self.find_minimal_state(new_states)
                self.depth += 1
                open_states.append(next_state.get_current_state())
                current_path.append(next_state.get_current_state())
                self.change_current_state(next_state)
            return self.path(current_path, open_states)
        else:
            return current_path


def find_path_and_depth(start_state, final_state):
    try:
        state = State(start_state, final_state, 0)
        path = state.path([state.get_current_state()], [state.get_current_state()])
        return path, state.get_depth()
    except:
        return find_path_and_depth(start_state, final_state)


def main():
    print("Only 3x3")
    # start_state = input("Enter start state:\n")
    # final_state = input("Enter final state:\n")
    start_state = "872651430"
    final_state = "123456780"
    state = State(start_state, final_state, 0)
    if state.is_solvable():
        path, depth = find_path_and_depth(start_state, final_state)
        print(f"Length is {len(path)}")
        for i in range(len(path)):
            print(f"Step {i}:\n{path[i][0:3]}\n{path[i][3:6]}\n{path[i][6:9]}\n")
        print(f"Depth is {depth}")
    else:
        print("Unsolvable")


if __name__ == '__main__':
    main()
