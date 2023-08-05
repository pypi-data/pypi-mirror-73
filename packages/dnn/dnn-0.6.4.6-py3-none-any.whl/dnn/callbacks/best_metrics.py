from tensorflow.keras.callbacks import Callback
from rs4.termcolor import tc, stty_size
from tensorflow.python.keras import backend as K
from . import base

class BestMetricsCallback (base.Display, Callback):
    def __init__(self, monitor='val_loss', confusion_matrix = None):
        Callback.__init__(self)
        self.monitor = monitor
        self.confusion_matrix = confusion_matrix
        self._reset ()

    def _reset (self):
        self.best_epoch = 0
        self.best = 0.0
        self.bests = {}
        self.confusion_matrix_buffer = []

    def on_train_begin(self, logs=None):
        self._reset()

    def on_epoch_end(self, epoch, logs):
        logs = logs or {}
        if 'lr' not in logs:
            logs['lr'] = K.get_value(self.model.optimizer.lr)

        current = logs.get (self.monitor)
        cl = tc.blue
        if current > self.best:
            self.best = current
            self.best_epoch = epoch
            if self.confusion_matrix:
                self.confusion_matrix_buffer = self.confusion_matrix.get_buffer ()
            cl = tc.warn
            for k, v in logs.items ():
                if k == self.monitor or k.startswith ('val_'):
                    self.bests [k] = v
        elogs = []
        elogs.append ('{}: {:.4f}'.format (cl ('epoch'), self.best_epoch))
        for k, v in self.bests.items ():
            elogs.append ('{}: {:.4f}'.format (cl ('best_{}'.format (k)), v))
        print ('Best', ' - '.join (elogs))
        if self.confusion_matrix_buffer:
            print ('\n'.join (self.confusion_matrix_buffer).strip ())
            self.draw_line ()

