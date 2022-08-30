# enpit2022_summer_drone_ctrl

This ROS1 package is using with: 
- https://github.com/GNagahashi/enpit2022_summer.git

## How to use

1. Clone this repository in src directory in catkin workspace.
```sh
# e.g.
cd ~/catkin_ws/src
git clone https://github.com/GNagahashi/enpit2022_summer_drone_ctrl.git
```

2. Rename this repository in the local from "enpit2022_summer_drone_ctrl" to "drone_ctrl".
```sh
# e.g.
cd ~/catkin_ws/src
mv enpit2022_summer_drone_ctrl/ drone_ctrl
```

3. Build on terminal.
```sh
# e.g.
cd ~/catkin_ws
catkin build
# or
catkin build drone_ctrl
```

4. Run in terminal.
```sh
# e.g.
# source ~/catkin_ws/devel/setup.bash
# roscore
rosrun drone_ctrl drone_ctrl_gui.py
```
