# Copyright (C) 2020  The LFCNN Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Test lfcnn.models
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

import numpy as np

from tensorflow.keras.backend import clear_session
from tensorflow.keras import optimizers, Model, Input
from tensorflow.keras.layers import Activation

from lfcnn.losses import MeanSquaredError
from lfcnn.metrics import MeanSquaredError as MSE_metric
from lfcnn.metrics import MeanAbsoluteError as MAE_metric
from lfcnn.metrics import get_lf_metrics, PSNR
from lfcnn.models import BaseModel

from lfcnn.generators import LfGenerator
from lfcnn.generators.reshapes import lf_identity
from lfcnn.models.autoencoder import Dummy as AeDummy
from lfcnn.models.center_and_disparity import Dummy as CdDummy


class MockModel(BaseModel):

    def __init__(self, **kwargs):
        super(MockModel, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = LfGenerator
        self._reshape_func = lf_identity
        return

    def create_model(self, inputs, augmented_shape=None):
        out = Activation('relu', name='light_field')(inputs)
        return Model(inputs, out, name="MockModel")


def get_model_kwargs():
    optimizer = optimizers.SGD(learning_rate=0.1)
    loss = dict(light_field=MeanSquaredError())
    metrics = dict(light_field=get_lf_metrics())

    model_kwargs = dict(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics,
        callbacks=[]
    )

    return model_kwargs


def get_train_kwargs(generated_shape,
                     input_shape=(9, 9, 36, 36, 3),
                     augmented_shape=(9, 9, 32, 32, 3)):
    dat = np.random.rand(8, *input_shape)
    data = dict(data=dat)
    valid_dat = np.random.rand(8, *input_shape)
    valid_data = dict(data=valid_dat)

    train_kwargs = dict(data=data,
                        valid_data=valid_data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=augmented_shape,
                        generated_shape=generated_shape,
                        batch_size=2,
                        epochs=1,
                        verbose=0
                        )

    return train_kwargs


def get_test_kwargs(generated_shape,
                    input_shape=(9, 9, 36, 36, 3),
                    augmented_shape=(9, 9, 32, 32, 3)):
    dat = np.random.rand(8, *input_shape)
    data = dict(data=dat)

    test_kwargs = dict(data=data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=augmented_shape,
                        generated_shape=generated_shape,
                        batch_size=1,
                        verbose=0
                        )

    return test_kwargs


def get_eval_kwargs(generated_shape,
                    input_shape=(9, 9, 64, 64, 3),
                    augmented_shape=(9, 9, 64, 64, 3)):
    dat = np.random.rand(4, *input_shape)
    data = dict(data=dat)

    eval__kwargs = dict(data=data,
                        data_key="data",
                        label_keys=[],
                        augmented_shape=augmented_shape,
                        generated_shape=generated_shape,
                        batch_size=1,
                        verbose=0
                        )

    return eval__kwargs


def test_init():

    model_kwargs = get_model_kwargs()
    model = MockModel(**model_kwargs)

    assert type(model.optimizer) == optimizers.SGD
    assert type(model.loss['light_field']) == MeanSquaredError
    assert type(model.metrics['light_field'][0]) == MAE_metric
    assert type(model.metrics['light_field'][1]) == MSE_metric
    assert type(model.metrics['light_field'][2]) == PSNR
    assert model.callbacks == []
    assert model.generator == LfGenerator
    assert model.reshape_func == lf_identity
    assert model.model_crop is None

    clear_session()
    return


def test_model_build():

    model_kwargs = get_model_kwargs()
    model = MockModel(**model_kwargs)

    assert model.keras_model is None

    generated_shape = [(9, 9, 32, 32, 3)]
    model.__build_model__(generated_shape, (9, 9, 32, 32, 3), gpus=1, cpu_merge=False)
    assert type(model.keras_model) == Model
    assert model.keras_model.name == "MockModel"

    # Model is compiled and should be trainable
    model.keras_model.fit(np.random.rand(8, 9, 9, 32, 32, 3))
    clear_session()

    # Update shape and check if rebuild necessary

    model_kwargs = get_model_kwargs()
    model = MockModel(**model_kwargs)

    generated_shape = [(9, 9, 64, 64, 3)]
    # Now update shape, and retrain
    assert model.__build_necessary__(generated_shape=generated_shape)

    model.__build_model__(generated_shape, (9, 9, 64, 64, 3), gpus=1, cpu_merge=False)

    # Model is compiled and should be trainable
    model.keras_model.fit(np.random.rand(8, 9, 9, 64, 64, 3))
    clear_session()

    return


def test_model_train():

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs((9, 9, 32, 32, 3))

    model = MockModel(**model_kwargs)
    res = model.train(**train_kwargs)

    assert 'loss' in res.history
    assert 'val_loss' in res.history
    clear_session()
    return


def test_model_test():

    model_kwargs = get_model_kwargs()
    test_kwargs = get_test_kwargs((9, 9, 32, 32, 3))

    model = MockModel(**model_kwargs)
    res = model.test(**test_kwargs)

    assert 'loss' in res.keys()
    clear_session()
    return


def test_model_evaluate_challenges():

    train_gen_shape = (32, 32, 9*9*3)
    train_augmented_shape = (9, 9, 32, 32, 3)
    train_input_shape = (9, 9, 36, 36, 3)

    eval_gen_shape = (256, 256, 9*9*3)
    eval_augmented_shape = (9, 9, 256, 256, 3)
    eval_input_shape = (9, 9, 256, 256, 3)

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs(generated_shape=train_gen_shape,
                                    input_shape=train_input_shape,
                                    augmented_shape=train_augmented_shape)
    eval_kwargs = get_eval_kwargs(generated_shape=eval_gen_shape,
                                  input_shape=eval_input_shape,
                                  augmented_shape=eval_augmented_shape)

    model = AeDummy(depth=2, **model_kwargs)
    model.train(**train_kwargs)
    res = model.evaluate_challenges(**eval_kwargs)
    for s in ["metrics", "light_field"]:
        assert s in res
        assert len(res[s]) == 4

    clear_session()
    return


def test_model_evaluate_challenges_fails():

    train_gen_shape = (32, 32, 9*9*3)
    train_augmented_shape = (9, 9, 32, 32, 3)
    train_input_shape = (9, 9, 36, 36, 3)

    eval_gen_shape = (256, 256, 9*9*3)
    eval_augmented_shape = (9, 9, 256, 256, 3)
    eval_input_shape = (9, 9, 256, 256, 3)

    model_kwargs = get_model_kwargs()
    train_kwargs = get_train_kwargs(generated_shape=train_gen_shape,
                                    input_shape=train_input_shape,
                                    augmented_shape=train_augmented_shape)
    eval_kwargs = get_eval_kwargs(generated_shape=eval_gen_shape,
                                  input_shape=eval_input_shape,
                                  augmented_shape=eval_augmented_shape)

    model = AeDummy(depth=2, **model_kwargs)
    model.train(**train_kwargs)
    res = model.evaluate_challenges(**eval_kwargs)
    for s in ["metrics", "light_field"]:
        assert s in res
        assert len(res[s]) == 4

    clear_session()
    return
