from ram_manager.RamManager import RamManager
from program.Program import Program
from pandas import DataFrame
from pag_table.PagTable import PagTable
from page_replacement.PRA import PRA
from page_replacement.LRU import LRU
import random


class Victoria:
    def __init__(self, PRA: PRA = LRU()):
        self.ram_manager = RamManager()
        self.programs: dict[int, Program] = dict()
        self.program_count: int = 0
        self.clock: int = 0
        self.disk: dict[(int, int):str] = dict()
        self.page_failure_count: int = 0
        self.requests: list[tuple[int, int]] = list()
        self.PRA = PRA

    def generate_requests(self, quantity=5):
        if self.program_count == 0:
            print("No programs loaded!")
            return

        programs_pids = list(self.programs.keys())

        for i in range(quantity):
            program = self.programs[
                programs_pids[random.randint(0, len(programs_pids) - 1)]
            ]
            self.requests.append(program.generate_memory_request())

    # basic control
    def load_program(self, pid: int, name, data):
        if pid in self.programs:
            raise RuntimeError("Check your pid's")

        self.programs[pid] = Program(pid, name, data)
        self.program_count += 1

    def find_program(self, pid) -> Program:
        if pid in self.programs:
            return self.programs[pid]

        raise RuntimeError(f"Program with pid {pid} doesn't exist")

    def terminate_program(pid):
        pass
        # FIXME Toma en cuenta que al eliminar un programa debes liberar todos sus marcos

    def disk_swap_out(self, pid, vpn, data):
        if (pid, vpn) in self.disk:
            raise RuntimeError("Unknown error, this should'nt suppose to happen")

        program = self.find_program(pid)
        program.page_table.unlink_page(vpn)
        self.disk[(pid, vpn)] = data

    def disk_swap_in(self, pid, vpn, pag_tab: PagTable, fpn):
        if (pid, vpn) not in self.disk:
            raise RuntimeError("Error, that reg is not in disk")

        data = self.disk[(pid, vpn)]

        pag_tab.link_page(vpn=vpn, fpn=fpn)
        self.ram_manager.update_frame(
            fpn=fpn, pid=pid, vpn=vpn, data=data, referenced_time=self.clock
        )
        del self.disk[(pid, vpn)]
        self.clock += 1000

    def check_in_disk(self, pid, vpn):
        return (pid, vpn) in self.disk

    def handle_page_hit(
        self, pag_tab: DataFrame, pid: int, vpn: int, frame_usage: DataFrame
    ):
        pag_tab.update_page(vpn)
        frame = pag_tab.table.loc[vpn, "frame"]
        fpn = frame_usage.loc[frame]
        fpn = frame_usage.loc[
            (frame_usage["pid"] == pid) & (frame_usage["vpn"] == vpn)
        ].index.tolist()
        frame_usage.loc[fpn[0], "referenced_time"] = self.clock
        self.clock += 1000

    def handle_page_fault(self) -> int:
        fpn = self.choose_free_frame()

        if fpn == -1:
            self.page_failure_count += 1
            fpn = self.PRA.execute_algorithm(self.ram_manager.frame_usage)
            program_target = self.ram_manager.find_vpn(fpn)
            pid_target, vpn_target = program_target
            program_target = self.find_program(pid=pid_target)
            isDirty = program_target.page_table.check_dirty(vpn_target)

            # check if is needed to save on disk
            if isDirty:
                self.disk_swap_out(
                    pid=pid_target, vpn=vpn_target, data=program_target.data
                )
            else:
                program_target.page_table.unlink_page(vpn=vpn_target)
        else:
            self.page_failure_count += 1
            program_target = self.ram_manager.find_vpn(fpn)
            pid_target, vpn_target = program_target
            if pid_target != -1:
                unlink_program = self.find_program(pid=pid_target)
                unlink_program.page_table.unlink_page(vpn=vpn_target)

        return fpn

    # core
    def access_memory(self, program: Program, vpn: int):
        pid = program.pid
        data = program.data
        pag_tab = program.page_table

        frame_usage = self.ram_manager.frame_usage

        # update referenced
        if pag_tab.check_valid(vpn):
            self.handle_page_hit(
                pag_tab=pag_tab, pid=pid, vpn=vpn, frame_usage=frame_usage
            )
            return

        fpn = self.handle_page_fault()

        if self.check_in_disk(pid, vpn):
            self.disk_swap_in(pid, vpn, pag_tab, fpn)
            return

        pag_tab.link_page(vpn=vpn, fpn=fpn)

        self.ram_manager.update_frame(
            fpn=fpn,
            pid=pid,
            vpn=vpn,
            data=data,
            load_time=self.clock,
            referenced_time=self.clock,
        )

        self.clock += 1000

    def choose_free_frame(self) -> int:
        frame_usage = self.ram_manager.frame_usage
        filter_frame = frame_usage["pid"] == -1
        free_indexes = frame_usage.loc[filter_frame].index.tolist()

        if free_indexes:
            return free_indexes[0]
        else:
            return -1
