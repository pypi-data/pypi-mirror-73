from assets.resnet import ResNet50

import sys
sys.path.append('..')
from interpretdl.interpreter.gradients.gradient_cam import GradCAMInterpreter



def grad_cam_example():
    def predict_fn(image_input):
        import paddle.fluid as fluid
        class_num = 1000

        model = ResNet50()
        logits = model.net(input=image_input, class_dim=class_num)

        probs = fluid.layers.softmax(logits, axis=-1)
        return probs

    gradcam = GradCAMInterpreter(predict_fn, "assets/ResNet50_pretrained", 1000,  'res5c.add.output.5.tmp_1', True)
    gradcam.interpret('assets/catdog.png', label = None, visual=True, save_path='gradcam_test.jpg')
if __name__ == '__main__':
    grad_cam_example()
