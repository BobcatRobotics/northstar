from calibration.CalibrationSession import CalibrationSession
import os
import cv2

FOLDER_NAME = r"C:\Users\Adithya Anand\Documents\GitHub\northstar\vision\northstar\images"


if __name__ == "__main__":
    calibration_session = CalibrationSession()
    for filename in [x for x in os.listdir(os.path.join("c:", os.sep, "Users", "Adithya Anand", "Documents", "Github", "northstar", "vision", "northstar", "images")) if not x.startswith(".")]:
        print("Calibrating with \"" + filename + "\"")
        image = cv2.imread(os.path.join(FOLDER_NAME, filename))
        calibration_session.process_frame(image, True)
    calibration_session.finish()
    print("Finished calibration")
