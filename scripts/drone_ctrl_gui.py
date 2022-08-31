#!/usr/bin/env python
# >>> import sys; sys.version
# '2.7.17 (default, Jul  1 2022, 15:56:32) \n[GCC 7.5.0]'

"""
This program don't send message for ROS Topic.
Only GUI.
"""


import os
import tkinter as tk
from enum import Enum
import rospy
from std_msgs.msg import String


def main():
    file_path, _ = os.path.split(os.path.abspath(__file__))

    # Create and setting for app window
    app = tk.Tk()
    app.title('Drone App')
    app.minsize(700, 476)
    app.resizable(False, False)

    # Create Publisher node
    publisher = rospy.Publisher('/gnc_node/cmd', String, queue_size = 10)
    rospy.init_node('command_pub', anonymous = True)
    r = rospy.Rate(1)

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
    e_handler = EventHandler(app)
    app.bind('<ButtonPress>', lambda e: e_handler.drone_ctrl_by_button(e, label_p1, publisher, r))
    app.bind('<ButtonRelease>', lambda e: e_handler.stop_drone(e, publisher, r, CmdText.START, CmdText.GRAB))

    app.mainloop()


class EventHandler(object):
    def __init__(self, root, delay_ms = 0):
        self.__state = True
        self.root_frame = root
        self.delay_ms = delay_ms  # ms

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
                msg = String(data = cmd)
                label['text'] = e.widget['text']
                print('Send message: {}'.format(cmd))
                pub.publish(msg)
                self.disable_handler()
                rate.sleep()
            else:
                print('Press invalid widget or Can not send msg to Topic')
        else:
            print('Event handler is disable or Press invalid button')

    def stop_drone(self, e, pub, rate, *args):
        if self.__state and e.widget.widgetName == 'button' and not ''.join([arg.value for arg in args if e.widget['text'].lower() == arg.value]):
            msg = String(data = 'stop')
            print('Send message: stop')
            pub.publish(msg)
            self.disable_handler()
            rate.sleep()
        else:
            print('Cancelled: send "stop" message (Release invalid widget or Event handler is disable)')


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
