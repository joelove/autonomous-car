import donkeycar

from donkeycar.parts import actuator, keras, camera, datastore, clock


def Steering(channel, left_pulse, right_pulse):
    steering_controller = actuator.PCA9685(channel)

    return actuator.PWMSteering(controller=steering_controller,
                                left_pulse=left_pulse,
                                right_pulse=right_pulse)


def Throttle(channel, max_pulse, zero_pulse, min_pulse):
    throttle_controller = actuator.PCA9685(channel)

    return actuator.PWMThrottle(controller=throttle_controller,
                                max_pulse=max_pulse,
                                zero_pulse=zero_pulse,
                                min_pulse=min_pulse)


def Tub(tub_path):
    return Tub(path=tub_path,
               inputs=['image'],
               types=['image_array'])


def Network(model_path):
    network = keras.KerasLinear()
    network.load(model_path)

    return network;


def Camera(resolution):
    return camera.PiCamera(resolution=CAMERA_RESOLUTION)


def TubWriter(tub_path):
    return datastore.TubWriter(path=config.TUB_PATH,
                               inputs=inputs,
                               types=types)


def TimeStamp():
    return clock.TimeStamp()


def train():
    """
    Training
    """
    config = donkeycar.load_config()

    TUB_INPUTS = ['image', 'angle', 'throttle', 'timestamp']
    TUB_TYPES = ['image_array', 'float', 'float',  'str']

    timestamp  = Timestamp()
    camera     = Camera(resolution=config.CAMERA_RESOLUTION)
    tub        = TubWriter(path=config.TUB_PATH,
                           inputs=TUB_INPUTS,
                           types=TUB_TYPES)

    controller = JoystickController(throttle_scale=config.JOYSTICK_MAX_THROTTLE,
                                    steering_scale=config.JOYSTICK_STEERING_SCALE,
                                    auto_record_on_throttle=config.AUTO_RECORD_ON_THROTTLE)

    vehicle = donkeycar.Vehicle()

    vehicle.add(timestamp, outputs=['timestamp'])
    vehicle.add(camera, outputs=['image'], threaded=True)
    vehicle.add(controller, outputs=['angle', 'throttle'], threaded=True)
    vehicle.add(steering, inputs=['angle'])
    vehicle.add(throttle, inputs=['throttle'])
    vehicle.add(tub, inputs=TUB_INPUTS)

    vehicle.start(rate_hz=config.DRIVE_LOOP_HZ,
                  max_loop_count=config.MAX_LOOPS)


def automatic():
    """
    Fully automatic driving
    """
    config = donkeycar.load_config()

    camera   = Camera(resolution=config.CAMERA_RESOLUTION)
    network  = Network(model_path=config.MODEL_PATH)
    steering = Steering(channel=config.STEERING_CHANNEL,
                        left_pulse=config.STEERING_LEFT_PWM,
                        right_pulse=config.STEERING_RIGHT_PWM)
    throttle = Throttle(channel=config.THROTTLE_CHANNEL,
                        max_pulse=config.THROTTLE_FORWARD_PWM,
                        zero_pulse=config.THROTTLE_STOPPED_PWM,
                        min_pulse=config.THROTTLE_REVERSE_PWM)

    vehicle = donkeycar.Vehicle()

    vehicle.add(camera, outputs=['image'], threaded=True)
    vehicle.add(network, inputs=['image'], outputs=['angle', 'throttle'])
    vehicle.add(steering, inputs=['angle'])
    vehicle.add(throttle, inputs=['throttle'])

    vehicle.start(rate_hz=config.DRIVE_LOOP_HZ,
                  max_loop_count=config.MAX_LOOPS)
