import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv1D, LeakyReLU, MultiHeadAttention, LayerNormalization, MaxPooling1D, Dropout
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold
import time
from sklearn.metrics import make_scorer, f1_score


def create_model_attention(optimizer="adam", num_heads=5, filter_size=225, kernel_size=5, epsilon=1e-6,
                 activation_function='relu', activation_output='softmax', loss='categorical_crossentropy'):
    # create model
    input_layer = keras.layers.Input(
        shape=(144, 3),
        name='Input',
    )
    conv_layer = Conv1D(filter_size, kernel_size=kernel_size, activation=activation_function)(input_layer)
    query = Dense(filter_size)(conv_layer)
    key = Dense(filter_size)(conv_layer)
    value = Dense(filter_size)(conv_layer)
    attention_layer = MultiHeadAttention(num_heads=num_heads, key_dim=1)(query, key, value)
    normalisation_layer = LayerNormalization(epsilon=epsilon)(attention_layer)
    conv_layer = Conv1D(filter_size, kernel_size=kernel_size, activation=activation_function)(normalisation_layer)
    flatten_layer = Flatten()(conv_layer)
    output_layer = Dense(19, activation=activation_output)(flatten_layer)
    attention_based_1d_model = keras.models.Model(inputs=input_layer, outputs=output_layer)
    attention_based_1d_model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    return attention_based_1d_model


def create_model_complex(optimizer="adam", filter_size_1=144, kernel_size_1=3, filter_size_2=12, kernel_size_2=1,
                 activation_function='relu', activation_output='softmax', loss='categorical_crossentropy', pool_size=3,
                 dropout_rate=0.1):
    # create model
    conv_1D = Sequential()
    # add model layers
    conv_1D.add(Conv1D(filter_size_1, kernel_size=kernel_size_1, activation=activation_function, input_shape=(144, 3)))
    conv_1D.add(MaxPooling1D(pool_size=pool_size))
    conv_1D.add(Dropout(dropout_rate))
    if filter_size_1 <= filter_size_2:
        filter_size_2 = 12
    if kernel_size_1 <= kernel_size_2:
        kernel_size_2 = 1
    conv_1D.add(Conv1D(filter_size_2, kernel_size=kernel_size_2, activation=activation_function))
    conv_1D.add(MaxPooling1D(pool_size=pool_size))
    conv_1D.add(Dropout(dropout_rate))
    conv_1D.add(Flatten())
    conv_1D.add(Dense(4, activation=activation_output))
    conv_1D.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    return conv_1D


def create_model(optimizer="adam", filter_size=144, kernel_size=3, activation_function='relu',
                 activation_output='softmax', loss='categorical_crossentropy'):
    # create model
    conv_1D = Sequential()
    # add model layers
    conv_1D.add(Conv1D(filter_size, kernel_size=kernel_size, activation=activation_function, input_shape=(144, 3)))
    conv_1D.add(Flatten())
    conv_1D.add(Dense(4, activation=activation_output))
    conv_1D.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    return conv_1D


def main():
    base_data_path = "/home/keegan/Desktop/UCT/Masters/Code/final-code/data-sets/"
    tcp_udp_path = base_data_path + "tcp_udp/"
    tcp_udp_144_3 = tcp_udp_path + "144-3/"
    print("hello")
    packet_data_bittorrent = np.load(tcp_udp_144_3 + "bittorrent-3.npy", allow_pickle=True)  # load pre processed data
    packet_data_bittorrent = np.reshape(packet_data_bittorrent, (-1, 432))
    df_bittorrent = pd.DataFrame(packet_data_bittorrent)
    df_bittorrent['label'] = 'BitTorrent'

    # facebook
    packet_data_facebook = np.load(tcp_udp_144_3 + "facebook-3.npy", allow_pickle=True)  # load pre processed data
    packet_data_facebook = np.reshape(packet_data_facebook, (-1, 432))
    df_facebook = pd.DataFrame(packet_data_facebook)
    df_facebook['label'] = 'Facebook'

    # instagram
    packet_data_instagram = np.load(tcp_udp_144_3 + "instagram-3.npy", allow_pickle=True)  # load pre processed data
    packet_data_instagram = np.reshape(packet_data_instagram, (-1, 432))
    df_instagram = pd.DataFrame(packet_data_instagram)
    df_instagram['label'] = 'Instagram'

    # messenger
    packet_data_messenger = np.load(tcp_udp_144_3 + "messenger-3.npy", allow_pickle=True)  # load pre processed data
    packet_data_messenger = np.reshape(packet_data_messenger, (-1, 432))
    df_messenger = pd.DataFrame(packet_data_messenger)
    df_messenger['label'] = 'Messenger'

    # tiktok
    packet_data_tiktok = np.load(tcp_udp_144_3 + "tiktok-3.npy", allow_pickle=True)  # load pre processed data
    packet_data_tiktok = np.reshape(packet_data_tiktok, (-1, 432))
    df_tiktok = pd.DataFrame(packet_data_tiktok)
    df_tiktok['label'] = 'WhatsApp'


    # whatsapp
    packet_data_whatsapp = np.load(tcp_udp_144_3 + "whatsapp-3.npy", allow_pickle=True)  # load pre processed data
    packet_data_whatsapp = np.reshape(packet_data_whatsapp, (-1, 432))
    df_whatsapp = pd.DataFrame(packet_data_whatsapp)
    df_whatsapp['label'] = 'TikTok'


    # youtube
    packet_data_youtube = np.load(tcp_udp_144_3 + "youtube-3.npy", allow_pickle=True)  # load pre processed data
    packet_data_youtube = np.reshape(packet_data_youtube, (-1, 432))
    df_youtube = pd.DataFrame(packet_data_youtube)
    df_youtube['label'] = 'YouTube'


    index_60 = 14160
    index_80 = 18880
    max = 23600
    index_streaming_60 = index_60 // 2
    index_streaming_80 = index_80 // 2
    index_messaging_60 = index_60 // 2
    index_messaging_80 = index_80 // 2
    index_social_media_60 = index_60 // 2
    index_social_media_80 = index_80 // 2
    index_messaging_end = max // 2
    index_social_media_end = max // 2
    index_streaming_end = max // 2
    df_train = pd.concat([df_youtube[:index_streaming_60], df_tiktok[:index_streaming_60],
                          df_messenger[:index_messaging_60], df_whatsapp[:index_messaging_60],
                          df_instagram[:index_social_media_60], df_facebook[:index_social_media_60],
                          df_bittorrent[:index_60]])

    df_test = pd.concat(
        [df_youtube[index_streaming_60:index_streaming_80], df_tiktok[index_streaming_60:index_streaming_80],
         df_messenger[index_messaging_60:index_messaging_80], df_whatsapp[index_messaging_60:index_messaging_80],
         df_instagram[index_social_media_60:index_social_media_80],
         df_facebook[index_social_media_60:index_social_media_80], df_bittorrent[index_60:index_80]])

    df_validation = pd.concat(
        [df_youtube[index_streaming_80:index_streaming_end], df_tiktok[index_streaming_80:index_streaming_end],
         df_messenger[index_messaging_80:index_messaging_end], df_whatsapp[index_messaging_80:index_messaging_end],
         df_instagram[index_social_media_80:index_social_media_end],
         df_facebook[index_social_media_80:index_social_media_end], df_bittorrent[index_80:max]])

    df_k_fold = pd.concat(
        [df_youtube[:index_streaming_80], df_tiktok[:index_streaming_80], df_messenger[:index_messaging_80],
         df_whatsapp[:index_messaging_80], df_instagram[:index_social_media_80], df_facebook[:index_social_media_80],
         df_bittorrent[:index_80]])

    y_train = df_train['label']
    y_test = df_test['label']
    y_validation = df_validation['label']
    y_k_fold = df_k_fold['label']

    # Add category labels
    y_train.replace(
        {"YouTube": "Streaming", "TikTok": "Streaming", "WhatsApp": "Messaging", "WhatsAppFiles": "Messaging",
         "Instagram": "SocialMedia", "Facebook": "SocialMedia", "Messenger": "Messaging"}, inplace=True)
    y_test.replace(
        {"YouTube": "Streaming", "TikTok": "Streaming", "WhatsApp": "Messaging", "WhatsAppFiles": "Messaging",
         "Instagram": "SocialMedia", "Facebook": "SocialMedia", "Messenger": "Messaging"}, inplace=True)
    y_validation.replace(
        {"YouTube": "Streaming", "TikTok": "Streaming", "WhatsApp": "Messaging", "WhatsAppFiles": "Messaging",
         "Instagram": "SocialMedia", "Facebook": "SocialMedia", "Messenger": "Messaging"}, inplace=True)
    y_k_fold.replace(
        {"YouTube": "Streaming", "TikTok": "Streaming", "WhatsApp": "Messaging", "WhatsAppFiles": "Messaging",
         "Instagram": "SocialMedia", "Facebook": "SocialMedia", "Messenger": "Messaging"}, inplace=True)

    # Encode Labels
    label_encoder = LabelEncoder()
    y_k_fold_encoded = label_encoder.fit_transform(y_k_fold.to_numpy())
    y_k_fold_encoded = keras.utils.np_utils.to_categorical(y_k_fold_encoded)

    x_train = np.array(df_train.drop("label", axis=1)).reshape(-1, 144, 3)
    x_train = x_train.astype(int) / 255
    x_test = np.array(df_test.drop("label", axis=1)).reshape(-1, 144, 3)
    x_test = x_test.astype(int) / 255
    x_validation = np.array(df_validation.drop("label", axis=1)).reshape(-1, 144, 3)
    x_validation = x_validation.astype(int) / 255
    x_k_fold = np.array(df_k_fold.drop("label", axis=1)).reshape(-1, 144, 3)
    x_k_fold = x_k_fold.astype(int) / 255

    f = open("random_search_1d_144_7_1000.csv", "w")
    model = KerasClassifier(build_fn=create_model)
    batch_size = [500, 750]
    epochs = [75, 100, 150, 200]
    optimizers = ['SGD', 'RMSprop', 'Adam']
    filter_sizes = [72, 144]
    kernel_sizes = [1, 3]
    cnn_activations = ['relu']
    output_activations = ['softmax', 'sigmoid']
    losses = ['categorical_crossentropy']
    num_folds = 5
    param_grid_cnn = dict(epochs=epochs, batch_size=batch_size, activation_function=cnn_activations,
                          kernel_size=kernel_sizes, filter_size=filter_sizes, optimizer=optimizers, loss=losses,
                          activation_output=output_activations)
    grid_cnn = GridSearchCV(model, param_grid_cnn, cv=KFold(n_splits=num_folds, shuffle=True), verbose=0,
                            scoring=make_scorer(f1_score, average='macro'))
    X = x_k_fold
    y = np.argmax(y_k_fold_encoded, axis=1)  # needed for f1 score
    start_time = time.time()
    grid_result_cnn = grid_cnn.fit(X, y, verbose=0)
    end_time = time.time()
    print('{},{}'.format(grid_result_cnn.best_score_, grid_result_cnn.best_params_))
    f.write('{},{}\n'.format(grid_result_cnn.best_score_, grid_result_cnn.best_params_))
    means = grid_result_cnn.cv_results_['mean_test_score']
    stds = grid_result_cnn.cv_results_['std_test_score']
    params = grid_result_cnn.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print('{},{},{}'.format(str(mean), str(stdev), str(param)))
        f.write('{},{},{}\n'.format(str(mean), str(stdev), str(param)))
    f.close()
    print('\n\nTotal time to run: {}'.format(end_time - start_time))


if __name__ == '__main__':
    main()
