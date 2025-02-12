from enum import Enum
import os

current_directory = os.getcwd()


class PathEnums(Enum):
    facetemplate = os.path.join(current_directory, "templates/face.html")
    # print(facetemplate)  # Output: /path/to/face_recognition2/templates/face.html
