from group import Group, GroupType
from tile import Tile


class Board:
    def __init__(self, board_str=None, board=None):
        if board is None:
            self.groups = []
            self.all_tiles = []
            self.unsolved = set()
            self.to_update = set()
            for i in range(9):
                self.groups.append(Group(group_type=GroupType.ROW, idx=i))
            for i in range(9):
                self.groups.append(Group(group_type=GroupType.COL, idx=i))
            for i in range(9):
                self.groups.append(Group(group_type=GroupType.SQUARE, idx=i))
            for y in range(9):
                row = []
                for x in range(9):
                    tile = Tile(x=x, y=y, num=0)
                    self.tile_to_groups(tile)
                    row.append(tile)
                    self.unsolved.add(tile)
                self.all_tiles.append(row)
            for idx, c in enumerate(board_str):
                num = int(c)
                if num > 0:
                    x = idx % 9
                    y = idx // 9
                    tile = self.all_tiles[y][x]
                    tile.init_num = num
                    self.to_update.add(tile)
        else:
            self.groups = []
            self.all_tiles = []
            for group in board.groups:
                self.groups.append(group.copy())
            for y in range(9):
                row = []
                for x in range(9):
                    tile = board.all_tiles[y][x].copy()
                    self.tile_to_groups(tile)
                    row.append(tile)
                self.all_tiles.append(row)
            self.unsolved = set([self.all_tiles[tile.y][tile.x] for tile in board.unsolved])
            self.to_update = set()

    def tile_to_groups(self, tile):
        self.groups[tile.y].add_tile(tile)
        self.groups[9 + tile.x].add_tile(tile)
        square_num = 3 * (tile.y // 3) + tile.x // 3
        self.groups[18 + square_num].add_tile(tile)

    def basic_updates(self, update_tiles):
        if len(update_tiles) == 0:
            return True
        next_updates = set()
        for tile in update_tiles:
            if tile.init_num:
                tile_updates = tile.update_num(tile.init_num)
            else:
                tile_updates = tile.update_num(list(tile.possible)[0])
            if tile_updates is None:
                return False
            next_updates.update(tile_updates)
            self.unsolved.remove(tile)
            if tile in next_updates:
                next_updates.remove(tile)
        return self.basic_updates(next_updates)

    def solve_board(self):
        if not self.basic_updates(self.to_update):
            return []
        if self.is_complete():
            return [self]
        tile = self.get_branch()
        vals = list(tile.possible)
        ret = []
        for val in vals:
            next_board = self.copy()
            next_tile = next_board.all_tiles[tile.y][tile.x]
            next_tile.init_num = val
            next_board.to_update.add(next_tile)
            ret.extend(next_board.solve_board())
        return ret

    def get_branch(self):
        unsolved = list(self.unsolved)
        return min(unsolved, key=lambda t: len(t.possible))

    def is_complete(self):
        return len(self.unsolved) == 0

    def board_str(self):
        ret = ''
        for y in range(9):
            for x in range(9):
                ret += str(self.all_tiles[y][x].num)
        return ret

    def display_board(self):
        for y in range(9):
            row = ''
            for x in range(9):
                row += str(self.all_tiles[y][x].num)
            print(row)

    def copy(self):
        return Board(board=self)
