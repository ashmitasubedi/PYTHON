"""
face_duplicate_checker.py
─────────────────────────
Drop this file next to student.py and face_recognition.py.

Usage inside student.py  →  generate_dataset():

    from face_duplicate_checker import FaceDuplicateChecker

    checker = FaceDuplicateChecker(data_dir="data")
    is_dup, matched_id, dist = checker.is_duplicate_face(cap, cascade_path)

    if is_dup:
        messagebox.showerror(
            "Duplicate Face Detected",
            f"This face is already registered as Student ID: {matched_id}\\n"
            f"(Similarity distance: {dist:.1f})\\n\\n"
            "Use 'Update Photo Sample' to re-capture for that student.",
            parent=self.root
        )
        return
"""

import os
import cv2
import numpy as np
from typing import Optional


# ─────────────────────────────────────────────────────────────────
# Tunables
# ─────────────────────────────────────────────────────────────────
LBPH_DUP_THRESHOLD   = 60    # distance below this → treat as same person
FRAMES_TO_SCAN       = 30    # how many camera frames to inspect
FACE_RESIZE          = (200, 200)   # must match what you use when saving samples
MIN_FACE_SIZE        = (80, 80)


class FaceDuplicateChecker:
    """
    Detects whether a live face already exists in the 'data/' folder
    under ANY student ID — not just the one currently being registered.

    Algorithm
    ─────────
    1. Build a mini LBPH model from ALL existing face samples found in
       data/user.<id>.<n>.jpg  (one model, labels = int(student_id)).
    2. Open the camera and scan up to FRAMES_TO_SCAN frames.
    3. For each detected face, call clf.predict().
    4. If distance < LBPH_DUP_THRESHOLD  →  duplicate found.
    """

    def __init__(self, data_dir: str = "data", face_size: tuple = FACE_RESIZE):
        self.data_dir  = os.path.abspath(data_dir)
        self.face_size = face_size

    # ──────────────────────────────────────────────
    # PUBLIC API
    # ──────────────────────────────────────────────

    def is_duplicate_face(
        self,
        cap: cv2.VideoCapture,
        cascade_path: str,
        exclude_student_id: Optional[str] = None,
    ) -> tuple[bool, Optional[str], Optional[float]]:
        """
        Scan the live camera feed and decide whether this face already
        exists in the data/ folder.

        Parameters
        ──────────
        cap               : already-opened cv2.VideoCapture
        cascade_path      : path to haarcascade_frontalface_default.xml
        exclude_student_id: skip this student's own photos during the check
                            (useful when re-capturing / updating samples)

        Returns
        ───────
        (is_duplicate, matched_student_id, best_distance)
            is_duplicate        : True if a duplicate was found
            matched_student_id  : str ID of the matched student, or None
            best_distance       : lowest LBPH distance seen, or None
        """
        # ── 1. Load face samples from disk ──
        faces, labels, id_map = self._load_existing_faces(exclude_student_id)

        if len(faces) == 0:
            # No existing photos → cannot be a duplicate
            return False, None, None

        # ── 2. Train a temporary LBPH model on the existing photos ──
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, np.array(labels))

        # ── 3. Load cascade ──
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            print("[DupChecker] WARNING: cascade failed to load")
            return False, None, None

        # ── 4. Scan camera frames ──
        best_distance    : Optional[float] = None
        best_matched_id  : Optional[str]   = None
        frames_checked   = 0

        while frames_checked < FRAMES_TO_SCAN:
            ret, frame = cap.read()
            if not ret:
                break
            frames_checked += 1

            gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_detected = face_cascade.detectMultiScale(
                gray, 1.3, 5, minSize=MIN_FACE_SIZE
            )

            for (x, y, w, h) in faces_detected:
                roi        = gray[y:y + h, x:x + w]
                roi_resized = cv2.resize(roi, self.face_size)

                try:
                    numeric_label, distance = clf.predict(roi_resized)
                except cv2.error:
                    continue

                print(
                    f"[DupChecker] frame={frames_checked}  "
                    f"predicted_label={numeric_label}  distance={distance:.2f}"
                )

                # Track the closest match seen so far
                if best_distance is None or distance < best_distance:
                    best_distance   = distance
                    best_matched_id = id_map.get(numeric_label)

                # Early exit on high-confidence hit
                if distance < LBPH_DUP_THRESHOLD:
                    return True, id_map.get(numeric_label), distance

        # ── 5. After scanning all frames ──
        is_dup = (best_distance is not None) and (best_distance < LBPH_DUP_THRESHOLD)
        return is_dup, best_matched_id if is_dup else None, best_distance

    # ──────────────────────────────────────────────
    # PRIVATE HELPERS
    # ──────────────────────────────────────────────

    def _load_existing_faces(
        self, exclude_student_id: Optional[str]
    ) -> tuple[list, list, dict]:
        """
        Walk data/ and load every  user.<id>.<n>.jpg  image.

        Returns
        ───────
        faces   : list of np.ndarray  (grayscale, resized)
        labels  : list of int         (numeric label per sample)
        id_map  : {int_label: str_student_id}
        """
        faces   : list = []
        labels  : list = []
        id_map  : dict = {}
        label_counter = 0

        if not os.path.exists(self.data_dir):
            return faces, labels, id_map

        # Collect all student IDs that have photos
        student_ids_seen: dict[str, int] = {}  # str_id → int_label

        for filename in sorted(os.listdir(self.data_dir)):
            if not (filename.startswith("user.") and filename.endswith(".jpg")):
                continue

            parts = filename.split(".")
            if len(parts) < 3:
                continue

            student_id_str = parts[1]

            # Skip this student's own photos if requested
            if exclude_student_id and student_id_str == str(exclude_student_id):
                continue

            # Assign a stable integer label per student_id
            if student_id_str not in student_ids_seen:
                student_ids_seen[student_id_str] = label_counter
                id_map[label_counter]             = student_id_str
                label_counter += 1

            int_label = student_ids_seen[student_id_str]

            # Load and resize the image
            img_path = os.path.join(self.data_dir, filename)
            img      = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            img_resized = cv2.resize(img, self.face_size)
            faces.append(img_resized)
            labels.append(int_label)

        print(
            f"[DupChecker] Loaded {len(faces)} face samples "
            f"from {len(student_ids_seen)} student(s)"
        )
        return faces, labels, id_map