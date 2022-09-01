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
from functools import partial
# import rospy
# from std_msgs.msg import String


def main():
    file_path, _ = os.path.split(os.path.abspath(__file__))

    # Create and setting for app window
    app = tk.Tk()
    app.title('Drone App')  # window title
    app.minsize(700, 476)  # window size
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
        # bg = '#ff0000'
    )
    frame_btn_move = tk.Frame(
        app,
        padx = 12,  # padding[px]
        pady = 12,  # padding[px]
        # bg = '#00ff00'
    )
    subframe_btn_move = tk.Frame(
        frame_btn_move,
        # bg = '#0000ff',
    )
    frame_btn_other = tk.Frame(
        app,
        padx = 12,  # padding[px]
        pady = 12,  # padding[px]
        # bg = '#0000ff',
    )
    subframe_btn_other = tk.Frame(
        frame_btn_other,
        # bg = '#0000ff',
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
        side = tk.LEFT,  # for this widget
        padx = (0, 6),  # margin(left, right)
    )
    label_p1.pack(
        expand = True,  # stretchable
        fill = tk.X,  # stretch direction
        side = tk.LEFT,  # for this widget
        padx = (0, 6),  # margin(left, right)
    )
    button_start.pack(
        side = tk.TOP,  # for this widget
    )
    button_grab.pack(
        side = tk.BOTTOM,  # for this widget
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
    subframe_btn_move.pack()
    frame_btn_move.pack(
        expand = True,  # stretchable
        fill = tk.Y,  # stretch direction
        side = tk.LEFT,  # for this frame
    )
    subframe_btn_other.pack(
        expand = True,  # stretchable
        fill = tk.Y,  # stretch direction
    )
    frame_btn_other.pack(
        expand = True,  # stretchable
        fill = tk.Y,  # stretch direction
        side = tk.RIGHT,  # for this frame
    )

    # Bind function
    e_handler = EventHandler(app)
    app.bind('<ButtonPress>', lambda e: e_handler.drone_ctrl_by_button(e, label_p1))
    app.bind('<ButtonRelease>', lambda e: e_handler.stop_drone(e, CmdText.START, CmdText.GRAB))

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
        command = partial(e_handler.halt_drone, 1, 2),
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

    # Check window size(debug)
    # app.update_idletasks()
    # print('width', app.winfo_width())
    # print('height', app.winfo_height())

    app.mainloop()


class EventHandler(object):
    def __init__(self, root, delay = 0):
        self.__state = True
        self.root_frame = root
        self.delay = delay  # ms

    def disable_handler(self):
        if self.delay != 0:
            self.root_frame.after(self.delay, self.enable_handler)
            self.__state = False
            print('Event handler is disable for {} ms'.format(self.delay))

    def enable_handler(self):
        self.__state = True
        print('Event handler is enable')

    def drone_ctrl_by_button(self, e, label):  # (self, e, label, pub, rate)
        if self.__state and e.widget.widgetName == 'button':  # key can press and widget is button?
            cmd = e.widget['text'].lower()
            if CmdText.is_member(cmd):  # and not rospy.is_shutdown()
                # msg = String(data = cmd)
                label['text'] = e.widget['text']
                print('Send message: {}'.format(cmd))  # rospy.loginfo('Send command: {}'.format(msg.data))
                # pub.publish(msg)
                # self.disable_handler()
                # rate.sleep()
                # if cmd = 'grab':
                #     ret = self.is_grab()
                #     if ret:
                #         label['text'] = label['text'] + '-> Success, You are get prize!'
                #     else:
                #         label['text'] = label['text'] + '-> Failure, Try agein!'
            else:
                print('Press invalid widget or Could not send msg(data = {}) to Topic'.format(cmd))
        else:
            print('Press invalid button or Event handler is disable')

    def stop_drone(self, e, *args):  # (self, e, pub, rate, *args)
        if e.widget.widgetName == 'button' and not ''.join([arg.value for arg in args if e.widget['text'].lower() == arg.value]):  # not rospy.is_shutdown()
            # msg = String(data = 'stop')
            # pub.publish(msg)
            print('Send message: stop')  # rospy.loginfo('Send command: {}'.format(msg.data))
            # rate.sleep()
        else:
            print('Could not send msg(data = stop) to Topic (An invalid button may have been released)')

    def halt_drone(self, a, b):
        if True:  # not rospy.is_shutdown()
            # String(data = 'halt')
            print('Send message: halt')
            print(a,b)
            # pub.publish(msg)
            # rate.sleep()
        else:
            print('Could not send msg(data = halt) to Topic')

    def is_grab(self):
        # srv/cli program
        # if collision detection is true
        print('grab!')
        #     return True
        # else:
        #     return False


class CmdText(Enum):
    START = 'start'
    GRAB = 'grab'
    FORWARD = 'forward'
    BACKWARD = 'backward'
    LEFT = 'left'
    RIGHT = 'right'

    @classmethod
    def is_member(cls, txt):
        if ''.join([key.value for key in CmdText if txt == key.value]):  # return '' or 'CmdText.value'
            return True  # 'CmdText.value'
        return False  # ''


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except rospy.ROSInterruptException:
    #     pass
    # finally:
    #     print('bye')
