#!/usr/bin/env python
# >>> import sys; sys.version
# '2.7.17 (default, Jul  1 2022, 15:56:32) \n[GCC 7.5.0]'

"""
This program don't send message for ROS Topic.
Only GUI.
"""


import tkinter as tk
import rospy
from std_msgs.msg import String


TXT_START = 'start'
TXT_GRAB = 'grab'
TXT_FORWARD = 'forward'
TXT_BACKWARD = 'backward'
TXT_LEFT = 'left'
TXT_RIGHT = 'right'
TXT_LIST = list([TXT_START, TXT_GRAB, TXT_FORWARD, TXT_BACKWARD, TXT_LEFT, TXT_RIGHT])


def main():
    # Create and setting for app window
    app = tk.Tk()
    app.title('Drone App')  # window title
    app.minsize(620, 280)  # window size
    app.resizable(False, False)  # fixed window size(both width and height)

    # Create Publisher node
    publisher = rospy.Publisher('/gnc_node/cmd', String, queue_size = 10)  # Node settings
    rospy.init_node('command_pub', anonymous = True)  # Define node name
    r = rospy.Rate(1)  # Set publishing rate

    # Create frame
    frame_label = tk.Frame(
        app,
        padx = 12,  # padding[px]
        pady = 12,  # padding[px]
        # bg = '#ff0000'
    )
    frame_btn = tk.Frame(
        app,
        padx = 12,  # padding[px]
        pady = 12,  # padding[px]
        # bg = '#00ff00'
    )
    subframe_btn = tk.Frame(
        frame_btn,
        # bg = '#0000ff',
    )

    # Create widget
    # label
    label_h1 = tk.Label(
        frame_label,
        anchor = tk.W,  # align left
        font = ('Helvetica', 12),
        # bg = '#afeeee',
        text = 'History:',
    )
    label_p1 = tk.Label(
        frame_label,
        anchor = tk.W,  # align left
        font = ('Helvetica', 12),
        # bg = '#fa5500',
        text = '',
    )
    # button
    button_start = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = TXT_START.capitalize(),
    )
    button_grab = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = TXT_GRAB.capitalize(),
    )
    button_forward = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = TXT_FORWARD.capitalize(),
    )
    button_backward = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = TXT_BACKWARD.capitalize(),
    )
    button_left = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = TXT_LEFT.capitalize(),
    )
    button_right = tk.Button(
        subframe_btn,
        width = 10,  # use font size
        height = 3,  # use font size
        font = ('Helvetica', 12),
        text = TXT_RIGHT.capitalize(),
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
    app.bind('<ButtonPress>', lambda e: e_handler.drone_ctrl_by_button(e, label_p1, publisher, r))
    app.bind('<ButtonRelease>', lambda e: e_handler.stop_drone(e, publisher, r))

    app.mainloop()


class EventHandler(object):
    def __init__(self, root, delay):
        self.__state = True
        self.root_frame = root
        self.delay = delay  # ms

    def drone_ctrl_by_button(self, e, label, pub, rate):
        if self.__state and e.widget.widgetName == 'button':  # key can press and widget is button?
            key = ''.join([key for key in TXT_LIST if e.widget['text'].lower() == key])
            if key and not rospy.is_shutdown():
                msg = String(data = key)
                label['text'] = e.widget['text']
                rospy.loginfo('Send command: {}'.format(msg.data))
                pub.publish(msg)
                self.disable_handler()
                rate.sleep()
            else:
                print('Press invalid button or Can not send msg to Topic')
        else:
            print('Event handler is disable or Press invalid widget')

    def disable_handler(self):
        if self.delay != 0:
            self.root_frame.after(self.delay, self.enable_handler)
            self.__state = False
            print('Event handler is disable for {} ms'.format(self.delay))

    def enable_handler(self):
        self.__state = True
        print('Event handler is enable')

    def stop_drone(self, e, pub, rate):
            if not rospy.is_shutdown():
                msg = String(data = 'stop')
                rospy.loginfo('Send command: {}'.format(msg.data))
                pub.publish(msg)
                rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    finally:
        print('bye')
