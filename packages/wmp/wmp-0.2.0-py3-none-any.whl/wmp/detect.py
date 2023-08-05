import dlib
from PIL import Image, ImageDraw
import numpy as np
import shutil
import os
import pickle
from pkg_resources import resource_filename


# Trained facial shape predictor and recognition model from:

# http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
FACE_LANDMARKS_68 = resource_filename(
    __name__, "models/shape_predictor_68_face_landmarks.dat"
)

# http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat
FACE_RECOGNITION_MODEL = resource_filename(
    __name__, "models/dlib_face_recognition_resnet_model_v1.dat"
)

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(FACE_LANDMARKS_68)
facerec = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL)


class Box:
    def __init__(self, rect):
        self._rect = rect
        self.top = rect.top()
        self.left = rect.left()
        self.bottom = rect.bottom()
        self.right = rect.right()

    def __repr__(self):
        return (
            f"Box(top={self.top},left={self.left},"
            f"bottom={self.bottom},right={self.right})"
        )

    def check_bounds(self, img_shape):
        self.top = max(self.top, 0)
        self.left = max(self.left, 0)
        self.bottom = min(self.bottom, img_shape[0])
        self.right = min(self.right, img_shape[1])

    def rect(self):
        return self._rect


def find_landmarks():
    shape = sp(img, det_face)


class Face:
    # TODO: draw face landmarks
    def __init__(self, face_image, box):
        self.source_faceimage = face_image
        self.box = box
        self.source_name = self.source_faceimage.source_name
        self.thumbnail_image = self._crop_face()
        self.landmarks = self._find_landmarks()
        self.thumbnail_landmarks = None
        self.encoding = self._encode_face()
        self.true_name = None
        self.comparison = None

    def __repr__(self):
        return f"Face(source_name={self.source_name}," f"box={self.box})"

    def _crop_face(self, pad_perc=None):
        thumb_array = self.source_faceimage.image_data[
            self.box.top : self.box.bottom, self.box.left : self.box.right
        ]
        return Image.fromarray(thumb_array)

    def _find_landmarks(self):
        return sp(self.source_faceimage.image_data, self.box.rect())

    def _encode_face(self):
        encoding = facerec.compute_face_descriptor(
            self.source_faceimage.image_data, self.landmarks
        )
        return np.array(encoding)

    def draw_landmarks(self):
        pass
        # draw = ImageDraw.Draw(self.thumbnail_image)
        # draw.point()

    def assign_name(self):
        f = os.path.split(self.source_name)[1]
        root = os.path.splitext(f)[0]
        self.true_name = root
        return root


class FaceImage:
    def __init__(self, img_location, vid_frame=None):
        self.source_name = img_location
        self.image_data = self.read_image() if vid_frame is None else vid_frame
        self.faces = []
        self.true_names = None
        self.comparison_names = None

    def __repr__(self):
        return f"FaceImage(source_name={source_name})"

    def read_image(self):
        ext = os.path.splitext(self.source_name)[-1]
        image = Image.open(self.source_name)
        if ext == ".jpg":
            return np.array(image)
        elif ext == ".png":
            base = Image.new("RGB", image.size, "white")
            image = Image.composite(image, base, image)
            return np.array(image)

        raise ValueError("Image isn't JPG or PNG")

    def retrieve_names(self):
        names = [f.true_name for f in self.faces]
        self.true_names = names
        return self.true_names

    def retrieve_comparisons(self):
        comparisons = np.vstack([f.comparison for f in self.faces])
        return self.comparison_names, comparisons

    def write_faces(self, outdir, marked=False, named=False):
        if os.path.exists(outdir):
            shutil.rmtree(outdir)

        os.makedirs(outdir)

        if marked:
            for i, face in enumerate(self.faces):
                n = i if face.true_name is None else face.true_name
                fp = os.path.join(outdir, f"{n}.jpg")
                face.landmarks.save(fp)
        else:
            for i, face in enumerate(self.faces):
                n = i if face.true_name is None else face.true_name
                fp = os.path.join(outdir, f"{n}.jpg")
                face.thumbnail_image.save(fp)


class FaceVideo:
    def __init__(self):
        pass


class FaceBatch:
    def __init__(self, faces, is_reference=False):
        self.batch_faces = faces
        self.true_names = None
        self.encodings = None
        self.make_reference() if is_reference else None

    def __repr__(self):
        return f"FaceBatch(true_names={true_names})"

    def make_reference(self):
        es = [f.encoding for f in self.batch_faces]
        self.true_names = [f.assign_name() for f in self.batch_faces]
        self.encodings = np.stack(es, axis=0)


class FaceDetector:
    def __init__(self):
        pass

    def find_faces(self, face_image: FaceImage):
        det_rects = detector(face_image.image_data, 1)
        boxes = [Box(d) for d in det_rects]
        faces = [Face(face_image, b) for b in boxes]
        face_image.faces = faces
        return face_image


class FaceRecognizer(FaceBatch):
    def __init__(self, reference_folder, comparison_threshold=0.6):
        self.reference_folder = reference_folder
        self.comparison_threshold = comparison_threshold
        super().__init__(self._open_reference_folder(), is_reference=True)

    def __repr__(self):
        return (
            f"FaceRecognizer(reference_folder={self.reference_folder},"
            f"true_names={self.true_names})"
        )

    def _open_reference_folder(self):
        ref_fp = os.path.join(self.reference_folder, "reference_batch.p")
        with open(ref_fp, "rb") as f:
            ref_b = pickle.load(f)
        return ref_b.batch_faces

    def predict_name(self, face: Face, store_comparisons=False):
        """Finds name given a `Face` object"""

        f_enc = np.repeat(face.encoding[np.newaxis, :], len(self.true_names), axis=0)
        distance = np.linalg.norm(f_enc - self.encodings, axis=1)  # (4,)
        name_idxs, *_ = np.where(distance < self.comparison_threshold)

        if len(name_idxs) == 0:
            face.true_name = "Unknown"
        elif len(name_idxs) == 1:
            face.true_name = self.true_names[name_idxs[0]]
        else:
            # Multiple people match below threshold
            face.true_name = self.true_names[np.argmin(distance)]

        if store_comparisons:
            face.comparison = distance

        return face

    def predict_names(self, faceimage: FaceImage, store_comparisons=False):
        [
            self.predict_name(f, store_comparisons=store_comparisons)
            for f in faceimage.faces
        ]
        if store_comparisons:
            faceimage.comparison_names = self.true_names

        return faceimage

    def write_validation(self, images, outdir):
        if os.path.exists(outdir):
            shutil.rmtree(outdir)

        shutil.copytree(self.reference_folder, outdir)

        for image in images:
            if len(image.faces) == 0:
                fp = os.path.split(image.source_name)[-1]
                fp = os.path.join(outdir, "No_Person", fp)
                shutil.copy2(image.source_name, fp)

            for i, face in enumerate(image.faces):
                sname = os.path.split(face.source_name)[-1]
                sname = os.path.splitext(sname)[0]
                fp = os.path.join(outdir, face.true_name, f"{sname}_{i}.jpg")
                face.thumbnail_image.save(fp)


class FaceValidator:
    def __init__(self):
        pass

    def write_prediction(self):
        pass
