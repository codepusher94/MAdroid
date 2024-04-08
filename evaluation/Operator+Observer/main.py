import argparse
import uiautomator2 as u2
import xmltodict

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from approach.utils import operator_utils
from approach.utils.base_utils import android_controller
from approach.utils.base_utils import memory
import Operator
import Observer

task_done = False


def get_all_comps(xml: str):
    if "<hierarchy rotation=" in xml:
        align_xml = xml
    else:
        align_xml = operator_utils.xml_align(xml)
    xml_dict = xmltodict.parse(align_xml)
    all_comps = operator_utils.getMergedComponents(xml_dict)
    t_list = []
    operator_utils.component_prompt("", all_comps, t_list)
    return t_list[0]


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

    memory_pool = memory.MemoryPool()
    memory_pool.align_1(appname, task, dtype, dip)
    controller_dict = {"memory_pool": memory_pool}

    observer = Observer.Observer_agent()

    observer.align1(appname, task, dtype[:1])

    for i in range(1):
        controller_dict[f"d{i + 1}"] = u2.connect(dip[i])
        controller_dict[f"controller{i + 1}"] = android_controller.AndroidController(dip[i])
        controller_dict[f"agent{i + 1}"] = Operator.Multi_agent(i + 1, 1)

    all_comps = ""
    matches_list = []
    while not task_done:
        current_device = memory_pool.current_device
        agent = controller_dict.get(f"agent{current_device}")
        device = controller_dict.get(f"d{current_device}")
        controller = controller_dict.get(f"controller{current_device}")

        xml = device.dump_hierarchy(compressed=False, pretty=False)
        activity = device.app_current().get("activity").split("/")[-1]
        all_comps = get_all_comps(xml)

        o_result = observer.run_observer(0, current_device, activity, all_comps, memory_pool, matches_list)
        if "action_infos" in o_result.response and "react" in o_result.response["action_infos"][0]:
            react = o_result.response["action_infos"][0]["react"]
            observer_reason = o_result.response["observer_response"]
            agent.observer_judge_flag = True
            agent.observer_reason = observer_reason

            if react == 2:
                controller.back()
                observer.remove_action_list_last_item(current_device)
                observer.remove_screen_history_last_item(current_device)
                print("Observer: back")
                observer.observer_skip_flag = True
                continue
            if react == 3:
                task_done = True
                break
            if react == 1:
                agent.wrong_flag = True
                agent.wrong_answer += f"{observer.sub_messages[current_device - 1].get('history_action')[-1]}; "
                observer.remove_action_list_last_item(current_device)
                observer.remove_screen_history_last_item(current_device)

        data_action = {"device_id": "test_001", "task_id": 100, "fragment": "",
                       "type": 0, "xml": xml,
                       "activity": activity}
        result = agent.task_execution(data_action, memory_pool)
        observer.ad_action_list(current_device, agent.last_action)
        matches_list = result.response["matches"]

        if result.response["status"] == 1:
            pass
        else:
            actionType = result.response["action_infos"][0]["action_type"]
            if actionType == android_controller.ActionType.NOP:
                pass
            elif actionType == android_controller.ActionType.ACTIVATE:
                pass
            elif actionType == android_controller.ActionType.CLICK:
                controller_dict.get("controller{}".format(current_device)).tap(
                    result.response["action_infos"][0]["bounds"][:2],
                    result.response["action_infos"][0]["bounds"][2:])
            else:
                for item in result.response["action_infos"]:
                    controller_dict.get("controller{}".format(current_device)).execute_action(
                        android_controller.ActionType.INPUT,
                        item["bounds"],
                        item["text"])
        if "device_switch" in result.response:
            o_result = observer.run_observer(1, current_device, activity, all_comps, memory_pool, matches_list)
            if not o_result.response["device_switch"]:
                agent.observer_reason = o_result.response["observer_reason"]
                memory_pool.current_device = current_device
                agent.device_switch_flag = True
                observer.observer_skip_flag = True
                observer.remove_screen_history_last_item(current_device)
                observer.remove_action_list_last_item(current_device)
            else:
                if memory_pool.current_device > memory_pool.device_total_num:
                    memory_pool.device_total_num += 1
                    controller_dict["controller{}".format(memory_pool.current_device)] = android_controller.AndroidController(dip[memory_pool.current_device-1])
                    controller_dict["d{}".format(memory_pool.current_device)] = u2.connect(dip[memory_pool.current_device-1])
                    controller_dict["agent{}".format(memory_pool.current_device)] = Operator.Multi_agent(memory_pool.current_device, 1)
        if "task_done" in result.response:
            o_result = observer.run_observer(2, current_device, activity, all_comps, memory_pool, matches_list)
            if not o_result.response["task_done"]:
                agent.observer_reason = o_result.response["observer_reason"]
                agent.task_not_done_flag = True
                observer.observer_skip_flag = True
                observer.remove_screen_history_last_item(current_device)
                observer.remove_action_list_last_item(current_device)
            else:
                task_done = True


