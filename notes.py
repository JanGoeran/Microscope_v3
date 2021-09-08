from eval import *
from scipy import stats

def basic_stat_2seg(df, event_repeat, plot_all_bool = False):

    plt.style.use('seaborn')
    centimeter = 1/2.54
    fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2, figsize=(20*centimeter, 20*centimeter))
    plt.subplots_adjust(left=None, bottom=0.2, right=None, top=None, wspace=None, hspace=None)
    ax1.set_title('individual devices')
    ax2.set_title('all devices box plot')
    ax3.set_title('relative change distribution')
    ax4.set_title('absolute change distribution')

    #plot all
    if plot_all_bool == True:
        plot_all(df)

    #drop dead devices
    dead_list = get_dead_devices(df, cutoff=0.01)
    live_list = get_live_devices(df, cutoff=0.01)
    print('dead devices are: ' + str(dead_list))
    print('live devices are: ' + str(live_list))

    df = df.loc[(df.device.isin(live_list))]

    #split at event repead
    df_before = df[df.repeat < event_repeat]
    df_after = df[df.repeat > event_repeat]

    #get averages
    df_G_before_av = get_G_average(df_before)
    df_G_after_av = get_G_average(df_after)
    df_for_box1 = pd.DataFrame({'before': list(df_G_before_av.G), 'after': list(df_G_after_av.G)})

    #paired ttest for G
    tt = stats.ttest_rel(df_G_before_av.G, df_G_after_av.G)
    print(tt)

    #error bar plot all
    for device in live_list:
        x = ['before', 'after']
        y = [float(df_G_before_av.G[df_G_before_av.device == device]), float(df_G_after_av.G[df_G_after_av.device == device])]
        yerr = [float(df_G_before_av.G_sterr[df_G_before_av.device == device]), float(df_G_after_av.G_sterr[df_G_after_av.device == device])]
        ax1.errorbar(x, y, yerr=yerr)

    ax1.set_ylabel('G (S)')

    #boxplot
    x = ['before', 'after']
    ax2.boxplot(df_for_box1, showmeans=True)
    ax2.set_xticklabels(labels=x)
    ax2.set_ylabel('G (S)')

    #relative hist
    rel_diff = (df_G_after_av.G - df_G_before_av.G)/df_G_before_av.G
    ax3.hist(rel_diff, fc='lightcoral', ec='black')
    ax3.set_xlabel(r'$(G_{after}-G_{after})/G_{before}$')
    ax3.set_ylabel('number of devices')
    ax3.axvline(rel_diff.mean(), color='k', linestyle='dashed', linewidth=1)

    #absolute hist
    abs_diff = (df_G_after_av.G - df_G_before_av.G)
    ax4.hist(abs_diff, fc='cornflowerblue', ec='black')
    ax4.set_xlabel(r'$G_{after}-G_{after}$')
    ax4.set_ylabel('number of devices')
    ax4.axvline(abs_diff.mean(), color='k', linestyle='dashed', linewidth=1)

    add_text = ('Dead devices were removed. Dead device list: ' + str(dead_list) + '\n' +
                'Total live devices: ' + str(len(live_list)) + '\n' +
                'Paired T-test for live devices: test statistic = ' + '{:.2f}'.format(tt[0]) +
                ' p-value =' + '{:.7f}'.format(tt[1]))
    ax1.text(-0.2, -1.8, add_text, transform=ax1.transAxes)

if __name__ == '__main__':
    df = pd.read_csv('C:/Users/jango/Desktop/test_1/keeper/simulation.csv')
    basic_stat_2seg(df, 20, True)
    print('done')