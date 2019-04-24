# import camera_interface
# import frame_analyzer
# import drive
from controller import read_controller


def main():
    # camera_interface.capture(frame_analyzer.handle_frame)
    # drive.manual()
    read_controller()


if __name__ == '__main__':
    main()
