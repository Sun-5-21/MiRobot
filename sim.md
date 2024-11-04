
## 仿真环境搭建

在赛事组提供的docker镜像中，已将实验所需的软件环境包含：

+ ros2-galactic (文件目录：/opt/ros/galactic)
+ gazebo11
+ eigen 库 (文件目录：/home/eigen-git-mirror)
+ lcm 通信库 (文件目录：/home/lcm) 
+ cyberdog 功能包（文件目录：/home/cyberdog_ws，该文件包含了 cyberdog 的主 要功能包、cyberdog 的全局管理、运控管理等 ROS 节点及通用接口库等)
+ cyberdog 仿真平台（文件目录：/home/cyberdog_sim，该文件包含了必要的 cyberdog_locomotion 及 cyberdog_simulator 两个平台。仿真提供了基于 Rviz2 的可 视化工具，将机器人状态的 lcm 数据转发到 ROS）

跟随[环境搭建教程](https://gitlab.eduxiji.net/csc1/csc-is/is2024/-/blob/main/cyberdog_race%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.pdf)即可部署仿真环境。

## 项目简介

### cyberdog_sim目录

位于`/home/cyberdog_sim`目录，Cyberdog SIM 整合`cyberdog_locomotion`与`cyberdog_simulator`仓库，实现gazebo与ROS2环境下的四足机器人仿真，同时，提供了基于Riz2的可视化工具，将机器人的状态lcm数据转发为ROS2 topics。

<img src="/Users/zhao2z/Library/Application Support/typora-user-images/image-20240428173837390.png" alt="image-20240428173837390" style="zoom: 67%;" />

在`install/`目录下，存放着一些setup脚本，用于配置和扩展环境变量以支持 ROS（Robot Operating System）的 Galatic 版本和其他相关软件包。其主要作用是在一个 ROS 项目中，确保各种依赖的环境设置被正确加载。

在`build/`目录下，存储了项目编译过程中生成的所有中间文件、编译缓存和对象文件。这些文件是源代码编译成可执行文件和库文件过程中产生的。

在`src/`目录下，则是两个子项目`cyberdog_locomotion`和`cyberdog_simulator`。

项目Github链接：https://github.com/MiRoboticsLab/cyberdog_sim

### cyberdog_locomotion项目

**MiRoboticsLab/cyberdog_locomotion** 项目是小米四足机器人的运动控制库，目录结构：

<img src="/Users/zhao2z/Library/Application Support/typora-user-images/image-20240428174351013.png" alt="image-20240428174351013" style="zoom: 67%;" />

主要包括以下几个部分：

- **common**：包含项目所需的公共配置、头文件和源代码。这包括动力学模型、控制器、命令接口、工具以及参数处理的头文件和实现。
- **control**：包含机器人的主要控制算法和系统。其子目录中有平衡控制器、估算器、有限状态机（FSM）、离线优化控制器、位置控制器、轨迹生成器和整体控制器（WBC）。
- **docker**：含有Dockerfile和使用Docker设置开发环境的指导。
- **document**：提供项目中使用的第三方库的许可证和文档。
- **hardware**：关注与硬件的集成，包括硬件抽象层、实时控制和管理硬件通信的实用工具。
- **scripts**：包含各种脚本，用于在硬件层面或在模拟中部署、管理和与系统交互。



在`scripts/`目录下，有多个脚本文件，每个文件都承担特定的功能，主要用于系统配置、管理和调试。以下是部分重要脚本的详细功能：

1. **adb_to_cyberdog.sh** - 将打包的软件和管理脚本通过ADB（Android Debug Bridge）推送到机器人硬件上。
2. **auto_lcminit_bp1.sh** - 自动配置网络以支持LCM（轻量级通信和封送），用于实时机器人控制消息的发布和订阅。
3. **config_network_lcm.sh** - 配置网络接口以支持LCM，包括对不同操作系统的适配和多个网络配置选项。
4. **get_git_hash.sh** - 生成当前Git仓库的哈希值和版本字符串，用于标识当前部署的软件版本。
5. **launch_lcm_log.sh / launch_lcm_logplayer.sh / launch_lcm_spy.sh** - 这些脚本用于启动LCM日志记录器、日志播放器和网络监控工具，以便于开发和调试过程中监控消息传递。
6. **make_types.sh** - 生成LCM消息类型的定义，这对于LCM系统中的消息传递至关重要。
7. **manager** - 一个shell脚本，用于启动和管理机器人的主控制过程。
8. **nx2loco.sh** - 通过SSH连接和控制网络中的机器人硬件，执行远程命令并同步数据。
9. **pack_runnable.sh** - 打包构建后的软件，准备用于部署。
10. **scp_by_nx_ip.sh / scp_to_cyberdog.sh** - 这些脚本通过SCP（安全复制协议）将软件包和配置从开发环境传输到机器人硬件。

这些脚本为机器人系统提供了全面的软件生命周期管理，包括开发、测试、部署和维护阶段的各种操作，确保系统能够在不同环境和配置下正常运行和调试。

### cyberdog_simulator项目

该[项目](https://github.com/MiRoboticsLab/cyberdog_simulator)用于模拟和测试CyberDog的运动和控制系统。项目包含几个主要的文件夹和文件，目录结构：

<img src="/Users/zhao2z/Library/Application Support/typora-user-images/image-20240428185113720.png" alt="image-20240428185113720" style="zoom: 67%;" />

**主要文件夹和文件功能：**

1. **cyberdog_example**
   - 包含示例应用程序代码，例如`keybroad_commander`键盘控制器和`cyberdogmsg_sender`消息发送器，用于演示如何与仿真环境中cyberdog进行交互。
2. **cyberdog_gazebo**
   - 这个文件夹是项目的**核心**，包含用于在Gazebo仿真环境中实现cyberdog模型的代码和资源。
   - 包括多个子文件夹，如 `include` 和 `src`，分别包含头文件和源代码，实现cyberdog的控制逻辑、传感器模拟和动态行为。
   - 提供了多个launch文件，用于启动Gazebo仿真环境和cyberdog模型。
3. **cyberdog_msg**
   - 定义了用于cyberdog仿真器之间通信的消息格式，如应力和参数配置。
4. **cyberdog_robot**
   - 包含cyberdog机器人模型的描述和视觉资源，使用xacro和dae格式。
   - 提供了RViz配置文件，用于在RViz中可视化cyberdog模型。
5. **cyberdog_visual**
   - 提供了一个用于视觉演示和回放的框架，包括LCM消息类型定义和RViz视觉配置。

**功能细节：**

- **Cyberdog控制与传感器模拟**：通过 `cyberdog_gazebo` 中的插件和控制参数实现。
- **仿真环境设置**：`launch` 文件夹包含用于设置和配置仿真环境的启动脚本。
- **通信和消息传递**：使用LCM进行跨进程或跨网络的数据通信。

#### Gazebo仿真平台

gazebo仿真平台能够使gazebo仿真程序直接与cyeberdog的控制程序cybredog_control进行通信，并将机器人的各关节数据与传感器数据转发为ros2 topic。

<img src="https://miroboticslab.github.io/blogs/cn/image/cyberdog_gazebo/flow.jpg" alt="img" style="zoom: 25%;" />

- cyberdog控制程序和gazebo之间通过sharedmemory进行通信，gazebo程序创建host的共享内存，控制程序通过attach到该内存上进行通信。其通信的内容为robotToSim/simToRobot。
- ros2仿真界面接受从控制程序通过lcm发送的电机和里程计信号等信号并通过topic转发为 /joint_states 与 /tf。
  - 可通过发送topic /yaml_parameter 向gazebo程序发送yaml中的robotparamter和userparameter的变更值，再由gazebo通过sharedmemory发送给控制程序。
- gazebo仿真程序会将仿真中的imu与激光雷达的数据以ros2 topic的形式进行发送，其topic名称为 /imu 和 /scan

运行Gazebo仿真程序可参考[教程](https://miroboticslab.github.io/blogs/#/cn/cyberdog_gazebo_cn?id=gazebo%e4%bb%bf%e7%9c%9f%e5%b9%b3%e5%8f%b0)。

## 仿真运动例程

在`cyberdog_simulator/cyberdog_example`中提供了仿真例程包，源代码见：https://github.com/MiRoboticsLab/cyberdog_simulator/tree/main/cyberdog_example

### keybroad_commander

keybroad_commander演示了如何使用gampad_lcmt向控制发送基本控制指令，keybroad_commander.cpp是一个基于ROS和LCM的仿真控制程序，用于模拟和控制CyberDog的行为。主要功能是通过键盘输入来控制仿真中的Cyberdog机器人。以下是对代码关键部分的分析和解释：


这段代码是一个使用ROS (Robot Operating System) 和 LCM (Lightweight Communications and Marshalling) 实现的机器人控制程序。其核心逻辑包括：

1. **ROS初始化和发布消息**：
   - 使用`rclcpp::init`初始化ROS节点系统。
   - 创建一个`ExampleNode`实例，该节点名为"kdcommand_node"。
   - 在这个节点上，创建一个名为"yaml_parameter"的发布者`para_pub_`，用于发布`cyberdog_msg::msg::YamlParam`类型的消息。
   - 发布一条消息，将参数`"use_rc"`设置为0，这可能用于切换游戏手柄控制模式，使得从模拟器程序进行控制成为可能。
2. **LCM初始化和消息循环**：
   - 初始化一个LCM实例`lcm_`并检查其状态。
   - 进入无限循环，接收用户输入指令并根据输入修改`gamepad_lcmt`结构体中的值，该结构体代表游戏手柄的状态。
   - 根据输入的键（如'w', 's', 'd', 'a'等）调整游戏手柄的模拟摇杆位置，影响机器人的运动和操作。
   - 使用`lcm_.publish`将修改后的`gamepad_lcmt`发布到LCM通道"gamepad_lcmt"。
3. **LCM消息控制**：
   - 在无限循环中，每次循环捕捉用户键盘输入，并据此调整手柄模拟的摇杆和按钮状态。
   - 除了基本的移动控制（前后左右、俯仰、偏航），还可以通过特定的键（如'e', 'r', 't', 'y'）控制机器人的其他动作（如站立、移动、恢复站立等）。
   - 在每次循环的末尾清除按钮状态（x, y, a, b），以避免命令的重复触发。

<img src="/Users/zhao2z/Library/Application Support/typora-user-images/image-20240428230023328.png" alt="image-20240428230023328" style="zoom: 67%;" />

这段代码通过键盘输入模拟了一个游戏手柄的功能，使用户能够实时控制Cyberdog仿真模型的动作和移动。



该程序运行方法如下（镜像中已提前编译放置在build目录下）：

````shell
# 在cyberdog_sim路径下
source /opt/ros/galactic/setup.bash
source install/setup.bash
./build/cyberdog_example/keybroad_commander
````

<video src="keyboard.mp4" />

### cyberdogmsg_sender

cyberdogmsg_sender演示了使用/yaml_parameter来对yaml文件中的控制参数进行实时修改，以及使用/apply_force来仿真中的机器人施加外力，其代码核心逻辑如下：

1. **初始化和创建发布者**:
   - 初始化ROS 2，创建一个名为`ExampleNode`的节点。
   - 设置两个发布者`para_pub_`和`force_pub_`，用于发布不同类型的控制消息（`YamlParam`和`ApplyForce`）。
2. **发送控制命令**:
   - 使用`YamlParam`消息切换cyberdog的控制模式，包括从手柄控制到恢复站立模式，再到移动控制模式。
   - 使用`ApplyForce`消息对cyberdog的特定部位（如前左腿的膝关节）施加力。
3. **执行和反馈**:
   - 在关键的控制命令之间使用暂停（`sleep`）确保命令得到处理。
   - 通过控制台输出提供执行反馈，通知当前控制模式的变更和施加力的状态。

该程序的运行方法如下（镜像中已提前编译放置在build目录下）：

````shell
# 在cyberdog_sim目录下运行
source /opt/ros/galactic/setup.bash
source install/setup.bash
./build/cyberdog_example/cyberdogmsg_sender
````

该例程先把参数use_rc置为0(该参数为1时为遥控模式，置为0后才能够通过仿真程序进行控制)；
然后通过设置control_mode参数使机器人站立起来，并进入locomotion模式，即原地踏步(control_mode的参数可参阅控制程序的control_flag.h文件)；
接着对机器人的左前小腿施加侧向的外力； 最后通过修改des_roll_pitch_height参数使机器人在踏步时roll角变为0.2弧度。

<video src="cyberdog.mp4"/>

---

在这两个示例中，我们展示了如何在C++中调用ROS和LCM库。我们鼓励同学们通过仔细阅读相关文档和源码来掌握机器人运动控制的编程技巧。

想要使用Python进行Cyberdog控制的同学，可以参考以下教程： [Python控制Cyberdog教程](https://miroboticslab.github.io/blogs/#/cn/cyberdog_loco_cn?id=_24-接口示例)

## 参考阅读

1. 运动控制二次开发接口：https://miroboticslab.github.io/blogs/#/cn/cyberdog_loco_cn
2. 仿真平台模块：https://miroboticslab.github.io/blogs/#/cn/cyberdog_gazebo_cn
3. Cyberdog_sim项目源码：https://github.com/MiRoboticsLab/cyberdog_sim
4. 开发者手册：https://miroboticslab.github.io/blogs/#/cn/developer_guide
5. cyberdog_ws项目源码：https://github.com/MiRoboticsLab/cyberdog_ws