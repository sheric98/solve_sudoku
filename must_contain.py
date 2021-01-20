class MustContain:
    def __init__(self, idxs, num):
        self.idxs = idxs
        self.num = num

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return hash(id(self))

    def get_key(self):
        return tuple(self.idxs)

    def remove_idx(self, idx):
        try:
            self.idxs.remove(idx)
            return True
        except ValueError:
            return False

    def clear(self):
        self.idxs = []

    def copy(self):
        return MustContain(self.idxs.copy(), self.num)
