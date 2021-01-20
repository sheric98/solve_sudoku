nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class Tile:
    def __init__(self, x=None, y=None, num=None, tile=None):
        if tile is None:
            self.x = x
            self.y = y
            self.num = num
            self.init_num = None
            self.possible = set(nums)
            self.mc_nums = set(nums)
            self.groups = []
        else:
            self.x = tile.x
            self.y = tile.y
            self.num = tile.num
            self.init_num = tile.init_num
            self.possible = tile.possible.copy()
            self.mc_nums = tile.mc_nums.copy()
            self.groups = []

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def add_group(self, group):
        self.groups.append(group)

    def get_possible(self):
        self.possible = set.intersection(*([g.missing for g in self.groups] + [self.mc_nums, self.possible]))
        return len(self.possible)

    def update_mc(self, mc_nums):
        if mc_nums == self.mc_nums:
            return False
        self.mc_nums = set.intersection(self.mc_nums, mc_nums)
        if self.init_num is not None or len(self.possible) == 1:
            return False
        return True

    def update_impossible(self, num, group):
        for g in self.groups:
            if group != g:
                g.remove_mc_tile(num, self)
        return set(self.groups)

    def update_num(self, num):
        if num not in self.possible:
            return None
        self.num = num
        update_tiles = set()
        for group in self.groups:
            to_update = group.update_tile(self, num)
            if to_update is None:
                return None
            update_tiles.update(to_update)
        return update_tiles

    def copy(self):
        return Tile(tile=self)
