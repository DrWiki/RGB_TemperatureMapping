import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy import interpolate
import os
import os.path


# plot double lines
def plot_double_lines(n, x, y1, pic_name, temp, flag_smooth):
    # initialize plot parameters
    print('picture name: %s, len of data: %d' % (pic_name, n))
    plt.rcParams['figure.figsize'] = (10 * 16 / 9, 10)
    plt.subplots_adjust(left=0.06, right=0.94, top=0.92, bottom=0.08)

    # 对x和y1进行插值
    x_smooth = np.linspace(x.min(), x.max(), 500)
    y1_smooth = make_interp_spline(x, y1)(x_smooth)
    # plot curve 1
    if flag_smooth:
        plt.plot(x_smooth, y1_smooth, label=temp)
    else:
        plt.plot(x, y1, label=temp)

    # 对x和y2进行插值
    # x_smooth = np.linspace(x.min(), x.max(), 50)
    # y2_smooth = make_interp_spline(x, y2)(x_smooth)
    # # plot curve 2
    # plt.plot(x_smooth, y2_smooth, label='Similarity')

    # show the legend
    plt.legend()
    plt.xlabel('Frame')
    plt.ylabel('Temprature')
    plt.ylim(10, 40)


# plot smooth curve
def plot_smooth_curve(n, x, y1, pic_name, temp, flag_smooth):
    # initialize plot parameters
    print('picture name: %s, len of data: %d' % (pic_name, n))
    plt.rcParams['figure.figsize'] = (10 * 16 / 9, 10)
    plt.subplots_adjust(left=0.06, right=0.94, top=0.92, bottom=0.08)

    # 对x和y1进行插值
    mem_x, mem_y1 = x[0], y1[0]
    x_smooth, y1_smooth = list(), list()
    x_smooth.append(mem_x)
    y1_smooth.append(mem_y1)
    for i, j in zip(x, y1):
        if j != mem_y1:
            x_smooth.append(i)
            y1_smooth.append(j)
            mem_x, mem_y1 = i, j
    x_smooth.append(x[-1])
    y1_smooth.append(y1_smooth[-1])
    # plot curve 1
    if flag_smooth:
        x_smooth, y1_smooth = np.array(x_smooth), np.array(y1_smooth)
        print(x_smooth.min(), x_smooth.max())
        x_smooth2 = np.linspace(x_smooth.min(), x_smooth.max(), 500)

        # y1_smooth2 = interpolate.interp1d(x_smooth, y1_smooth)(x_smooth2)

        f = interpolate.interp1d(x_smooth, y1_smooth, kind=1)
        y1_smooth2 = f(x_smooth2)

        plt.plot(x_smooth2, y1_smooth2, label=temp)
    else:
        plt.plot(x, y1, label=temp)

    # 对x和y2进行插值
    # x_smooth = np.linspace(x.min(), x.max(), 50)
    # y2_smooth = make_interp_spline(x, y2)(x_smooth)
    # # plot curve 2
    # plt.plot(x_smooth, y2_smooth, label='Similarity')

    # show the legend
    plt.legend()
    plt.xlabel('Frame')
    plt.ylabel('Temprature')
    plt.ylim(10, 40)




if __name__ == '__main__':
    log_dir = './'

    for parent, dirnames, filenames in os.walk(log_dir):
        for filename in filenames:
            if filename[-3:] == 'npy':
                temp_seq = np.load(f'{filename}')
                xs = np.arange(1, len(temp_seq) + 1)
                plot_smooth_curve(len(xs), xs, temp_seq, 'Visualization of Linking Prediction', filename[-21:-19], flag_smooth=False)

    # show the picture
    plt.show()