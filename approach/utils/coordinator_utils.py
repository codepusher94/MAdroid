

coordinator_start_template = """You are an agent that is trained to act as a coordinator to assist in completing 
testing tasks for mobile apps. Our task involves conducting tests related to social interactions, which means that more 
than one device is involved in the testing process.

We will provide you with our testing task, and you need to inform us how many devices are required to complete this task. 
Then, we will ask you other questions related to this task.\n\n"""

device_num_template = """We want to test "<app name>" app, the following is an overview of our tasks: "<overview task>". 
In our task, how many devices do you think we need? You just need to output the number of devices，and do not output 
anything other than pure numbers.\n"""

first_device_start_template = """Ok, if we need <device total number> devices for testing, and in our task, you are
assigned the role of Device <current device number>. Do you think the task should start with you? If you believe the 
task should start with you, please output 'Test Start'; if you think the task should start with another device, please 
output 'Switch to device x'(x is that device's number), the output should be enclosed in single quotes.\n"""


def task_divide_template(app_name: str, overview_task: str, device_type_list: list):
    prompt = """"Now you are a task divider. I will tell you about our current testing task, and you need to divide 
    the subtasks to be completed by each device,. For example, let's assume our task is as follows: "In a video call 
    scenario, the initiating user opens the chat, clicks on the + sign, initiates a video call, and waits for the 
    other party to accept; the receiving user accepts the video call, and the video call window appears normally." 
    In this case, device 1's type is "user device", device 2's type is "user device". Then, the sub-tasks you need to
    break it down into are:
    1. You are the initiating user of the video call, and you need to open the chat with another user, click on the + sign, 
    initiate the video call, and then switch to device 2, wait for the other party to accept. 
    2. You are the receiving user of the video call, and you need to accept the video call and wait for the video call 
    window to appear normally.
    Note: You should add "switch to device x" in necessary place, especially when it is necessary to switch devices 
    after completing a task (or part of a task) on one device.
    Since our task is within the app, please do not include operations like opening/closing the app in the task description.
    """
    prompt += """\nNow we want to test "{}" app, The following is an overview of our tasks: "{}". Which {} sub-tasks do you 
    think our overview task should be divide into? Our devices types are as follows: \n""".format(app_name,
                                                                                                  overview_task,
                                                                                                  len(device_type_list))
    for i in range(len(device_type_list)):
        prompt += "Device{}: {}   ".format(str(i + 1), device_type_list[i])
    prompt += """\n You should output each sub-task line by line, and we need the sub-task order you output to correspond 
    one-to-one with the device types. For example, the first sub-task you output is the task that device 1 needs to perform, 
    the second sub-task is the task that device 2 needs to perform, and so on.\n"""
    return prompt


def add_new_mes(mes: list, p_rompt: str):
    new_mes = {"role": "user", "content": p_rompt}
    mes.append(new_mes)

