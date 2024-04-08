# Evaluation

We provide the experimental setup we used to evaluate MADROID in terms of its performance.

- **RQ1:** How effective is our approach in automating multi-user interactive feature tasks?
- **RQ2:** How does our approach compare to the state-of-the-art methods?
- **RQ3:** How useful is our approach in real-world multi- user interactive feature testing?

For RQ1, we present the general performance of our approach in automating multi-user interactive tasks.
Moreover, we assess the impact of individual components within our approach by conducting an ablation study. 
For RQ2, we carry out experiments to check the effectiveness of our approach against three state-of-the-art baselines. 
For RQ3, we evaluate the usefulness of our approach to detect interactive bugs within real-world development environments.

## Experimental Dataset Collection

Task Id | App                                                                                           | App Version                          | App Downloads | Task Description
--- |-----------------------------------------------------------------------------------------------|--------------------------------------|---------------|-|
[1](Dataset/tiktok_task1) | *[TikTok](https://play.google.com/store/apps/details?id=com.ss.android.ugc.trill)*            | 33.2.0                               | 500M+         | UserA invites UserB by voice video
[2](Dataset/tiktok_task2) | *[Tiktok](https://play.google.com/store/apps/details?id=com.ss.android.ugc.trill)*            | 33.2.0                               | 500M+         | UserA sends a call connection to UserB
[3](Dataset/tiktok_task3) | *[Tiktok](https://play.google.com/store/apps/details?id=com.ss.android.ugc.trill)*            | 33.2.0                               | 500M+         | UserA sends an interactive card, activated by UserB
[4](Dataset/tiktok_task4) | *[Tiktok](https://play.google.com/store/apps/details?id=com.ss.android.ugc.trill)*            | 33.2.0                               | 500M+         | UserA comments UserB in live stream
[5](Dataset/tiktok_task5) | *[Tiktok](https://play.google.com/store/apps/details?id=com.ss.android.ugc.trill)*            | 33.2.0                               | 500M+         | UserA sends a PK invitation to UserB
[6](Dataset/skype_task1) | *[Skype](https://play.google.com/store/apps/details?id=com.skype.raider)*                     | 8.112.0.210                          | 1B+           | UserA makes a video call to UserB
[7](Dataset/skype_task2) | *[Skype](https://play.google.com/store/apps/details?id=com.skype.raider)*                     | 8.112.0.210                          | 1B+           | UserA starts a group call, UserB and UserC join
[8](Dataset/skype_task3) | *[Skype](https://play.google.com/store/apps/details?id=com.skype.raider)*                     | 8.112.0.210                          | 1B+           | UserA makes a voice call to UserB , then invite UserC to join
[9](Dataset/skype_task4) | *[Skype](https://play.google.com/store/apps/details?id=com.skype.raider)*                     | 8.112.0.210                          | 1B+           | UserA invites UserB and UserC to join conference meeting
[10](Dataset/skype_task5) | *[Skype](https://play.google.com/store/apps/details?id=com.skype.raider)*                     | 8.112.0.210                          | 1B+           | UserA invites UserB to join conference meeting, then UserC
[11](Dataset/snapchat_task1) | *[Snapchat](https://play.google.com/store/apps/details?id=com.snapchat.android)*              | 12.76.0.34                           | 1B+           | UserA invites UserB to real-time location sharing
[12](Dataset/snapchat_task2) | *[Snapchat](https://play.google.com/store/apps/details?id=com.snapchat.android)*              | 12.76.0.34                           | 1B+           | UserA makes a voice call to UserB
[13](Dataset/snapchat_task3) | *[Snapchat](https://play.google.com/store/apps/details?id=com.snapchat.android)*              | 12.76.0.34                           | 1B+           | UserA starts a group call and UserB joins
[14](Dataset/wechat_task1) | *[Wechat](https://play.google.com/store/apps/details?id=com.tencent.mm)*                      | 3.8.5                                | 100M+         | UserA invites UserB by face-to-face code
[15](Dataset/wechat_task2) | *[Wechat](https://play.google.com/store/apps/details?id=com.tencent.mm)*                      | 3.8.5                                | 100M+         | UserA makes a video call to UserB
[16](Dataset/douyin_task1) | *[Douyin](https://www.douyin.com/?recommend=1)*                                               | 27.6.0                               | 500M+         | UserA makes a video call to UserB
[17](Dataset/douyin_task2) | *[Douyin](https://www.douyin.com/?recommend=1)*                                               | 27.6.0                               | 500M+         | UserA makes a video call to UserB and UserC
[18](Dataset/douyin_task3) | *[Douyin](https://www.douyin.com/?recommend=1)*                                               | 27.6.0                               | 500M+         | UserA invites UserB to play together
[19](Dataset/douyin_task4) | *[Douyin](https://www.douyin.com/?recommend=1)*                                               | 27.6.0                               | 500M+         | UserA invites UserB from group chat to watch together
[20](Dataset/douyin_task5) | *[Douyin](https://www.douyin.com/?recommend=1)*                                               | 27.6.0                               | 500M+         | UserA invites UserB by face-to-face code
[21](Dataset/googlemeet_task1) | *[GoogleMeet](https://play.google.com/store/apps/details?id=com.google.android.apps.tachyon)* | 231.0.<br/>604156477.duo.<br/>android_2024 | 5B+           | UserA starts a conference meeting, UserB joins by code
[22](Dataset/googlemeet_task2) | *[GoogleMeet](https://play.google.com/store/apps/details?id=com.google.android.apps.tachyon)* | 231.0.<br/>604156477.duo.<br/>android_2024 | 5B+           | UserA invites UserB to video conference meeting
[23](Dataset/gmail_task1) | *[Gmail](https://play.google.com/store/apps/details?id=com.google.android.gm)*                | 2024.02.04.<br/>604829058    | 10B+          | UserA invites UserB to video conference meeting
[24](Dataset/gmail_task2) | *[Gmail](https://play.google.com/store/apps/details?id=com.google.android.gm)*                | 2024.02.04.<br/>604829058    | 10B+          | UserA lowers UserB raised hand in conference meeting
[25](Dataset/messenger_task1) | *[Messager](https://play.google.com/store/apps/details?id=com.facebook.orca)* | 447.0.0.0.4                          | 5B+           | UserA makes a video call to UserB
[26](Dataset/messenger_task2) | *[Messager](https://play.google.com/store/apps/details?id=com.facebook.orca)* | 447.0.0.0.4                          | 5B+           | UserA makes a voice call to UserB , who switches to video
[27](Dataset/mega_task1) | *[MEGA](https://play.google.com/store/apps/details?id=mega.privacy.android.app)* | 11.6(240380719)<br/>(1e9f45c749)          | 5B+           | UserA makes a video call to UserB
[28](Dataset/teams_task1) | *[Microsoft Teams](https://play.google.com/store/apps/details?id=com.microsoft.teams)* | 1416/1.0.0.<br/>2021032401 | 100M+         | UserA makes a video call to UserB
[29](Dataset/teams_task2) | *[Microsoft Teams](https://play.google.com/store/apps/details?id=com.microsoft.teams)* | 1416/1.0.0.<br/>2021032401 | 100M+         | UserA invites UserB to video conference meeting
[30](Dataset/teams_task3) | *[Microsoft Teams](https://play.google.com/store/apps/details?id=com.microsoft.teams)* | 1416/1.0.0.<br/>2021032401 | 100M+         | UserA makes a video call to UserB and UserC
[31](Dataset/telegram_task1) | *[Telegram](https://play.google.com/store/apps/details?id=org.telegram.messenger)* | 10.9.2 | 1B+           | UserA makes a video call to UserB
[32](Dataset/telegram_task2) | *[Telegram](https://play.google.com/store/apps/details?id=org.telegram.messenger)* | 10.9.2 | 1B+           | UserA makes a voice call to UserB , who switches to video
[33](Dataset/whatsapp_task1) | *[Whatsapp Messager](https://play.google.com/store/apps/details?id=com.whatsapp)* | 2.24.5.77 | 5B+           | UserA makes a video call to UserB
[34](Dataset/whatsapp_task2) | *[Whatsapp Messager](https://play.google.com/store/apps/details?id=com.whatsapp)* | 2.24.5.77 | 5B+           | UserA starts a group call and UserB joins


To gather a collection of multi-user tasks, we recruited four Master students with two-year backgrounds in Android development.
The four annotators were assigned to investigate the 30 most popular apps on Google Play, chosen specifically for their popularity, as it often correlates with a higher likelihood of featuring multi-user interactive features. We asked them to independently navigate through these apps, identify multi-user interactive features, and label the ground truth, which included task descriptions and the corresponding execution traces.

To ensure the quality of the dataset, we invited two professional app developers from a large tech company to review the collected tasks. In total, we obtained 34 multi-user interactive tasks derived from 12 apps, with an average of 2.36 actions required per device to complete each task.
Note that, all the tasks were freshly identified and labeled by human annotators specifically for this study, mitigating the potential bias for data leakage that could arise from the use of LLMs.


## RQ1: Performance of MADROID

To answer RQ1, we evaluate the ability of our approach to accurately automate multi-user interactive features from a given task description. We set up three ablation studies as baselines to compare with our approach. MADROID is structured around two types of multi-agents: task agents (i.e., Operator) and methodology agents (i.e., Coordinator and Observer). As the task agents primarily focus on managing interactions with devices, we created variants of our approach that exclude the methodology agents to assess their individual contributions.

### Setup

1. Prepare a GPT API key, and go to approach/utils/base_utils/llm.py, replace the api_key with your own API key.
2. Make sure you have connected the devices via ADB and installed the necessary Python libraries dependencies.
3. Open the app you want to test and navigate to the social scene interface (ensure that each device has entered the interface).

### Operator only
First, we introduced a variant called *Operator only*. This variation operates solely on the Operator agents that given a multi-user interactive task, it autonomously determines the actions on the GUI screen to accomplish the task.

To conduct the experiments of *Operator only*, run the script in [Operator.py](Operator_only/operator.py)
```
# app's name
APP_NAME = "whatsapp"

# multi-user interactive task
TASK_DESCRIPTION = "A makes a voice call to B"

# device from the device farm
DEVICE_SERIES-1 = "emulator_5554"
DEVICE_SERIES-2 = "emulator_5555"
DEVICE_SERIES-N = ...

python operator.py --appname ${APP_NAME} \
                   --task ${TASK_DESCRIPTION} \
                   --dip ${DEVICE_SERIES-1} ... ${DEVICE_SERIES-N}
```

### Operator+Coordinator
Second, we set up a variant, namely *Operator+Coordinator*, that gains the planning capability of the Coordinator agent to deduce the number of devices needed, divide the tasks into sub-tasks, and determine the sequence of interactions.

To conduct the experiments of *Operator+Coordinator*, run the script in [main.py](Coordinator+Operator/main.py)
```
# app's name
APP_NAME = "whatsapp"

# multi-user interactive task
TASK_DESCRIPTION = "A makes a voice call to B"

# device from the device farm
DEVICE_SERIES-1 = "emulator_5554"
DEVICE_SERIES-2 = "emulator_5555"
DEVICE_SERIES-N = ...

python main.py --appname ${APP_NAME} --task ${TASK_DESCRIPTION} \
               --dip ${DEVICE_SERIES-1} ... ${DEVICE_SERIES-N}
```

### Operator+Observer
Third, to assess the importance of the Observer, we established another variant named *Operator+Observer*. In this setup, the Operator executes the task with the oversight and auditing functions that the Observer provides.

To conduct the experiments of *Operator+Observer*, run the script in [main.py](Operator+Observer/main.py)
```
# app's name
APP_NAME = "whatsapp"

# multi-user interactive task
TASK_DESCRIPTION = "A makes a voice call to B"

# device from the device farm
DEVICE_SERIES-1 = "emulator_5554"
DEVICE_SERIES-2 = "emulator_5555"
DEVICE_SERIES-N = ...

python main.py --appname ${APP_NAME} --task ${TASK_DESCRIPTION} \
               --dip ${DEVICE_SERIES-1} ... ${DEVICE_SERIES-N}
```

### Results

Our approach achieves an average action similarity of 93.1%, successfully completing 79.4% of multi-user interactive tasks, which significantly surpasses the results of the ablation baselines. For the detailed results, please refer to [result](../README.md).

## RQ2: Comparison with State-of-the-Art

To answer RQ2, we compare the performance of our approach with that of state-of-the-art baselines. We set up three state-of-the-art methods as baselines for comparison with our approach. These methods include one task-driven (AdbGPT) and two random-based (Monkey, Humanoid), all commonly utilized in automated app testing.


### Setup


**_Monkey_**

1. Install Android SDK: First, make sure you have the Android SDK installed on your machine. You can download it from the official Android developer website [here](https://developer.android.com/studio#downloads)
2. Set up Environment Variables: Set the ANDROID_HOME environment variable to the location of your Android SDK installation. Add the SDK's platform-tools and tools directories to your system's PATH variable.
3. Download AOSP Source Code: Download the Android Open Source Project (AOSP) source code. Follow the instructions on the AOSP website [here](https://source.android.com/setup/build/downloading) to download the source code using the repo tool.
4. Build the AOSP Source Code: Build the AOSP source code by following the instructions provided on the AOSP website [here](https://source.android.com/setup/build/building).
5. Navigate to Monkey Directory: Once the AOSP source code is built, navigate to the Monkey directory. The Monkey tool's source code is located in the following directory: path_to_aosp_source_code/frameworks/base/cmds/monkey
6. Build Monkey: Build the Monkey tool by running the following command:
```
make Monkey
```
7. Push Monkey to Device: Connect an Android device or emulator to your machine and push the Monkey binary to the device using the following command:
```
adb push path_to_aosp_source_code/out/target/product/device_name/system/bin/monkey /data/local/tmp
```
8. Grant Permissions: Grant execute permissions to the Monkey binary on the device using the following command:
```
adb shell chmod 777 /data/local/tmp/monkey
```
9. Run Monkey: Run the Monkey tool on the device using the following command:
```
adb shell /data/local/tmp/monkey -p your.package.name -v 500
Replace your.package.name with the package name of the app you want to test. The -v option is used to specify the number of events to generate (e.g., 500).
```

**_Humanoid_**
1. Prerequisite: Python 3.x, Tensorflow, DroidBot, PyFlann
2. Clone the Repository: First, you need to clone the repository from GitHub. Open your terminal and type the following command:
 ```
 git clone https://github.com/yzygitzh/Humanoid.git
 ```
3. Install Dependencies: Navigate to the cloned directory and install the required dependencies. You can do this by typing the following command:
 ```
 pip install -r requirements.txt
 ```
4. Start Humanoid service by
```
 python3 agent.py -c config.json
```
5. Running Humanoid:After seeing
```
=== Humanoid RPC service ready at localhost:50405 ===
```
you can start DroidBot instances with -humanoid localhost:50405 parameter. Now DroidBot will make use of Humanoid model when using model-based policies, such as dfs_greedy.

**_AdbGPT_**
1. Prerequisite: 

- Python 3.10.9
- Android Emulators in Genymotion
- ADB (Android Debug Bridge) version 1.0.41

2. Clone the Repository: First, you need to clone the repository from GitHub. Open your terminal and type the following command:
 ```
 git clone https://github.com/sidongfeng/AdbGPT.git
 ```

3. Install Dependencies following the requirements, especially updating OpenAI command-line interface (CLI), and set up the openai API key:
```
pip install --upgrade openai

# cfgs.py
OPENAI_TOKEN = <OPENAI_API_KEY>
```

4. Add a task-related actions in the script.
```
# main.py lines 24-25
action_prompt = """Available actions: [tap, input, scroll, double tap, long tap, switch_device, end_task]\n"""
primtive_prompt ="""Action primitives: [Tap] [Component], [Scroll] [Direction], [Input] [Component] [Value], [Double-tap] [Component], [Long-tap] [Component], [Switch_device] [Device_no] [Message], [End_task]\n""" 
```

5. Run the script for corresponding interactive task description.
```
python main.py
```

### Results
Our approach outperforms the others across all evaluated metrics, achieving an average increase of 47% in success rate and 31.2% in action similarity over the best baseline, AdbGPT.
Our observations indicate that Monkey and Humanoid manage to successfully cover 5.9% and 8.8% of the multi-user interactive tasks, respectively. This indicates that random exploration can incidentally cover some level of multi-user interactive features. However, this approach falls short for more complex multi-user interactive tasks.


## RQ3: Usefulness of MADROID

To answer RQ3, we assess the perceived usefulness of the MADROID in finding bugs in the real-world development scenarios of regression tests, i.e., taking task descriptions from previous app versions and applying them to the later versions to identify any bugs.
To this end, we first collected a sample of 18 open-source apps from F-Droid and engaged four annotators and two professional developers to identify 37 multi-user interactive tasks from the apps’ earlier releases.

> Please refer to the implementation of MAdroid for approach setup in [Approach](../approach/)

### Results

Issue Id | App               |  APK file                                                                           | Code Version | GitHub Stars | Bug report                                                              | Status 
--- |-------------|--------------------------------------------------------------------------------------------|--------------|--------------|-------------------------------------------------------------------------|--------|
1 | *[DeKu-SMS-Android](https://github.com/deku-messaging/Deku-SMS-Android )*           |  [data](https://github.com/deku-messaging/Deku-SMS-Android/tree/master/app/release) | 0.32.0                                                                                                                            | 144    |   [#156](https://github.com/deku-messaging/Deku-SMS-Android/issues/156) | fixed
2 | *[DeKu-SMS-Android](https://github.com/deku-messaging/Deku-SMS-Android )*           | [data](https://github.com/deku-messaging/Deku-SMS-Android/tree/master/app/release) | 0.32.0                                                                            | 144                                                         | [#213](https://github.com/deku-messaging/Deku-SMS-Android/issues/213)             | fixed
3 | *[Linphone-android](https://github.com/BelledonneCommunications/linphone-android )* | [data](https://download.linphone.org/releases/android/?C=M;O=D)                    | 5.1.0                                                                              | 1.1k                                         | [#2039](https://github.com/BelledonneCommunications/linphone-android/issues/2039)                           | fixed
4 | *[Linphone-android](https://github.com/BelledonneCommunications/linphone-android )* | [data](https://download.linphone.org/releases/android/?C=M;O=D)                    | 5.1.0                                                                             | 1.1k                                    | [#2061](https://github.com/BelledonneCommunications/linphone-android/issues/2061)                                | fixed
5 | *[Linphone-android](https://github.com/BelledonneCommunications/linphone-android )* | [data](https://download.linphone.org/releases/android/?C=M;O=D)                    | 5.1.0                                                                             | 1.1k                                     | [#2062](https://github.com/BelledonneCommunications/linphone-android/issues/2062)                               | fixed
6 | *[Messages](https://github.com/FossifyOrg/Messages )*                               | [data](https://github.com/FossifyOrg/Messages/releases)                            | 1.1.4                                                                             | 322                                        | [#41](https://github.com/FossifyOrg/Messages/issues/41)                              | confirmed
7 | *[Phone](https://github.com/FossifyOrg/Phone )*  |  [data](https://github.com/FossifyOrg/Phone/releases)                              | 5.18.1                                                                            | 299                                              | [#107](https://github.com/FossifyOrg/Phone/issues/107)                       | fixed




Across the testing of 37 multi-user interactive features on 18 apps, our MADROID identified 11 bugs involving 6 apps. To further validate the effectiveness of the detected bugs, we cross-referenced them with related issues reported in their respective repositories, where 7 bugs have been confirmed/fixed as shown in Table.



