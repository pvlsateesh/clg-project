import os
from ultralytics import YOLO
import cv2

OUTPUT_FOLDER ='static/output'
def prediction_image(image_path):
    # Load the YOLO model
    model = YOLO(r'Users\ship.pt')

    # Load and process the image
    image = cv2.imread(image_path)

    # Perform detection
    results = model.predict(image)

    # Visualize results
    annotated_image = results[0].plot()  # Annotated image with bounding boxes
    cv2.imshow("Ship Detection", annotated_image)
    cv2.waitKey(0)
    

    # Save the output
    output_path = os.path.join(OUTPUT_FOLDER, "output.jpg")
    cv2.imwrite(output_path, annotated_image)
    
    return output_path
