from rhme.api import *
from rhme.config import Configuration
from rhme.helpers.exceptions import *
import base64
import numpy as np
import cv2

configs = Configuration()

class Example:

    def __init__(self):
        hme_recognizer = HME_Recognizer()

        images = [configs.package_path + '/images/validacao/nao/30.png']

        expression = ""

        for image in images:
            try:
                hme_recognizer.load_image(image,'path')
                expression, img = hme_recognizer.recognize()

            except (GrammarError, SintaticError, LexicalError) as e:
                if 'latex_string_original' in e.data:
                    expression = e.data['latex_string_original']

            print("\nExpressão: ", expression)
            print(hme_recognizer.get_lex_errors())
            print(hme_recognizer.get_yacc_errors())
Example()
