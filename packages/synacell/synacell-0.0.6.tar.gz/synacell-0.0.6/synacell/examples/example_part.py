import synacell.cmodule
import synacell.signal
import matplotlib.pyplot as plt


def plot_CellEMA() -> (int, str):
    """
    Test CellIntegrator

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=123.0, amp=1000.0, phase=0.0)
    sin2 = signal.func_generator(func_name="sin", freq=246.0, amp=2000.0, phase=0.0)
    sin3 = signal.func_generator(func_name="sin", freq=173.0, amp=1347.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin2_arr = signal.func_to_nparray(func=sin2, t_min=0.5, t_max=1.0)
    sin3_arr = signal.func_to_nparray(func=sin3, t_min=0.3, t_max=1.0)
    signal.make_wav(sin1_arr + sin2_arr + sin3_arr, "./CellEMA.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./CellEMA.wav")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.add_part("id=1,type=CellValve,ofs=0,opn=5,cls=23")
    net.add_part("id=1001,type=SynaBuffer,ciid=0,coid=2")
    net.add_part("id=2,type=CellValve,ofs=0,opn=7,cls=14")
    net.add_part("id=1002,type=SynaBuffer,ciid=1,coid=3")
    net.add_part("id=1003,type=SynaBuffer,ciid=2,coid=3")
    net.add_part("id=3,type=CellBuffer")
    net.add_part("id=1004,type=SynaRPC,ciid=1,coid=4")
    net.add_part("id=1005,type=SynaRPC,ciid=2,coid=4")
    net.add_part("id=4,type=CellBuffer")
    net.add_part("id=1006,type=SynaRPC,ciid=1,coid=5")
    net.add_part("id=1007,type=SynaRPC,ciid=2,coid=5")
    net.add_part("id=5,type=CellIntegrator")
    net.add_part("id=1008,type=SynaRPC,ciid=1,coid=6")
    net.add_part("id=1009,type=SynaRPC,ciid=2,coid=6")
    net.add_part("id=6,type=CellEMA,alpha=0.1")
    net.add_part("id=1010,type=SynaRPC,ciid=1,coid=7")
    net.add_part("id=1011,type=SynaRPC,ciid=2,coid=7")
    net.add_part("id=7,type=CellEMA,alpha=0.9")
    net.add_part("id=1012,type=SynaBuffer,ciid=5,coid=8")
    net.add_part("id=8,type=CellEMA,alpha=0.02")
    net.add_part("id=1013,type=SynaBuffer,ciid=5,coid=9")
    net.add_part("id=9,type=CellEMA,alpha=0.002")

    net.connect_syna()
    net.set_recorder("id=0,pid=0,value=vo,beg=0,size=10000")
    net.set_recorder("id=1,pid=1,value=vi,beg=0,size=10000")
    net.set_recorder("id=2,pid=1,value=vo,beg=0,size=10000")
    net.set_recorder("id=3,pid=2,value=vo,beg=0,size=10000")
    net.set_recorder("id=4,pid=3,value=vi,beg=0,size=10000")
    net.set_recorder("id=5,pid=4,value=vi,beg=0,size=10000")
    net.set_recorder("id=6,pid=5,value=vo,beg=0,size=10000")
    net.set_recorder("id=7,pid=6,value=vo,beg=0,size=10000")
    net.set_recorder("id=8,pid=7,value=vo,beg=0,size=10000")
    net.set_recorder("id=9,pid=8,value=vo,beg=0,size=10000")
    net.set_recorder("id=10,pid=9,value=vo,beg=0,size=10000")

    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record = [
        net.get_record(0),
        net.get_record(1),
        net.get_record(2),
        net.get_record(3),
        net.get_record(4),
        net.get_record(5),
        net.get_record(6),
        net.get_record(7),
        net.get_record(8),
        net.get_record(9),
        net.get_record(10),
    ]

    fig, ax = plt.subplots(3, 1, sharex='col')
    fig.suptitle('CellIntegrator test')
    # plot 1
    ax[0].plot([i * 1.0 / 16000.0 for i in record[0].pc], record[0].data, '-', label="input signal")
    ax[0].plot([i * 1.0 / 16000.0 for i in record[4].pc], record[4].data, '--',
               label="valve 1 + valve 2")
    ax[0].grid(True)
    ax[0].legend()

    # plot 2
    ax[1].plot([i * 1.0 / 16000.0 for i in record[5].pc], record[5].data*10, '-',
               label="valve 1 + valve 2 -> buffer (SynaRPC)")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[6].pc], record[6].data, '.-',
               label="valve 1 + valve 2 -> integrator (SynaRPC)")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[7].pc], record[7].data, '-',
               label="valve 1 + valve 2 -> ema 1.0 (SynaRPC)")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[8].pc], record[8].data, '-',
               label="valve 1 + valve 2 -> ema 0.5 (SynaRPC)")
    ax[1].grid(True)
    ax[1].legend()

    # plot 3
    ax[2].plot([i * 1.0 / 16000.0 for i in record[9].pc], record[9].data, '-',
               label="integrator -> ema 0.02 (SynaBuffer)")
    ax[2].plot([i * 1.0 / 16000.0 for i in record[10].pc], record[10].data, '-',
               label="integrator -> ema 0.002 (SynaBuffer)")
    ax[2].grid(True)
    ax[2].legend()

    plt.xlabel("Time [s]")
    plt.show()

    return 0, "Success"


def run_part(part_name=""):
    if part_name == "CellEMA":
        plot_CellEMA()
    else:
        print(f"Part name '{part_name}' not recognized")


if __name__ == '__main__':
    '''
    1. If the module is ran (not imported) the interpreter sets this at the top of your module:
    ```
    __name__ = "__main__"
    ```
    2. If the module is imported: 
    ```
    import rk
    ```
    The interpreter sets this at the top of your module:
    ```
    __name__ = "rk"
    ```
    '''
    plot_CellEMA()
