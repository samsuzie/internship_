import matplotlib.pyplot as plt
import numpy as np
import trimesh
import open3d

def visualize_model(mes,point_cloud=None,show=True,save_path=None):
    fig = plt.figure(figsize=(12,12))
    axis = fig.add_subplot(111,projection='3d')

    # different handling based on mesh size
    if isinstance(mes,trimesh.Trimesh):
        vertices = mes.vertices
        faces = mes.faces

        # plotting it 
        axis.plot_trisurf(
            vertices[:,0],vertices[:,1],vertices[:,2],
            triangles = faces,
            cmap='viridis',
            alpha=0.7
        )
    
    elif isinstance(mes,o3d.geometry,TriangleMesh):
        vertices = np.asarray(mes.vertices)
        faces = np.asarray(mes.triangles)

        # plotting
        axis.plot_trisurf(
            # extracting the x,y,z coordinates respectively 
            vertices[:,0],vertices[:,1],vertices[:,2],
            triangles = faces,
            cmap='viridis',
            alpha =0.7
        )

    if point_cloud is not None and isinstance(point_cloud,o3d.geometry.Pointcloud):
        points = np.asarray(point_cloud.points)
        colors = np.asarray(point_cloud.colors)

        axis.scatter(
            points[:,0],points[:,1],points[:,2],
            c= colors if len(colors)>0 else 'r',
            s=1,
            alpha=0.6
        )  

    
    axis.set_label('X')
    axis.set_label('Y')
    axis.set_label('Z')
    axis.set_title('3D MODEL VISUALIZATION')

    axis.set_box_aspect([1, 1, 1])
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig, axis


    