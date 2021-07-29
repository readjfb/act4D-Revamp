from matplotlib import pyplot as plt
import matplotlib.animation as animation
from data_intake import NI_Interface
from multiprocessing import Queue

display_num_pts = 2000

'''
    Create Matplotlib subplots and lineplots
    For elbow torque magnitudes
'''
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(5,7))

line_target, = ax1.plot([0], [0])
ax1.set_title('Target Elbow Torque', fontsize=10)
line_upper, = ax2.plot([0], [0])
ax2.set_title('Upper Limit Elbow Torque', fontsize=10)
line_lower, = ax3.plot([0], [0])
ax3.set_title('Lower Limit Elbow Torque', fontsize=10)
line_matching, = ax4.plot([0], [0])
ax4.set_title('Matching Elbow Torque', fontsize=10)

plt.tight_layout(h_pad=0.2)

ax1.set_xticks([])
ax2.set_xticks([])
ax3.set_xticks([])

# These lists will hold the data. The values in the lists are just random initial values
times = [0, .1]
datapoints_target, datapoints_upper = [0, .1], [0, .1]
datapoints_lower, datapoints_matching = [0, .1], [0, .1]

'''
    Cache the limits; done for performance boost
'''

#set ymax to mvt value?
ax1_ymin, ax1_ymax = -10, 50
ax2_ymin, ax2_ymax = -10, 50
ax3_ymin, ax3_ymax = -10, 50
ax4_ymin, ax4_ymax = -10, 50

update1, update2, update3, update4 = False, False, False, False

ax1.set_ylim([ax1_ymin, ax1_ymax])
ax2.set_ylim([ax2_ymin, ax2_ymax])
ax3.set_ylim([ax3_ymin, ax3_ymax])
ax4.set_ylim([ax4_ymin, ax4_ymax])

data =[]

def animate(i, xs, ys1, ys2, ys3, ys4, communication_queue=None):
    global ax1_ymax, ax1_ymin, ax2_ymin, ax2_ymax, ax3_ymax, ax3_ymin, ax4_ymax, ax4_ymin,\
        update1, update2, update3, update4
    running = True

    ni_interface = NI_Interface()
    while running:
        samples = ni_interface.read_samples()

        if samples:
            data.extend(samples)

        while not communication_queue.empty():
            val = communication_queue.get_nowait()

            if val == "EXIT":
                ni_interface.safe_exit()
                running = False

        # Expects data coming in to be in the form [[var1, var2..., time], [var1, var2, time2]]?
        # Probably not correct
        ys1.append(data[0][0])
        ys2.append(data[0][1])
        ys3.append(data[0][2])
        ys4.append(data[0][3])
        xs.append(data[0][-1])

    xs = xs[-display_num_pts:]
    ys1 = ys1[-display_num_pts:]
    ys2 = ys2[-display_num_pts:]
    ys3 = ys3[-display_num_pts:]
    ys4 = ys4[-display_num_pts:]

    line_target.set_data(xs, ys1)
    line_upper.set_data(xs, ys2)
    line_lower.set_data(xs, ys3)
    line_matching.set_data(xs, ys4)

    ax1.set_xlim([xs[0], xs[-1]])
    ax2.set_xlim([xs[0], xs[-1]])
    ax3.set_xlim([xs[0], xs[-1]])
    ax4.set_xlim([xs[0], xs[-1]])

    # Ensuring that the window doesn't change axis more than is necessary. Speeds up performance.
    if min(-10, min(ys1)) != ax1_ymin:
        update1 = True
        ax1_ymin = min(-10, min(ys1))

    if max(50, max(ys1)) != ax1_ymax:
        update1 = True
        ax1_ymax = max(50, max(ys1))

    if min(-10, min(ys2)) != ax2_ymin:
        update2 = True
        ax2_ymin = min(-10, min(ys2))

    if max(50, max(ys2)) != ax2_ymax:
        update2 = True
        ax2_ymax = max(50, max(ys2))

    if min(-10, min(ys3)) != ax3_ymin:
        update3 = True
        ax3_ymin = min(-10, min(ys3))

    if max(50, max(ys3)) != ax3_ymax:
        update3 = True
        ax3_ymax = max(50, max(ys3))

    if min(-10, min(ys4)) != ax4_ymin:
        update4 = True
        ax4_ymin = min(-10, min(ys4))

    if max(50, max(ys4)) != ax4_ymax:
        update4 = True
        ax4_ymax = max(50, max(ys4))

    if update1:
        ax1.set_ylim([ax1_ymin, ax1_ymax])

    if update2:
        ax2.set_ylim([ax2_ymin, ax2_ymax])

    if update3:
        ax3.set_ylim([ax3_ymin, ax3_ymax])

    if update4:
        ax4.set_ylim([ax4_ymin, ax4_ymax])

def animation_control(communication_queue):
    ani = animation.FuncAnimation(fig, animate,
                                  fargs=(times, datapoints_target, datapoints_upper,
                                     datapoints_lower, datapoints_matching, communication_queue),
                                  interval=30)
    plt.show()


if __name__ == "__main__":
    plotter_queue = Queue()
    animation_control(plotter_queue)