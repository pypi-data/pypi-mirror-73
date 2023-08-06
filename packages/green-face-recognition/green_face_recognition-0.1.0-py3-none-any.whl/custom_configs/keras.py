# Config GPU
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session


tf_version = tf.__version__

if int(tf_version.split('.')[0]) == 2:
	config = tf.compat.v1.ConfigProto()
else:
	config = tf.ConfigProto()
config.gpu_options.allow_growth = True
# config.gpu_options.per_process_gpu_memory_fraction = 0.1
if int(tf_version.split('.')[0]) == 2:
	set_session(tf.compat.v1.Session(config=config)) 
else:
	set_session(tf.Session(config=config)) 
	