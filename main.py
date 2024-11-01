from src.ImageProcessor import ImageProcessor


def main() -> None:
    try:
        folder_path = input("Enter the path to the folder containing the images: ")
        processor = ImageProcessor(folder_path)

        new_size = int(input("Enter the new size for the images: "))
        processor.process_folder(new_size)
    except Exception as e:
        print("An error occurred: ", e)


if __name__ == "__main__":
    main()
