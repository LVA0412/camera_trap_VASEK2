# Pillow-SIMD намного быстрее чем Pillow.
# Для ускорения работы можно удалить Pillow и установить Pillow-SIMD
# при этом изменять в коде ничего не надо!
# https://github.com/uploadcare/pillow-simd

import argparse
from PIL import Image as ImagePIL
import os
import cv2


def arg_parser():
    epilog_text = """
    Детальное описание параметров
    здесь
    """

    parser = argparse.ArgumentParser(description='Определение дефектных фото', epilog=epilog_text)
    parser.add_argument('srcpath', metavar='SOURCE_PATH', type=str,
                        help='Путь к папке - источнику изображений')
    parser.add_argument('targetpath', metavar='TARGET_PATH', type=str,
                        help='Путь к целевой папке найденных (дефектных) изображений')
    parser.add_argument("-tb", "--threshold_blur", type=float, default=250.0,
                        help="Порог 'размытости' изображений (по умолчанию = 250.0)")
 
    return parser.parse_args()

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def main():
    global ARG

    ARG = arg_parser()
    
    # TODO добавить проверку на версию Pillow
    print("Recommended installing Pillow-SIMD to speed up")

   
    for root, dirs, files in os.walk(ARG.srcpath):
        path = root.split(os.sep)
        print((len(path) - 1) * '--', os.path.basename(root))
        for file in files:
            print(len(path) * '--', file) 
            full_filename = os.path.join(root, file)
            # TODO перенести в отдельную ф-ю
            image = cv2.imread(full_filename)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = variance_of_laplacian(gray)
            text = "Not Blurry"
            if fm < ARG.threshold_blur:
                text = "Blurry"
            cv2.putText(image, "{}: {:.2f}".format(text, fm), (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            #cv2.imshow("Image", image) # показать на экране
            cv2.imwrite(os.path.join(ARG.targetpath, file), image)
        
    print("Press any key to continue")
    key = cv2.waitKey(0)

    # TODO отделить только картинки, т.к. могут быть другие файлы
    # TODO определить кол-во картинок
           
if __name__ == "__main__":
    main()
