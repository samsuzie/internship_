import cv2
import numpy as np
from PIL import Image

def process_image(img_path):
    """Process an input image for 3D model generation."""
    # Load the image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not load image: {img_path}")
    
    # Converting bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Basic preprocessing 
    img = cv2.resize(img, (512, 512))
    
    # Using GrabCut algorithm for foreground extraction
    masking = np.zeros(img.shape[:2], np.uint8)
    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)
    
    # Setting a rectangle around the center of the image
    rectangle = (50, 50, img.shape[1]-100, img.shape[0]-100)
    cv2.grabCut(img, masking, rectangle, bg_model, fg_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # Create mask where only sure foreground is set to 1
    masking_2 = np.where((masking==2) | (masking==0), 0, 1).astype('uint8')
    
    # Multiply image with the mask so that we can get foreground
    res = img * masking_2[:, :, np.newaxis]
    
    # converting back to pil formatt
    processed_img = Image.fromarray(res)
    
    return processed_img

def extract_depth_map(img):
    
    
    # we'll simulate a depth map
    # Convert to grayscale and invert (closer is lighter)
    grayscale = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    # Create a simple radial gradient depth map
    h, w = grayscale.shape
    cen_x, cen_y = w // 2, h // 2
    Y, X = np.ogrid[:h, :w]
    # calculating the distance of every point from center(euclidean dist)
    center_dist = np.sqrt((X - cen_x)**2 + (Y - cen_y)**2)
    # Normalize and invert
    depth_map = 1 - (center_dist / center_dist.max())
    # Combine with grayscale to make objects appear
    depth_map = depth_map * (grayscale / 255.0)
    return depth_map