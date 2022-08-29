# enpit2022_summer_drone_ctrl

This ROS1 package is using with: 
- https://github.com/GNagahashi/enpit2022_summer.git

## How to use

1. Clone this repository in src directory in catkin workspace.
```sh
# e.g.
cd ~/catkin_ws/src
git clone https://github.com/GNagahashi/enpit2022_summer_drone_ctrl.git
# If you needed, rename directory.
mv enpit2022_summer_drone_ctrl/ drone_ctrl
```

2. Build on terminal.
```sh
# e.g.
cd ~/catkin_ws
catkin build
```

3. Run in terminal.
```sh
# e.g.
# source ~/catkin_ws/devel/setup.bash
rosrun enpit2022_summer_drone_ctrl drone_ctrl_gui.py
# or
rosrun drone_ctrl drone_ctrl_gui.py
```
