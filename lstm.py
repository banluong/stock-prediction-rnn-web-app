"""
LSTM RNN model

created by: Ban Luong
"""

from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from keras.optimizers import Adam


def build_model(LSTM_unit, dropout, lr, train):
    model = Sequential()
    model.add(LSTM(units=LSTM_unit, return_sequences=True, input_shape=(train.shape[-2:])))
    model.add(Dropout(dropout))

    model.add(LSTM(units=LSTM_unit, return_sequences=True))
    model.add(Dropout(dropout))

    model.add(LSTM(units=LSTM_unit, return_sequences=True))
    model.add(Dropout(dropout))

    model.add(LSTM(units=LSTM_unit))
    model.add(Dropout(dropout))

    model.add(Dense(units=1))

    model.compile(optimizer=Adam(lr), loss='mean_squared_error')

    return model


model = build_model(50, 0.2, 0.001, X_train)

model.summary()

history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=128,
    validation_split=0.1,
    verbose=1,
    shuffle=False
)
