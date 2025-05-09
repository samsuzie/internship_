# Photo/Text to 3D Model Converter

A Python prototype that converts photos or text descriptions into simple 3D models.

## Features

- Process single-object photos to create 3D models
- Generate 3D models from text descriptions
- Export models as .obj or .stl files
- Visualize the generated 3D models

## Installation

1. Clone this repository
2. Create a virtual environment:

3. Run the code
- python main.py --text "A star" --output output/star_model
- python main.py --text "A 6 pointed star" --output output/star_model

- run the code using image
- python main.py --image path/to/your/image.jpg --output output/image_model

  ## My thought process

1. **Problem Understanding**: The assignment required creating a prototype that can convert 2D information  into 3D models.

2. **Technical Approach**: I decided to:
   - For images: Use depth estimation and point cloud reconstruction
   - For text: Use parameterized 3D models based on keywords

3. **Implementation Challenges**:
   - Simplifying 3D reconstruction 
   - Creating a flexible pipeline for both input types
   - Balancing complexity with functionality

##  **Future Directions**: The prototype could be enhanced with more advanced AI models for more realistic and accurate 3D generation like Unity and all
