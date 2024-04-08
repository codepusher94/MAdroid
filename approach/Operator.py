import argparse
import random
import re
import threading
from time import sleep

import xmltodict
import uiautomator2 as u2

from utils.base_utils import android_controller
from utils import operator_utils
from utils.base_utils import llm
from utils.base_utils import memory
from utils import mes_compress_agent
from utils import text_generate_agent

task_done = False


class ReturnData:
    def __init__(self, data_type: int, device_switch: int, response: dict):
        self.data_type = data_type
        # data_type: 0 normal for task execute; 1 switch device; 2 normal for task create
        self.device_switch = device_switch
        self.response = response


class Multi_agent:
    # The device_id starts from 1, where the execute_state of the first device is 0, and the execute_state of other
    # devices is 1.
    def __init__(self, device_id, execute_state):
        self.llm = llm.GeneralGPT()
        self.compression_agent = mes_compress_agent.Message_compression_agent()
        self.device_id = device_id
        self.execute_state = execute_state

        # The above variables are assigned values in the task_create phase.
        self.app_name = ""
        self.overview_task = ""
        self.device_total_num = 1
        self.device_type_list = []
        self.device_ip_list = []
        self.messages = []
        self.device_sub_task_list = []
        self.wrong_answer = ""  # Record of error components that cannot be clicked.
        self.wrong_flag = False  # When LLM selects a non-existent component, the flag will be set to True, forcing
        # the prompt to reselect the component.
        self.pre_xml = " "

        self.last_action = ""
        self.t_list = []
        self.observer_judge_flag = False
        self.task_not_done_flag = False
        self.device_switch_flag = False
        self.observer_reason = ""

    # Synchronize the information of each operator.
    def task_info_align(self, m_pool: memory.MemoryPool):

        if m_pool.is_info1_ok:
            self.app_name = m_pool.app_name
            self.overview_task = m_pool.overview_task
            self.device_type_list = m_pool.device_type_list
            self.device_ip_list = m_pool.device_ip_list

        if m_pool.is_info2_ok:
            self.device_total_num = m_pool.device_total_num
            self.device_sub_task_list = m_pool.device_sub_task_list

    def task_execution(self, execute_info: dict, pool: memory.MemoryPool):
        e_prompt = ""  # Prompt for the agent's first run.
        input_task = ""  # Store specified tasks for text input.

        xml = execute_info.get("xml")
        if "<hierarchy rotation=" in xml:
            align_xml = xml
        else:
            align_xml = operator_utils.xml_align(xml)
        xml_dict = xmltodict.parse(align_xml)
        activity = execute_info.get("activity")
        all_components = operator_utils.getMergedComponents(xml_dict)

        if pool.current_device != self.device_id:
            response = {"action_infos": [{"action_type": android_controller.ActionType.NOP}], "status": 0}
            return ReturnData(0, 0, response)

        # Initialization of the prompt for the current agent.
        if self.execute_state == 1:
            if not pool.is_info1_ok:
                print("Device {}: Coordinator has not yet completed its task.".format(self.device_id))
                response = {"action_infos": [{"action_type": android_controller.ActionType.NOP}], "status": 0}
                return ReturnData(0, 0, response)
            self.task_info_align(pool)
            e_prompt += operator_utils.device_start_template
            e_prompt += operator_utils.first_prompt_template(self.app_name,
                                                             self.device_sub_task_list,
                                                             self.overview_task, self.device_type_list,
                                                             self.device_id,
                                                             pool.memory_pool_list)
            self.t_list = []
            e_prompt += operator_utils.component_prompt(activity, all_components,
                                                        self.t_list) + operator_utils.last_prompt_template
            self.execute_state = 2

        # Task execution phase.
        if self.execute_state == 2:
            if e_prompt != "":
                prompt = e_prompt
            else:
                if xml != self.pre_xml and not self.wrong_flag:
                    self.pre_xml = xml
                    self.t_list = []
                    prompt = operator_utils.re1_prompt(activity, all_components, self.device_sub_task_list,
                                                       self.overview_task, self.device_type_list, self.device_id,
                                                       pool.memory_pool_list, self.t_list)
                    self.wrong_answer = ""
                else:
                    self.pre_xml = xml
                    self.wrong_flag = False
                    self.t_list = []
                    prompt = operator_utils.re2_prompt(activity, all_components, self.wrong_answer,
                                                       self.device_sub_task_list,
                                                       self.overview_task, self.device_type_list, self.device_id,
                                                       self.t_list)

            if self.observer_judge_flag:
                prompt += (
                    f"\n Our last action was considered wrong, and here is the reason: \n\"{self.observer_reason}\"\n"
                    f"Maybe we can choose another action this time.")
                self.observer_judge_flag = False
                self.observer_reason = ""
            if self.task_not_done_flag:
                prompt += ("\nOur last action was 'Task done', but maybe it is not the right time to end all tasks? "
                           "And here is the reason:\n\"{}\"\n"
                           "Please double-check to see if all devices have completed their tasks. Please refer to the "
                           "previously mentioned overview_task. If other devices have not completed their tasks, "
                           "switch to another device. If you still have unfinished tasks, please continue completing "
                           "them.").format(self.observer_reason)
                self.task_not_done_flag = False
                self.observer_reason = ""
            if self.device_switch_flag:
                prompt += ("\nOur last action was 'Switch to device...', but maybe it is not the right operation? And "
                           "here is the reason:\n\"{}\"\n"
                           "Please double-check to see if all your task has done. Please refer to the previously "
                           "mentioned overview_task. If you still have unfinished tasks, please continue completing "
                           "them.").format(self.observer_reason)
                self.device_switch_flag = False
                self.observer_reason = ""

            operator_utils.ad_new_mes(self.messages, prompt)
            result = self.llm.ask_gpt_message(messages=self.messages)

            print("\n" + f"Device {self.device_id}: " + result['content'])
            # message压缩
            if len(self.messages) > 2:
                compress_mes = self.compression_agent.messages_compression(self.messages[-1]['content'], True)
                self.messages[-1]['content'] = compress_mes

            self.messages.append(result)
            self.wrong_answer += (result['content'] + "; ")
            self.last_action = result['content']
            # self.action_list.append(result['content'])
            matches = re.findall(r"'(.*?)'", result['content'])
            if len(matches) == 2 and matches[0].lower() == "tap":
                target_text = matches[1]
                target_list = []
                for item in all_components:
                    if '@text' in item and item['@text'] == target_text:
                        target_list = [item]
                        break
                    elif '@text' in item and target_text in item['@text']:
                        target_list.append(item)
                    elif item['@content-desc'] == target_text or target_text in item['@content-desc']:
                        target_list.append(item)
                    elif item['@resource-id'] == target_text or target_text in item['@resource-id']:
                        target_list.append(item)
                if len(target_list) != 0:
                    target = random.choice(target_list)
                    response = {
                        "action_infos": [{
                            "action_type": android_controller.ActionType.CLICK,
                            "bounds": [int(num) for substring in target['@bounds'].strip("[]").split("][") for num in
                                       substring.split(",")],
                            "resource_id": target['@resource-id'],
                            "class": target['@class'],
                            "text": target['@content-desc'],
                            "throttle": 500
                        }],
                        "status": 0, "matches": matches
                    }
                    return ReturnData(0, 0, response)
                else:
                    self.wrong_flag = True
                    print("Device {}: Wrong component selected.".format(self.device_id))
                    response = {"action_infos": [{"action_type": android_controller.ActionType.NOP}], "status": 0, "matches": matches}
                    return ReturnData(0, 0, response)
            elif len(matches) > 0 and matches[0] == 'Switch to input generation':
                if len(matches) == 1:
                    self.execute_state = 3
                elif len(matches) == 2:
                    self.execute_state = 4
                    input_task = matches[1]
            elif len(matches) > 0 and matches[0].startswith("Switch to device"):
                pool.current_device = int(re.search(r'\d+', matches[0]).group())
                pool.memory_pool_list.append({"role": self.device_type_list[self.device_id - 1],
                                              "device_id": self.device_id, "message": matches[1]})

                if pool.current_device > int(pool.device_total_num):
                    response = {"action_infos": [{"action_type": android_controller.ActionType.ACTIVATE}], "status": 0}
                else:
                    response = {"action_infos": [{"action_type": android_controller.ActionType.NOP}], "status": 0, "device_switch": True, "matches": matches}
                return ReturnData(0, 0, response)
            elif len(matches) > 0 and matches[0] == 'Task done':
                response = {"action_infos": [{}], "status": 1, "matches": matches}
                return ReturnData(0, 0, response)

        if self.execute_state == 3:
            input_agent = text_generate_agent.Text_generate_agent("")
            data_action = {"xml": xml, "activity": activity, "type": 1}
            result = input_agent.input_generate(self.app_name, data_action, 0, "")
            self.execute_state = 2
            result.response["matches"] = []
            return result

        if self.execute_state == 4:
            input_agent = text_generate_agent.Text_generate_agent("")
            data_action = {"xml": xml, "activity": activity, "type": 1}
            result = input_agent.input_generate(self.app_name, data_action, 1, input_task)
            self.execute_state = 2
            result.response["matches"] = []
            return result

    # def remove_action_list_last_item(self):
    #     del self.action_list[-1]


# result_queue = queue.Queue()


def task_execute(i: int, controller_dict: dict):
    global task_done
    while not task_done:
        xml = controller_dict.get("d{}".format(i + 1)).dump_hierarchy(compressed=False, pretty=False)
        activity = controller_dict.get("d{}". format(i +1)).app_current().get("activity").split("/")[-1]

        memory_pool = controller_dict.get("memory_pool")
        agent = controller_dict.get("agent{}".format(i + 1))

        data_action = {"device_id": "test_001", "task_id": 100, "fragment": "",
                       "type": 0, "xml": xml,
                       "activity": activity}
        result = agent.task_execution(data_action, controller_dict.get("memory_pool"))
        if result.response["status"] == 1:
            task_done = True
            break

        actionType = result.response["action_infos"][0]["action_type"]
        if actionType == android_controller.ActionType.NOP:
            pass
        elif actionType == android_controller.ActionType.CLICK:
            controller_dict.get("controller{}".format(i + 1)).tap(result.response["action_infos"][0]["bounds"][:2],
                                                                  result.response["action_infos"][0]["bounds"][2:])

        elif actionType == android_controller.ActionType.ACTIVATE:
            target_device = memory_pool.current_device
            if target_device > memory_pool.device_total_num:
                controller_dict[f"agent{target_device}"] = Multi_agent(target_device, 1)
                memory_pool.device_total_num += 1
                t = threading.Thread(target=task_execute, args=(target_device - 1, controller_dict))
                t.start()
        else:
            for item in result.response["action_infos"]:
                controller_dict.get("controller{}".format(i + 1)).execute_action(android_controller.ActionType.INPUT, item["bounds"], item["text"])
        sleep(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--appname", help="app's name")
    parser.add_argument("--task", help="task's description")
    parser.add_argument("--dip", nargs= '+', help="device's ip")
    args = parser.parse_args()
    appname = args.appname
    task = args.task
    dtype = []
    dip = args.dip

    for i in range(len(dip)):
        dtype.append("user device")

    r_pool = memory.MemoryPool()
    r_pool.align_1(appname, task, dtype, dip)
    agent1 = Multi_agent(1, 1)
    agent1.task_info_align(r_pool)
    controller_dict = {"agent1": agent1,
                       "memory_pool": r_pool}

    for i in range(len(dip)):
        controller_dict[f"d{i+1}"] = u2.connect(dip[i])
        controller_dict[f"controller{i+1}"] = android_controller.AndroidController(dip[i])

    t = threading.Thread(target=task_execute, args=(0, controller_dict))
    t.start()
