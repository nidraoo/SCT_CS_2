import tkinter as tk 
from tkinter import filedialog, messagebox #filedialog is for 
from PIL import Image,ImageTk # PIL is python immaging library which is used to open, process and save the image files.
import numpy as np  #used to manipulate the image pixels data as arrays for encryption and decryption operations.
import os
from datetime import datetime
from encrypt import swap_pixels, unswap_pixels, xor_encrypt, xor_decrypt,password_tokeys

class ImageEncryption:
    def __init__(self,root):
        self.root =root
        self.root.title("Image Encrytion Tool")
        self.root.geometry("950x650")
        self.root.configure(bg="white")
        
        self.image=None
        self.image_path=None
        self.encrypted_image=None
        self.decrypted_image=None
        self.indices=None
        
        self.xor_key= 90
        self.swap_key=123
        
        self.setup_gui()
        
    def setup_gui(self):
        heading =tk.Label(self.root,text='IMAGE PIXEL MANIPULATION TOOL',font=('Times New Roman',18,'bold italic'),bg='white',fg='black')
        heading.pack(pady=5) #this makes the heading title for the page with padding y axis 5
        
        button_frame=tk.Frame(self.root,bg='white')
        button_frame.pack(pady=5) #this is creating frames a row for all the buttons
        
        #making buttons of other colors for upload, save, encrypt, decrypt, and clear
        tk.Button(button_frame,text="Upload Image",command=self.upload_image,bg='#4CAF50', fg='white',width=15).pack(side=tk.LEFT,padx=5)
        tk.Button(button_frame, text='ENCRYPT IMAGE', command=self.encrypt_image, bg='#2196F3', fg='white',width=15).pack(side=tk.LEFT,padx=5)
        tk.Button(button_frame,text='DECRYPT IMAGE',command=self.decrypt_image, bg="#FF9800",fg='white',width=15).pack(side=tk.LEFT,padx=5)
        tk.Button(button_frame,text='Save Current Image', command=self.save_image, bg='#9C27B0',fg='white',width=15).pack(side=tk.LEFT,padx=5)
        tk.Button(button_frame,text='Clear',command=self.clear_all,bg="#d51c0e",fg='white',width=15).pack(side=tk.LEFT,padx=5)

        self.canvas = tk.Label(self.root,bg='gray')
        self.canvas.pack(pady=10)
        
        tk.Label(self.root,text="Enter password for the key: ",bg='white',font=("Times New Roman",12)).pack()
        self.password_enter= tk.Entry(self.root,show=" ",width=30)
        self.password_enter.pack(pady=5)
        self.password_enter.delete(0,tk.END)
    
        tk.Label(self.root,text="HISTORY",bg='white',font=("Times New Roman",12,"bold"),anchor='w').pack(pady=(10,0))
        self.history=tk.Text(self.root,height=12,width=110,bg='lightyellow')
        self.history.pack(pady=10)
        self.display_security_note()
        self.history.insert(tk.END, "[+] Ready! Upload an image and set a password to start.\n")
        
    def display_security_note(self):
        self.history.insert(tk.END,"\n[!] NOTE: THIS  TOOL USES PIXEL SHUFFLING AND XOR.\n")
        self.history.insert(tk.END,"[!]FOR EDUCATIONAL AND DEMO PURPOSES ONLY.\n")
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if file_path:
            self.image_path=file_path
            self.image=Image.open(file_path).convert('RGB')
            self.display_image(self.image)
            self.history.insert(tk.END,f"[+] Uploaded image: {file_path} \n")
    
    def display_image(self,img):
        img_resize=img.resize((400,400))
        self.tk_image= ImageTk.PhotoImage(img_resize)
        self.canvas.config(image=self.tk_image) 
        
    def get_keys_frompassword(self):
        password= self.password_enter.get() 
        if not password or password=="Enter Password":
            messagebox.showerror("ERROR!","PLEASE ENTER A VALID PASSWORD.")
            return None, None
        xor_key,swap_key=password_tokeys(password)
        return xor_key,swap_key
    
    def encrypt_image(self):
        if self.image is None:
            messagebox.showerror("ERROR!","PLEASE UPLAOD AN IMAGE")
            return 
        self.xor_key, self.swap_key= self.get_keys_frompassword()
        if self.xor_key is None:
            return
        pixels=np.array(self.image).astype(np.uint8)
        swapped, self.indices = swap_pixels(pixels, key=self.swap_key)
        encrypt=xor_encrypt(swapped,key=self.xor_key)
        self.encrypted_image = Image.fromarray(encrypt)
        self.display_image(self.encrypted_image)
        self.history.insert(tk.END,"[+] Image encrypted with password-derived keys.\n")
        
    def decrypt_image(self):
        if self.encrypted_image is None or self.indices is None:
            messagebox.showerror("ERROR","NO ENCRYPTED IMAGE FOUND!!")
            return
        self.xor_key, self.swap_key = self.get_keys_frompassword()
        if self.xor_key is None:
            return
        
        pixels=np.array(self.encrypted_image).astype(np.uint8)
        xor_decrypted=xor_decrypt(pixels,key=self.xor_key)
        unswapped=unswap_pixels(xor_decrypted,self.indices)
        self.decrypted_image= Image.fromarray(unswapped)
        self.display_image(self.decrypted_image)  
        self.history.insert(tk.END,"[+] Image decrypted successfully.\n")
    
    def save_image(self):
        if self.encrypted_image is None and self.decrypted_image is None:
            messagebox.showerror("ERROR","NO IMAGE TO SAVE")
            return
        image_to_save= self.decrypted_image if self.decrypted_image else self.encrypted_image
        timestamp= datetime.now().strftime("%Y%m%d_%H%M%S")
        filename=f"saved_image_{timestamp}.jpg"
        image_to_save.save(filename)
        self.history.insert(tk.END, f"[+] Image saved as {filename}\n")
        messagebox.showinfo("SAVED",f"Image saved as {filename}")
        
    def clear_all(self):
        self.image=None
        self.image_path=None
        self.encrypted_image= None
        self.decrypted_image=None
        self.indices= None
        self.password_enter.delete(0,tk.END)
        self.canvas.config(image='')
        self.history.insert(tk.END,"[+] Cleared all data and image from memory.\n")
            
          
if __name__=='__main__':
    root=tk.Tk()
    app=ImageEncryption(root)
    root.mainloop()
    
        












































'''    
to only run in terminal and check

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
'''