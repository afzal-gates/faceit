"""
Data definitions for manual landmark picker feature.
Provides standard facial landmark labels and utility functions.
"""

# Standard facial landmark labels based on common face tracking systems
MANUAL_LANDMARK_LABELS = [
    # Face Outline (17 points)
    ("face_outline_0", "Face Outline 0 (Chin Center)"),
    ("face_outline_1", "Face Outline 1 (Jaw Right)"),
    ("face_outline_2", "Face Outline 2 (Jaw Right)"),
    ("face_outline_3", "Face Outline 3 (Jaw Right)"),
    ("face_outline_4", "Face Outline 4 (Jaw Right)"),
    ("face_outline_5", "Face Outline 5 (Jaw Right)"),
    ("face_outline_6", "Face Outline 6 (Jaw Right)"),
    ("face_outline_7", "Face Outline 7 (Jaw Right)"),
    ("face_outline_8", "Face Outline 8 (Jaw Right)"),
    ("face_outline_9", "Face Outline 9 (Jaw Left)"),
    ("face_outline_10", "Face Outline 10 (Jaw Left)"),
    ("face_outline_11", "Face Outline 11 (Jaw Left)"),
    ("face_outline_12", "Face Outline 12 (Jaw Left)"),
    ("face_outline_13", "Face Outline 13 (Jaw Left)"),
    ("face_outline_14", "Face Outline 14 (Jaw Left)"),
    ("face_outline_15", "Face Outline 15 (Jaw Left)"),
    ("face_outline_16", "Face Outline 16 (Jaw Left)"),

    # Left Eyebrow (5 points)
    ("left_eyebrow_outer", "Left Eyebrow Outer"),
    ("left_eyebrow_outer_mid", "Left Eyebrow Outer Mid"),
    ("left_eyebrow_center", "Left Eyebrow Center"),
    ("left_eyebrow_inner_mid", "Left Eyebrow Inner Mid"),
    ("left_eyebrow_inner", "Left Eyebrow Inner"),

    # Right Eyebrow (5 points)
    ("right_eyebrow_inner", "Right Eyebrow Inner"),
    ("right_eyebrow_inner_mid", "Right Eyebrow Inner Mid"),
    ("right_eyebrow_center", "Right Eyebrow Center"),
    ("right_eyebrow_outer_mid", "Right Eyebrow Outer Mid"),
    ("right_eyebrow_outer", "Right Eyebrow Outer"),

    # Nose Bridge (4 points)
    ("nose_bridge_top", "Nose Bridge Top"),
    ("nose_bridge_mid", "Nose Bridge Mid"),
    ("nose_bridge_low", "Nose Bridge Low"),
    ("nose_tip", "Nose Tip"),

    # Nose Bottom (5 points)
    ("nose_bottom_left", "Nose Bottom Left"),
    ("nose_bottom_left_mid", "Nose Bottom Left Mid"),
    ("nose_bottom_center", "Nose Bottom Center"),
    ("nose_bottom_right_mid", "Nose Bottom Right Mid"),
    ("nose_bottom_right", "Nose Bottom Right"),

    # Left Eye (6 points)
    ("left_eye_outer", "Left Eye Outer Corner"),
    ("left_eye_top_outer", "Left Eye Top Outer"),
    ("left_eye_top_inner", "Left Eye Top Inner"),
    ("left_eye_inner", "Left Eye Inner Corner"),
    ("left_eye_bottom_inner", "Left Eye Bottom Inner"),
    ("left_eye_bottom_outer", "Left Eye Bottom Outer"),

    # Right Eye (6 points)
    ("right_eye_inner", "Right Eye Inner Corner"),
    ("right_eye_top_inner", "Right Eye Top Inner"),
    ("right_eye_top_outer", "Right Eye Top Outer"),
    ("right_eye_outer", "Right Eye Outer Corner"),
    ("right_eye_bottom_outer", "Right Eye Bottom Outer"),
    ("right_eye_bottom_inner", "Right Eye Bottom Inner"),

    # Mouth Outer (12 points)
    ("mouth_left_corner", "Mouth Left Corner"),
    ("mouth_upper_left_outer", "Mouth Upper Left Outer"),
    ("mouth_upper_left_mid", "Mouth Upper Left Mid"),
    ("mouth_upper_center", "Mouth Upper Center (Cupid's Bow)"),
    ("mouth_upper_right_mid", "Mouth Upper Right Mid"),
    ("mouth_upper_right_outer", "Mouth Upper Right Outer"),
    ("mouth_right_corner", "Mouth Right Corner"),
    ("mouth_lower_right_outer", "Mouth Lower Right Outer"),
    ("mouth_lower_right_mid", "Mouth Lower Right Mid"),
    ("mouth_lower_center", "Mouth Lower Center"),
    ("mouth_lower_left_mid", "Mouth Lower Left Mid"),
    ("mouth_lower_left_outer", "Mouth Lower Left Outer"),

    # Mouth Inner (8 points)
    ("mouth_inner_left", "Mouth Inner Left"),
    ("mouth_inner_upper_left", "Mouth Inner Upper Left"),
    ("mouth_inner_upper_center", "Mouth Inner Upper Center"),
    ("mouth_inner_upper_right", "Mouth Inner Upper Right"),
    ("mouth_inner_right", "Mouth Inner Right"),
    ("mouth_inner_lower_right", "Mouth Inner Lower Right"),
    ("mouth_inner_lower_center", "Mouth Inner Lower Center"),
    ("mouth_inner_lower_left", "Mouth Inner Lower Left"),

    # Teeth (2 points)
    ("teeth_upper", "Upper Teeth"),
    ("teeth_lower", "Lower Teeth"),

    # Tongue (3 points)
    ("tongue_tip", "Tongue Tip"),
    ("tongue_center", "Tongue Center"),
    ("tongue_back", "Tongue Back"),

    # Left Ear (6 points)
    ("left_ear_top", "Left Ear Top"),
    ("left_ear_helix", "Left Ear Helix (Outer Rim)"),
    ("left_ear_middle", "Left Ear Middle"),
    ("left_ear_tragus", "Left Ear Tragus (Front)"),
    ("left_ear_lobe_bottom", "Left Ear Lobe Bottom"),
    ("left_ear_lobe_attach", "Left Ear Lobe Attachment"),

    # Right Ear (6 points)
    ("right_ear_top", "Right Ear Top"),
    ("right_ear_helix", "Right Ear Helix (Outer Rim)"),
    ("right_ear_middle", "Right Ear Middle"),
    ("right_ear_tragus", "Right Ear Tragus (Front)"),
    ("right_ear_lobe_bottom", "Right Ear Lobe Bottom"),
    ("right_ear_lobe_attach", "Right Ear Lobe Attachment"),
]


def get_landmark_categories():
    """
    Returns landmark categories for organized UI display.
    Returns dict with category name as key and list of landmark identifiers as value.
    """
    categories = {
        "Face Outline": [lm[0] for lm in MANUAL_LANDMARK_LABELS if lm[0].startswith("face_outline")],
        "Eyebrows": [lm[0] for lm in MANUAL_LANDMARK_LABELS if "eyebrow" in lm[0]],
        "Eyes": [lm[0] for lm in MANUAL_LANDMARK_LABELS if "eye" in lm[0] and "eyebrow" not in lm[0]],
        "Nose": [lm[0] for lm in MANUAL_LANDMARK_LABELS if "nose" in lm[0]],
        "Mouth": [lm[0] for lm in MANUAL_LANDMARK_LABELS if "mouth" in lm[0]],
        "Teeth": [lm[0] for lm in MANUAL_LANDMARK_LABELS if "teeth" in lm[0]],
        "Tongue": [lm[0] for lm in MANUAL_LANDMARK_LABELS if "tongue" in lm[0]],
        "Ears": [lm[0] for lm in MANUAL_LANDMARK_LABELS if "ear" in lm[0]],
    }
    return categories


def get_landmark_label_dict():
    """Returns a dictionary mapping landmark identifiers to their display names."""
    return {lm[0]: lm[1] for lm in MANUAL_LANDMARK_LABELS}


def get_landmark_enum_items():
    """Returns landmark labels as enum items for Blender properties."""
    return [(lm[0], lm[1], lm[1]) for lm in MANUAL_LANDMARK_LABELS]


def get_landmark_mirror_map():
    """
    Returns a dictionary mapping landmark IDs to their mirrored counterparts.
    Returns None for landmarks that don't have a mirror (e.g., center points).
    """
    mirror_map = {}

    # Face outline mirrors (0=center, 1-8 right side, 9-16 left side)
    mirror_map["face_outline_0"] = None  # Center, no mirror
    for i in range(1, 9):
        mirror_map[f"face_outline_{i}"] = f"face_outline_{17-i}"
        mirror_map[f"face_outline_{17-i}"] = f"face_outline_{i}"

    # Eyebrow mirrors
    left_eyebrow_landmarks = ["left_eyebrow_outer", "left_eyebrow_outer_mid", "left_eyebrow_center",
                              "left_eyebrow_inner_mid", "left_eyebrow_inner"]
    right_eyebrow_landmarks = ["right_eyebrow_outer", "right_eyebrow_outer_mid", "right_eyebrow_center",
                               "right_eyebrow_inner_mid", "right_eyebrow_inner"]

    for left, right in zip(left_eyebrow_landmarks, right_eyebrow_landmarks):
        mirror_map[left] = right
        mirror_map[right] = left

    # Eye mirrors
    left_eye_landmarks = ["left_eye_outer", "left_eye_top_outer", "left_eye_top_inner",
                         "left_eye_inner", "left_eye_bottom_inner", "left_eye_bottom_outer"]
    right_eye_landmarks = ["right_eye_outer", "right_eye_top_outer", "right_eye_top_inner",
                          "right_eye_inner", "right_eye_bottom_inner", "right_eye_bottom_outer"]

    for left, right in zip(left_eye_landmarks, right_eye_landmarks):
        mirror_map[left] = right
        mirror_map[right] = left

    # Nose mirrors (center points have no mirror)
    mirror_map["nose_bridge_top"] = None
    mirror_map["nose_bridge_mid"] = None
    mirror_map["nose_bridge_low"] = None
    mirror_map["nose_tip"] = None
    mirror_map["nose_bottom_center"] = None

    # Nose bottom left/right
    mirror_map["nose_bottom_left"] = "nose_bottom_right"
    mirror_map["nose_bottom_right"] = "nose_bottom_left"
    mirror_map["nose_bottom_left_mid"] = "nose_bottom_right_mid"
    mirror_map["nose_bottom_right_mid"] = "nose_bottom_left_mid"

    # Mouth outer mirrors
    mirror_map["mouth_left_corner"] = "mouth_right_corner"
    mirror_map["mouth_right_corner"] = "mouth_left_corner"
    mirror_map["mouth_upper_left_outer"] = "mouth_upper_right_outer"
    mirror_map["mouth_upper_right_outer"] = "mouth_upper_left_outer"
    mirror_map["mouth_upper_left_mid"] = "mouth_upper_right_mid"
    mirror_map["mouth_upper_right_mid"] = "mouth_upper_left_mid"
    mirror_map["mouth_upper_center"] = None  # Center
    mirror_map["mouth_lower_left_outer"] = "mouth_lower_right_outer"
    mirror_map["mouth_lower_right_outer"] = "mouth_lower_left_outer"
    mirror_map["mouth_lower_left_mid"] = "mouth_lower_right_mid"
    mirror_map["mouth_lower_right_mid"] = "mouth_lower_left_mid"
    mirror_map["mouth_lower_center"] = None  # Center

    # Mouth inner mirrors
    mirror_map["mouth_inner_left"] = "mouth_inner_right"
    mirror_map["mouth_inner_right"] = "mouth_inner_left"
    mirror_map["mouth_inner_upper_left"] = "mouth_inner_upper_right"
    mirror_map["mouth_inner_upper_right"] = "mouth_inner_upper_left"
    mirror_map["mouth_inner_upper_center"] = None  # Center
    mirror_map["mouth_inner_lower_left"] = "mouth_inner_lower_right"
    mirror_map["mouth_inner_lower_right"] = "mouth_inner_lower_left"
    mirror_map["mouth_inner_lower_center"] = None  # Center

    # Teeth mirrors (center landmarks, no mirroring)
    mirror_map["teeth_upper"] = None  # Center
    mirror_map["teeth_lower"] = None  # Center

    # Tongue mirrors (all center landmarks, no mirroring)
    mirror_map["tongue_tip"] = None  # Center
    mirror_map["tongue_center"] = None  # Center
    mirror_map["tongue_back"] = None  # Center

    # Ear mirrors
    left_ear_landmarks = ["left_ear_top", "left_ear_helix", "left_ear_middle",
                         "left_ear_tragus", "left_ear_lobe_bottom", "left_ear_lobe_attach"]
    right_ear_landmarks = ["right_ear_top", "right_ear_helix", "right_ear_middle",
                          "right_ear_tragus", "right_ear_lobe_bottom", "right_ear_lobe_attach"]

    for left, right in zip(left_ear_landmarks, right_ear_landmarks):
        mirror_map[left] = right
        mirror_map[right] = left

    return mirror_map
