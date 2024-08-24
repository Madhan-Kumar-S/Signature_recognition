import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from signature import match

# Match Threshold
THRESHOLD = 85

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("test")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)
            img_name = "./temp/test_img{}.png".format(sign)
            cv2.imwrite(filename=img_name, img=frame)
            print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    filename = os.getcwd()+'\\temp\\test_img{}.png'.format(sign)
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if(result <= THRESHOLD):
        messagebox.showerror("Failure: Signatures Do Not Match",
                             "Signatures are "+str(result)+f" % similar!!")
    else:
        messagebox.showinfo("Success: Signatures Match",
                            "Signatures are "+str(result)+f" % similar!!")
    return True

root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x700")

# Styles
style = {
    'font': ("Arial", 12),
    'bg': "#f0f0f0",
    'button_font': ("Arial", 10),
    'button_bg': "#0078D7",
    'button_fg': "#ffffff",
    'button_active_bg': "#0053ba",
}

root.configure(bg=style['bg'])

uname_label = tk.Label(root, text="Compare Two Signatures:", font=style['font'], bg=style['bg'])
uname_label.place(x=90, y=50)

img1_message = tk.Label(root, text="Signature 1", font=style['font'], bg=style['bg'])
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=style['font'])
image1_path_entry.place(x=150, y=120)

img1_capture_button = tk.Button(
    root, text="Capture", font=style['button_font'], bg=style['button_bg'], fg=style['button_fg'],
    activebackground=style['button_active_bg'], command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=style['button_font'], bg=style['button_bg'], fg=style['button_fg'],
    activebackground=style['button_active_bg'], command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=400, y=140)

image2_path_entry = tk.Entry(root, font=style['font'])
image2_path_entry.place(x=150, y=240)

img2_message = tk.Label(root, text="Signature 2", font=style['font'], bg=style['bg'])
img2_message.place(x=10, y=250)

img2_capture_button = tk.Button(
    root, text="Capture", font=style['button_font'], bg=style['button_bg'], fg=style['button_fg'],
    activebackground=style['button_active_bg'], command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.place(x=400, y=210)

img2_browse_button = tk.Button(
    root, text="Browse", font=style['button_font'], bg=style['button_bg'], fg=style['button_fg'],
    activebackground=style['button_active_bg'], command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=400, y=260)

compare_button = tk.Button(
    root, text="Compare", font=style['button_font'], bg=style['button_bg'], fg=style['button_fg'],
    activebackground=style['button_active_bg'], command=lambda: checkSimilarity(window=root,
                                                                              path1=image1_path_entry.get(),
                                                                              path2=image2_path_entry.get()))
compare_button.place(x=200, y=320)

footer = tk.Label(root, text="© Madhan Kumar S and Ajith K Narayan All rights reserved.", font=style['font'], bg=style['bg'])
footer.place(relx=0.5, rely=1.0, anchor='s', y=-10)

root.mainloop()

