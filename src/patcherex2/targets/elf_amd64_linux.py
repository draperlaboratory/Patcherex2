from ..components.allocation_managers.allocation_manager import AllocationManager
from ..components.archinfo.amd64 import Amd64Info
from ..components.assemblers.keystone import Keystone, keystone
from ..components.binary_analyzers.angr import Angr
from ..components.binfmt_tools.elf import ELF
from ..components.compilers.clang import Clang
from ..components.disassemblers.capstone import Capstone, capstone
from ..components.utils.utils import Utils
from .target import Target


class ElfAmd64Linux(Target):
    @staticmethod
    def detect_target(binary_path):
        with open(binary_path, "rb") as f:
            magic = f.read(0x14)
            if magic.startswith(b"\x7fELF") and magic.startswith(
                b"\x3e\x00", 0x12
            ):  # EM_X86_64
                return True
        return False

    def get_assembler(self, assembler):
        assembler = assembler or "keystone"
        if assembler == "keystone":
            return Keystone(
                self.p,
                keystone.KS_ARCH_X86,
                keystone.KS_MODE_LITTLE_ENDIAN + keystone.KS_MODE_64,
            )
        raise NotImplementedError()

    def get_allocation_manager(self, allocation_manager):
        allocation_manager = allocation_manager or "default"
        if allocation_manager == "default":
            return AllocationManager(self.p)
        raise NotImplementedError()

    def get_compiler(self, compiler):
        compiler = compiler or "clang"
        if compiler == "clang":
            return Clang(self.p)
        elif compiler == "clang19":
            return Clang(self.p, clang_version=19)
        raise NotImplementedError()

    def get_disassembler(self, disassembler):
        disassembler = disassembler or "capstone"
        if disassembler == "capstone":
            return Capstone(
                capstone.CS_ARCH_X86,
                capstone.CS_MODE_LITTLE_ENDIAN + capstone.CS_MODE_64,
            )
        raise NotImplementedError()

    def get_binfmt_tool(self, binfmt_tool):
        binfmt_tool = binfmt_tool or "pyelftools"
        if binfmt_tool == "pyelftools":
            return ELF(self.p, self.binary_path)
        raise NotImplementedError()

    def get_binary_analyzer(self, binary_analyzer):
        binary_analyzer = binary_analyzer or "angr"
        if binary_analyzer == "angr":
            return Angr(self.binary_path)
        raise NotImplementedError()

    def get_utils(self, utils):
        utils = utils or "default"
        if utils == "default":
            return Utils(self.p, self.binary_path)
        raise NotImplementedError()

    def get_archinfo(self, archinfo):
        archinfo = archinfo or "default"
        if archinfo == "default":
            return Amd64Info()
        raise NotImplementedError()

    def get_cc(self, preserve_none=False, archinfo=None):
        archinfo = self.get_archinfo(archinfo)
        if preserve_none:
            return archinfo.cc['LinuxPreserveNone']
        else:
            return archinfo.cc['Linux']

    def get_cc_float(self, archinfo=None):
        archinfo = self.get_archinfo(archinfo)
        return archinfo.cc_float['Linux']

    def get_callee_preserved(self, archinfo=None):
        archinfo = self.get_archinfo(archinfo)
        return archinfo.callee_preserved['Linux']