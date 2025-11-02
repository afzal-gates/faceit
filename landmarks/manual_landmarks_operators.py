"""
Operators for manual landmark picker feature.
Provides vertex selection and landmark management functionality.
"""

import bpy
import bmesh
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, IntProperty
from mathutils import Vector

from .manual_landmarks_data import (
    MANUAL_LANDMARK_LABELS,
    get_landmark_label_dict,
    get_landmark_categories,
    get_landmark_mirror_map
)
from ..core import faceit_utils as futils


class FACEIT_OT_PickLandmarkVertex(Operator):
    """Pick a vertex from the mesh to set as a landmark point"""
    bl_idname = "faceit.pick_landmark_vertex"
    bl_label = "Pick Landmark Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    landmark_id: StringProperty(
        name="Landmark ID",
        description="The landmark to set",
        default=""
    )

    @classmethod
    def poll(cls, context):
        return (context.mode in {'OBJECT', 'EDIT_MESH'} and
                context.scene.faceit_manual_landmarks_target_mesh is not None)

    def execute(self, context):
        scene = context.scene
        target_mesh = scene.faceit_manual_landmarks_target_mesh

        if not target_mesh:
            self.report({'WARNING'}, "No target mesh selected")
            return {'CANCELLED'}

        if context.mode != 'EDIT_MESH' or context.active_object != target_mesh:
            # Switch to edit mode on target mesh
            futils.clear_object_selection()
            futils.set_active_object(target_mesh.name)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            self.report({'INFO'}, f"Select a vertex for {self.landmark_id} and confirm")
            return {'FINISHED'}

        # Get selected vertex
        mesh = target_mesh.data
        bm = bmesh.from_edit_mesh(mesh)
        bm.verts.ensure_lookup_table()

        selected_verts = [v for v in bm.verts if v.select]

        if len(selected_verts) == 0:
            self.report({'WARNING'}, "No vertex selected. Please select a vertex.")
            return {'CANCELLED'}

        if len(selected_verts) > 1:
            self.report({'WARNING'}, "Multiple vertices selected. Please select only one vertex.")
            return {'CANCELLED'}

        vertex_index = selected_verts[0].index

        # Store the landmark data
        landmark_item = None
        for lm in scene.faceit_manual_landmarks:
            if lm.landmark_id == self.landmark_id:
                landmark_item = lm
                break

        if landmark_item is None:
            # Create new landmark item
            landmark_item = scene.faceit_manual_landmarks.add()
            landmark_item.landmark_id = self.landmark_id

        landmark_item.vertex_index = vertex_index
        landmark_item.object_name = target_mesh.name
        landmark_item.is_set = True

        # Deselect vertex
        bpy.ops.mesh.select_all(action='DESELECT')

        label_dict = get_landmark_label_dict()
        landmark_label = label_dict.get(self.landmark_id, self.landmark_id)

        report_message = f"Landmark '{landmark_label}' set to vertex {vertex_index}"

        # Handle mirroring if enabled
        if scene.faceit_manual_landmarks_mirror:
            mirror_map = get_landmark_mirror_map()
            mirror_landmark_id = mirror_map.get(self.landmark_id)

            if mirror_landmark_id:
                # Get the original vertex position
                vertex = mesh.vertices[vertex_index]
                vertex_co = vertex.co.copy()

                # Mirror the position across X axis (assuming X is the symmetry axis)
                mirrored_co = Vector((-vertex_co.x, vertex_co.y, vertex_co.z))

                # Find the closest vertex to the mirrored position
                closest_vert_index = None
                min_distance = float('inf')

                for v in mesh.vertices:
                    distance = (v.co - mirrored_co).length
                    if distance < min_distance:
                        min_distance = distance
                        closest_vert_index = v.index

                if closest_vert_index is not None:
                    # Set the mirrored landmark
                    mirror_landmark_item = None
                    for lm in scene.faceit_manual_landmarks:
                        if lm.landmark_id == mirror_landmark_id:
                            mirror_landmark_item = lm
                            break

                    if mirror_landmark_item is None:
                        # Create new landmark item
                        mirror_landmark_item = scene.faceit_manual_landmarks.add()
                        mirror_landmark_item.landmark_id = mirror_landmark_id

                    mirror_landmark_item.vertex_index = closest_vert_index
                    mirror_landmark_item.object_name = target_mesh.name
                    mirror_landmark_item.is_set = True

                    mirror_landmark_label = label_dict.get(mirror_landmark_id, mirror_landmark_id)
                    report_message += f" | Mirrored to '{mirror_landmark_label}' (V:{closest_vert_index})"

        self.report({'INFO'}, report_message)

        # Update preview if enabled
        if scene.faceit_manual_landmarks_preview:
            bpy.ops.faceit.preview_manual_landmarks('INVOKE_DEFAULT', enable=True)

        return {'FINISHED'}


class FACEIT_OT_ClearLandmark(Operator):
    """Clear a specific landmark"""
    bl_idname = "faceit.clear_landmark"
    bl_label = "Clear Landmark"
    bl_options = {'REGISTER', 'UNDO'}

    landmark_id: StringProperty(
        name="Landmark ID",
        default=""
    )

    def execute(self, context):
        scene = context.scene

        # Find and remove the landmark
        for i, lm in enumerate(scene.faceit_manual_landmarks):
            if lm.landmark_id == self.landmark_id:
                scene.faceit_manual_landmarks.remove(i)
                break

        # Update preview if enabled
        if scene.faceit_manual_landmarks_preview:
            bpy.ops.faceit.preview_manual_landmarks('INVOKE_DEFAULT', enable=True)

        self.report({'INFO'}, f"Cleared landmark {self.landmark_id}")
        return {'FINISHED'}


class FACEIT_OT_ClearAllLandmarks(Operator):
    """Clear all manual landmarks"""
    bl_idname = "faceit.clear_all_landmarks"
    bl_label = "Clear All Landmarks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        scene.faceit_manual_landmarks.clear()

        # Disable preview and clean up empties
        if scene.faceit_manual_landmarks_preview:
            scene.faceit_manual_landmarks_preview = False
            bpy.ops.faceit.preview_manual_landmarks('INVOKE_DEFAULT', enable=False)

        self.report({'INFO'}, "Cleared all manual landmarks")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class FACEIT_OT_ResetManualLandmarks(Operator):
    """Reset all manual landmarks (clear and reinitialize)"""
    bl_idname = "faceit.reset_manual_landmarks"
    bl_label = "Reset Manual Landmarks"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        # Clear existing landmarks
        scene.faceit_manual_landmarks.clear()

        # Disable preview and clean up empties
        if scene.faceit_manual_landmarks_preview:
            scene.faceit_manual_landmarks_preview = False
            bpy.ops.faceit.preview_manual_landmarks('INVOKE_DEFAULT', enable=False)

        # Reinitialize landmarks
        for landmark_id, landmark_label in MANUAL_LANDMARK_LABELS:
            item = scene.faceit_manual_landmarks.add()
            item.landmark_id = landmark_id
            item.vertex_index = -1
            item.object_name = ""
            item.is_set = False

        self.report({'INFO'}, f"Reset all landmarks - ready to pick {len(MANUAL_LANDMARK_LABELS)} points")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class FACEIT_OT_InitializeManualLandmarks(Operator):
    """Initialize the manual landmarks collection with all landmark IDs"""
    bl_idname = "faceit.initialize_manual_landmarks"
    bl_label = "Initialize Manual Landmarks"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        scene = context.scene

        # Clear existing landmarks
        scene.faceit_manual_landmarks.clear()

        # Add all landmark IDs
        for landmark_id, landmark_label in MANUAL_LANDMARK_LABELS:
            item = scene.faceit_manual_landmarks.add()
            item.landmark_id = landmark_id
            item.vertex_index = -1
            item.object_name = ""
            item.is_set = False

        self.report({'INFO'}, f"Initialized {len(MANUAL_LANDMARK_LABELS)} landmarks")
        return {'FINISHED'}


class FACEIT_OT_PreviewManualLandmarks(Operator):
    """Toggle preview of manual landmarks using empties"""
    bl_idname = "faceit.preview_manual_landmarks"
    bl_label = "Preview Manual Landmarks"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    enable: BoolProperty(
        name="Enable",
        default=True
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        collection_name = "FaceIt_Manual_Landmarks_Preview"

        if not self.enable:
            # Remove all preview empties
            collection = bpy.data.collections.get(collection_name)
            if collection:
                for obj in list(collection.objects):
                    bpy.data.objects.remove(obj, do_unlink=True)
                bpy.data.collections.remove(collection)
            return {'FINISHED'}

        # Create or get the preview collection
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            collection = bpy.data.collections.new(collection_name)
            context.scene.collection.children.link(collection)

        # Clear existing preview objects
        for obj in list(collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

        # Create empties for each set landmark
        label_dict = get_landmark_label_dict()

        for lm in scene.faceit_manual_landmarks:
            if not lm.is_set:
                continue

            mesh_obj = bpy.data.objects.get(lm.object_name)
            if not mesh_obj or mesh_obj.type != 'MESH':
                continue

            # Get vertex world position
            mesh = mesh_obj.data
            if lm.vertex_index < 0 or lm.vertex_index >= len(mesh.vertices):
                continue

            vertex = mesh.vertices[lm.vertex_index]
            world_pos = mesh_obj.matrix_world @ vertex.co

            # Create empty at vertex position
            landmark_label = label_dict.get(lm.landmark_id, lm.landmark_id)
            empty_name = f"LM_{lm.landmark_id}"
            empty = bpy.data.objects.new(empty_name, None)
            empty.empty_display_type = 'SPHERE'
            empty.empty_display_size = 0.01
            empty.location = world_pos
            empty.show_name = True
            empty.show_in_front = True

            # Set custom property for easy identification
            empty["faceit_manual_landmark"] = lm.landmark_id

            collection.objects.link(empty)

        self.report({'INFO'}, "Updated landmark preview")
        return {'FINISHED'}


class FACEIT_OT_ExportManualLandmarks(Operator):
    """Export manual landmarks to a JSON file"""
    bl_idname = "faceit.export_manual_landmarks"
    bl_label = "Export Manual Landmarks"
    bl_options = {'REGISTER'}

    filepath: StringProperty(
        name="File Path",
        description="Path to save the landmark data",
        subtype='FILE_PATH'
    )

    def execute(self, context):
        import json

        scene = context.scene
        landmarks_data = {}

        for lm in scene.faceit_manual_landmarks:
            if lm.is_set:
                landmarks_data[lm.landmark_id] = {
                    "vertex_index": lm.vertex_index,
                    "object_name": lm.object_name
                }

        try:
            with open(self.filepath, 'w') as f:
                json.dump(landmarks_data, f, indent=4)
            self.report({'INFO'}, f"Exported {len(landmarks_data)} landmarks to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FACEIT_OT_ImportManualLandmarks(Operator):
    """Import manual landmarks from a JSON file"""
    bl_idname = "faceit.import_manual_landmarks"
    bl_label = "Import Manual Landmarks"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(
        name="File Path",
        description="Path to load the landmark data from",
        subtype='FILE_PATH'
    )

    def execute(self, context):
        import json

        scene = context.scene

        try:
            with open(self.filepath, 'r') as f:
                landmarks_data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import: {str(e)}")
            return {'CANCELLED'}

        # Initialize landmarks if not already done
        if len(scene.faceit_manual_landmarks) == 0:
            bpy.ops.faceit.initialize_manual_landmarks()

        # Apply imported data
        loaded_count = 0
        for landmark_id, data in landmarks_data.items():
            for lm in scene.faceit_manual_landmarks:
                if lm.landmark_id == landmark_id:
                    lm.vertex_index = data.get("vertex_index", -1)
                    lm.object_name = data.get("object_name", "")
                    lm.is_set = True
                    loaded_count += 1
                    break

        # Update preview if enabled
        if scene.faceit_manual_landmarks_preview:
            bpy.ops.faceit.preview_manual_landmarks('INVOKE_DEFAULT', enable=True)

        self.report({'INFO'}, f"Imported {loaded_count} landmarks from {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FACEIT_OT_GenerateRigFromManualLandmarks(Operator):
    """Generate facial rig from manually placed landmarks"""
    bl_idname = "faceit.generate_rig_from_manual_landmarks"
    bl_label = "Generate Rig from Manual Landmarks"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        # Check if we have manual landmarks
        if not scene.faceit_manual_landmarks:
            return False
        # Check if target mesh is set
        if not scene.faceit_manual_landmarks_target_mesh:
            return False
        # Check if at least some landmarks are set
        return any(lm.is_set for lm in scene.faceit_manual_landmarks)

    def execute(self, context):
        from .manual_landmarks_rig import (
            create_faceit_landmarks_from_manual,
            validate_manual_landmarks_for_rig
        )

        scene = context.scene

        # Validate landmarks
        is_valid, message = validate_manual_landmarks_for_rig(context)
        if not is_valid:
            self.report({'WARNING'}, message)
            return {'CANCELLED'}

        # Store original mode
        original_mode = context.mode

        # Switch to object mode
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Create facial_landmarks object from manual landmarks
        landmarks_obj = create_faceit_landmarks_from_manual(context)

        if not landmarks_obj:
            self.report({'ERROR'}, "Failed to create landmarks object from manual landmarks")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Created facial landmarks object with {len(landmarks_obj.data.vertices)} vertices")

        # Check if FaceIt rig generation operator is available
        if not hasattr(bpy.ops.faceit, 'generate_rig'):
            self.report({'ERROR'}, "FaceIt rig generation operator not found. Make sure FaceIt addon is properly installed.")
            # Clean up landmarks object
            bpy.data.objects.remove(landmarks_obj, do_unlink=True)
            return {'CANCELLED'}

        # Add target mesh to face objects if not already there
        target_mesh = scene.faceit_manual_landmarks_target_mesh
        if target_mesh:
            # Check if target mesh is registered in FaceIt
            face_objects = scene.faceit_face_objects
            if target_mesh.name not in [obj.name for obj in face_objects]:
                # Try to register the mesh
                try:
                    item = face_objects.add()
                    item.name = target_mesh.name
                    self.report({'INFO'}, f"Added {target_mesh.name} to FaceIt face objects")
                except:
                    self.report({'WARNING'}, f"Could not register {target_mesh.name} in FaceIt. Rig generation may fail.")

        # Call FaceIt's rig generation operator
        try:
            result = bpy.ops.faceit.generate_rig('INVOKE_DEFAULT')

            if result == {'FINISHED'}:
                self.report({'INFO'}, "Successfully generated rig from manual landmarks")
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "Rig generation completed with warnings. Check FaceIt panel for details.")
                return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error generating rig: {str(e)}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        # Show confirmation dialog with landmark count
        scene = context.scene
        set_count = sum(1 for lm in scene.faceit_manual_landmarks if lm.is_set)
        total_count = len(scene.faceit_manual_landmarks)

        if set_count < total_count * 0.5:  # Less than 50% landmarks set
            return context.window_manager.invoke_confirm(self, event)

        return self.execute(context)
