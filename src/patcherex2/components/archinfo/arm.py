class ArmInfo:
    nop_bytes = b"\x00\xF0\x20\xE3"  # TODO: thumb
    nop_size = 4
    jmp_asm = "b {dst}"
    jmp_size = 4
    call_asm = "bl {dst}"