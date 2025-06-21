import numpy as np
import hashlib #hashlib it provides secure hash functions like SHA-256.

def swap_pixels(pixels, key=42): #this is a function which scrambles the pixel positions of an image using a random number generator controlled by a key,  so that later we can reverse it using the same key, it makes it easier for encryption and decryption
   np.random.seed(key) #it sets the random seed for mumpys random number generator. if this is not  given then the shuffle wouldbe different each time and decryption would be impossible. it makes the same shuffling order happen everytime lets us use the same key to reverse it. it is basically a password that controls the randomness
   flat=pixels.reshape(-1,3) #it converts the 3D image array into a 2D list of pixels. i.e shape is (height,width,3) where 3 is RGB it reshapes to: (height*width,3) now its a flat list of individual RGB pixels making it easier to shuffle them.
   indices=np.arange(len(flat)) #it creates a list of all pixel indices from 0 to the number of pixels in the image. it is needed so that we can shuffle the positions in the next step.
   np.random.shuffle(indices) #randomly shuffles the pixel positions using the random key(seeded above). the order of the pixel indices gets randomized, it tells us where each pixel goes. this is the encryption key for pixel positions. 
   shuffled= flat[indices] #rearranges the picels based on the shuffled indices. new pixel = encrypted version.
   return shuffled.reshape(pixels.shape),indices #reshapes back to original image shape and returns the shuffled pixels along with the indices used for shuffling. the indices are needed for decryption later to know how to reverse the shuffle.

def unswap_pixels(pixels,indices): #this function is essentially used for decryption, ,it takes the encrypted pixel array pixels that has its pixels shuffled and orginal shuffle indices which records how the pixels were rearranged and it reconstructs the original image by undoing the shuffle
    flat=pixels.reshape(-1,3) #flattens the 3D array of RGM into a 2D array. each row is now a pixel with RGB values.
    original=np.zeros_like(flat) #creates an array of the shape shape of the flat but filled with zeros. this will hold the original values after unswapping. it is like a blank canvas on which the each correct pixel is stored
    original[indices]=flat #uses the indices to place each pixel back in its original position. it fills the original array with the pixels in the correct order.
    return original.reshape(pixels.shape) #reshapes the 2D array to the original image shape. 

def xor_encrypt(pixels,key=99): #thisfunction applies a simple XOR bitwise operation to each pixel using a key. it is a basic encryption technique that flips bits based on a key. it is used to further encrypt the pixel values after shuffling.
    return pixels ^ key #applies the XOR operation to each pixel value with the key. it flips the bits of each pixel based on the key. this is a simple encryption step that can be reversed by applying the same XOR operation again with the same key. ^ python bitwise operator for XOR

def xor_decrypt(pixels,key=99): #this function reverses the XOR operation by applying the same key again. it is used to decrypt the pixel values after shuffling.
    return pixels ^ key #applies the XOR operation again with the same key to reverse the encryption. it flips the bits back to their original values. this is a simple decryption step that can be reversed by applying the same XOR operation again with the same key.

def password_tokeys(password): #this is a function which converts the string entered to hash
    hashed= hashlib.sha256(password.encode()).hexdigest() #here  first the password.encode() it converts the string into bytes which is required for hashing, hashlib.sha256() it creates the SHA 256 hash object from the objects, the hexdigest converts the hash to a hexadecimal string
    xor_key = int(hashed[:4],16) % 256 #it takes the first 4 characters of the hash, converts it to an integer using base 16, and then takes modulo 256 to ensure it is in the range of 0-255. this is used as the key for XOR encryption.
    swap_key = int(hashed[5:9],16) #4 characters from position 5 to 9  
    return xor_key,swap_key 