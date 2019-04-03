import camera
import frame_analyzer

def main():
    camera.capture(frame_analyzer.handle_frame)

if __name__ == '__main__':
    main()
