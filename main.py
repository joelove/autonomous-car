import camera_interface
import frame_analyzer
# import drive


def main():
    camera_interface.capture_webcam(frame_analyzer.handle_frame)
    # drive.manual()


if __name__ == '__main__':
    main()
