
# Camouflage - Video Steganography

The Camouflage project is a steganography tool, where user is able to encode and decode their secret message into a video. This tool can be used for securely communicating with each other without any other third party knowing what the information has been sent. The conversation can be camouflaged as a normal video sending between two users with an alternative motive of sending hidden text messages. This system can also be used for copyright claims of YouTube videos.





## Installation

First clone the project 

```bash
  git clone https://github.com/whyme-duh/video-steganography.git
```

Go the project directory, then install the requirements.txt file

```bash
  pip install -r requirements.txt
```
In the camouflage folder, you can see manage.py file. First, you need to migrate, in order to that follow this:
```bash
  python manage.py makemigrations
  python manage.py migrate
```

Before running the app, few folders must be created. Inside media folder, created three folders: encoded, decoded and videos. Inside encoded folder create another folder called "image_encode." The overall file structure should look like this.

```bash
media/
├── decoded/
├── encoded/
│ └── image_encode
├── images/
├── icons/
└── videos/
```
Then you can run the website by using following command.

```bash
  python manage.py runserver
```

## Images

![Images](media\icons\camouflage.png?raw=true "Title")