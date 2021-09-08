from eval import *

df = pd.read_csv('G:/Shared drives/Nanoelectronics Team Drive/Data/2021/Marta/20210716/KCl/test.csv')

plot_all(df, cutoff=1E-5, plot_repeat=True)

#looks like repeat 10 is event_repeat
#dropping dead devices manually based on first 5 repeats.

live_list = get_live_devices(df[df.repeat < 5], cutoff=1E-5)
df = df.loc[(df.device.isin(live_list))]

plot_all(df, cutoff=1E-5, plot_repeat=True)

#basic stats plots
basic_stat_2seg(df,event_repeat=10)

#check out devices that look like they may have died.
died_list = []
survived_list = []
df1 = df[df.repeat > 11]
av1 = get_G_average(df1)
av1['lower95'] = av1.G-2*av1.G_sterr

for device in live_list:
    if float(av1.lower95[av1.device == device]) <= 0:
        died_list.append(device)
    else:
        survived_list.append(device)
print('died_list: ' + str(died_list))
print('survived_list: ' + str(survived_list))

plot_IV(df, device=1, repeat=20)

#plot multiple IVs for one device
fig, ax1 = plt.subplots()
device = 1
for r in range(13,17):
    df1 = df.loc[(df['device'] == device) & (df['repeat'] == r)]
    x = list(map(float, df1['V_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
    y = list(map(float, df1['I_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
    ax1.plot(x, y)

fig1, ax1 = plt.subplots()
device = 1
for r in range(1,5):
    df1 = df.loc[(df['device'] == device) & (df['repeat'] == r)]
    x = list(map(float, df1['V_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
    y = list(map(float, df1['I_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
    ax1.plot(x, y)

#plots for survived list only

df_s = df.loc[(df.device.isin(survived_list))]
plot_all(df_s, cutoff=0, plot_repeat=False)
basic_stat_2seg(df_s, event_repeat=10)
