import json
import os
import re
import time
from django.shortcuts import redirect, render
from . models import Encoding
from . forms import DecodeForm, EncodeForm
from PIL import Image
from django.contrib import messages
from moviepy.editor import VideoFileClip
from .RC4.rc4 import RC4


# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def home(request):
    return render(request, 'core/home.html')




#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2


# In[2]:


def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result



def KSA(key):
    key_length = len(key)
    S=list(range(256)) 
    j=0
    for i in range(256):
        j=(j+S[i]+key[i % key_length]) % 256
        S[i],S[j]=S[j],S[i]
    return S


# In[15]:


def PRGA(S,n):
    i=0
    j=0
    key=[]
    while n>0:
        n=n-1
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        K=S[(S[i]+S[j])%256]
        key.append(K)
    return key


# In[16]:


def preparing_key_array(s):
    return [ord(c) for c in s]


# In[17]:


def encryption(plaintext, key):
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(plaintext)))
    plaintext=np.array([ord(i) for i in plaintext])

    cipher=keystream^plaintext
    ctext=''
    for c in cipher:
        ctext=ctext+chr(c)
    return ctext


# In[18]:





# In[19]:


def embed(frame, msg, key): #  here msg is the parameter that is sent to this function for accepting the messages 
    data=encryption(msg, key)    # here the msg is encrypted
    print("The encrypted data is : ",data)
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')

    data +='*^*^*'
    
    binary_data=msgtobinary(data)
    length_data = len(binary_data)
    
    index_data = 0
    
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
        return frame


# In[20]:



# In[21]:


def encode_vid_data(request, file, frame_no, msg, key,encoded_filename):
    cap=cv2.VideoCapture(file)
    vidcap = cv2.VideoCapture(file)    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))
    size = (frame_width, frame_height)
    max_frame=0;
    output_filename = 'encoded/'+encoded_filename+'.mp4'
    out_filename = 'media/'+output_filename
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    if (frame_no > max_frame or frame_no < 0):
        print("error")
    n=frame_no
    frame_number = 0
    out = cv2.VideoWriter(out_filename,fourcc, 25.0, size)

    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:    
            change_frame_with = embed(frame, msg, key)
            frame_ = change_frame_with 
            frame = change_frame_with
        out.write(frame)
    print("\nEncoded the data successfully in the video file.")
    request.session['encoded_video'] = output_filename  
    out.release()
    vidcap.release()
    cv2.destroyAllWindows()  
    return frame_

def decryption(ciphertext, secret_message):
    key=secret_message
    key=preparing_key_array(key)

    S=KSA(key)
    print(secret_message)
    keystream=np.array(PRGA(S,len(ciphertext)))
    ciphertext=np.array([ord(i) for i in ciphertext])

    decoded=keystream^ciphertext
    dtext=''
    for c in decoded:
        dtext=dtext+chr(c)
    return dtext

def extract(frame, secret_message):
    data_binary = ""
    final_decoded_msg = ""
    print('frame', frame)
    frame_list = json.loads(frame) 
    frame_array = np.array(frame_list)
    print(type(frame_array))
    for i in frame_array:
        for pixel in i:
            # print('i' , i)
            # print('pixel' , msgtobinary(pixel))
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]   
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            # print('total bytes', total_bytes)
            decoded_data = ""
            for byte in total_bytes:
                # print(byte)
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    for i in range(0,len(decoded_data)-5):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg, secret_message)
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n",final_decoded_msg)
                    return 




# In[22]:
def give_message(request,id):
    encoded_object = Encoding.objects.get(id = id)
    message = encoded_object.message
    return render(request, 'core/sucess.html',{'message':message})

def decode_vid_data(request,id):
    video = Encoding.objects.filter(id)
    print(video.video.url)
    print(filename)
    cap = cv2.VideoCapture(video.video.url)
    max_frame=0
    while(cap.isOpened()):
        ret, frame_ = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    vidcap = cv2.VideoCapture(filename)
    frame_number = 0
    # print(frame)
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame_ = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            print('matched')
            # message = extract(frame ,secret_message)
            return
        
    vidcap.release()
    return render(request, 'core/sucess.html',{'message':message})


# In[23]:

# In[ ]:

#allowing user to first upload a video that could provide a result of total number of video frames

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



def sucess(request):
    return render(request, 'core/sucess.html')


def check_message(filename, frame_number, secret_key ,encoded_filename):
    encoding = Encoding.objects.all()
    message = ''
    print(frame_number, secret_key)
    for object in encoding:
        if (object.frame_number == frame_number and object.secret_key == secret_key and object.encoded_file_name == encoded_filename):
            
            return object.message
        else:
            message = 'Cannot found'
    return message
    



# %%
 

def about_us(request):
    return render(request, 'core/about.html')



class Video:
    rc4 = RC4()

    @staticmethod
    def read_video_frames(video_path):
        frames = []
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        if not cap.isOpened():
            print("Error: Couldn't open the video file.")
            return frames, None

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()

        # Now read audio from the video file
        video_clip = VideoFileClip(video_path)
        audio = video_clip.audio

        return frames, audio, fps
    

    @staticmethod
    def encode(key: str, message: str, frames):
        frames = np.array(frames)
        height, width, color_channel = frames[0].shape

        # first frame always for storing the length of the message and start frame index
        total_encodeable_amount = frames[1:,:,:,:].size

        total_encodeable_amount_single_frame = total_encodeable_amount // (len(frames)-1)
        total_message_bits = len(message) * 8

        if total_encodeable_amount < total_message_bits:
            print("Error: Message too long to be encoded in the video.")
            return frames
        
        extra_bits = total_message_bits % total_encodeable_amount_single_frame

        
        # Now encode the length of the message in the first frame
        # convert the length of the message to binary

        # Append space to the message
        message += ' ' * ((total_encodeable_amount_single_frame - extra_bits) // 8)
        length_binary = bin(len(message))[2:]
        length_binary = length_binary.zfill(48)

        # Encrypt the message
        ciphertext = Video.rc4.encrypt(key=key, plaintext=message)

        # Append 0 to the ciphertext to make it a multiple of color_channel
        ciphertext += '0' * (len(ciphertext) % color_channel)

        # Now split the ciphertext into frames
        ciphertext_frames = np.array(list(ciphertext)).astype(int)
        
        # resize the ciphertext_frames to the size (x, height, width, color_channel)
        ciphertext_frames = ciphertext_frames.reshape((-1, height, width, color_channel))
        
        # choose a random frame index to store the ciphertext_frames except the first frame
        random_index = np.random.randint(1, len(frames)-ciphertext_frames.shape[0])
        
        binary_frame_lsb = frames[random_index: ciphertext_frames.shape[0]+random_index] % 2
        # Now store the ciphertext_frames in the frame starting from the random_index
        frames[random_index: ciphertext_frames.shape[0]+random_index] ^= np.logical_xor(binary_frame_lsb, ciphertext_frames)
        frames = frames.astype(np.uint8)

        # Now convert random index to binary
        random_index_binary = np.binary_repr(random_index, width=48)

        # Now store the length of the message and the random index in the first frame
        # Combine the length_binary and random_index_binary
        bin_array = np.array(list(length_binary + random_index_binary), dtype=np.uint8)
        binary_frame_lsb = frames[0] % 2

        # Pad the bin_array to make it equal to the size of the first frame
        bin_array = np.pad(bin_array, (0, frames[0].size - len(bin_array)), 'constant')
        bin_array = bin_array.reshape(frames[0].shape)
        frames[0] ^= np.logical_xor(binary_frame_lsb, bin_array)
        frames = frames.astype(np.uint8)

        return frames



    @staticmethod
    def decode(key: str, frames):
        # Get the length of the message and the random index from the first frame
        length_binary = ""
        random_index_binary = ""
        
        frames = np.array(frames)
        frame = frames[0]
        unpacked_bits = np.unpackbits(frame)
        bin_array = ''.join(map(str, unpacked_bits.reshape((-1, 8))[:, -1]))
        length_binary += bin_array[:48]
        random_index_binary += bin_array[48:96]

        length = int(length_binary, 2) * 8
        random_index = int(random_index_binary, 2)

        # Get number of frames required to store the message
        total_encodeable_amount = frames[1,:,:,:].size
        # print("Total encodeable amount: ", total_encodeable_amount)
        total_frames = length // total_encodeable_amount
        # print("Total frames: ", total_frames)

        # print("Length of the message: ", length)
        # print("Random index: ", random_index)
        # Now get the ciphertext from the random_index
        ciphertext = ""
        for frame in frames[random_index: random_index+total_frames, :, :, :]:
            # print(frame.shape)
            unpacked_bits = np.unpackbits(frame)
            ciphertext += ''.join(map(str, unpacked_bits.reshape((-1, 8))[:, -1]))

        # Now decrypt the ciphertext
        plaintext = Video.rc4.decrypt(key=key, ciphertext=ciphertext)
        return plaintext


                    
    @staticmethod
    def write_video(frames, audio, output_path, fps):
        # Get the shape of the frames assuming all frames have the same shape
        height, width, layers = frames[0].shape

        # Create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'FFV1') 
        video_writer = cv2.VideoWriter('temp_video.avi', fourcc, fps, (width, height))

        # Write frames to the video file
        for frame in frames:
            video_writer.write(frame)

        # Release the video writer object
        video_writer.release()

        # Now add audio to the video file
        video_clip = VideoFileClip('temp_video.avi')
        video_clip.set_audio(audio).write_videofile(output_path,codec='ffv1', audio_codec='aac')

        os.remove('temp_video.avi')



def encode(request):
    
    form = EncodeForm(request.POST or None, request.FILES or None)
    context = {'form': form}

    if request.method == 'POST':
        if form.is_valid():
            start = time.time()
            form_list = form.save()
            file_location = form_list.video.path
            secret_key = form.cleaned_data['secret_key']
            message = form.cleaned_data['message']
            encoded_filename = form.cleaned_data['encoded_file_name']
            frames, audio, fps = Video.read_video_frames(video_path=file_location)
            if frames and audio and fps:
                encoded_frames = Video.encode(key=secret_key, message=message, frames=frames)
                if encoded_frames is not None:
                    output_path = "media/encoded/" + encoded_filename + '.avi'
                    Video.write_video(frames=encoded_frames, audio=audio, output_path=output_path, fps=fps)
                    form_list.encoded_file_name = encoded_filename
                    form_list.encoded_file = output_path
                    request.session['encoded_video'] = "/encoded/" + encoded_filename + '.avi'
                    form_list.save()
                    end = time.time()
                    completion = end - start
                    request.session['video_completion_time'] = completion
                    messages.success(request, 'Your video has been encoded succesfully')
                    return redirect('success')
                else:
                    messages.error(request, "Error during encoding.")
        else:
            return render(request, 'core/encode.html', context)

    else:
        form = EncodeForm(None)
        return render(request, 'core/encode.html', context)
   

def decode(request):
    sent_message = False
    message = ''
    error = False
    form = DecodeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form_list = form.save()
        file_name = form_list.video.path
        secret_key = form.cleaned_data['secret_key']
        frames, audio, fps = Video.read_video_frames(video_path=file_name)
        if frames and audio and fps:
            # message = check_message(file_name, frame_number, secret_key, encoded_filename)
            decoded_message = Video.decode(key=secret_key, frames=frames).rstrip(' ')
            sent_message = True

            if re.match("^[ -~\s]+$", decoded_message):
                secret_key = "Secret Key : " + secret_key
                message = "Your decoded message : " +  decoded_message
                lines = [secret_key, message]
                with open('media/decode.txt', 'w') as f:
                    for line in lines:
                        f.write(line)
                        f.write('\n')
                sent_message = True
            else:
                error = True
                sent_message = True
                message = "Error in retrieving the encoded message, might be because of incorrect secret key"
            form_list.save()
        else:
            message.error(request, f'The given video with frame key cannot be decoded')
    context ={ 'form' : form, 'message' : message, 'error' : error, 'sent_message' : sent_message }
    return render(request, 'core/decode.html',  context)




