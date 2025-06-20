from PIL import Image
import numpy as np 
from encrypt import swap_pixels, unswap_pixels, xor_encrypt, xor_decrypt

input_file= "cat.jpg"
encrypted_file = "encrypted_cat.jpg"
decrypted_file = "decrypted_cat.jpg"

swap_key = 123
xor_key = 99

img = Image.open(input_file).convert('RGB')
pixels=np.array(img).astype(np.uint8)

swapped, indices= swap_pixels(pixels,key=swap_key)
xor_encrypted= xor_encrypt(swapped, key=xor_key)
Image.fromarray(xor_encrypted).save(encrypted_file)
print(f"[+] Image encrypted and saved as {encrypted_file}")

xor_decrypted = xor_decrypt(xor_encrypted, key=xor_key)
unswapped=unswap_pixels(xor_decrypted,indices)
Image.fromarray(unswapped).save(decrypted_file)
print(f"[+] Image decrypted and saved as {decrypted_file}")