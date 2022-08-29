#!/usr/bin/env python

# >>> import sys; sys.version
# '2.7.17 (default, Jul  1 2022, 15:56:32) \n[GCC 7.5.0]'

import tkinter as tk
# from functools import partial


TXT_START = 'start'
TXT_GRAB = 'grab'
TXT_FORWARD = 'forward'
TXT_BACKWARD = 'bakcward'
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
    # code

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
    app.bind('<ButtonPress>', lambda e: ctrl_by_button(e, label_p1))
    # app.bind('<ButtonPress>', lambda e: ctrl_by_button(e, label_p1))

    # label_p1.update_idletasks()
    # print('label_p1.winfo_width(): {}'.format(label_p1.winfo_width()))

    app.mainloop()


def ctrl_by_button(e, label):
    # print('ctrl_by_button')
    # print('type(e.widget[\'text\'])', type(e.widget['text']))
    # print('e.widget[\'text\']', e.widget['text'])
    if e.widget.widgetName == 'button':
        for i in TXT_LIST:
            if e.widget['text'].lower() == i:
                # label['text'] = e.widget['text'] + ', ' + label['text']
                label['text'] = e.widget['text']
                print('Send message: {}'.format(i))  # similar ROS_INFO()


if __name__ == '__main__':
    main()
