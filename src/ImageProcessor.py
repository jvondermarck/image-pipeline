import os
from datetime import datetime

from PIL import Image


class ImageProcessor:
    PADDING_COLOR = (114, 114, 114)
    OUTPUT_FOLDER = "dataset"
    DATETIME_FORMAT = "%Y%m%d%H%M%S"

    def __init__(self, relative_path_image_folder: str) -> None:
        if not os.path.exists(relative_path_image_folder):
            raise Exception("Folder does not exist...")

        self.relative_path_image_folder = relative_path_image_folder
        self.output_folder_path = self._generate_output_folder(
            self.output_dataset_folder_name
        )

    @property
    def output_dataset_folder_name(self) -> str:
        return datetime.now().strftime(self.DATETIME_FORMAT)

    def _generate_output_folder(self, folder_name) -> str:
        folder_path = os.path.join(self.OUTPUT_FOLDER, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    @staticmethod
    def _get_dimensions(img: Image, new_size: int) -> tuple[int, int]:
        width, height = img.size
        ratio = width / height
        if width > height:
            new_width = new_size
            new_height = int(new_size / ratio)
        else:
            new_height = new_size
            new_width = int(new_size * ratio)
        return new_width, new_height

    def _add_padding(self, img: Image, new_size: int) -> Image:
        width, height = img.size

        if width == height:
            return img

        new_image = Image.new("RGB", (new_size, new_size), self.PADDING_COLOR)
        new_image.paste(img, (0, 0))
        return new_image

    def process_image(self, file_path: str, filename: str, new_size: int) -> None:
        """
        Resize and add padding to an image

        :param file_path: the path to the image
        :param filename: the name of the image
        :param new_size: the new size for the image
        :return: None
        """
        try:
            with Image.open(file_path) as img:
                new_width, new_height = self._get_dimensions(img, new_size)
                img = img.resize((new_width, new_height))
                img = self._add_padding(img, new_size)
                output_path = os.path.join(self.output_folder_path, filename)
                img.save(output_path)
        except Exception as e:
            print(f"An unexpected error occurred while processing '{filename}': {e}")

    def process_folder(self, new_size: int) -> None:
        """
        Process all images in the folder

        :param new_size: the new size for the images
        :return: None
        """
        for filename in os.listdir(self.relative_path_image_folder):
            file_path = os.path.join(self.relative_path_image_folder, filename)
            if os.path.isfile(file_path):
                self.process_image(file_path, filename, new_size)
