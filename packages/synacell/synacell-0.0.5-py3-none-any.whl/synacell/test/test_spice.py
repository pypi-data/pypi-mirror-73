import synacell.cmodule
import synacell.signal as signal
from synacell.test.testfunc import Test
import matplotlib.pyplot as plt


def generate_spice_input_1():
    """
    Generates PWL file for loading in spice.
    """
    # Generate wav file
    sin1 = signal.func_generator(func_name="sin", freq=133.0, amp=30.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    signal.make_wav(sin1_arr, "./test_spice_1.wav")

    # Get CellValve output
    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./test_spice_1.wav")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.add_part("id=1,type=CellValve,ofs=10,opn=7,cls=14")
    net.connect_syna()
    net.set_recorder("id=0,pid=1,value=vo,beg=0,size=16000")
    net.reset()
    net.run(16000, 1.0 / 16000.0)
    rec = net.get_record(0)

    # Generate pwl file
    rec.print_pwl(file_name='./test_spice_1.pwl')

    plt.plot([i * 1.0 / 16000.0 for i in rec.pc], rec.data, label="CellValve_vo")
    plt.grid(True)
    plt.xlabel("Time [s]")
    plt.legend()
    plt.show()


def test_spice_1():
    # Generate wav file
    sin1 = signal.func_generator(func_name="sin", freq=133.0, amp=30.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    signal.make_wav(sin1_arr, "./test_generate_spice_input.wav")

    # Run file through RPC synapse
    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./test_plot_2.wav")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.add_part("id=1,type=CellValve,ofs=10,opn=7,cls=14")
    net.add_part("id=1001,type=SynaRPC,ciid=1,coid=2")
    net.add_part("id=2,type=CellBuffer")
    net.connect_syna()
    net.set_recorder("id=0,pid=2,value=vi,beg=0,size=16000")
    net.reset()
    net.run(16000, 1.0 / 16000.0)
    rec = net.get_record(0)
    spice = signal.load_spice_out('./test_spice_1.txt')

    plt.plot([i * 1.0 / 16000.0 for i in rec.pc[0:300]], rec.data[0:300], '.-', label="SynaRPC[vo]")
    plt.plot(spice.values[0:300, 0], spice.values[0:300, 2], '.--', label=spice.keys()[2])
    plt.grid(True)
    plt.xlabel("Time [s]")
    plt.legend()
    plt.show()

    return 0, "Success"


def run_all_spice():
    """
    Run net on generated wav data. Gather output and compare with LTSpice output for
    verification of Runge-Kutta method for circuit solving.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """
    # Run this function to generate input for spice
    # generate_spice_input_1()
    test_li = [test_spice_1]
    return Test.run_test_li(test_li, "test_spice")


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
    run_all_spice()
