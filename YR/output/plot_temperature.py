import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


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


def plot_smooth_curve(n, x, y1, pic_name, temp, flag_smooth):
    # initialize plot parameters
    print('picture name: %s, len of data: %d' % (pic_name, n))
    plt.rcParams['figure.figsize'] = (10 * 16 / 9, 10)
    plt.subplots_adjust(left=0.06, right=0.94, top=0.92, bottom=0.08)

    # 对x和y1进行插值
    mem_x, mem_y = x[0], y1[0]
    x_smooth, y1_smooth = list(), list()
    x_smooth.append(mem_x)
    y1_smooth.append(mem_y)
    for i, j in zip(x, y1):
        if i != mem_x:
            x_smooth.append(mem_x)
            y1_smooth.append(mem_y)
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




if __name__ == '__main__':
    # xs = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    # y1s = np.array([8.0, 6.0, 5.7, 5.6, 5.2, 1.0, 0.8, 0.6])
    # y2s = np.array([0.9, 0.8, 0.75, 0.41, 0.03, 0.01, 0.0, 1.0])
    temps = [15, 18, 19, 20, 25, 28, 30, 37, 38]

    for temp in temps:
        file_name = f'temperature_604_951_{temp}.npy'
        temp_seq = np.load(f'{file_name}')
        xs = np.arange(1, len(temp_seq) + 1)

        plot_double_lines(len(xs), xs, temp_seq, 'Visualization of Linking Prediction', temp, flag_smooth=True)

    # show the picture
    plt.show()