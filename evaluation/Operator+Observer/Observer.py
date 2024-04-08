import argparse
import re
from time import sleep

import xmltodict

from approach.utils.base_utils import llm
from approach.utils.base_utils import memory
from approach.utils.base_utils.android_controller import ActionType
from approach.utils import observer_utils
from Operator import ReturnData
from approach.utils import operator_utils

system_prompt = ("I want you to act as an automated testing judgment assistant for a mobile app. You will help assess "
                 "whether the action on the current interface is correct. I will provide you with the current testing "
                 "task, action sequence of the entire task, and elements on the current page. You need to tell me if "
                 "the current task flow is correct based on the current interface and the history of actions.")


class Observer_agent:
    def __init__(self):
        self.app_name = ""
        self.overview_task = ""
        self.device_type_list = []
        self.is_info1_ok = False
        self.llm = llm.GeneralGPT()
        self.messages = [{"role": "system", "content": system_prompt}]
        self.sub_messages = []
        # t_dict = {"history_screen": [],
        #           "history_action": [],
        #           "activity": []}
        # self.sub_messages.append(t_dict)

        self.observer_skip_flag = False
        self.observer_response = ""
        self.wrong_answer = ""

    def align1(self, app_name: str, overview_task: str, device_type_list: list):
        self.app_name = app_name
        self.overview_task = overview_task
        self.device_type_list = device_type_list
        self.is_info1_ok = True

        for i in range(len(self.device_type_list)):
            t_dict = {"history_screen": [],
                      "history_action": [],
                      "activity": []}
            self.sub_messages.append(t_dict)

    def history_init(self, device_id: int, activity_name: str, all_comps: str):
        if len(self.sub_messages[device_id - 1]["history_screen"]) == 0:
            abstract = self.page_abstract(activity_name, "", "", all_comps)
            self.sub_messages[device_id - 1]["history_screen"].append(abstract)
            self.sub_messages[device_id - 1]["activity"].append(activity_name)

    def remove_screen_history_last_item(self, device_num: int):
        del self.sub_messages[device_num - 1]["history_screen"][-1]

    def remove_action_list_last_item(self, device_id: int):
        del self.sub_messages[device_id - 1]["history_action"][-1]

    def ad_action_list(self, device_id: int, last_action: str):
        self.sub_messages[device_id - 1]["history_action"].append(last_action)

    def assess(self, current_device_num: int, activity_name: str, all_comps: str, action_list: list, memory_list: list,
               t_ob: list):
        if len(action_list) == 0:
            return
        print("\nObserver: Observer is running....")
        self.sub_messages[current_device_num - 1]["history_action"] = action_list
        prompt = observer_utils.observer_start_template_1 + observer_utils.observer_start_template_2
        prompt += observer_utils.observer_prompt_start(self.app_name, self.overview_task, self.device_type_list,
                                                       current_device_num)
        prompt += observer_utils.observer_prompt_history(current_device_num,
                                                         self.sub_messages[current_device_num - 1].get(
                                                             "history_screen"),
                                                         self.sub_messages[current_device_num - 1].get(
                                                             "history_action"),
                                                         activity_name, all_comps)
        prompt += observer_utils.other_device_history(self.device_type_list, self.sub_messages, current_device_num,
                                                      memory_list)
        prompt += observer_utils.observer_prompt_last()
        t_ob[0] = prompt

        abstract = self.page_abstract(activity_name, self.sub_messages[current_device_num - 1]["activity"][-1],
                                      action_list[-1], all_comps)
        self.sub_messages[current_device_num - 1]["history_screen"].append(abstract)
        self.sub_messages[current_device_num - 1]["activity"].append(activity_name)

        new_message = {"role": "user", "content": prompt}
        self.messages.append(new_message)

        # pprint.pprint(self.messages)

        result = self.llm.ask_gpt_message(messages=self.messages)

        self.messages = [{"role": "system", "content": system_prompt}]
        print("\n-----------")
        print(result)
        print("-----------\n")
        return result['content']

    def assess_device_switch(self, current_device_num: int, memory_list: list, matches_list: list, sub_messages: list,
                             all_comps: str):
        print("Observer is assessing whether the device should be switch...")
        prompt = observer_utils.observer_prompt_device_switch(self.app_name, self.overview_task, self.device_type_list,
                                                              current_device_num, memory_list, matches_list,
                                                              sub_messages,
                                                              all_comps)
        new_message = {"role": "user", "content": prompt}
        self.messages.append(new_message)

        # pprint.pprint(self.messages)

        result = self.llm.ask_gpt_message(messages=self.messages)

        self.messages = [{"role": "system", "content": system_prompt}]
        print("\n-----------")
        print(result)
        print("-----------\n")
        return result['content']

    def assess_task_done(self, current_device_num: int, memory_list: list, task_done_summary: str, sub_messages: list,
                         all_comps: str):
        print("Observer is assessing whether the task is over...")
        prompt = observer_utils.observer_prompt_task_done(self.app_name, self.overview_task, self.device_type_list,
                                                          current_device_num, memory_list, task_done_summary,
                                                          sub_messages, all_comps)
        new_message = {"role": "user", "content": prompt}
        self.messages.append(new_message)
        result = self.llm.ask_gpt_message(messages=self.messages)
        self.messages = [{"role": "system", "content": system_prompt}]
        print("\n-----------")
        print(result)
        print("-----------\n")
        return result['content']

    def page_abstract(self, activity_name: str, pre_activity_name: str, pre_action: str, all_comps: str):
        print("\nObserver: Current screen is abstracting...")
        abstract_system_prompt = ("I want you to act as a UI page summarizer. I will provide you with a screen of a "
                                  "mobile app, and your task is to summarize it. The information I will provide "
                                  "includes the app's name, the activity_name of the screen, and the names "
                                  "of all the components on that screen. Your goal is to summarize the content and "
                                  "functionality of the screen in a brief two to three sentences.")
        mes = [{"role": "system", "content": abstract_system_prompt}]
        prompt = f"This is a app named {self.app_name}. The current screen is named: '{activity_name}'. "
        if pre_activity_name != "":
            prompt += f"And it is reached from screen '{pre_activity_name}' through action '{pre_action}'"
        prompt += f"\nHere is the elements on current screen '{activity_name}': \n"
        prompt += all_comps
        prompt += "\nI want you to summarize this screen in a brief two to three sentences."
        new_message = {"role": "user", "content": prompt}
        mes.append(new_message)
        res = self.llm.ask_gpt_message(messages=mes)
        return res['content']

    def expand(self, device_type_list: list):
        self.device_type_list = device_type_list
        t_dict = {"history_screen": [],
                  "history_action": [],
                  "activity": []}
        self.sub_messages.append(t_dict)

    # j_flag, represents the type identified by the observer.
    # all_comps, components on current screen (after last action from action list).
    # matches, content from operator.
    def run_observer(self, j_flag: int, device_id: int, activity: str, all_comps: str,
                     pool: memory.MemoryPool, matches: list):
        self.history_init(device_id, activity, all_comps)
        if len(self.sub_messages[device_id-1].get("history_action")) == 0:
            response = {"action_infos": [{}], "status": 0, "device_switch": False, "task_done": False}
            return ReturnData(0, 0, response)
        if self.observer_skip_flag:
            self.observer_skip_flag = False
            response = {"action_infos": [{}], "status": 0, "device_switch": False, "task_done": False}
            return ReturnData(0, 0, response)

        action_list = self.sub_messages[device_id - 1].get("history_action")

        if j_flag == 0:
            t_ob = [""]
            assess_result = self.assess(device_id, activity, all_comps, action_list,
                                        pool.memory_pool_list, t_ob)
            sleep(0.5)

            match_list = re.findall(r"'([^']*)'", assess_result)
            if len(match_list) == 5 and match_list[4] == "Task done":
                response = {"action_infos": [{"aciton_list": action_list}], "status": 1}
                return ReturnData(0, 0, response)
            if match_list[0] == "yes":
                # self.observer_judge_flag = True
                self.observer_response = match_list[4]
                if match_list[2] == "yes":
                    resp = {"action_infos": [
                        {"react": 3, "wrong_list": action_list, "wrong_step": int(match_list[1])}],
                        "status": 0, "observer_response": self.observer_response}
                    self.observer_response = ""
                    return ReturnData(0, 0, resp)
                elif match_list[3] == "yes":
                    resp = {"action_infos": [{"react": 2, "wrong_list": action_list, "wrong_step": int(match_list[1])}],
                            "status": 0, "observer_response": self.observer_response}
                    self.observer_response = ""
                    return ReturnData(0, 0, resp)
                # self.wrong_flag = True
                self.wrong_answer += (action_list[-1] + "; ")
                resp = {"action_infos": [{"react": 1, "wrong_list": action_list, "wrong_step": int(match_list[1])}],
                        "status": 0, "observer_response": self.observer_response}
                self.observer_response = ""
                return ReturnData(0, 0, resp)
        if j_flag == 1:
            assess_special_operation_result = self.assess_device_switch(device_id, pool.memory_pool_list,
                                                                        matches, self.sub_messages,
                                                                        all_comps)
            assess_matches = re.findall(r"'(.*?)'", assess_special_operation_result)
            if assess_matches[0] == 'no':
                self.remove_action_list_last_item(device_id)
                self.remove_screen_history_last_item(device_id)
                # self.device_switch_flag = True
                self.observer_response = assess_matches[1]
                self.observer_skip_flag = True
                # self.wrong_flag = True
                response = {
                    "action_infos": [{"action_type": ActionType.NOP,
                                      "action_list": self.sub_messages[device_id - 1]["history_action"]}],
                    "status": 0, "observer_response": self.observer_response, "device_switch": False}
                self.observer_response = ""
                return ReturnData(0, 0, response)
            else:
                response = {"action_infos": [{}], "status": 0, "device_switch": True}
                return ReturnData(0, 0, response)
        if j_flag == 2:
            assess_task_done_result = self.assess_task_done(device_id, pool.memory_pool_list, matches[1],
                                                            self.sub_messages, all_comps)
            assess_matches = re.findall(r"'(.*?)'", assess_task_done_result)
            if assess_matches[0] == "yes":
                response = {"action_infos": [{}], "status": 1, "task_done": True}
                return ReturnData(0, 0, response)
            else:
                # self.task_not_done_flag = True
                self.observer_response = assess_matches[1]
                self.observer_skip_flag = True
                print("Observer: Task haven't been completed yet.")

                self.remove_action_list_last_item(device_id)
                self.remove_screen_history_last_item(device_id)

                response = {"action_infos": [{"action_type": ActionType.NOP}], "status": 0,
                            "observer_response": self.observer_response,
                            "task_done": False}
                self.observer_response = ""
                return ReturnData(0, 0, response)
        response = {"action_infos": [{}], "status": 0}
        return ReturnData(0, 0, response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--appname", help="app's name")
    parser.add_argument("--task", help="task's description")
    parser.add_argument("--dtype", nargs='+', help="device's account type/label")
    parser.add_argument("--deviceid", help="Current device's id, like '1', '2'.")
    parser.add_argument("--historyAction", nargs='+', help="action history of this device")
    parser.add_argument("--historyScreen", nargs='+', help="screen history of previous action")
    parser.add_argument("--historyActivity", nargs='+', help="activity history of history screen")
    parser.add_argument("--currentXml", help="Xml file path.")
    args = parser.parse_args()
    appname = args.appname
    task = args.task
    dtype = args.dtype.split(",") if args.dtype else []
    device_id = int(args.deviceid)
    history_action = args.historyAction.split(";;") if args.historyAction else []
    history_screen = args.historyScreen.split(";;") if args.historyScreen else []
    history_activity = args.historyActivity.split(",") if args.historyActivity else []
    xml_path = args.currentXml

    try:
        with open(xml_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print("File not exist.")
    except IOError:
        print("Can not open file.")

    xml = content
    if "<hierarchy rotation=" in xml:
        align_xml = xml
    else:
        align_xml = operator_utils.xml_align(xml)
    xml_dict = xmltodict.parse(align_xml)
    all_comps = operator_utils.getMergedComponents(xml_dict)
    t_list = []
    operator_utils.component_prompt(str(device_id), all_comps, t_list)

    observer = Observer_agent()
    observer.align1(appname, task, dtype)
    for i in range(len(observer.device_type_list)):
        if i > 0:
            observer.expand(observer.device_type_list[:i + 1])

    observer.sub_messages[device_id - 1]["history_screen"] = history_screen
    observer.sub_messages[device_id - 1]["history_action"] = history_action
    observer.sub_messages[device_id - 1]["activity"] = history_activity

    memory_pool = memory.MemoryPool()

    matches = re.findall(r"'(.*?)'", history_action[-1])
    j_flag = 0
    if len(matches) > 0 and matches[0].startswith("Switch to device"):
        j_flag = 1
    if len(matches) > 0 and matches[0] == 'Task done':
        j_flag = 2
    observer.run_observer(j_flag, device_id, history_activity[-1], t_list[0], memory_pool, matches)
