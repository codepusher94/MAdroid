class MemoryPool:
    def __init__(self):
        self.current_device = 1
        self.is_info1_ok = False
        self.is_info2_ok = False

        self.app_name = ""
        self.overview_task = ""
        self.device_type_list = []
        self.device_ip_list = []

        self.device_total_num = 1
        self.device_sub_task_list = []

        self.memory_pool_list = []

    def align_1(self, app_name: str, overview_task: str, device_type_list: list, device_ip_list: list):
        self.app_name = app_name
        self.overview_task = overview_task
        self.device_type_list = device_type_list
        self.device_ip_list = device_ip_list

        self.is_info1_ok = True

    def align_2(self, device_total_num: int, device_sub_task_list: list):
        self.device_total_num = device_total_num
        self.device_sub_task_list = device_sub_task_list

        self.is_info2_ok = True

