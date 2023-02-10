import numpy as np
import keras
import time


class ClassificationModel(object):
    CLASSES = ['Apple', 'AppleiCloud', 'AppleiTunes', 'BitTorrent', 'Facebook', 'GMail', 'Google', 'GoogleCloud',
               'GoogleServices', 'Instagram', 'Messenger', 'Snapchat', 'Spotify', 'TLS', 'TikTok', 'Twitter',
               'WhatsApp', 'WhatsAppFiles', 'YouTube']

    def __init__(self, model_file):
        print('importing')
        try:
            print(model_file)
            self.model = keras.models.load_model(model_file)
        except Exception as e:
            print('error loading model')
            print(e)

            time.sleep(5)

    def predict_flow(self, packet_arr):
        start_time = time.time()
        packet_array = np.array(packet_arr).reshape(-1, 144, 3)
        x_test = packet_array.astype(int) / 255
        prediction = self.model.predict(x_test)
        end_time = time.time()
        time_elapsed = end_time - start_time
        return ClassificationModel.CLASSES[np.argmax(prediction)], time_elapsed
