import bpy
from mathutils import Vector, Matrix
import bmesh
# Get the selected object

bl_info = {
    "name": "myCustomAddons",
    "author": "coconut",
    "version": (0, 9, 96),
    "location": "Properties > Active Tool and Workspace Settings > Bezier Utilities",
    "description": "Collection of Bezier curve utility ops",
    "category": "Object",
    "wiki_url": "https://github.com/Shriinivas/blenderbezierutils/blob/master/README.md",
    "blender": (2, 80, 0),
}


class SetPivotToMedian(bpy.types.Operator):

    bl_idname = bl_info["name"].lower() + ".SetPivotToMedian".lower() 
    bl_label = "Set Origin to Median"
    bl_description = "Set the origin of the selected object to the median of its selected vertices"
    

    def execute(self, context):
        self.pivotToMedian()
        return {'FINISHED'}
    
    def pivotToMedian( self):
        obj = bpy.context.active_object
                  
        mode = bpy.context.object.mode
        bpy.ops.object.mode_set( mode='OBJECT')
        

        #bpy.ops.ed.undo_push()

        
        for obj in bpy.context.selected_objects:
            
            if mode == 'EDIT':
                selected_verts = [v for v in obj.data.vertices if v.select]                
            else:
                selected_verts = [v for v in obj.data.vertices]
            if len( selected_verts) == 0:
                continue

            median = Vector();
            for v in selected_verts:
                median += v.co

            median /= len( selected_verts)


            offsetPos = obj.matrix_world @ Matrix.Translation(  median)
            obj.data.transform( Matrix.Translation( -median))
            obj.matrix_world = offsetPos
            #obj.location += median

            print(median)
            
        #bpy.ops.ed.undo()
        bpy.ops.ed.undo_push()
        bpy.ops.object.mode_set( mode=mode)

        
        
class VertexDraw(bpy.types.Operator):

    bl_idname = bl_info["name"].lower() + ".VertexDraw".lower() 
    bl_label = "Create a single vertex objct"
    bl_description = "Set the origin of the selected object to the median of its selected vertices"
    
    def execute(self, context):
        mesh = bpy.data.meshes.new("SingleVertexMesh")

        obj = bpy.data.objects.new("SingleVertexObject", mesh)

        # Set the location of the object to (0, 0, 0)
        obj.location = (0, 0, 0)

        # Link the object to the scene
        bpy.context.scene.collection.objects.link(obj)

        # Create a new bmesh
        bm = bmesh.new()

        # Add a new vertex to the bmesh at (0, 0, 0)
        bm.verts.new((0, 0, 0))

        # Make sure the bmesh is updated
        bm.to_mesh(mesh)
        bm.free()

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set( mode='EDIT')

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
         
        return {'FINISHED'}

    
        
        
def register():
    print( "Register "  + SetPivotToMedian.bl_idname)  
    bpy.utils.register_class( SetPivotToMedian)
    bpy.utils.register_class( VertexDraw)

def unregister():
    bpy.utils.unregister_class( SetPivotToMedian)
    bpy.utils.unregister_class( VertexDraw)
        
        
if __name__ == "__main__":
    register()

