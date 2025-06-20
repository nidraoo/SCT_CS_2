from PIL import Image # PIL is python immaging library which is used to open, process and save the image files.
import numpy as np  #used to manipulate the image pixels data as arrays for encryption and decryption operations.
from encrypt import swap_pixels, unswap_pixels, xor_encrypt, xor_decrypt

input_file= "cat.jpg" 
encrypted_file = "encrypted_image.jpg"
decrypted_file = "decrypted_image.jpg"

swap_key = 250 #its likes a password for position scrambling, it controls how the pixels aree shuffled. it is used to scramble the pixel positions of an image using a random number generator controlled by a key, so that later we can reverse it using the same key, it makes it easier for encryption and decryption.
xor_key = 80 #used to modify pixel values using a bitwise XOR. this makes it unreadable without the correct key. 

img = Image.open(input_file).convert('RGB') #very important , it opens the image and it converts any scale or format image to RGB format, so that we can work with it as a standard 3 channel image. this is needed because some images might be in grayscale or have an alpha channel.
pixels=np.array(img).astype(np.uint8) #it converts the image to NUmPy array of shape (height,width,3) and astype(np.uint8) ensures pixel values are in the 0-255 range (8bit unsigned integers).

swapped, indices= swap_pixels(pixels,key=swap_key) #from the function called the swapped is the shuffled pixel array and indices is the list of indices used to shuffle the pixels. it scrambles the pixel positions of an image using a random number generator controlled by a key, so that later we can reverse it using the same key, it makes it easier for encryption and decryption.
xor_encrypted= xor_encrypt(swapped, key=xor_key) #this applies a simple XOR bitwise operation to each pixel using a key. it is a basic encryption technique that flips bits based on a key. it is used to further encrypt the pixel values after shuffling.
Image.fromarray(xor_encrypted).save(encrypted_file) #Converts  theNUmPy array back into an image
print(f"[+] Image encrypted and saved as {encrypted_file}")

xor_decrypted = xor_decrypt(xor_encrypted, key=xor_key) #this function reverses the XOR again using the same key , it is decryption step, the image pixels back to original
unswapped=unswap_pixels(xor_decrypted,indices) #uses  original indices to get the original position to reverse to form it, that is unshuffle the pixels back to their original positions. it reconstructs the original image by undoing the shuffle.
Image.fromarray(unswapped).save(decrypted_file) #converts the unshuffled pixel arrage to back to an image
print(f"[+] Image decrypted and saved as {decrypted_file}")