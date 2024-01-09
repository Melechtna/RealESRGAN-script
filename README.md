# RealESRGAN-script

I needed this for a project, this ones a little more complex, it takes an input folder and an output folder, if the output folder doesn't exist, it creates it. The help (-h) will be quite important should you use it and run into any errors, as likely you're missing dependancies, or don't know what models are available.

On first run it will take a while to get going, as it needs to clone RealESRGAN, ensure the files are in the right place, and assuming no dependancy issues, download the requested model. It might be able to handle videos directly, but the script is specifically designed to handle Image Collages, as this is the best way to handle upscaling video that I've found.

Other than that, it should make the task relatively simple, and resumable. It checks every image between the input and output folder, and if it finds one doesn't exist, recreates them, then will skip ahead until it finds the next one that doesn't exist, this is incase you lose power, need to reboot, whatever, you can then resume upscaling from where you left off.

Important to note, the script expects frame-$010d.png, which my extraction script specifically conforms to. If you're having issues with file detection, this is likely why.
