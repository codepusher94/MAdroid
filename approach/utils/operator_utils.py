
# Uniform format of the retrieved XML file.
def xml_align(f: str):
    temp1 = """<hierarchy rotation="0">"""
    temp2 = """</hierarchy>"""

    if f.startswith("<?xml version="):
        return f[:f.index(">") + 1] + temp1 + f[f.index(">") + 1:] + temp2

    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + temp1 + f + temp2


def ad_new_mes(mes: list, p_rompt: str):
    new_mes = {"role": "user", "content": p_rompt}
    mes.append(new_mes)
    # print(p_rompt + "\n")


# Merge the text of multiple small components under a large component into the large component.
def getMergedComponents(jsondata: dict):
    root = jsondata['hierarchy']
    stack = [root]
    res = []
    while stack:
        currentNode = stack.pop(0)
        #  if '@resource-id' in currentNode:
        if (('@resource-id' in currentNode and '@package' not in currentNode) or
                ('@resource-id' in currentNode and '@package' in currentNode and
                 'com.android.systemui' not in currentNode['@package'])):
            # Attempt to merge if the node is clickable and has child nodes.
            if currentNode['@clickable'] == 'true' and 'node' in currentNode:
                currentNode['@clickable'] = 'false'
                mergeStack = [currentNode]
                mergeStr = ''
                mergedList = []
                # merge loop
                while mergeStack:
                    mergedNode = mergeStack.pop(0)

                    if mergedNode['@clickable'] != "true":
                        size = len(mergeStr)
                        if '@text' in mergedNode and mergedNode['@text'] != "":
                            if mergedNode['@text'] not in mergeStr:
                                mergeStr += mergedNode['@text']
                        elif mergedNode['@content-desc'] != "":
                            if mergedNode['@content-desc'] not in mergeStr:
                                mergeStr += mergedNode['@content-desc']

                        elif (mergedNode['@resource-id'] != "" and "Layout" not in mergedNode['@resource-id']
                              and "layout" not in mergedNode['@resource-id']):
                            result = mergedNode['@resource-id'].split(":id/")[-1]
                            if ("Layout" not in result and "layout" not in result and "container" not in result and
                                    "Container" not in result and "Avatar" not in result and "avatar" not in result and
                                    "root" not in result and "content" not in result and "list" not in result and "group" not in result):
                                if result not in mergeStr:
                                    mergeStr += result

                        if size != len(mergeStr):
                            # Delimiter symbol.
                            mergeStr += ' '
                            mergedList.append(mergedNode)
                        if 'node' in mergedNode:
                            if type(mergedNode['node']).__name__ == 'dict':
                                mergeStack.insert(0, mergedNode['node'])
                            else:
                                for node in mergedNode['node']:
                                    mergeStack.insert(0, node)
                    else:
                        while mergeStack:
                            tempNode = mergeStack.pop(0)
                            stack.insert(0, tempNode)
                        while mergedList:
                            tempNode = mergedList.pop(0)
                            res.append(tempNode)
                        stack.insert(0, mergedNode)
                        mergeStr = 'Error: Ano'

                if mergeStr != 'Error: Ano':
                    currentNode['@text'] = mergeStr
                    res.append(currentNode)
                continue
            else:
                res.append(currentNode)

        if 'node' in currentNode:
            if type(currentNode['node']).__name__ == 'dict':
                stack.insert(0, currentNode['node'])
            else:
                for Node in currentNode['node']:
                    stack.insert(0, Node)
    return res


# Prompt for the start of operator execution.
device_start_template = """You are an agent that is trained to perform some tasks on a smartphone. Our task 
involves conducting tests related to social interactions, which means that more than one device is involved in the 
testing process. However, you only need to operate one of the devices. You will be provided with the task description 
and texts of the components on the current interface, and you need to select the component you want to operate.

You can output the following commands to push the task:

1. 'tap' + 'component'
This command is used to tap on a component. 
'component' is the text of the component on the current interface that we shown you before you output the command.
A simple use case can be 'tap' + 'video call'， which taps the 'video call' component on the current page.

2. 'Switch to device x' + 'message' 
This command is used to let another device operate. In our testing, the 'Current 
Executing Device' is similar to a token, and only the device holding the token is allowed to perform operations. If 
you can reply to me, it means the current token is in your control. Therefore, when you need to wait for another 
device to complete a task, you need to use this command to transfer the token to the device you are waiting for. 
When you send this command, you should put a "message" behind the 'Switch to device x' command, the 'message' is a summary 
of what you have done previously. The summary should be based on the sequence of your actions, without referring to 
the components present on the current interface. If it includes specific information that another device needs to 
know, such as token passwords or group entry codes, you should explicitly write them in the summary. If you haven't 
done anything previously, leave this option blank, and the return will be 'Switch to device x' + ''. 'x' is the 
device number of another device. 'message' is a summary of what you have done previously. A simple use case can be 
'Switch to device 2' + 'Initiated the creation of a group chat, and the entry password is "3579".'.
If you need to share content through the method of copying a link, you need to include the link or relevant content in 
the 'message' following the 'Switch' command. This is because the clipboard is not shared across different devices.

3. 'Switch to input generation'
This command is used to input non-fixed text in current page. You don't have ability to input text on the screen(except for tasks such as entering the group password), after 
you output this command, I will call another model to text in text-input component on the current page. Please note that for text input, you need to open(tap) the search box before you can switch.

4. 'Switch to input generation' + 'task'
This command is used to input fixed text in current page. When you feel the need to input fixed text, you should specify
where to input and the input content to form a task returned together. And when there is a password disk like 1-9 on the page, there is no need to switch to input generation, you can tap the number and input a password.
'task' is the input fixed text task. Please note that for text input, you need to open(tap) the search box before you can switch.
A simple use case can be Switch to input generation' + 'search for "winter gloves" in the search box'.

5. 'Task done' This command is used to terminate all tasks, including the device you are operating and other devices 
of all other agents in the multi-agent system. You should only use it after ensuring that you and all other devices 
have completed the relevant operations. 
When confirming that other devices have completed their tasks, you need to pay attention to which stage of the overview 
task your own sub-task belongs to. At the same time, compare it with the sub-tasks of other devices. If there are other 
devices that have not completed their tasks, you should perform the switch device operation instead of marking the whole 
task as done.

Tips: During the testing execution, if the effect of a component operation is not as expected and I have not specifically 
alerted you about the incorrect operation, you can try performing the operation again to observe the result. However, if 
the result is still not as expected after two attempts, it is advisable to try a different operation.\n\n"""


def first_prompt_template(app_name: str, task: list, overview_task: str, device_type_list: list, de_num,
                          memory_pool_list: list):
    prompt = """We want to test {} app, the overview of our task is: "{}". In our task""".format(app_name, overview_task)
    for i in range(len(device_type_list)):
        prompt += ", "
        prompt += "device{}'s type is \"{}\"".format(str(i + 1), device_type_list[i])
    prompt += ". And you are assigned the role of Device {}\n".format(de_num)
    if len(memory_pool_list) != 0:
        prompt += (
            "And below is the task execution message for the devices that performed their tasks before you, "
            "There may be information that can help you complete the task or understand the task.: \n")
        for item in memory_pool_list:
            prompt += "Device {}(role: {}): \"message:{}\"".format(item['device_id'], item['role'], item['message'])
            prompt += "\n"
    return prompt


def component_prompt(activity_name: str, all_components: list, components_list: list):
    component_info = ""
    prompt = "On your \"{}\" page, it has following components:\n".format(activity_name)
    for c in all_components:
        if '@text' in c and c['@text'] != "":
            prompt += "id:\'{}\', clickable={}>\n".format(c['@text'].replace("\n", " "), c['@clickable'])
            component_info += "id:\'{}\', clickable={}\n".format(c['@text'].replace("\n", " "), c['@clickable'])
            continue
        elif c['@content-desc'] != "":
            prompt += "id:\'{}\', clickable={}\n".format(c['@content-desc'].replace("\n", " "), c['@clickable'])
            component_info += "id:\'{}\', clickable={}\n".format(c['@content-desc'].replace("\n", " "), c['@clickable'])
            continue
        elif "Layout" in c['@resource-id']:
            continue
        elif c['@resource-id'] != "":
            result = c['@resource-id'].split(":id/")[-1]
            if (
                    "Layout" not in result and "layout" not in result and "container" not in result and "Container" not in result and "Avatar" not in
                    result and "avatar" not in result and "root" not in result and "content" not in result and "list" not
                    in result and "group" not in result):
                prompt += "id:\'{}\', clickable={}\n".format(result.replace("\n", " "), c['@clickable'])
                component_info += "id:'{}\', clickable={}\n".format(result.replace("\n", " "), c['@clickable'])
        else:
            continue
    prompt += """\nThe content within each single quotation mark above represents a component, and the comma or blank does not 
indicate component separation but rather serves to separate information within the component. I need you to make a 
selection from them, the format of the output is 'operation' + 'component'. After you have made the selection of components, you need to output the entire 
content within that single quotation mark.\n"""
    components_list.append(component_info)
    # print(components_list[0])
    return prompt


last_prompt_template = """Our task may require multiple steps to complete. Never click on components that I have not 
mentioned above. On this page, which component should I operate? Or do you think it is time to switch devices or 
finish task? If you believe device switching is required, please output 'Switch to device x'(x is that device's 
number); If you believe the task is over, please output 'Task done'. and both of the output should be closed in 
single quotes."""


# Never click on components that I have not mentioned above.

def re1_prompt(activity_name: str, all_comps: list, task: list, overview_task: str, device_type_list: list, de_num,
               memory_pool_list: list, t_list: list):
    prompt = ""
    prompt += "We have done the above operation, and our overview task is \"{}\". In our task".format(overview_task)
    for i in range(len(device_type_list)):
        prompt += ", "
        prompt += "device{}'s type is \"{}\"".format(str(i + 1), device_type_list[i])
    prompt += ". And you are assigned the role of Device {}\n".format(de_num)

    if len(memory_pool_list) != 0:
        prompt += (
            "And below is the task execution message for the devices that performed their tasks before you, "
            "There may be information that can help you complete the task or understand the task.: \n")
        for item in memory_pool_list:
            prompt += "Device {}(role: {}): \"message:{}\"".format(item['device_id'], item['role'], item['message'])
            prompt += "\n"

    prompt += component_prompt(activity_name, all_comps, t_list)
    prompt += last_prompt_template
    return prompt


def re2_prompt(activity_name: str, all_comps: list, w_answer: str, task: list, overview_task: str,
               device_type_list: list, de_num, t_list: list):
    prompt = ""
    prompt += """Sorry we didn't choose correctly, last operation {} is not the right answer, please select other component. 
    Our overview task is \"{}\". In our task \n""".format(w_answer, overview_task)
    for i in range(len(device_type_list)):
        prompt += ", "
        prompt += "device{}'s type is \"{}\"".format(str(i + 1), device_type_list[i])
    prompt += ". And you are assigned the role of Device {}\n".format(de_num)
    prompt += "I will show you the components on the page again.\n"
    prompt += component_prompt(activity_name, all_comps, t_list)
    prompt += last_prompt_template
    return prompt

