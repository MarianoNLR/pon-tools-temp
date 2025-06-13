from PySide6.QtCore import QThread
from components.worker_thread import WorkerThread

class TaskManager:
    """
    This component is in charge of run tasks on a different thread than the main
    It works as a general manager for tasks.
    Main function is run_task and needs the task_func which is what we want to excute on a different thread and callbacks to execute depending on the result.
    """
    
    def __init__(self):
        self._active_threads = []

    def run_task(self, task_func, args=(), kwargs={},
                 on_result=None, on_error=None, on_finished=None, on_canceled=None):

        worker = WorkerThread(task_func, *args, **kwargs)
        thread = QThread()
        worker.moveToThread(thread)

        # Conexiones de señales
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        # Connect differents results if a function was passed to run_task
        if on_result:
            worker.result.connect(on_result)
        if on_error:
            worker.error.connect(on_error)
        if on_finished:
            worker.finished.connect(on_finished)
        if on_canceled:
            worker.canceled.connect(on_canceled)

        # def cleanup():
        #     if (thread, worker) in self._active_threads:
        #         self._active_threads.remove((thread, worker))

        #worker.finished.connect(cleanup)

        self._active_threads.append((thread, worker))
        thread.start()
        return worker  # por si querés cancelarlo después