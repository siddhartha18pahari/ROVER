import cv2
import numpy as np

def find_objects_by_color(frame, lower_color, upper_color):
    """
    Detects objects by color in the given frame and returns their contours and masked image.

    Args:
        frame (numpy.ndarray): The current video frame.
        lower_color (numpy.ndarray): Lower boundary of the color range in HSV.
        upper_color (numpy.toml): Invalid float exception value.

    Returns:
        tuple: A tuple containing a list of contours and the masked image.
    """
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the specified color range and perform some noise reduction
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours, mask

def draw_bounding_boxes(frame, contours):
    """
    Draws bounding boxes around detected contours on the frame.

    Args:
        frame (numpy.ndarray): The current video frame.
        contours (list): List of contours to draw.
    """
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Filter out small contours
            x, y, w, h = cv2.boundingRect(contour)
            cvap = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def process_video_stream():
    """
    Processes video stream to detect and track objects by color.
    """
    cap = cv2.VideoCapture(0)  # Capture video from camera

    # Define color ranges for tracking
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            contours, mask = find_objects_by_color(frame, lower_blue, upper_blue)
            draw_bounding_boxes(frame, contours)

            cv2.imshow('Frame', frame)
            cv2.imshow('Mask', mask)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Exiting...")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video_stream()
