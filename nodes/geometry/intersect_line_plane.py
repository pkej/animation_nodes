import bpy
from ... base_types.node import AnimationNode

class IntersectLinePlaneNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_IntersectLinePlaneNode"
    bl_label = "Intersect Line Plane"
    bl_width_default = 160
    
    def create(self):
        self.newInput("Vector", "Line Start", "lineStart")
        self.newInput("Vector", "Line End", "lineEnd").value = (0, 0, 1)

        self.newInput("Vector", "Plane Point", "planePoint")
        self.newInput("Vector", "Plane Normal", "planeNormal").value = (0, 0, 1)

        self.newOutput("Vector", "Intersection", "intersection")
        self.newOutput("Boolean", "Is Valid", "isValid")

    def getExecutionCode(self):
        isLinked = self.getLinkedOutputsDict()
        if not any(isLinked.values()): return ""
    
        intersection = isLinked["intersection"]
        isValid = isLinked["isValid"]
        
        yield "if planeNormal.length_squared == 0: planeNormal = mathutils.Vector((0, 0, 1))"
        yield "int = mathutils.geometry.intersect_line_plane(lineStart, lineEnd, planePoint, planeNormal, False)"

        yield "if int is None:"
        if intersection : yield "    intersection = mathutils.Vector((0, 0, 0))"
        if isValid: yield "    isValid = False"
        yield "else:"
        if intersection : yield "    intersection = int"
        if isValid: yield "    isValid = True"

    def getUsedModules(self):
        return ["mathutils"]
