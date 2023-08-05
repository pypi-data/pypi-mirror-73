import os
import shutil
import re


def glob(d, regex):
    def has_match(s):
        if re.search(regex, s) is None:
            return False
        return True

    fs = os.listdir(d)
    fs = list(filter(has_match, fs))
    return [os.path.join(d, f) for f in fs]


def load_image():
    pass


def _write_image():
    pass


def write_file():
    pass


def write_images():
    pass


def create_reference_dir(src, dst):
    """Create directory.

        dst
        ├───Donald_Trump
        │       _reference.jpg
        │
        ├───Hillary_Clinton
        │       _reference.jpg
        │
        └───Bernie_Sanders
                _reference.jpg

    """
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.makedirs(dst)

    for i in os.listdir(src):
        image_name = os.path.splitext(i)[0]
        image_ext = os.path.splitext(i)[1]
        pdir = os.path.join(dst, image_name)
        os.makedirs(pdir)
        s = os.path.join(src, i)
        d = os.path.join(pdir, f"_reference{image_ext}")
        shutil.copy2(s, d)


def add_subdirectory(d, *args):
    [os.makedirs(os.path.join(d, arg)) for arg in args]
