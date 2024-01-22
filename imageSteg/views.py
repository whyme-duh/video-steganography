import re
import time
from django.shortcuts import redirect, render
from .forms import ImageEncodeForm, DecodeForm
from PIL import Image
from django.contrib import messages

def genData(data):

		# list of binary codes
		# of given data
		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
				# pix[j] -= 1

		# Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1
			
def encode(request, files, data):
	start = time.time()
	print(str(files))
	image = Image.open(files, 'r')

	if (len(data) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, data)
	newimg.save('C:/Users/ritik_yxb9lpe/OneDrive/Documents/python-django-projects/steganography/camouflage/media/encoded/image_encode/encoded.png')
	request.session['image_location'] = 'media/encoded/image_encode/encoded.png'
	end = time.time()
	completion_time = end-start
	messages.success(request, f'Encoded Successfully!')
	return completion_time

def image_sucess(request):
	return render(request, 'imageSteg/success.html')

def encode_request(request):
	request.session['image_location'] = ''
	form = ImageEncodeForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form_list = form.save()
		form_list.user = request.user
		form_list.save()
		image = form.cleaned_data['image_file']
		message = form.cleaned_data['message']
		completion_time = encode(request,image,message)
		request.session['completion_time'] = completion_time
		return redirect('image-success')
	
	context = {
		'form' : form
    }
	return render(request, 'imageSteg/imageEncode.html',context )

def decode(image_file):
	image = Image.open(image_file, 'r')

	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data
		
def decode_req(request):
	error = False
	sent_message =False
	form = DecodeForm()
	data =''
	if request.method == 'POST':
		form = DecodeForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			encoded_file = form.cleaned_data['encoded_image']
			data = "Your decoded message is : " + decode(encoded_file)
			if re.match("^[ -~\s]+$", data):
				sent_message =True
				with open('media/image_decode.txt', 'w') as f:
					f.write(data)
				messages.success(request, f'Decoded Successfully ')
			else:
				error = True
				sent_message = True
				data = "error"
	return render(request, 'imageSteg/imageDecode.html', {'form' : form, 'data' : data, 'sent_message':sent_message, 'error': error})

			