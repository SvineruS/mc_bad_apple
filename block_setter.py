
def block_setter(start_pos, size, command_func):
    def _set_transition():
        if x % 4 == 0 or (x+1) % 4 == 0:
            for i in range(2):
                command_func(f"setblock {x + i} {y0} {z+dir_} minecraft:redstone_wire")
            command_func(f"setblock {x+1} {y0} {z} minecraft:repeater[facing={'north' if dir_ == -1 else 'south'}]")
            command_func(f"setblock {x} {y0 + 1} {z+dir_} minecraft:sandstone")
        else:
            for i in range(2):
                command_func(f"setblock {x + i} {y0} {z+dir_*2} minecraft:redstone_wire")
            command_func(f"setblock {x+1} {y0} {z+dir_} minecraft:sandstone")
            command_func(f"setblock {x+1} {y0+1} {z+dir_} minecraft:redstone_wire")
            command_func(f"setblock {x+1} {y0} {z} minecraft:redstone_wire")

    x0, y0, z0 = start_pos
    xs, zs = size
    dir_ = +1

    command_func(f'fill {x0} {y0-1} {z0} {x0+xs} {y0-1} {z0+zs} minecraft:sandstone')

    for x in range(x0, x0+xs):
        for z in range(z0+2, z0+zs-1, 2) if dir_ == 1 else range(z0+zs-4, z0-1, -2):
            yield x, y0, z
            command_func(f"setblock {x} {y0} {z+dir_} minecraft:repeater[facing={'north' if dir_ == 1 else 'south'}]")
        _set_transition()
        dir_ *= -1
