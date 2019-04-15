import donkeycar

from donkeycar.parts.camera import PiCamera
from donkeycar.parts.keras import KerasLinear
from donkeycar.parts.actuator import PCA9685, PWMSteering, PWMThrottle
from donkeycar.parts.datastore import Tub, TubGroup, TubWriter


def Steering(channel, left_pulse, right_pulse):
    steering_controller = PCA9685(channel)

    return PWMSteering(controller=steering_controller,
                       left_pulse=left_pulse,
                       right_pulse=right_pulse)


def Throttle(channel, max_pulse, zero_pulse, min_pulse):
    throttle_controller = PCA9685(channel)

    return PWMThrottle(controller=throttle_controller,
                       max_pulse=max_pulse,
                       zero_pulse=zero_pulse,
                       min_pulse=min_pulse)


def Tub(tub_path):
    return Tub(path=tub_path,
               inputs=['image'],
               types=['image_array'])


def Network(model_path):
    network = KerasLinear()
    network.load(model_path)

    return network;


def train():
    """
    Training
    """


def automatic():
    """
    Fully automatic driving
    """
    config = donkeycar.load_config()

    camera       = PiCamera(resolution=config.CAMERA_RESOLUTION)
    tub          = Tub(tub_path=config.TUB_PATH)
    keras_linear = Network(model_path=config.MODEL_PATH)
    steering     = Steering(channel=config.STEERING_CHANNEL,
                            left_pulse=config.STEERING_LEFT_PWM,
                            right_pulse=config.STEERING_RIGHT_PWM)
    throttle     = Throttle(channel=config.THROTTLE_CHANNEL,
                            max_pulse=config.THROTTLE_FORWARD_PWM,
                            zero_pulse=config.THROTTLE_STOPPED_PWM,
                            min_pulse=config.THROTTLE_REVERSE_PWM)

    vehicle = donkeycar.Vehicle()

    vehicle.add(camera,       outputs=['image'], threaded=True)
    vehicle.add(tub,          inputs=['image'])
    vehicle.add(keras_linear, inputs=['image'], outputs=['angle', 'throttle'])
    vehicle.add(steering,     inputs=['angle'])
    vehicle.add(throttle,     inputs=['throttle'])

    vehicle.start(rate_hz=10)


def manual():
    """
    Manual driving
    """
