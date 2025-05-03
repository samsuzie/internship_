import numpy as np
import trimesh
import open3d as o3d
import os

def generating_model_from_img(processed_img,depth_map):
    
    # creating points cloud and color cloud
    h,w = depth_map.shape
    points=[]
    colors=[]

    img_arr = np.array(processed_img)

    # creating points that are visible to the camera
    for y in range(h):
        for x in range(w):
            if depth_map[y,x]>0.1:
                # scaling up for better visiblity
                z = depth_map[y,x]*2.0
                points.append([x/w-0.5,-(y/h-0.5),z])
                colors.append(img_arr[y,x]/255.0)

    points = np.array(points)
    colors = np.array(colors)

    # creating point clouds
    point_clouds = o3d.geometry.PointCloud()
    # assigining the location of points to the points_cloud
    point_clouds.points = o3d.utility.Vector3dVector(points)
    point_clouds.colors = o3d.utility.Vector3dVector(colors[:,:3])
    # after assigining whether the thing is facing up or down or where we will estimate normals
    point_clouds.estimate_normals()

    # creating mesh that will act as binding blanket for all the points in points cloud
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug)as cm:
        mesh,denisity=o3d.gemetry.TriangleMesh.create_from_point_cloud_poisson(
            point_clouds,depth=9
        )
    
    # removing the vertices with lower density
    vertex_to_remove = denisity<np.quantile(denisity,0.1)
    mesh.remove_vertices_by_mask(vertex_to_remove)

    return mesh,point_clouds


# generating 3d model from text
def generate_model_from_text(input):
    shapes={
        "car": create_car,
        "cube": create_cube,
        "sphere": create_sphere,
        "cylinder": create_cylinder,
        "toy": create_toy,
        "chair": create_chair
    }

    for keyword, func in shapes.items():
        if keyword in input:
            return func(input)
    # default condition 
    return create_cube(input)

# create cube
def create_cube(text,size=2.0):
    mesh=trimesh.creation.box(extents=[size,size,size])
    return mesh, None
# create sphere
def create_sphere(text,radius=0.6):
    """create a simple sphere mesh"""
    mesh=trimesh.creation.icosphere(radius=radius)
    return mesh,None

def create_cylinder(text,radius=0.8,height=2.0):
    mesh = trimesh.creation.cylinder(radius=radius,height=height)
    return mesh,None


def create_car(text):

    mainbody=trimesh.creation.box(extents=[3.0,2.0,1.0])

    cabinat= trimesh.creation.box(extents=[1.5,0.9,0.5])
    cabinat.apply_translation([0.2,0,0.75])

    wheel_1=trimesh.creation.cylinder(radius=0.25,height=0.1)
    wheel_1.apply_translation([0.5, 0.55, -0.15])
    wheel_1.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
    
    wheel_2 = trimesh.creation.cylinder(radius=0.25, height=0.1)
    wheel_2.apply_translation([-0.5, 0.55, -0.15])
    wheel_2.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
    
    wheel_3 = trimesh.creation.cylinder(radius=0.25, height=0.1)
    wheel_3.apply_translation([0.5, -0.55, -0.15])
    wheel_3.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
    
    wheel_4 = trimesh.creation.cylinder(radius=0.25, height=0.1)
    wheel_4.apply_translation([-0.5, -0.55, -0.15])
    wheel_4.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))


    # combining all of thrm
    car = trimesh.util.concatenate([mainbody,cabinat,wheel_1,wheel_2,wheel_3,wheel_4])

    return car,None

def create_chair(text):
    # Seat
    Seat = trimesh.creation.box(extents=[1.0, 1.0, 0.1])
    Seat.apply_translation([0, 0, 0.5])
    
    # Backrest
    backrest = trimesh.creation.box(extents=[0.1, 1.0, 1.0])
    backrest.apply_translation([-0.45, 0, 1.0])
    
    # Legs
    leg1 = trimesh.creation.cylinder(radius=0.05, height=0.5)
    leg1.apply_translation([0.4, 0.4, 0.25])
    
    leg2 = trimesh.creation.cylinder(radius=0.05, height=0.5)
    leg2.apply_translation([0.4, -0.4, 0.25])
    
    leg3 = trimesh.creation.cylinder(radius=0.05, height=0.5)
    leg3.apply_translation([-0.4, 0.4, 0.25])
    
    leg4 = trimesh.creation.cylinder(radius=0.05, height=0.5)
    leg4.apply_translation([-0.4, -0.4, 0.25])
    
    # Combine all meshes
    chair = trimesh.util.concatenate([Seat, backrest, leg1, leg2, leg3, leg4])
    
    return chair, None

def create_toy(text):
    """Create a simple toy-like mesh."""
    if "car" in text:
        return create_car(text)
    # Body
    Body = trimesh.creation.box(extents=[0.5, 0.3, 0.8])
    
    # Head
    Head = trimesh.creation.icosphere(radius=0.25)
    Head.apply_translation([0, 0, 0.65])
    Arm1 = trimesh.creation.cylinder(radius=0.08, height=0.6)
    Arm1.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
    Arm1.apply_translation([0, 0, 0.3])
    
    # Legs
    Leg1 = trimesh.creation.cylinder(radius=0.1, height=0.5)
    Leg1.apply_translation([0.15, 0, -0.25])
    
    leg2 = trimesh.creation.cylinder(radius=0.1, height=0.5)
    leg2.apply_translation([-0.15, 0, -0.25])
    
    # Combine all meshes
    toy = trimesh.util.concatenate([Body, Head, Arm1, Leg1, leg2])
    
    return toy, None

def save_models(mesh, outputpath, file_format="obj"):
    """Save the generated 3D model to a file."""

    os.makedirs(os.path.dirname(outputpath), exist_ok=True)
    
    if file_format == "obj":
        if isinstance(mesh, o3d.geometry.TriangleMesh):
            # convertung ti trimesh for saving
            vertices = np.asarray(mesh.vertices)
            faces = np.asarray(mesh.triangles)
            tm_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            tm_mesh.export(outputpath)
        else:
            # already a trimesh 
            mesh.export(outputpath)
    elif file_format == "stl":
        if isinstance(mesh, o3d.geometry.TriangleMesh):
            vertices = np.asarray(mesh.vertices)
            faces = np.asarray(mesh.triangles)
            tm_mesh = trimesh.Trimesh(vertices=vertices,faces=faces)
            tm_mesh.export(outputpath)
        else:
            mesh.export(outputpath)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
    return outputpath