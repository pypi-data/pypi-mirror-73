# Config GPU
import tensorflow as tf

tf_version = tf.__version__

if int(tf_version.split('.')[0]) == 2:
	config = tf.compat.v1.ConfigProto()
	config.gpu_options.allow_growth = True
	config.gpu_options.per_process_gpu_memory_fraction = 0.1
else:
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	config.gpu_options.per_process_gpu_memory_fraction = 0.1