import os
from datetime import datetime

from PIL import Image


class ImageProcessor:
    PADDING_COLOR = (114, 114, 114)

    def __init__(self, relative_path_image_folder: str):
        self.relative_path_image_folder = relative_path_image_folder
        if not os.path.exists(self.relative_path_image_folder):
            raise Exception("Folder does not exist...")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.output_folder = os.path.join("dataset", timestamp)
        os.makedirs(self.output_folder, exist_ok=True)

    @staticmethod
    def __get_dimensions(img: Image, new_size: int) -> tuple[int, int]:
        width, height = img.size
        ratio = width / height
        if width > height:
            new_width = new_size
            new_height = int(new_size / ratio)
        else:
            new_height = new_size
            new_width = int(new_size * ratio)
        return new_width, new_height

    def __add_padding(self, img: Image, new_size: int) -> Image:
        width, height = img.size

        if width == height:
            return img

        new_image = Image.new("RGB", (new_size, new_size), self.PADDING_COLOR)
        new_image.paste(img, (0, 0))
        return new_image

    def process_image(self, file_path: str, filename: str, new_size: int) -> None:
        """
            Resize and add padding to an image
        :param file_path:
        :param filename:
        :param new_size:
        :return:
        """
        with Image.open(file_path) as img:
            new_width, new_height = self.__get_dimensions(img, new_size)
            img = img.resize((new_width, new_height))
            img = self.__add_padding(img, new_size)
            output_path = os.path.join(self.output_folder, filename)
            img.save(output_path)

    def process_folder(self, new_size: int) -> None:
        """
            Process all images in the folder
        :param new_size: the new size for the images
        :return:
        """
        for filename in os.listdir(self.relative_path_image_folder):
            file_path = os.path.join(self.relative_path_image_folder, filename)
            if os.path.isfile(file_path):
                self.process_image(file_path, filename, new_size)
