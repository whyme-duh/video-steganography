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
def error_404_view(request, exception):
    return render(request, 'core/404.html')

def error_500_view(request):
    return render(request, 'core/404.html')
# it shows the list of the semester





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
        video_clip = VideoFileClip(video_path)
        audio = video_clip.audio
        return frames, audio, fps
    
    @staticmethod
    def encode(key: str, message: str, frames):
        frames = np.array(frames)
        height, width, color_channel = frames[0].shape
        total_encodeable_amount = frames[1:,:,:,:].size
        total_encodeable_amount_single_frame = total_encodeable_amount // (len(frames)-1)
        total_message_bits = len(message) * 8
        if total_encodeable_amount < total_message_bits:
            print("Error: Message too long to be encoded in the video.")
            return frames
        extra_bits = total_message_bits % total_encodeable_amount_single_frame
        message += ' ' * ((total_encodeable_amount_single_frame - extra_bits) // 8)
        length_binary = bin(len(message))[2:]
        length_binary = length_binary.zfill(48)
        ciphertext = Video.rc4.encrypt(key=key, plaintext=message)
        ciphertext += '0' * (len(ciphertext) % color_channel)
        ciphertext_frames = np.array(list(ciphertext)).astype(int)
        ciphertext_frames = ciphertext_frames.reshape((-1, height, width, color_channel))
        random_index = np.random.randint(1, len(frames)-ciphertext_frames.shape[0])
        binary_frame_lsb = frames[random_index: ciphertext_frames.shape[0]+random_index] % 2
        frames[random_index: ciphertext_frames.shape[0]+random_index] ^= np.logical_xor(binary_frame_lsb, ciphertext_frames)
        frames = frames.astype(np.uint8)
        random_index_binary = np.binary_repr(random_index, width=48)
        bin_array = np.array(list(length_binary + random_index_binary), dtype=np.uint8)
        binary_frame_lsb = frames[0] % 2
        bin_array = np.pad(bin_array, (0, frames[0].size - len(bin_array)), 'constant')
        bin_array = bin_array.reshape(frames[0].shape)
        frames[0] ^= np.logical_xor(binary_frame_lsb, bin_array)
        return frames



    @staticmethod
    def decode(key: str, frames):
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
        total_encodeable_amount = frames[1,:,:,:].size
        total_frames = length // total_encodeable_amount
        ciphertext = ""
        for frame in frames[random_index: random_index+total_frames, :, :, :]:
            unpacked_bits = np.unpackbits(frame)
            ciphertext += ''.join(map(str, unpacked_bits.reshape((-1, 8))[:, -1]))
        plaintext = Video.rc4.decrypt(key=key, ciphertext=ciphertext)
        return plaintext

                    
    @staticmethod
    def write_video(request,frames, audio, output_path, fps):
        height, width, layers = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'FFV1') 
        video_writer = cv2.VideoWriter('temp_video.avi', fourcc, fps, (width, height))
        for frame in frames:
            video_writer.write(frame)
        video_writer.release()
        video_clip = VideoFileClip('temp_video.avi')
        video_clip.set_audio(audio).write_videofile(output_path,codec='ffv1', audio_codec='aac')
        request.session['encoded_size_video']= round((os.path.getsize(output_path)/1024**2),2)
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
            if frames:
                encoded_frames = Video.encode(key=secret_key, message=message, frames=frames)
                if encoded_frames is not None:
                    output_path = "media/encoded/" + encoded_filename + '.avi'
                    Video.write_video(request, frames=encoded_frames, audio=audio, output_path=output_path, fps=fps)
                    form_list.encoded_file_name = encoded_filename
                    form_list.encoded_file = output_path
                    request.session['original_size_video'] =round((os.path.getsize(file_location)/1024**2),2)
                    request.session['encoded_video'] = "/encoded/" + encoded_filename + '.avi'
                    form_list.save()
                    end = time.time()
                    completion = round(end - start,2)
                    request.session['video_completion_time'] = completion
                    messages.success(request, 'Your video has been encoded succesfully')
                    return redirect('success')
                else:
                    messages.error(request, "Error during encoding.")
                
        else:
            return render(request, 'core/encode.html', context)
    return render(request, 'core/encode.html', context)

   

def decode(request):
    sent_message = False
    message = ''

    error = False
    completion_time = None
    form = DecodeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        start = time.time()
        form_list = form.save()
        file_name = form_list.video.path
        secret_key = form.cleaned_data['secret_key']
        frames, audio, fps = Video.read_video_frames(video_path=file_name)
        if frames:
            # message = check_message(file_name, frame_number, secret_key, encoded_filename)
            decoded_message = Video.decode(key=secret_key, frames=frames).rstrip(' ')
            sent_message = True

            if re.match("^[ -~\s]+$", decoded_message):
                secret_key = "Secret Key : " + secret_key
                message = "Your decoded message : " +  decoded_message
                end = time.time()
                completion_time = round(end - start,2)
                lines = [secret_key, message]
                with open('media/decode.txt', 'w') as f:
                    for line in lines:
                        f.write(line)
                        f.write('\n')
                sent_message = True
            else:
                error = True
                sent_message = True
                message = "Might be because of incorrect secret key or the video is not encoded."
            form_list.save()
        else:
            messages.error(request, f'The given video with frame key cannot be decoded')
    context ={ 'form' : form, 'message' : message, 'error' : error, 'sent_message' : sent_message , 'completion_time' : completion_time}
    return render(request, 'core/decode.html',  context)




