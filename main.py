import os
import argparse
from image_processor import process_image,extract_depth_map
from text_processor import text_processing
from model_generator import generate_model_from_text
from model_generator import generating_model_from_img
from model_generator import save_models

from visualizer import visualize_model

def main():
    parser = argparse.ArgumentParser(description="convert the photo or text to a 3D model")

    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--image',type=str,help='path to input image')
    inputs.add_argument('--text',type=str,help='text describing the object')

    parser.add_argument('--output',type=str,default='output/model',
                        help='path ton save the output')
    parser.add_argument('--format',type=str,choices=['obj','stl'],default='obj',
                        help='output filr format')
    parser.add_argument('--no_vis',action='store_true',help='disable visualization')


    # combining all the instructions that we have added for our output
    arguments = parser.parse_args()

    os.makedirs(os.path.dirname(arguments.output),exist_ok=True)


    # process input 
    if arguments.image:
        print(f"Processing image: {arguments.image}")
        processed_image = process_image(arguments.image)
        depth_map = extract_depth_map(processed_image)
        mesh, point_cloud = generating_model_from_img(processed_image, depth_map)
    else:
        print(f"Processing text prompt: {arguments.text}")
        processed_text = text_processing(arguments.text)
        mesh, point_cloud = generate_model_from_text(processed_text)


    output_file = f"{arguments.output}.{arguments.format}"
    save_models(mesh, output_file, arguments.format)
    print(f"3D model saved as: {output_file}")

    if not arguments.no_vis:
        vis_output = f"{arguments.output}_vis.png"
        visualize_model(mesh, point_cloud, save_path=vis_output)
        print(f"Visualization saved as: {vis_output}")


if __name__=="__main__":
    main()