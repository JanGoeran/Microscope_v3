from eval import *

#test chips
#G:\Shared drives\Nanoelectronics Team Drive\Data\2021\Marta\Noise measurements - June 1st week\Microscope\10kOhm_bottom

df = pd.read_csv('G:/Shared drives/Nanoelectronics Team Drive/Data/2021/Marta/Noise measurements - June 1st week/Microscope/10kOhm_bottom/test10kOhm_bottom.csv')
plot_all(df)
check_values(df, R_ev = 10e3, type = 'bottom', tol = 0.1, rel_std = 0.005, R_zero_tol = 1e6, zero_std_tol = 1e6)