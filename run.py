import multiprocessing
import time
import importlib.util

def run_script(script_name):
    spec = importlib.util.find_spec(script_name)
    if spec is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        print(f"Script {script_name} not found")

if __name__ == "__main__":
    scripts = [
        'run_processes.server_green',
        'run_processes.client_red',
        'run_processes.client_blue'
    ]
    processes = []

    for script in scripts:
        process = multiprocessing.Process(target=run_script, args=(script,))
        process.start()
        processes.append(process)

    time.sleep(300)

    for process in processes:
        process.terminate()

    for process in processes:
        process.join()
