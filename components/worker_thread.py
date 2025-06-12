from PySide6.QtCore import QObject, Signal, QThread, Slot
import time

class WorkerThread(QObject):
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
            if not self._is_canceled:
                result = self._task_func(*self._args)
                self.result.emit(result)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    def cancel(self):
        self._is_canceled = True

    def is_canceled(self):
        return self._is_canceled