class State:
    def __init__(self, current_state, final_state, depth, manhattan_distance=True, weight=True):
        self.current_state = current_state
        self.final_state = final_state
        self.depth = depth
        self.manhattan_distance = self.calculate_manhattan_distance() if manhattan_distance else manhattan_distance
        self.weight = self.calculate_weight() if weight else weight

    def __str__(self):
        return "\n".join([self.current_state[0:3], self.current_state[3:6], self.current_state[6:9]])

    def full_print(self):
        print(self)
        print(f"Manhattan distance is: {self.get_manhattan_distance()}")
        print(f"Depth is: {self.get_depth()}")
        print(f"Function is: {self.get_weight()}\n")

    def get_current_state(self):
        return self.current_state

    def get_final_state(self):
        return self.final_state

    def get_manhattan_distance(self):
        return self.manhattan_distance

    def get_depth(self):
        return self.depth

    def get_weight(self):
        return self.weight

    @staticmethod
    def get_x(index):
        return index % 3

    @staticmethod
    def get_y(index):
        return index // 3

    @staticmethod
    def get_index(x, y):
        return y * 3 + x

    def get_attributes(self):
        return vars(self).values()

    def calculate_weight(self):
        return self.get_manhattan_distance() + self.get_depth()

    def compare(self):
        return self.get_current_state() == self.get_final_state()

    def is_solvable(self):
        start_state_is_odd = self.count_inversions() % 2 == 1
        final_state_is_odd = self.count_inversions(start=False) % 2 == 1
        return start_state_is_odd == final_state_is_odd

    def calculate_manhattan_distance(self):
        distance = 0
        for i in range(len(self.get_current_state())):
            x1, x2 = self.get_x(i), 0
            y1, y2 = self.get_y(i), 0
            for j in range(len(self.get_final_state())):
                if self.get_current_state()[i] == self.get_final_state()[j]:
                    x2 = self.get_x(j)
                    y2 = self.get_y(j)
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
    def min_path(list_of_states):
        min_weight = list_of_states[0].get_weight()
        j = 0
        for i in range(len(list_of_states)):
            if list_of_states[i].get_weight() <= min_weight:
                min_weight = list_of_states[i].get_weight()
                j = i
        return min_weight, j

    def move(self, direction):
        z_index = self.get_current_state().find("0")
        z_x = self.get_x(z_index)
        z_y = self.get_y(z_index)
        if direction == "left" and z_x == 0 \
                or direction == "right" and z_x >= 2 \
                or direction == "down" and z_y >= 2 \
                or direction == "up" and z_y == 0:
            return False, self
        index = 0
        if direction == "left":
            index = self.get_index(z_x - 1, z_y)
        elif direction == "up":
            index = self.get_index(z_x, z_y - 1)
        elif direction == "down":
            index = self.get_index(z_x, z_y + 1)
        elif direction == "right":
            index = self.get_index(z_x + 1, z_y)
        temp_current_state = self.get_current_state()
        temp_final_state = self.get_final_state()
        temp_current_state = self.swap(temp_current_state, index, z_index)
        state = State(temp_current_state, temp_final_state, self.get_depth() + 1)
        return True, state

    @staticmethod
    def swap(string, index1, index2):
        string = list(string)
        string[index1], string[index2] = string[index2], string[index1]
        return "".join(string)

    def path(self):
        open_path = []
        all_paths = [self]
        correct_path = [State(*self.get_attributes())]
        step = 1
        while not self.compare():
            print(f"Step {step}")
            temp_path = []
            print(f"Possible movement options ")
            for direction in ["left", "right", "up", "down"]:
                temp = self.move(direction)
                if temp[0] and temp[1] != all_paths:
                    temp_path.append(temp[1])
                    temp[1].full_print()
                    all_paths.append(temp[1])
            self.change_state(self.get_min_element(temp_path, open_path))
            min_path = self.min_path(open_path)
            if self.get_weight() > min_path[0]:
                print("Encountered the terminal node ")
                for k in range(self.get_depth() - open_path[min_path[1]].get_depth()):
                    correct_path.pop()
                print("Back to state: ")
                self.change_state(open_path[min_path[1]])
                open_path[-1], open_path[min_path[1]] = open_path[min_path[1]], open_path[-1]
                print(open_path.pop(), "\n")
            else:
                correct_path.append(State(*self.get_attributes()))
                print("Selected state: ")
                self.full_print()
            step += 1
        return correct_path

    def change_state(self, state):
        self.current_state = state.get_current_state()
        self.final_state = state.get_final_state()
        self.depth = state.get_depth()
        self.manhattan_distance = state.get_manhattan_distance()
        self.weight = state.get_weight()

    @staticmethod
    def get_min_element(temp_vector, paths):
        min_weight = temp_vector[0].get_weight()
        index = 0
        for i in range(1, len(temp_vector)):
            if temp_vector[i].get_weight() < min_weight:
                index = i
                min_weight = temp_vector[i].get_weight()
        for i in range(len(temp_vector)):
            if i != index:
                paths.append(temp_vector[i])
        return temp_vector[index]


def main():
    print("Only 3x3")
    start_state = input("Enter start state:\n")
    final_state = input("Enter final state:\n")
    state = State(start_state, final_state, 0)
    if state.is_solvable():
        path = state.path()
        print("Path is")
        for i in range(len(path)):
            print(f"Step {i + 1}:\n{path[i]}\n")
    else:
        print("Unsolvable")


if __name__ == '__main__':
    main()
