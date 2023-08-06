import typing
from typing import Any, Callable, List, Tuple, Union

from interpretdl.interpreter.abc_interpreter import Interpreter
from interpretdl.data_processor.readers import preprocess_image, read_image

import IPython.display as display
import cv2
import numpy as np
import paddle.fluid as fluid
import os, sys
from PIL import Image

class IntGradInterpreter(Interpreter):
    """
    Integrated Gradients Interpreter.

    More details regarding the Integrated Gradients method can be found in the original paper:
    http://proceedings.mlr.press/v70/sundararajan17a/sundararajan17a.pdf
    """

    def __init__(self, predict_fn, trained_model_path, class_num, use_cuda, model_input_shape = [3, 224, 224]) -> None:
        """
        Initialize the IntGradInterpreter

        Args:
            predict_fn: A user-defined function that gives access to model predictions. It takes the following arguments:
                    - image_input: An image input.
                    example:
                        def predict_fn(image_input):
                            import paddle.fluid as fluid
                            class_num = 1000
                            model = ResNet50()
                            logits = model.net(input=image_input, class_dim=class_num)
                            probs = fluid.layers.softmax(logits, axis=-1)
                            return probs
            trained_model_path: The pretrained model directory.
            class_num: Number of classes for the model.
            use_cuda: Whether or not to use cuda.
            model_input_shape: The input shape of the model

        Returns:
        """
        Interpreter.__init__(self)
        self.predict_fn = predict_fn
        self.trained_model_path = trained_model_path
        self.class_num = class_num
        self.use_cuda = use_cuda
        self.model_input_shape = model_input_shape

    def set_params(self):
        """
        Set parameters for the interpreter.
        """
        pass

    def interpret(self, img_path, label = None, baseline = None, steps = 50, num_random_trials=10, visual=True, save_path=None):
        """
        Main function of the interpreter.

        Args:
            img_path: The input image filepath.
            label: The target label to analyze. If None, the most likely label will be used.
            baseline: The baseline input. If None, all zeros will be used. If 'random', random Guassian initialization will be used.
            setps: number of steps in the Riemman approximation of the integral
            num_random_trials: number of random initializations to take average in the end.
            visual: Whether or not to visualize the processed image.
            save_path: The filepath to save the processed image. If None, the image will not be saved.

        Returns:
        """
        startup_prog = fluid.Program()
        main_program = fluid.Program()
        with fluid.program_guard(main_program, startup_prog):
            with fluid.unique_name.guard():

                image_op = fluid.data(name='image', shape=[1] + self.model_input_shape, dtype='float32')
                label_op = fluid.layers.data(name='label', shape=[1], dtype='int64')
                alpha_op = fluid.layers.data(name='alpha', shape=[1], dtype='double')

                if baseline == 'random':
                    x_baseline = fluid.layers.gaussian_random([1] + self.model_input_shape, dtype="float32")
                else:
                    x_baseline = fluid.layers.zeros_like(image_op)
                x_diff = image_op - x_baseline

                x_step = x_baseline + alpha_op * x_diff

                probs = self.predict_fn(x_step)
                if isinstance(probs, tuple):
                    probs = probs[0]

                for op in main_program.global_block().ops:
                    if op.type == 'batch_norm':
                        op._set_attr('use_global_stats', True)

                one_hot = fluid.layers.one_hot(label_op, self.class_num)
                one_hot = fluid.layers.elementwise_mul(probs, one_hot)
                target_category_loss = fluid.layers.reduce_sum(one_hot)

                p_g_list = fluid.backward.append_backward(target_category_loss)

                gradients_map = fluid.gradients(one_hot, x_step)[0]

        if self.use_cuda:
            gpu_id = int(os.environ.get('FLAGS_selected_gpus', 0))
            place = fluid.CUDAPlace(gpu_id)
        else:
            place = fluid.CPUPlace()
        exe = fluid.Executor(place)

        fluid.io.load_persistables(exe, self.trained_model_path, main_program)
        # Read in image
        with open(img_path, 'rb') as f:
            org = Image.open(f)
            org = org.convert('RGB')
            org = np.array(org)
        img = read_image(img_path, crop_size = self.model_input_shape[1])
        images = preprocess_image(img)  # transpose to [N, 3, H, W], scaled to [0.0, 1.0]

        # if label is None, let it be the most likely label
        if label is None:
            out = exe.run(main_program, feed={
                    'image': images,
                    'label': np.array([[0]]),
                    'alpha': np.array([[float(1)]]),
                }, fetch_list=[probs])
            label = np.argmax(out[0][0])

        gradients_list = []

        if baseline is None:
            num_random_trials = 1

        for i in range(num_random_trials):
            total_gradients = np.zeros_like(images)
            for alpha in np.linspace(0, 1, steps):
                gradients, image_diff = exe.run(main_program, feed={
                        'image': images,
                        'label': np.array([[label]]),
                        'alpha': np.array([[alpha]]),
                    }, fetch_list=[gradients_map, x_diff])
                total_gradients += np.array(gradients)
            ig_gradients = total_gradients * np.array(image_diff) / steps
            gradients_list.append(ig_gradients)
        avg_gradients = np.average(np.array(gradients_list), axis=0)[0]
        avg_gradients = avg_gradients.transpose((1,2,0))
        interpretation = np.clip(avg_gradients, 0, 1)
        channel = [0, 255, 0]
        interpretation = np.average(interpretation, axis=2)

        m, e = np.percentile(np.abs(interpretation), 99.5), np.min(np.abs(interpretation))
        transformed = (np.abs(interpretation) - e) / (m - e)

        # Recover the original sign of the interpretation.
        transformed *= np.sign(interpretation)

        # Clip values above and below.
        transformed = np.clip(transformed, 0.0, 1.0)

        interpretation = np.expand_dims(transformed, 2) * channel
        interpretation = np.clip(0.7 * img[0] + 0.5 * interpretation, 0, 255)

        x = np.uint8(interpretation)
        x = Image.fromarray(x)

        if visual:
            display.display(display.Image(x))

        if save_path is not None:
            x.save(save_path)
