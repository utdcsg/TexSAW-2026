This is a stegonography challenge that has the user extract APL code from an image and run the code on the image to reveal the flag.

1. Getting the APL code
    - Download STEGOSAURUS.png from the CTFd website
    - Run a stegonography extraction tool on the image to discover the APL code hidden wihtin the image
2. Running the code
    - Recognize that the code is written in APL
    - Import the image into gnu APL using the PNG system tool
    - Run the hidden code on the image (treating the image as a matrix)
3. Flag is revealed
    - After the code is run on the image, GNU apl should print the flag.
    - "texsaw{Steg0s@urus_Eats_APL1eS}"
