"""Unit-tests for kestrel
"""

import kestrel
import os
import pytest


def _generate_image_path(image_name):
    return os.path.join("resources/", image_name)


def test_that_trash_in_image_raises_exception_with_invalid_image_path():
    with pytest.raises(FileNotFoundError):
        invalid_image_path = "invalid-path"
        kestrel.trash_in_image(invalid_image_path)


def test_that_trash_in_image_detects_trash_in_image():
    image_with_trash_path = _generate_image_path("plastic-bottle-in-grass.jpg")

    assert kestrel.trash_in_image(image_with_trash_path)


def test_that_trash_in_image_detects_no_trash_in_image():
    image_without_trash_path = _generate_image_path("just-grass.jpg")

    assert kestrel.trash_in_image(image_without_trash_path) == False
