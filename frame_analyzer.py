import cv2
import image_processor

def handle_frame(frame):
    filtered_image = image_processor.apply_filters(frame)

    cv2.imwrite('preview.jpg', frame)
    # cv2.imshow('Preview', filtered_image)
