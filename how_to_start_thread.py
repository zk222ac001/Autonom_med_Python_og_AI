import logging # for printing timestamps and messages.
import threading # for running code in a separate thread.
import time # for simulating a delay.


# Function to be executed in a separate thread
def thread_function(name):
    # Simulate a simple threaded task
    logging.info(f"Thread {name}: starting")
    time.sleep(2)
    logging.info(f"Thread {name}: finishing")

# main function
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s [%(threadName)s] %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S"
    )
    logging.info("Main    : before creating thread")

    # Create a thread and give it a name
    thread = threading.Thread(target=thread_function, args=(1,), name="Worker-1")

    logging.info("Main    : before running thread")
    thread.start()

    logging.info("Main    : wait for the thread to finish")
    thread.join()  # Wait until thread finishes

    logging.info("Main    : all done")

'''
Summary of the code:
A thread is a lightweight flow of execution inside a program. This script starts a background thread
to run thread_function while the main program continues; join() is used so the main program waits for
that background thread to finish before exiting. Logging is used to show the order of events and which
thread produced each message.

'''

'''
logging.basicConfig(...)
format="%(asctime)s [%(threadName)s] %(message)s":
%(asctime)s — timestamp.
%(threadName)s — the logging-friendly name of the thread (e.g. MainThread or Worker-1).
%(message)s — the message given to logging.info.
level=logging.INFO — show INFO and higher severity messages.
datefmt="%H:%M:%S" — format for the timestamp.

'''

'''
thread = threading.Thread(target=thread_function, args=(1,), name="Worker-1")
threading.Thread(...) creates a Thread object but does not start it yet.
target=thread_function — the callable to execute in the new thread.
args=(1,) — tuple of positional arguments passed to thread_function; here name will be 1.
Important: include the trailing comma for single-element tuples.
name="Worker-1" — optional human-readable thread name used by logging and debugging.
Common student mistake: forgetting the comma in args=(1,) — args=(1) becomes 1 (not a tuple) and raises an error.

'''

'''
thread.start()
Actually starts the thread; Python schedules the thread to run thread_function.
Starting a thread returns immediately to the caller — it does not wait for the thread to finish.
Analogy: start() is like telling a student “go work on your task” — you don’t wait at the desk;
the student begins working independently.
'''

'''
thread.join()
join() blocks the caller (here: the main thread) until the thread finishes.
Ensures the program won’t exit while background threads are still running.
Teaching point: Explain differences between:
No join() → main may exit before thread finishes (background thread terminated abruptly when process ends).
With join() → main waits until that thread completes.
'''
