import argparse
import csv
import dataclasses
import enum
import logging
import os
import shutil
import typing
import tqdm


logging.basicConfig(filename='img_distributer.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ImageType(enum.Enum):
    BROKEN = 'broken'
    EMPTY = 'empty'
    ANIMAL = 'animal'


@dataclasses.dataclass
class Classification:
    img_path: str
    type: ImageType


def read_images_classification(classification_file) -> typing.Iterable[Classification]:
    TYPE_BY_ACTIVE_COLUMN = {
        1: ImageType.BROKEN,
        2: ImageType.EMPTY,
        3: ImageType.ANIMAL,
    }
    with open(classification_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            try:
                active_column = next(i for i in range(1, 4) if row[i] == '1')
                image_type = TYPE_BY_ACTIVE_COLUMN[active_column]
                yield Classification(row[0], image_type)
            except Exception as ex:
                logger.info(f'Пропущен некорректный файл {" ".join(row)} ; ошибка: {str(ex)}')


TYPE_DIRS = {
    ImageType.BROKEN: 'broken',
    ImageType.EMPTY: 'empty',
    ImageType.ANIMAL: 'animal',
}


def make_result_subdirs(result_dir: str, head: str):
    for type_dir in TYPE_DIRS.values():
        os.makedirs(os.path.join(result_dir, head, type_dir), exist_ok=True)


def distribute_pictures(args):
    classification_file = args.classification

    if args.source:
        source_head = args.source
    else:
        source_head, _ = os.path.split(classification_file)
        if not source_head:
            source_head = './'  # текущая директория
    result_dir = args.result
    dirs_created: typing.Set[str] = set()
    classifications = [c for c in read_images_classification(classification_file)]
    for classification in tqdm.tqdm(classifications):
        head, tail = os.path.split(classification.img_path)
        if os.path.isabs(head):
            print(f'Путь к изображению должен быть относительным, изображение {classification.img_path} пропущено')
            continue
        if head not in dirs_created:
            make_result_subdirs(result_dir, head)
            dirs_created.add(head)
        source_img_path = os.path.join(source_head, classification.img_path)
        try:
            shutil.copy(source_img_path, os.path.join(result_dir, head, TYPE_DIRS[classification.type]))
            logger.info('Изображение %s успешно скопировано', classification.img_path)
        except Exception as ex:
            logger.info(f'Изображение {classification.img_path} пропущено: файл не найден по пути {source_img_path}, детали ошибки: {ex}')


parser = argparse.ArgumentParser(
    description='Применить полученную детектором '  
                'классификацию для распределения картинок по поддиректориям'
)
parser.add_argument('classification', type=str, help='Путь к файлу классификации в формате csv')
parser.add_argument('result', type=str, help='Путь к корневой папке результата')
parser.add_argument('-s', '--source', type=str, required=False, help='Путь к корневой папке исходных изображений (по умолчанию совпадает с расположением файла классификации)')

args = parser.parse_args()
distribute_pictures(args)
