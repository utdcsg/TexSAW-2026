README

## Lost my keys

## Challenge Description
I can't find my original house key anywhere! Can you help me find it? Here's a picture of my keys the nanny took before they were lost. It must be hidden somewhere!


## Solution
1) The image contains a zip file hidden inside it. To reveal the zip file, use the command, "mv Temoc_keyring.png key.zip". The name of the zip file can be found in the provided image itself. Adjusting image settings such as contrast and brightness can help make the words easier to see.

2) Unzip 'key.zip' which will reveal 'Temoc_keyring(orig).png' and 'where_are_my_keys.png'. 
	'Temoc_keyring(orig).png' is the original image and 'where_are_my_keys.png' is the decrypter

3) Using a software program like SSuite Picsel Encrytion, the image can be decrypted to reveal the hidden flag: texsaw{keys_are_the_secret_to_success}

## Author name 
@Coy

## Build instructions
In case the challenge needs to be rebuilt.
1 - Building key.zip: Use a smaller image file than what you intend to use as your cover image. Using SSuite Picsel Encrytion, encrypt the image with the flag 'texsaw{keys_are_the_secret_to_success}'. Save this image, this will be used to decrypt the original image. Zip both images together as 'key.zip'

2 - Building the cover image: With a larger sized image, add hint text to the image itself. In a photo editor, use color picker on the background and adjust the color slightly and write 'key' then save the image. MUST BE PNG FORMAT. 

3 - Hiding zip file in image: Use the terminal and with both 'key.zip' and the cover image in the same folder, use the command 'copy /b cover.png + key.zip Temoc_keyring.png'

##Deployment
Challenge only requires inclusion of image png, 'Temoc_keyring.png'
