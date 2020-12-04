from enum import Enum


class TypeMap (Enum):
    """Les différentes grilles """
    A = {"name": "A", "path": "data/input/a_example.txt"}
    B = {"name": "B", "path": "data/input/b_single_arm.txt"}
    C = {"name": "C", "path": "data/input/c_few_arms.txt"}
    D = {"name": "D", "path": "data/input/d_tight_schedule.txt"}
    E = {"name": "E", "path": "data/input/e_dense_workspace.txt"}
    F = {"name": "F", "path": "data/input/f_decentralized.txt"}

    def __str__(self):
        return self.value["name"]

    def get_path(self):
        return self.value["path"]
