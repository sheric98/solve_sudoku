from enum import Enum
from must_contain import MustContain


idxs = [0, 1, 2, 3, 4, 5, 6, 7, 8]
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class GroupType(Enum):
    ROW = 1
    COL = 2
    SQUARE = 3


class Group:
    def __init__(self, group_type=None, idx=None, group=None):
        self.tiles = [None] * 9
        if group is None:
            self.missing = set(nums)
            self.unoccupied = set(idxs)
            self.type = group_type
            self.idx = idx
            self.must_contain = []
            for i in range(9):
                self.must_contain.append(MustContain(idxs[:], i + 1))
            self.idxs_mc = {tuple(idxs): set(self.must_contain)}
        else:
            self.missing = group.missing.copy()
            self.unoccupied = group.unoccupied.copy()
            self.type = group.type
            self.idx = group.idx
            self.must_contain = [mc.copy() for mc in group.must_contain]
            mc_map = {}
            for i in range(9):
                mc_map[group.must_contain[i]] = self.must_contain[i]
            self.idxs_mc = {}
            for k, v in group.idxs_mc.items():
                self.idxs_mc[k] = set([mc_map[mc] for mc in v])

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return hash(id(self))

    def add_tile(self, tile):
        idx = self.tile_to_idx(tile)
        self.tiles[idx] = tile
        tile.add_group(self)

    def update_tile(self, tile, num):
        idx = self.tile_to_idx(tile)
        self.missing.remove(num)
        self.unoccupied.remove(idx)
        mc = self.must_contain[num - 1]
        mc.clear()
        update_dict = {}
        for idxs, mcs in self.idxs_mc.items():
            key_list = list(idxs)
            if mc in mcs:
                mcs.remove(mc)
            if idx in key_list:
                key_list.remove(idx)
                new_key = tuple(key_list)
                for check_mc in mcs:
                    check_mc.remove_idx(idx)
                update_dict[(idxs, new_key)] = mcs
        for (old_k, new_k), mcs in update_dict.items():
            del self.idxs_mc[old_k]
            if len(mcs) > 0:
                if new_k not in self.idxs_mc:
                    self.idxs_mc[new_k] = set()
                self.idxs_mc[new_k].update(mcs)
        updated_groups = set()
        updated_tiles = set()
        for tile in self.tiles:
            if tile and tile.num == 0:
                groups = tile.update_impossible(num, self)
                updated_groups.update(groups)
                updated_tiles.add(tile)
        for group in updated_groups:
            to_update = group.check_mc()
            if to_update is None:
                return None
            updated_tiles.update(to_update)
        next_updates = set()
        for tile in updated_tiles:
            possible_len = tile.get_possible()
            if possible_len == 0:
                return None
            if possible_len == 1:
                next_updates.add(tile)
        return next_updates

    def tile_to_idx(self, tile):
        if self.type == GroupType.ROW:
            return tile.x
        elif self.type == GroupType.COL:
            return tile.y
        else:
            sq_x = self.idx % 3
            sq_y = self.idx // 3
            return 3 * (tile.y - 3 * sq_y) + tile.x - 3 * sq_x

    def remove_mc(self, num, idx):
        mc = self.must_contain[num - 1]
        prev_key = mc.get_key()
        if not mc.remove_idx(idx):
            return
        new_key = mc.get_key()
        prev_set = self.idxs_mc[prev_key]
        prev_set.remove(mc)
        if len(prev_set) == 0:
            del self.idxs_mc[prev_key]
        if new_key not in self.idxs_mc:
            self.idxs_mc[new_key] = set()
        self.idxs_mc[new_key].add(mc)

    def remove_mc_tile(self, num, tile):
        self.remove_mc(num, self.tile_to_idx(tile))

    def check_mc(self):
        updated_tiles = set()
        for idxs, mcs in self.idxs_mc.items():
            if len(idxs) < len(mcs):
                return None
            if len(idxs) == len(mcs):
                nums = set([mc.num for mc in mcs])
                for idx in idxs:
                    tile = self.tiles[idx]
                    if tile.update_mc(nums):
                        updated_tiles.add(tile)
        return updated_tiles

    def complete(self):
        return len(self.missing) == 0

    def copy(self):
        return Group(group=self)
