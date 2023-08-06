from assets.resnet import ResNet50

import sys
sys.path.append('..')
from interpretdl.interpreter.gradients.integrated_gradients import IntGradInterpreter



def int_grad_example():
    def predict_fn(image_input):
        import paddle.fluid as fluid

        class_num = 1000

        model = ResNet50()
        logits = model.net(input=image_input, class_dim=class_num)

        probs = fluid.layers.softmax(logits, axis=-1)
        return probs

    ig = IntGradInterpreter(predict_fn, "assets/ResNet50_pretrained", 1000, True)
    ig.interpret('assets/catdog.png', label = None, baseline = 'random', steps = 50, num_random_trials=1, visual=True, save_path='ig_test.jpg')

if __name__ == '__main__':
    int_grad_example()
