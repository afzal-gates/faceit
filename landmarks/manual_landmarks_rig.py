"""
Rig generation from manual landmarks.
Maps manual landmark IDs to FaceIt rig system and generates facial rig.
"""

import bpy
from mathutils import Vector


def get_manual_to_faceit_landmark_mapping():
    """
    Maps manual landmark IDs to FaceIt facial_landmarks vertex indices.
    FaceIt uses indexed vertices (0-71 for face, 100+ for special points).
    """
    mapping = {
        # Face Outline (17 points) → FaceIt landmarks 0-16
        "face_outline_0": 0,   # Chin center
        "face_outline_1": 2,   # Jaw right start
        "face_outline_2": 3,
        "face_outline_3": 4,
        "face_outline_4": 20,
        "face_outline_5": 19,
        "face_outline_6": 24,
        "face_outline_7": 60,
        "face_outline_8": 59,  # Top right
        "face_outline_9": 67,  # Top left
        "face_outline_10": 66,
        "face_outline_11": 25,
        "face_outline_12": 12,
        "face_outline_13": 5,
        "face_outline_14": 1,
        "face_outline_15": 10,
        "face_outline_16": 11,  # Jaw left end

        # Right Eyebrow (5 points) → FaceIt landmarks 48, 50, 51, 53, 55 (mirrored)
        "right_eyebrow_inner": 51,
        "right_eyebrow_inner_mid": 55,
        "right_eyebrow_center": 64,
        "right_eyebrow_outer_mid": 58,
        "right_eyebrow_outer": 50,

        # Left Eyebrow (5 points) → FaceIt landmarks 47, 52, 54, 56, 49
        "left_eyebrow_outer": 49,
        "left_eyebrow_outer_mid": 57,
        "left_eyebrow_center": 63,
        "left_eyebrow_inner_mid": 56,
        "left_eyebrow_inner": 52,

        # Nose (9 points) → FaceIt landmarks for nose
        "nose_bridge_top": 36,      # Nose bridge top
        "nose_bridge_mid": 21,       # Nose bridge mid
        "nose_bridge_low": 103,      # Nose bridge low
        "nose_tip": 105,             # Nose tip
        "nose_bottom_left": 17,      # Nose wing left
        "nose_bottom_left_mid": 26,  # Nose side left
        "nose_bottom_center": 14,    # Nose bottom center
        "nose_bottom_right_mid": 27, # Nose side right
        "nose_bottom_right": 18,     # Nose wing right

        # Left Eye (6 points) → FaceIt landmarks for left eye
        "left_eye_outer": 32,             # Left eye outer corner
        "left_eye_top_outer": 34,         # Left eye top outer
        "left_eye_top_inner": 37,         # Left eye top inner
        "left_eye_inner": 41,             # Left eye inner corner
        "left_eye_bottom_inner": 44,      # Left eye bottom inner
        "left_eye_bottom_outer": 30,      # Left eye bottom outer

        # Right Eye (6 points) → FaceIt landmarks for right eye
        "right_eye_inner": 42,            # Right eye inner corner
        "right_eye_top_inner": 38,        # Right eye top inner
        "right_eye_top_outer": 35,        # Right eye top outer
        "right_eye_outer": 33,            # Right eye outer corner
        "right_eye_bottom_outer": 31,     # Right eye bottom outer
        "right_eye_bottom_inner": 43,     # Right eye bottom inner

        # Mouth Outer (12 points) → FaceIt landmarks for mouth
        "mouth_left_corner": 12,          # Mouth left corner (lips.L)
        "mouth_upper_left_outer": 11,     # Upper lip left outer
        "mouth_upper_left_mid": 10,       # Upper lip left mid
        "mouth_upper_center": 9,          # Upper lip center (cupid's bow)
        "mouth_upper_right_mid": 8,       # Upper lip right mid
        "mouth_upper_right_outer": 7,     # Upper lip right outer
        "mouth_right_corner": 13,         # Mouth right corner (lips.R)
        "mouth_lower_right_outer": 8,     # Lower lip right outer
        "mouth_lower_right_mid": 2,       # Lower lip right mid
        "mouth_lower_center": 6,          # Lower lip center
        "mouth_lower_left_mid": 3,        # Lower lip left mid
        "mouth_lower_left_outer": 7,      # Lower lip left outer

        # Mouth Inner (8 points) - use similar to outer for approximation
        "mouth_inner_left": 12,
        "mouth_inner_upper_left": 11,
        "mouth_inner_upper_center": 9,
        "mouth_inner_upper_right": 8,
        "mouth_inner_right": 13,
        "mouth_inner_lower_right": 8,
        "mouth_inner_lower_center": 6,
        "mouth_inner_lower_left": 7,

        # Teeth (2 points) → FaceIt special landmarks 106-107
        "teeth_upper": 106,
        "teeth_lower": 107,

        # Tongue (3 points) → FaceIt special landmarks 112-114
        "tongue_tip": 112,
        "tongue_center": 113,
        "tongue_back": 114,

        # Ears (12 points) → FaceIt special landmark 116
        # FaceIt has limited ear support, map all to general ear position
        "left_ear_top": 116,
        "left_ear_helix": 116,
        "left_ear_middle": 116,
        "left_ear_tragus": 116,
        "left_ear_lobe_bottom": 116,
        "left_ear_lobe_attach": 116,
        "right_ear_top": 116,
        "right_ear_helix": 116,
        "right_ear_middle": 116,
        "right_ear_tragus": 116,
        "right_ear_lobe_bottom": 116,
        "right_ear_lobe_attach": 116,

        # Special landmarks for eyes and jaw
        # These will be computed from existing landmarks
    }

    return mapping


def create_faceit_landmarks_from_manual(context):
    """
    Creates a 'facial_landmarks' object from manual landmarks.
    This allows using the existing FaceIt rig generation system.

    Returns the created landmarks object or None if insufficient data.
    """
    scene = context.scene
    manual_landmarks = scene.faceit_manual_landmarks

    if not manual_landmarks:
        return None

    # Check if we have the target mesh
    target_mesh = scene.faceit_manual_landmarks_target_mesh
    if not target_mesh:
        return None

    # Get mapping
    mapping = get_manual_to_faceit_landmark_mapping()

    # Create vertex positions dictionary
    # FaceIt expects vertices at indices 0-71, plus special points at 100+
    vertex_positions = {}

    # Collect manual landmark positions
    for lm in manual_landmarks:
        if not lm.is_set:
            continue

        # Get the mesh object
        mesh_obj = bpy.data.objects.get(lm.object_name)
        if not mesh_obj or mesh_obj.type != 'MESH':
            continue

        # Get vertex world position
        mesh = mesh_obj.data
        if lm.vertex_index < 0 or lm.vertex_index >= len(mesh.vertices):
            continue

        vertex = mesh.vertices[lm.vertex_index]
        world_pos = mesh_obj.matrix_world @ vertex.co

        # Map to FaceIt landmark index
        faceit_index = mapping.get(lm.landmark_id)
        if faceit_index is not None:
            # Store position (multiple manual landmarks may map to same faceit index)
            # Use average if multiple map to same index
            if faceit_index in vertex_positions:
                # Average the positions
                existing_pos = vertex_positions[faceit_index]
                vertex_positions[faceit_index] = (existing_pos + world_pos) / 2
            else:
                vertex_positions[faceit_index] = world_pos

    # Check if we have enough landmarks
    if len(vertex_positions) < 30:  # Minimum required landmarks
        return None

    # Calculate special landmark positions (eyes, jaw)
    # Eye positions (101 = left eye center, 111 = right eye center)
    left_eye_landmarks = ["left_eye_outer", "left_eye_top_outer", "left_eye_top_inner",
                         "left_eye_inner", "left_eye_bottom_inner", "left_eye_bottom_outer"]
    right_eye_landmarks = ["right_eye_outer", "right_eye_top_outer", "right_eye_top_inner",
                          "right_eye_inner", "right_eye_bottom_inner", "right_eye_bottom_outer"]

    # Calculate left eye center (landmark 101)
    left_eye_positions = []
    for lm_id in left_eye_landmarks:
        for lm in manual_landmarks:
            if lm.landmark_id == lm_id and lm.is_set:
                mesh_obj = bpy.data.objects.get(lm.object_name)
                if mesh_obj:
                    mesh = mesh_obj.data
                    if lm.vertex_index < len(mesh.vertices):
                        vertex = mesh.vertices[lm.vertex_index]
                        world_pos = mesh_obj.matrix_world @ vertex.co
                        left_eye_positions.append(world_pos)

    if left_eye_positions:
        vertex_positions[101] = sum(left_eye_positions, Vector((0, 0, 0))) / len(left_eye_positions)

    # Calculate right eye center (landmark 111)
    right_eye_positions = []
    for lm_id in right_eye_landmarks:
        for lm in manual_landmarks:
            if lm.landmark_id == lm_id and lm.is_set:
                mesh_obj = bpy.data.objects.get(lm.object_name)
                if mesh_obj:
                    mesh = mesh_obj.data
                    if lm.vertex_index < len(mesh.vertices):
                        vertex = mesh.vertices[lm.vertex_index]
                        world_pos = mesh_obj.matrix_world @ vertex.co
                        right_eye_positions.append(world_pos)

    if right_eye_positions:
        vertex_positions[111] = sum(right_eye_positions, Vector((0, 0, 0))) / len(right_eye_positions)

    # Jaw master position (landmark 102) - between chin and jaw points
    if 0 in vertex_positions:  # Use chin center
        # Offset slightly back and up for jaw master
        chin_pos = vertex_positions[0]
        vertex_positions[102] = chin_pos + Vector((0, -0.05, 0.02))

    # Face center (landmark 109) - average of key face points
    face_center_indices = [36, 21, 6, 0]  # nose top, nose mid, mouth center, chin
    face_center_positions = [vertex_positions[i] for i in face_center_indices if i in vertex_positions]
    if face_center_positions:
        vertex_positions[109] = sum(face_center_positions, Vector((0, 0, 0))) / len(face_center_positions)

    # Tongue master position (landmark 108) - from tongue landmarks
    tongue_landmarks = ["tongue_tip", "tongue_center", "tongue_back"]
    tongue_positions = []
    for lm_id in tongue_landmarks:
        for lm in manual_landmarks:
            if lm.landmark_id == lm_id and lm.is_set:
                mesh_obj = bpy.data.objects.get(lm.object_name)
                if mesh_obj:
                    mesh = mesh_obj.data
                    if lm.vertex_index < len(mesh.vertices):
                        vertex = mesh.vertices[lm.vertex_index]
                        world_pos = mesh_obj.matrix_world @ vertex.co
                        tongue_positions.append(world_pos)

    if tongue_positions:
        vertex_positions[108] = sum(tongue_positions, Vector((0, 0, 0))) / len(tongue_positions)

    # Create the facial_landmarks mesh object
    # Remove existing facial_landmarks if present
    old_landmarks = bpy.data.objects.get('facial_landmarks')
    if old_landmarks:
        bpy.data.objects.remove(old_landmarks, do_unlink=True)

    # Create new mesh
    mesh = bpy.data.meshes.new('facial_landmarks')
    landmarks_obj = bpy.data.objects.new('facial_landmarks', mesh)

    # Link to scene collection
    context.scene.collection.objects.link(landmarks_obj)

    # Create vertices at the maximum index we need
    max_index = max(vertex_positions.keys())
    vertices = []

    # Create vertices - fill gaps with zero vectors
    for i in range(max_index + 1):
        if i in vertex_positions:
            vertices.append(vertex_positions[i])
        else:
            # Fill missing indices with zero vector
            vertices.append(Vector((0, 0, 0)))

    # Create mesh from vertices
    mesh.from_pydata(vertices, [], [])
    mesh.update()

    # Mark the object as facial_landmarks
    landmarks_obj['faceit_landmarks'] = True

    return landmarks_obj


def validate_manual_landmarks_for_rig(context):
    """
    Validates that manual landmarks have sufficient data for rig generation.
    Returns (is_valid, message) tuple.
    """
    scene = context.scene
    manual_landmarks = scene.faceit_manual_landmarks

    if not manual_landmarks:
        return (False, "No manual landmarks initialized")

    target_mesh = scene.faceit_manual_landmarks_target_mesh
    if not target_mesh:
        return (False, "No target mesh selected")

    # Count set landmarks
    set_count = sum(1 for lm in manual_landmarks if lm.is_set)

    if set_count < 30:
        return (False, f"Insufficient landmarks set ({set_count}/85). At least 30 required for rig generation")

    # Check for critical landmark groups
    critical_groups = {
        "Face Outline": ["face_outline_0", "face_outline_8", "face_outline_9"],
        "Eyes": ["left_eye_outer", "left_eye_inner", "right_eye_outer", "right_eye_inner"],
        "Mouth": ["mouth_left_corner", "mouth_right_corner", "mouth_upper_center", "mouth_lower_center"],
        "Nose": ["nose_tip", "nose_bridge_top"],
    }

    missing_groups = []
    for group_name, landmark_ids in critical_groups.items():
        has_any = any(
            lm.landmark_id in landmark_ids and lm.is_set
            for lm in manual_landmarks
        )
        if not has_any:
            missing_groups.append(group_name)

    if missing_groups:
        return (False, f"Missing critical landmark groups: {', '.join(missing_groups)}")

    return (True, f"Ready to generate rig ({set_count}/85 landmarks set)")
