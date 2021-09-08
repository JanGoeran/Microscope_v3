from eval import *
from simulate_measurement import *

comment = 'comment'

df, basePath = simulate_measure(repeats=10,
                 event_repeat=5,
                 deviceList=[i for i in range(20,30)],
                 comment=comment,
                 plot_speed=2)

print('done')

#basic_stat_2seg(df, event_repeat=5, plot_all_bool=False)

