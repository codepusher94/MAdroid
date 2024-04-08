import argparse
import threading

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import uiautomator2 as u2
from approach.utils.base_utils import memory
from approach.utils.base_utils import android_controller
import Coordinator
import Operator


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--appname", help="app's name")
    parser.add_argument("--task", help="task's description")
    parser.add_argument("--dip", nargs='+', help="device's ip")
    args = parser.parse_args()
    appname = args.appname
    task = args.task
    dtype = []
    dip = args.dip

    for i in range(len(dip)):
        dtype.append("user device")

    r_pool = memory.MemoryPool()
    r_pool.align_1(appname, task, dtype, dip)

    coordinator = Coordinator.Coordinator_agent(appname, task)
    coordinator.task_create(dtype, dip, r_pool)

    r_pool.device_total_num = 1

    agent1 = Operator.Multi_agent(1, 1)
    agent1.task_info_align(r_pool)
    controller_dict = {"agent1": agent1,
                       "memory_pool": r_pool}

    for i in range(len(dip)):
        controller_dict[f"d{i + 1}"] = u2.connect(dip[i])
        controller_dict[f"controller{i + 1}"] = android_controller.AndroidController(dip[i])

    t = threading.Thread(target=Operator.task_execute, args=(0, controller_dict))
    t.start()
