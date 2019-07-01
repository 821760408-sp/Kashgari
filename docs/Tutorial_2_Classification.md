# Tutorial 2: Text Classification

Kashgari provides `CNN_Model`, `CNN_LSTM_Model` and `BLSTM_Model` for text classification, All classification models inherit from the `ClassificationModel`. You could easily switch from one model to another just by changing one line of code.

Also, it is very easy to customize your own model by using the `ClassificationModel` class. And all the models could build with Word2vec embedding, BERT embedding or just an empty embedding layer.

Here is a real-life example of how to train and save on your own corpus.

```python
from kashgari.utils.logger import init_logger
init_logger()

from kashgari.tasks.classification import CNNLSTMModel

# prepare corpus
train_x = [
            list('语言学（英语：linguistics）是一门关于人类语言的科学研究'),
            list('语言学（英语：linguistics）是一门关于人类语言的科学研究'),
            list('语言学（英语：linguistics）是一门关于人类语言的科学研究'),
            list('语言学包含了几种分支领域。'),
            list('在语言结构（语法）研究与意义（语义与语用）研究之间存在一个重要的主题划分'),
        ]
train_y = ['a', 'a', 'a', 'b', 'c']

# train model
model = CNNLSTMModel()
model.fit(train_x, train_y)

# save model
model.save('./some-where-some-where/')
```


## Load trained model
```python
from kashgari.tasks.classification import ClassificationModel

model = ClassificationModel.load_model('./some-where-some-where/')
model.predict(list('加载完成咯'))
```


## Adjust models hyper params
```python
from kashgari.tasks.classification import CNNLSTMModel
hyper_params = CNNLSTMModel.base_hyper_parameters.copy()
print(hyper_params)
# {'conv_layer': {'filters': 32, 'kernel_size': 3, 'padding': 'same', 'activation': 'relu'}, 'max_pool_layer': {'pool_size': 2}, 'lstm_layer': {'units': 100}}

hyper_params['lstm_layer']['units'] = 300
model = CNNLSTMModel(hyper_parameters=hyper_params)
```

## Customize your own model

It is very easy and straightforward to build your own customized model, just inherit the `ClassificationModel` and implement the `build_model()` function.

```python
from keras.layers import LSTM, Dense, Dropout
from keras.models import Model
from kashgari.tasks.classification import ClassificationModel


class MyOwnModel(ClassificationModel):
    __architect_name__ = 'MyOwnModel'
    
    def _prepare_model(self):
        base_model = self.embedding.model
        lstm_layer = LSTM(100, return_sequences=True)(base_model.output)
        drop_out_layer = Dropout(0.3)(lstm_layer)
        dense_layer = Dense(len(self.label2idx), activation='sigmoid')(drop_out_layer)
        output_layers = [dense_layer]
        
        self.model = Model(base_model.inputs, output_layers)

    def _compile_model(self):
        self.model.compile(optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])

model = MyOwnModel()
model.fit(train_x, train_y)

model.save('./my_own_model')

loaded_model = MyOwnModel.load_model('./my_own_model')
```

## Use pre-embedding embedding layer

see [Tutorial 1: Word Embeddings](Tutorial_1_Embedding.md) for detail. All models, include the customized one support using word2vec or BERT embedding as the embedding layer. 


## Use callbacks

Kashgari is based on keras so that you could use all of the [keras callbacks](https://keras.io/callbacks/) directly with Kashgari model. For example, here is how to visualize training with tensorboard.

```python
import keras

tf_board_callback = keras.callbacks.TensorBoard(log_dir='./logs', update_freq=1000)


model = CNNModel()
model.fit(train_x,
          train_y,
          val_x,
          val_y,
          batch_size=100,
          fit_kwargs={'callbacks': [tf_board_callback]})
```
