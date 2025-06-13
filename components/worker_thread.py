from PySide6.QtCore import QObject, Signal, Slot

class WorkerThread(QObject):
    """
    Threaded worker that executes a task function in a separate thread.

    This class is designed to run background tasks by receiving a callable ('task_func')
    """
    finished = Signal()
    result = Signal(object)
    error = Signal(str)
    canceled = Signal()
    
    def __init__(self, task_func, *args, **kwargs):
        super().__init__()
        self._task_func = task_func
        self._args = args
        self._kwargs = kwargs
        self._is_canceled = False
    
    @Slot()
    def run(self):
        try:
            result = self._task_func(*self._args)
            self.result.emit(result)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    # def cancel(self):
    #     self._is_canceled = True

    # def is_canceled(self):
    #     return self._is_canceled