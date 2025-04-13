import os
sma = 100
es = [0.01,0.1,0.3,0.5]
spins = [0.5,0.9]
Mbhs = [5,6,7]
windows_5 = ['[[0,8000]]','[[0,8000],[24000,32000],[48000,54000],[70000,78000]]','[[0,8000],[88000,96000],[176000,184000],[264000,272000],[352000,360000]]', '[[0,8000],[88000,96000],[176000,184000],[264000,272000],[352000,360000],[440000,448000],[528000,536000],[616000,624000],[704000,712000],[792000,800000],[880000,888000],[968000,976000],[1056000,1064000],[1144000,1152000],[1232000,1240000],[1320000,1328000],[1408000,1416000],[1496000,1504000],[1584000,1592000],[1672000,1680000]]']
windows_6 = ['[[0,80000]]','[[0,80000],[240000,320000],[480000,540000],[700000,780000]]','[[0,80000],[880000,960000],[1760000,1840000],[2640000,2720000],[3520000,3600000]]','[[0,80000],[880000,960000],[1760000,1840000],[2640000,2720000],[3520000,3600000],[4400000,4480000],[5280000,5360000],[6160000,6240000],[7040000,7120000],[7920000,8000000],[8800000,8880000],[9680000,9760000],[10560000,10640000],[11440000,11520000],[12320000,12400000],[13200000,13280000],[14080000,14160000],[14960000,15040000],[15840000,15920000],[16720000,16800000]]']
windows_7 = ['[[0,800000]]','[[0,800000],[2400000,3200000],[4800000,5400000],[7000000,7800000]]','[[0,800000],[8800000,9600000],[17600000,18400000],[26400000,27200000],[35200000,36000000]]', '[[0,800000],[8800000,9600000],[17600000,18400000],[26400000,27200000],[35200000,36000000],[44000000,44800000],[52800000,53600000],[61600000,62400000],[70400000,71200000],[79200000,80000000],[88000000,88800000],[96800000,97600000],[105600000,106400000],[114400000,115200000],[123200000,124000000],[132000000,132800000],[140800000,141600000],[149600000,150400000],[158400000,159200000],[167200000,168000000]]']
preamble = "#!/bin/bash\n#SBATCH --job-name=timing_sampler\n#SBATCH --partition=sched_mit_kburdge_r8\n#SBATCH --gres=gpu:1\n\n"

for e in es:
    for spin in spins:
        for Mbh in Mbhs:
            if Mbh == 5:
                windows = windows_5
            elif Mbh == 6:
                windows = windows_6
            elif Mbh == 7:
                windows = windows_7
            for i, window in enumerate(windows):
                if Mbh == 7 and i > 0:
                    dt = 100
                else:
                    dt = 10
                timing_file = f'timings_sma={sma}_e={e}_a={spin}_Mbh={Mbh}_windows={i}.dat'
                window_file = f'windows_sma={sma}_e={e}_a={spin}_Mbh={Mbh}_windows={i}.dat'
                outfile = f'sma={sma}_e={e}_a={spin}_Mbh={Mbh}_windows={i}.h5'
                os.system(f'echo "{preamble}" > sample.sh')
                cmd = f'python generate_timings.py {sma} {e} 60 {spin} {Mbh} {window} {timing_file} {window_file}'
                os.system(f'echo "{cmd}" >> sample.sh')
                cmd = f'python mcmc_fixedphase.py {outfile} {timing_file} {window_file} 20000 1000 {sma} {Mbh} {dt}'
                os.system(f'echo "{cmd}" >> sample.sh')
                os.system('sbatch -p sched_mit_kburdge_r8 --gres=gpu:1 sample.sh')
