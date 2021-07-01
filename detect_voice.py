import tensorflow as tf
from tensorflow.keras import models
import numpy as np
import matplotlib.pyplot as plt
from live_recording import Record

model = models.load_model("Model")

def get_spectrogram(waveform):
    # Padding for files with less than 16000 samples
    zero_padding = tf.zeros([8000] - tf.shape(waveform), dtype=tf.float32)
    # Concatenate audio with padding so that all audio clips will be of the same length
    waveform = tf.cast(waveform, tf.float32)
    equal_length = tf.concat([waveform, zero_padding], 0)
    spectrogram = tf.signal.stft(equal_length, frame_length=255, frame_step=64)
    spectrogram = tf.abs(spectrogram)
    return spectrogram

def predict_live(audio_binary):
    classes=['Human', 'Noise']
    #sample_file = rec.recording()
    #audio_binary = tf.io.read_file(sample_file)
    audio, _ = tf.audio.decode_wav(audio_binary)
    print('\n*** data of audio', audio)
    _audio = tf.squeeze(audio, axis=-1)
    _spectrogram = get_spectrogram(_audio)
    spectrogram = tf.expand_dims(_spectrogram, -1)
    spectrogram = tf.expand_dims(spectrogram, 0)
    # np.argmax(model.predict(spectrogram), axis=1)
    print(spectrogram.shape)
    pred = model(spectrogram)
    cls = np.argmax(tf.nn.softmax(pred[0]))
    output = 'Human' if cls==0 else 'Noise'
    print('\n*** output:',output)
    if output=='Human':
        plt.bar(classes, tf.nn.softmax(pred[0]))
    else:
        plt.bar(classes, tf.nn.softmax(pred[0]), color='r')

    plt.title(f'Predicted "{output}"')
    plt.show()
