import cv2
import mediapipe as mp
import pyautogui
import pytesseract
import pyttsx3
import threading
import logging
import numpy as np

# Configuration
CONFIG = {
    'min_detection_confidence': 0.7,
    'min_tracking_confidence': 0.7,
    'cursor_sensitivity': 1.0,
    'tesseract_path': r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    'debug_mode': False
}

# Set up logging
logging.basicConfig(
    level=logging.INFO if not CONFIG['debug_mode'] else logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=CONFIG['min_detection_confidence'], 
    min_tracking_confidence=CONFIG['min_tracking_confidence']
)
mp_draw = mp.solutions.drawing_utils

# Initialize Tesseract OCR
try:
    pytesseract.pytesseract.tesseract_cmd = CONFIG['tesseract_path']
except Exception as e:
    logging.error(f"Error configuring Tesseract: {e}")

# Initialize Pyttsx3 for talk-back
engine = pyttsx3.init()

# Smooth cursor movement variables
previous_x, previous_y = 0, 0
smooth_factor = 0.5

def smooth_cursor_movement(current_x, current_y):
    """
    Apply smooth cursor movement interpolation
    """
    global previous_x, previous_y
    smooth_x = previous_x + (current_x - previous_x) * smooth_factor
    smooth_y = previous_y + (current_y - previous_y) * smooth_factor
    previous_x, previous_y = smooth_x, smooth_y
    return smooth_x, smooth_y

def map_to_screen(x, y, sensitivity=CONFIG['cursor_sensitivity']):
    """
    Map normalized hand landmarks to screen coordinates with sensitivity
    """
    screen_width, screen_height = pyautogui.size()
    mapped_x = int(x * screen_width * sensitivity)
    mapped_y = int(y * screen_height * sensitivity)
    return smooth_cursor_movement(mapped_x, mapped_y)

def is_finger_raised(lm_list, tip, dip):
    """
    Check if a specific finger is raised by comparing tip and dip joint positions
    """
    return lm_list[tip].y < lm_list[dip].y

def speak_text_async(text):
    """
    Asynchronously speak given text to prevent blocking
    """
    def talk():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logging.error(f"Text-to-speech error: {e}")
    
    thread = threading.Thread(target=talk)
    thread.start()

def get_text_under_cursor():
    """
    Capture and extract text under the cursor using Tesseract OCR
    """
    try:
        screen_width, screen_height = pyautogui.size()
        screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        return pytesseract.image_to_string(screenshot)
    except Exception as e:
        logging.error(f"Text extraction error: {e}")
        return ""

def get_application_name():
    """
    Identify application or file name near the cursor
    """
    try:
        x, y = pyautogui.position()
        screenshot = pyautogui.screenshot(region=(x - 50, y - 50, 100, 100))
        app_name = pytesseract.image_to_string(screenshot).strip()
        if app_name:
            logging.info(f"Detected application: {app_name}")
        return app_name
    except Exception as e:
        logging.error(f"Application detection error: {e}")
        return ""

def main():
    """
    Main hand gesture control loop
    """
    # Webcam setup
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        try:
            success, frame = cap.read()
            if not success:
                break

            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)

            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process frame to detect hand landmarks
            results = hands.process(rgb_frame)

            # Check if hand landmarks are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks on the frame
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Extract landmarks as a list
                    lm_list = hand_landmarks.landmark

                    # Map index finger tip position to screen coordinates
                    index_tip = lm_list[8]  # Index finger tip (landmark 8)
                    index_x, index_y = map_to_screen(index_tip.x, index_tip.y)

                    # Check finger states
                    index_raised = is_finger_raised(lm_list, 8, 6)  # Index tip above DIP joint
                    middle_raised = is_finger_raised(lm_list, 12, 10)  # Middle tip above DIP joint

                    # Cursor movement
                    if index_raised and not middle_raised:
                        pyautogui.moveTo(index_x, index_y)
                        
                        # Talk-back feature: Speak the application or file name under the cursor
                        app_name = get_application_name()
                        if app_name:
                            speak_text_async(f"You are on {app_name}")

                    # Click feature
                    if index_raised and middle_raised:
                        pyautogui.click()

            # Display the video frame
            cv2.imshow("Hand Tracking", frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            logging.error(f"Main loop error: {e}")
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Unhandled error: {e}")