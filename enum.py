def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# --------------------------------------------------------

Key = enum("JUMP", "GRAB", "CN", "CU", "CD", "CF", "CB", "VN", "VU", "VD", "VF", "VB")

# --------------------------------------------------------

MoveStyle = enum("ANIM_DRIVEN", "PHYSICS_DRIVEN")

# --------------------------------------------------------

DamageType = enum('NORMAL')
