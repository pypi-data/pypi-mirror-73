__version__ = "0.6.4.11"

from .layers import layers

def subprocess (train_func, *args):
    from multiprocessing import Pool
    with Pool(1) as p:
        return p.apply (train_func, args)

def setup_gpus (memory_limit = 'growth', gpu_devices = []):
    import tensorflow as tf

    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        if gpu_devices:
            visibles = [gpus [i] for i in gpu_devices]
        else:
            visibles = gpus
        for gpu in visibles:
            if memory_limit == 'growth':
                tf.config.experimental.set_memory_growth (gpu, True)
            else:
                tf.config.set_logical_device_configuration (gpu, [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory_limit)])
        tf.config.set_visible_devices(visibles, 'GPU')
