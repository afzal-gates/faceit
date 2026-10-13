import bmesh
import bpy
from mathutils import Vector

from ..core import expresso_utils as futils
from ..core import vgroup_utils as vg_utils


GROUP_KEYWORDS = {
    "expresso_upper_teeth": ("upperteeth", "upper_teeth", "teethupper", "teeth_upper", "teeth.t", "toothupper", "uppergum", "gumupper"),
    "expresso_lower_teeth": ("lowerteeth", "lower_teeth", "teethlower", "teeth_lower", "teeth.b", "toothlower", "lowergum", "gumlower"),
    "expresso_tongue": ("tongue", "tounge", "toung"),
    "expresso_eyelashes": ("eyelash", "lash", "eyelid", "eyeshell", "tearline", "tear_line"),
    "expresso_facial_hair": ("eyebrow", "brow", "beard", "moustache", "mustache", "facialhair", "facial_hair", "hair_face"),
    "expresso_rigid": ("glasses", "earring", "piercing", "helmet", "mask", "rigid", "accessory"),
}


def _normalized_name(name):
    return "".join(ch for ch in name.lower() if ch.isalnum() or ch in "._")


def _all_vertex_indices(obj):
    return [v.index for v in obj.data.vertices]


def _object_bounds(obj, indices=None):
    indices = set(indices) if indices is not None else None
    coords = [obj.matrix_world @ v.co for v in obj.data.vertices if indices is None or v.index in indices]
    if not coords:
        return None
    mins = Vector((min(co.x for co in coords), min(co.y for co in coords), min(co.z for co in coords)))
    maxs = Vector((max(co.x for co in coords), max(co.y for co in coords), max(co.z for co in coords)))
    center = (mins + maxs) * 0.5
    size = maxs - mins
    return mins, maxs, center, size


def _classify_by_name(name):
    clean_name = _normalized_name(name)
    if any(key in clean_name for key in ("eyeball.r", "righteyeball", "eyeballright")):
        return "expresso_right_eyeball"
    if any(key in clean_name for key in ("eyeball.l", "lefteyeball", "eyeballleft")):
        return "expresso_left_eyeball"
    if any(key in clean_name for key in ("righteye", "eye.r", "eyer", "rightiris", "iris.r", "pupil.r", "cornea.r")):
        return "expresso_right_eyes_other"
    if any(key in clean_name for key in ("lefteye", "eye.l", "eyel", "leftiris", "iris.l", "pupil.l", "cornea.l")):
        return "expresso_left_eyes_other"
    if any(key in clean_name for key in ("head", "face", "body", "skin", "base", "mesh")):
        return "expresso_main"
    for group_name, keywords in GROUP_KEYWORDS.items():
        if any(keyword in clean_name for keyword in keywords):
            return group_name
    return None


def _get_mesh_islands(obj):
    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        paths = {v.index: {e.other_vert(v).index for e in v.link_edges} for v in bm.verts}
    finally:
        bm.free()

    islands = []
    while paths:
        start = next(iter(paths))
        stack = [start]
        island = set()
        while stack:
            index = stack.pop()
            if index in island:
                continue
            island.add(index)
            stack.extend(paths.pop(index, ()))
        islands.append(island)
    return islands


def _classify_island(obj, island, character_bounds):
    bounds = _object_bounds(obj, island)
    if bounds is None or character_bounds is None:
        return None
    char_min, char_max, char_center, char_size = character_bounds
    _mins, _maxs, center, size = bounds
    count = len(island)
    mesh_count = max(1, len(obj.data.vertices))
    height = max(char_size.z, 0.0001)
    width = max(char_size.x, 0.0001)
    rel_z = (center.z - char_min.z) / height
    rel_x = (center.x - char_center.x) / width
    rel_y = (center.y - char_center.y) / max(char_size.y, 0.0001)
    size_ratio = count / mesh_count

    if size_ratio > 0.35:
        return "expresso_main"
    if rel_z > 0.55 and abs(rel_x) > 0.08 and size.z < height * 0.18 and size.x < width * 0.28:
        return "expresso_right_eyes_other" if rel_x < 0 else "expresso_left_eyes_other"
    if 0.35 < rel_z < 0.68 and abs(rel_x) < 0.22 and size.z < height * 0.16:
        return "expresso_upper_teeth" if center.z >= char_center.z else "expresso_lower_teeth"
    if 0.25 < rel_z < 0.62 and abs(rel_x) < 0.18 and rel_y < 0.2 and size.x < width * 0.35:
        return "expresso_tongue"
    if rel_z > 0.55 and size_ratio < 0.08 and size.z < height * 0.12:
        return "expresso_facial_hair"
    return None


def _register_object(scene, obj):
    if obj.name in scene.expresso_face_objects:
        return
    item = scene.expresso_face_objects.add()
    item.name = obj.name
    item.obj_pointer = obj
    scene.expresso_face_index = scene.expresso_face_objects.find(obj.name)


class EXPRESSO_OT_AutoDetectFaceParts(bpy.types.Operator):
    """Detect common character face parts and assign Expresso vertex groups."""
    bl_idname = "expresso.auto_detect_face_parts"
    bl_label = "Auto Detect Face Parts"
    bl_options = {"UNDO"}

    use_selected_only: bpy.props.BoolProperty(
        name="Selected Only",
        default=True,
        description="Only scan selected mesh objects. Disable to scan visible mesh objects in the scene.",
    )
    clear_existing_expresso_groups: bpy.props.BoolProperty(
        name="Replace Expresso Groups",
        default=True,
        description="Remove existing Expresso vertex groups from scanned objects before assigning detected groups.",
    )

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "use_selected_only")
        layout.prop(self, "clear_existing_expresso_groups")

    def _candidate_objects(self, context):
        if self.use_selected_only:
            objects = context.selected_objects
        else:
            objects = context.scene.objects
        return [obj for obj in objects if obj.type == "MESH" and not futils.get_hide_obj(obj)]

    def execute(self, context):
        objects = self._candidate_objects(context)
        if not objects:
            self.report({"WARNING"}, "No mesh objects found to detect.")
            return {"CANCELLED"}

        scene = context.scene
        detected = {}
        main_candidates = []
        for obj in objects:
            if self.clear_existing_expresso_groups:
                vg_utils.remove_expresso_vertex_grps(obj)
            _register_object(scene, obj)
            group_name = _classify_by_name(obj.name)
            if group_name:
                detected.setdefault(obj, {}).setdefault(group_name, set()).update(_all_vertex_indices(obj))
                if group_name == "expresso_main":
                    main_candidates.append(obj)

        if not main_candidates:
            main_candidates = sorted(objects, key=lambda item: len(item.data.vertices), reverse=True)[:1]
            for obj in main_candidates:
                detected.setdefault(obj, {}).setdefault("expresso_main", set()).update(_all_vertex_indices(obj))

        character_bounds = _object_bounds(max(main_candidates, key=lambda item: len(item.data.vertices)))
        for obj in objects:
            if _classify_by_name(obj.name):
                continue
            for island in _get_mesh_islands(obj):
                group_name = _classify_island(obj, island, character_bounds)
                if group_name:
                    detected.setdefault(obj, {}).setdefault(group_name, set()).update(island)

        assigned_count = 0
        for obj, groups in detected.items():
            for group_name, indices in groups.items():
                valid_indices = [index for index in indices if index < len(obj.data.vertices)]
                if valid_indices:
                    vg_utils.assign_vertex_grp(obj, valid_indices, group_name, overwrite=True)
                    assigned_count += 1

        bpy.ops.expresso.init_retargeting("EXEC_DEFAULT", quick_search=True)
        self.report({"INFO"}, f"Auto detected {assigned_count} Expresso vertex group assignments.")
        return {"FINISHED"}
