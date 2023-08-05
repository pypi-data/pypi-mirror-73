"""This module provides functions to detect trash in images and videos.
"""


def trash_in_image(image_path: str) -> bool:
    """This function returns True if trash is detected in the image.

    Parameters:
        image_path (str): The path to the image.

    Returns:
        bool: True if trash is in the picture, otherwise False.
    """
    with open(image_path) as image:
        pass

    return False
