import os
import sys
import subprocess
import shutil

def print_help():
    print("Used to download and run RealESRGAN.")
    print("You will need to handle the dependencies as listed in requirements.txt, which can be found at ~/.local/bin/RealESRGAN.")
    print("It is primarily designed to handle image collages.")
    print("\nAvailable Models:")
    print("RealESRGAN_x4plus, RealESRGAN_x2plus, RealESRNet_x4plus, realesr-general-x4v3, RealESRGAN_x4plus_anime_6B, realesr-animevideov3")
    print("Please visit https://github.com/xinntao/Real-ESRGAN/blob/master/docs/model_zoo.md for more details.")
    print("\nArguments: [Modelname] (-s # defaults to 4) [input-folder] [output-folder]")
    sys.exit(0)

def update_real_esrgan(model_name):
    real_esrgan_path = os.path.expanduser("~/.local/bin/RealESRGAN")
    if os.path.exists(real_esrgan_path):
        # If RealESRGAN directory exists, perform git pull
        subprocess.run(["git", "pull"], cwd=real_esrgan_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        # If RealESRGAN directory doesn't exist, clone it
        subprocess.run(["git", "clone", "https://github.com/xinntao/Real-ESRGAN.git", real_esrgan_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Create version.py in the realesrgan folder if it doesn't exist
    version_file_path = os.path.join(real_esrgan_path, "realesrgan", "version.py")

    # Check if version.py already exists
    if not os.path.exists(version_file_path):
        os.makedirs(os.path.dirname(version_file_path), exist_ok=True)
        try:
            with open(version_file_path, 'w') as version_file:
                version_file.write("version = '0.3.0'\n")
        except Exception as e:
            print(f"Error writing version file: {e}")

    return os.path.join(real_esrgan_path, "inference_realesrgan.py"), model_name

def process_frame(frame_path, output_folder, esrgan_script, scaling_factor):
    input_frame = frame_path

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Set the final output path with the correct naming convention
    output_frame = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_frame))[0]}_out.png")

    # Check if the output frame already exists, if yes, skip processing
    if os.path.exists(output_frame):
        return

    # Run RealESRGAN on the input frame
    esrgan_command = [
        "python",
        esrgan_script,
        "--fp32",
        "-n",
        model_name,
        "-i",
        input_frame,
        "-o",
        output_folder,  # Directly using the output folder without specifying a filename
        "-s",
        str(scaling_factor),
    ]

    # Suppress RealESRGAN output
    with open(os.devnull, "w") as null_output:
        result = subprocess.run(
            esrgan_command, stdout=null_output, stderr=null_output, text=True
        )

def main(model_name, scaling_factor, esrgan_script, input_folder, output_folder):
    # Get a list of frame paths for image files only
    frame_paths = [
        os.path.join(input_folder, frame)
        for frame in os.listdir(input_folder)
        if frame.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    total_frames = len(frame_paths)
    completed_frames = 0

    # Check for existing output frames
    for frame_path in frame_paths:
        output_frame = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(frame_path))[0]}_out.png")
        if not os.path.exists(output_frame):
            break
        completed_frames += 1
        print(
            f"\rProcessed: {completed_frames}/{total_frames} ({(completed_frames/total_frames)*100:.2f}%)",
            end="",
            flush=True
        )

    # Process frames using RealESRGAN starting from the first non-existing output frame
    for frame_path in frame_paths[completed_frames:]:
        process_frame(frame_path, output_folder, esrgan_script, scaling_factor)
        completed_frames += 1
        print(
            f"\rProcessed: {completed_frames}/{total_frames} ({(completed_frames/total_frames)*100:.2f}%)",
            end="",
            flush=True
        )

    print("\nESRGAN processing complete. Frames saved in:", output_folder)

if __name__ == "__main__":
    # Check for the help flag
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()

    # Parse command-line arguments
    model_name = sys.argv[1]
    scaling_factor = 4  # Default scaling factor

    if model_name not in ["RealESRGAN_x4plus", "RealESRGAN_x2plus", "RealESRNet_x4plus", "realesr-general-x4v3", "RealESRGAN_x4plus_anime_6B", "realesr-animevideov3"]:
        print("Invalid model name. Please choose from the available models.")
        sys.exit(1)

    if "-s" in sys.argv:
        try:
            scaling_factor_index = sys.argv.index("-s") + 1
            scaling_factor = float(sys.argv[scaling_factor_index])
            sys.argv.pop(scaling_factor_index)
            sys.argv.pop(scaling_factor_index - 1)
        except (IndexError, ValueError):
            print("Invalid usage of -s flag. Using default scaling factor (4).")

    esrgan_script, model_name = update_real_esrgan(model_name)

    input_folder = sys.argv[-2]
    output_folder = sys.argv[-1]

    main(model_name, scaling_factor, esrgan_script, input_folder, output_folder)

