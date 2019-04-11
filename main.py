import camera
import lane_detector


def main():
    camera.capture(lane_detector.detect_lanes)


if __name__ == '__main__':
    main()
