#!/usr/bin/env python
# >>> import sys; sys.version
# '2.7.17 (default, Jul  1 2022, 15:56:32) \n[GCC 7.5.0]'

"""
This program don't send message for ROS Topic.
Only GUI.
"""


import tkinter as tk
from enum import Enum
# import rospy
# from std_msgs.msg import String


def main():
    # Create and setting for app window
    app = tk.Tk()
    app.title('Drone App')  # window title
    app.minsize(620, 280)  # window size
    app.resizable(False, False)  # fixed window size(both width and height)

    # Create Publisher node
    # publisher = rospy.Publisher('/gnc_node/cmd', String, queue_size = 10)  # Node settings
    # rospy.init_node('command_pub', anonymous = True)  # Define node name
    # r = rospy.Rate(1)  # Set publishing rate

    # Create frame
    frame_label = tk.Frame(
        app,
        padx = 12,  # padding[px]
        pady = 12,  # padding[px]
        bg = '#ff0000'
    )
    frame_btn = tk.Frame(
        app,
        padx = 12,  # padding[px]
        pady = 12,  # padding[px]
        bg = '#00ff00'
    )
    subframe_btn = tk.Frame(
        frame_btn,
        bg = '#0000ff',
    )

    # Create widget
    # label
    label_h1 = tk.Label(
        frame_label,
        anchor = tk.W,  # align left
        font = ('Helvetica', 12),
        text = 'History:',
    )
    label_p1 = tk.Label(
        frame_label,
        anchor = tk.W,  # align left
        font = ('Helvetica', 12),
        text = '',
    )
    # button
    button_start = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = CommandTxt.START.value.capitalize(),
    )
    button_grab = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = CommandTxt.GRAB.value.capitalize(),
    )
    button_forward = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = CommandTxt.FORWARD.value.capitalize(),
    )
    button_backward = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = CommandTxt.BACKWARD.value.capitalize(),
    )
    button_left = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = CommandTxt.LEFT.value.capitalize(),
    )
    button_right = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = CommandTxt.RIGHT.value.capitalize(),
    )

    # Set widget on top of a frame
    label_h1.pack(
        side = tk.LEFT,  # for this widget
        padx = (0, 6),  # margin(left, right)
    )
    label_p1.pack(
        expand = True,  # stretchable
        fill = tk.X,  # stretch direction
        side = tk.LEFT,  # for this widget
        padx = (0, 6),  # margin(left, right)
    )
    button_start.grid(
        column = 4,
        row = 2,
    )
    button_grab.grid(
        column = 3,
        row = 2,
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
        expand = True,  # stretchable
        fill = tk.BOTH,  # stretch direction
        side = tk.TOP,  # for this frame
        anchor = tk.N,  # for widgets in this frame
    )
    subframe_btn.pack(
        side = tk.TOP,  # for this frame
        anchor = tk.CENTER,  # for widgets in this frame
    )
    frame_btn.pack(
        expand = True,  # stretchable
        fill = tk.BOTH,  # stretch direction
        side = tk.TOP,  # for this frame
        anchor = tk.N,  # for widgets in this frame
    )

    # Bind function
    e_handler = EventHandler(app, 0)
    app.bind('<ButtonPress>', lambda e: e_handler.drone_ctrl_by_button(e, label_p1))
    app.bind('<ButtonRelease>', lambda e: e_handler.stop_drone(e, CommandTxt.START, CommandTxt.GRAB))

    app.mainloop()


class EventHandler(object):
    def __init__(self, root, delay):
        self.__state = True
        self.root_frame = root
        self.delay = delay  # ms

    def disable_handler(self):
        if self.delay != 0:
            self.root_frame.after(self.delay, self.enable_handler)
            self.__state = False

    def enable_handler(self):
        self.__state = True
        print('Event handler is enable')

    def drone_ctrl_by_button(self, e, label):  # (self, e, label, pub, rate)
        if self.__state and e.widget.widgetName == 'button':  # key can press and widget is button?
            cmd = e.widget['text'].lower()
            if CommandTxt.is_member(cmd):  # and not rospy.is_shutdown()
                # msg = String(data = cmd)
                label['text'] = e.widget['text']
                print('Send message: {}'.format(cmd))  # rospy.loginfo('Send command: {}'.format(msg.data))
                # pub.publish(msg)
                self.disable_handler()
                # rate.sleep()
            else:
                print('Press invalid widget or Can not send msg to Topic')
        else:
            print('Event handler is disable or Press invalid button')

    def stop_drone(self, e, *args):  # (self, e, pub, rate, *args)
        if e.widget.widgetName == 'button' and not ''.join([arg.value for arg in args if e.widget['text'].lower() == arg.value]):
            # msg = String(data = 'stop')
            print('Send message: stop')  # rospy.loginfo('Send command: {}'.format(msg.data))
            # pub.publish(msg)
            # rate.sleep()
        else:
            print('Cancelled: send "stop" message (Release invalid widget)')


class CommandTxt(Enum):
    START = 'start'
    GRAB = 'grab'
    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'left'
    RIGHT = 'right'

    @classmethod
    def is_member(cls, txt):
        if ''.join([key.value for key in CommandTxt if txt == key.value]):  # return '' or 'CommandTxt.value'
            return True  # 'CommandTxt.value'
        return False  # ''


if __name__ == '__main__':
    main()
