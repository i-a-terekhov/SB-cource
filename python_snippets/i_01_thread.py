# реализация многопоточности с блокировками посредством захвата/высвобождения и через контекстный менеджер

import threading


# Создаем блокировку
lock = threading.Lock()

shared_variable = 0


def increment_shared_variable(context_manager=True):
    global shared_variable
    for _ in range(100):
        if context_manager:
            with lock:
                shared_variable -= 1
                print(shared_variable, "operation: minus")

        else:
            # Захватываем блокировку
            lock.acquire()
            shared_variable += 2
            print(shared_variable, "operation: plus")
            # Освобождаем блокировку
            lock.release()


# Создаем два потока, которые увеличивают общую переменную
thread1 = threading.Thread(target=increment_shared_variable, args=(True,))
thread2 = threading.Thread(target=increment_shared_variable, args=(False,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Final value of shared_variable:", shared_variable)
