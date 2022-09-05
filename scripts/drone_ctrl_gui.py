#!/usr/bin/env python
# >>> import sys; sys.version
# '2.7.17 (default, Jul  1 2022, 15:56:32) \n[GCC 7.5.0]'


import os
from enum import Enum
from functools import partial
import tkinter as tk
import rospy
from std_msgs.msg import String
from drone_position.srv import CheckPos
"""
Define of msg/srv

- String:
    string data
- CheckPos:
    string request
    ---
    bool response
"""


def main():
    # Name used by ROS (service, topic)
    gnc_node_cmd = '/gnc_node/cmd'
    check_position = 'check_position'
    file_path, _ = os.path.split(os.path.abspath(__file__))

    # Create and setting for app window
    app = tk.Tk()
    app.title('Drone claw machine')
    app.minsize(700, 476)
    app.resizable(False, False)

    # Create event handler
    e_handler = EventHandler(app)

    # Create node
    rospy.init_node('drone_ctrl', anonymous = True)

    # Create Publisher
    rospy.loginfo('Create publisher for {}, please wait a minute...'.format(gnc_node_cmd))
    publisher = rospy.Publisher(gnc_node_cmd, String, queue_size = 10)
    # Create client 
    rospy.loginfo('Create client for {}, please wait a minute...'.format(check_position))
    rospy.wait_for_service(check_position)
    e_handler.handler_for_check_position = rospy.ServiceProxy(check_position, CheckPos)
    r = rospy.Rate(1)

    rospy.loginfo('Ready to GUI app')

    # Create frame
    frame_label = tk.Frame(
        app,
        padx = 12,
        pady = 12,
    )
    frame_btn_move = tk.Frame(
        app,
        padx = 12,
        pady = 12,
    )
    subframe_btn_move = tk.Frame(
        frame_btn_move,
    )
    frame_btn_other = tk.Frame(
        app,
        padx = 12,
        pady = 12,
    )
    subframe_btn_other = tk.Frame(
        frame_btn_other,
    )

    # Create widget
    # label
    label_h1 = tk.Label(
        frame_label,
        anchor = tk.W,
        font = ('Helvetica', 12),
        text = 'History:',
    )
    label_p1 = tk.Label(
        frame_label,
        anchor = tk.W,
        font = ('Helvetica', 12),
        text = '',
    )
    # button
    img_start = tk.PhotoImage(
        file = file_path + '/drone_ctrl_gui_button-button_round_y.png',
    )
    button_start = tk.Button(
        subframe_btn_other,
        relief = tk.FLAT,
        font = ('Helvetica', 12),
        text = CmdText.START.value.capitalize(),
        compound = 'center',
        image = img_start,
    )
    img_grab = tk.PhotoImage(
        file = file_path + '/drone_ctrl_gui_button-button_round_p.png',
    )
    button_grab = tk.Button(
        subframe_btn_other,
        relief = tk.FLAT,
        font = ('Helvetica', 12),
        text = CmdText.GRAB.value.capitalize(),
        compound = 'center',
        image = img_grab,
    )
    img_forward = tk.PhotoImage(
        file = file_path + '/drone_ctrl_gui_button-button_forward.png',
    )
    button_forward = tk.Button(
        subframe_btn_move,
        relief = tk.FLAT,
        font = ('Helvetica', 12),
        text = CmdText.FORWARD.value.capitalize(),
        compound = 'center',
        image = img_forward,
    )
    img_backward = tk.PhotoImage(
        file = file_path + '/drone_ctrl_gui_button-button_backward.png',
    )
    button_backward = tk.Button(
        subframe_btn_move,
        relief = tk.FLAT,
        font = ('Helvetica', 12),
        text = CmdText.BACKWARD.value.capitalize(),
        compound = 'center',
        image = img_backward,
    )
    img_left = tk.PhotoImage(
        file = file_path + '/drone_ctrl_gui_button-button_left.png',
    )
    button_left = tk.Button(
        subframe_btn_move,
        relief = tk.FLAT,
        font = ('Helvetica', 12),
        text = CmdText.LEFT.value.capitalize(),
        compound = 'center',
        image = img_left,
    )
    img_right = tk.PhotoImage(
        file = file_path + '/drone_ctrl_gui_button-button_right.png',
    )
    button_right = tk.Button(
        subframe_btn_move,
        relief = tk.FLAT,
        font = ('Helvetica', 12),
        text = CmdText.RIGHT.value.capitalize(),
        compound = 'center',
        image = img_right,
    )

    # Set widget on top of a frame
    label_h1.pack(
        side = tk.LEFT,
        padx = (0, 6),
    )
    label_p1.pack(
        expand = True,
        fill = tk.X,
        side = tk.LEFT,
        padx = (0, 6),
    )
    button_start.pack(
        side = tk.TOP,
    )
    button_grab.pack(
        side = tk.BOTTOM,
    )
    button_forward.grid(
        column = 1,
        row = 0,
    )
    button_backward.grid(
        column = 1,
        row = 2,
    )
    button_left.grid(
        column = 0,
        row = 1,
    )
    button_right.grid(
        column = 2,
        row = 1,
    )

    # Set frame on top of a window
    frame_label.pack(
        expand = True,
        fill = tk.BOTH,
        side = tk.TOP,
        anchor = tk.N,
    )
    subframe_btn_move.pack()
    frame_btn_move.pack(
        expand = True,
        fill = tk.Y,
        side = tk.LEFT,
    )
    subframe_btn_other.pack(
        expand = True,
        fill = tk.Y,
    )
    frame_btn_other.pack(
        expand = True,
        fill = tk.Y,
        side = tk.RIGHT,
    )

    # Bind function
    app.bind('<ButtonPress>', lambda e: e_handler.drone_ctrl_by_button(e, label_p1, publisher, r))
    app.bind('<ButtonRelease>', lambda e: e_handler.drone_stop(e, publisher, r, CmdText.START, CmdText.GRAB))

    # Create menu bar
    app_menubar = tk.Menu()

    menu_system = tk.Menu(app_menubar, tearoff = False)
    menu_system.add_command(
        label = 'Close this application',
        command = app.destroy,
    )
    menu_drone = tk.Menu(app_menubar, tearoff = False)
    menu_drone.add_command(
        label = 'Send "halt" event to drone',
        command = partial(e_handler.drone_halt, publisher, r),
    )

    app_menubar.add_cascade(
        label = 'System',
        menu = menu_system,
    )
    app_menubar.add_cascade(
        label = 'Drone',
        menu = menu_drone,
    )

    app.config(
        menu = app_menubar,
    )

    app.mainloop()


class EventHandler(object):
    def __init__(self, root, delay_ms = 0):
        self.__state = True
        self.root_frame = root
        self.delay_ms = delay_ms
        self.__handler_for_check_position = None

    @property
    def handler_for_check_position(self):
        return self.__handler_for_check_position

    @handler_for_check_position.setter
    def handler_for_check_position(self, handler):
        self.__handler_for_check_position = handler

    def disable_handler(self):
        if self.delay_ms != 0:
            self.root_frame.after(self.delay_ms, self.enable_handler)
            self.__state = False
            print('Event handler is disable for {} ms'.format(self.delay_ms))

    def enable_handler(self):
        self.__state = True
        print('Event handler is enable')

    def drone_ctrl_by_button(self, e, label, pub, rate):
        if self.__state and e.widget.widgetName == 'button':
            cmd = e.widget['text'].lower()
            if CmdText.is_member(cmd) and not rospy.is_shutdown():
                label['text'] = e.widget['text']
                msg = String(data = cmd)
                pub.publish(msg)
                rospy.loginfo('Send message: {}'.format(cmd))
                self.disable_handler()
                rate.sleep()
                if cmd == CmdText.GRAB.value:
                    if self.is_grab():
                        label['text'] = label['text'] + ' -> Success, You are get prize!'
                    else:
                        label['text'] = label['text'] + ' -> Failure, Try agein!'
            else:
                print('Press invalid widget or Could not send msg(data = {}) to Topic'.format(cmd))
        else:
            print('Press invalid button or Event handler is disable')

    def drone_stop(self, e, pub, rate, *args):
        if e.widget.widgetName == 'button' and not rospy.is_shutdown() and not ''.join([arg.value for arg in args if e.widget['text'].lower() == arg.value]):
            msg = String(data = 'stop')
            pub.publish(msg)
            rospy.loginfo('Send message: stop')
            rate.sleep()
        else:
            print('Could not send msg(data = stop) to Topic (An invalid button may have been released)')

    def drone_halt(self, pub, rate):
        if not rospy.is_shutdown():
            msg = String(data = 'halt')
            pub.publish(msg)
            rospy.loginfo('Send message: halt')
            rate.sleep()
        else:
            print('Could not send msg(data = halt) to Topic')

    def is_grab(self):
        res = self.handler_for_check_position('Can drone grab a prize?')
        return res.response


class CmdText(Enum):
    START = 'start'
    GRAB = 'grab'
    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'left'
    RIGHT = 'right'

    @classmethod
    def is_member(cls, txt):
        if ''.join([key.value for key in CmdText if txt == key.value]):
            return True
        return False


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    finally:
        print('bye')
