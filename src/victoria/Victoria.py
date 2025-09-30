from ram_manager.RamManager import RamManager
from program.Program import Program
from pandas import DataFrame
from pag_table.PagTable import PagTable
from page_replacement.PRA import PRA
from page_replacement.LRU import LRU
import random
from static.Static import (
    ACCESS_RAM_COST,
    PAGE_FAULT_COST,
    SWAP_IN_COST,
    SWAP_OUT_COST,
    RESET_R_INTERVAL,
)
from metrics.Metrics import Metrics


class Victoria:
    def __init__(self, PRA: PRA = LRU(), metrics: Metrics = Metrics()):
        self.ram_manager = RamManager()
        self.programs: dict[int, Program] = dict()
        self.program_count: int = 0
        self.clock: int = 0
        self.disk: dict[(int, int):str] = dict()
        self.page_failure_count: int = 0
        self.requests: list[tuple[int, int]] = list()
        self.PRA = PRA
        self.next_reset_time = RESET_R_INTERVAL
        self.memory_access_count: int = 0
        self.metrics: Metrics = metrics

    def generate_random_requests(self, quantity=5):
        if self.program_count == 0:
            print("No programs loaded!")
            return

        for i in range(quantity):
            random_pid = random.choice(list(self.programs.keys()))
            program = self.programs[random_pid]
            mode = random.choice(["w", "r"])
            self.requests.append(program.generate_memory_request(mode=mode))

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
        self.clock += SWAP_OUT_COST

    def disk_swap_in(self, pid, vpn, pag_tab: PagTable, fpn, mode: str):
        if (pid, vpn) not in self.disk:
            raise RuntimeError("Error, that reg is not in disk")

        data = self.disk[(pid, vpn)]

        pag_tab.link_page(vpn=vpn, fpn=fpn)
        self.ram_manager.update_frame(
            fpn=fpn, pid=pid, vpn=vpn, data=data, referenced_time=self.clock, mode=mode
        )
        del self.disk[(pid, vpn)]
        self.clock += SWAP_IN_COST

    def check_in_disk(self, pid, vpn):
        return (pid, vpn) in self.disk

    def handle_page_hit(
        self, pag_tab: DataFrame, pid: int, vpn: int, mode: str, frame_usage: DataFrame
    ):
        frame = pag_tab.table.loc[vpn, "frame"]
        fpn = frame_usage.loc[frame]
        fpn = frame_usage.loc[
            (frame_usage["pid"] == pid) & (frame_usage["vpn"] == vpn)
        ].index.tolist()
        if mode == "w":
            pag_tab.update_page(vpn)
            frame_usage.loc[fpn[0], "M"] = 1
        frame_usage.loc[fpn[0], "referenced_time"] = self.clock
        frame_usage.loc[fpn[0], "R"] = 1

        self.clock += ACCESS_RAM_COST

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
    def access_memory(self, program: Program, vpn: int, mode: str):
        self.memory_access_count += 1
        pid = program.pid
        data = program.data
        pag_tab = program.page_table

        frame_usage = self.ram_manager.frame_usage

        # update referenced
        if pag_tab.check_valid(vpn):
            self.handle_page_hit(
                pag_tab=pag_tab, pid=pid, vpn=vpn, mode=mode, frame_usage=frame_usage
            )
            return

        fpn = self.handle_page_fault()

        if self.check_in_disk(pid, vpn):
            self.disk_swap_in(pid, vpn, pag_tab, fpn, mode=mode)
            return

        pag_tab.link_page(vpn=vpn, fpn=fpn)

        self.ram_manager.update_frame(
            fpn=fpn,
            pid=pid,
            vpn=vpn,
            data=data,
            load_time=self.clock,
            referenced_time=self.clock,
            mode=mode,
        )

        self.clock += PAGE_FAULT_COST

    def choose_free_frame(self) -> int:
        frame_usage = self.ram_manager.frame_usage
        filter_frame = frame_usage["pid"] == -1
        free_indexes = frame_usage.loc[filter_frame].index.tolist()

        if free_indexes:
            return free_indexes[0]
        else:
            return -1

    def masive_r_reset(self):
        if self.clock >= self.next_reset_time:
            self.ram_manager.reset_r()
            self.next_reset_time = self.clock + RESET_R_INTERVAL

    def init(self):
        for pid, vpn, mode in self.requests:
            program = self.find_program(pid)
            self.masive_r_reset()
            self.access_memory(program, vpn, mode)
            self.metrics.add_ram_log(
                frame_usage=self.ram_manager.frame_usage,
                ram=self.ram_manager.ram,
                total_faults=self.page_failure_count,
                clock=self.clock,
                total_accesses=self.memory_access_count,
                busy_frames=self.ram_manager.get_busy_frames_count(),
            )
        self.metrics.print_step_by_step()
