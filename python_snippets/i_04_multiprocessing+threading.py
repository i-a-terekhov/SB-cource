import multiprocessing
import threading
import time
import random


class MainTask(multiprocessing.Process):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.num_threads = random.randint(3, 10)
        self.threads = []

    def task_thread(self, thread_name):
        for i in range(3):
            print(f"Task {self.name} - Thread {thread_name}: Iteration {i}")
            time.sleep(random.uniform(0.1, 0.5))

    def run(self):
        print(f"MainTask {self.name} - Process started.")

        for i in range(self.num_threads):
            thread_name = f"{self.name}-Thread-{i}"
            thread = threading.Thread(target=self.task_thread, args=(thread_name,))
            self.threads.append(thread)

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

        print(f"MainTask {self.name} - Process finished.")


if __name__ == "__main__":
    processes = []

    for i in range(3):
        main_task = MainTask(name=f"Task-{i}")
        processes.append(main_task)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("All processes and threads are done!")
