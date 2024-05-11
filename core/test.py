import cv2


def read_video_frames(video_path):
        frames = []
        cap=cv2.VideoCapture(video_path) 
        print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) 
        print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) 
        print("CAP_PROP_FPS : '{}'".format(cap.get(cv2.CAP_PROP_FPS))) 
        print("CAP_PROP_POS_MSEC : '{}'".format(cap.get(cv2.CAP_PROP_POS_MSEC))) 
        print("CAP_PROP_FRAME_COUNT  : '{}'".format(cap.get(cv2.CAP_PROP_FRAME_COUNT))) 
        print("CAP_PROP_MONOCHROME : '{}'".format(cap.get(cv2.CAP_PROP_MONOCHROME))) 
        print("CAP_PROP_SHARPNESS: '{}'".format(cap.get(cv2.CAP_PROP_SHARPNESS))) 
        print("CAP_PROP_SATURATION : '{}'".format(cap.get(cv2.CAP_PROP_SATURATION))) 
        print("CAP_PROP_TEMPERATURE : '{}'".format(cap.get(cv2.CAP_PROP_TEMPERATURE))) 
        print("CAP_PROP_GAMMA  : '{}'".format(cap.get(cv2.CAP_PROP_GAMMA))) 
        print("CAP_PROP_CONVERT_RGB : '{}'".format(cap.get(cv2.CAP_PROP_CONVERT_RGB))) 
        fps = cap.get(cv2.CAP_PROP_FPS)
        if not cap.isOpened():
            print("Error: Couldn't open the video file.")
            return frames, None
        
        cap.release()
       

def main():
     read_video_frames('C:/Users/ritik_yxb9lpe/OneDrive/Documents/python-django-projects/steganography/camouflage/media/stego_video.mp4')

main()