#! /usr/bin/env python

import pymesh, argparse

def create_helix(L, nL, R, pitch, dr, dtheta):
    from box import create_box_simple
    import numpy as np

    box_min = [-dr/2, -dtheta/2, -L/2]
    box_max = [dr/2,  dtheta/2,  L/2]

    mesh = create_box_simple(box_min, box_max)

    tol = min([box_max[0] - box_min[0],
               box_max[1] - box_min[1],
               box_max[2] - box_min[2]]) / 4

    for i in range(7):
        mesh  =  pymesh.subdivide(mesh, order=1, method="simple")
        mesh, __ = pymesh.collapse_short_edges(mesh, tol, preserve_feature=True)

    vertices = mesh.vertices
    
    phi   = np.arctan2(pitch / 2 * np.pi, R)

    theta = vertices[:,2] * (2 * np.pi / pitch)

    # orientation step: orient the box along the helix
    xp = vertices[:,0]
    yp = np.cos(phi) * vertices[:,1] - np.sin(phi) * vertices[:,2]
    zp = np.sin(phi) * vertices[:,1] + np.cos(phi) * vertices[:,2]    
    
    x = np.cos(theta) * xp - np.sin(theta) * yp
    y = np.sin(theta) * xp + np.cos(theta) * yp
    z = zp

    # guide: how a vertical line is transformed to helix
    xg = R * np.cos(theta)
    yg = R * np.sin(theta)
    zg = 1.0 * vertices[:,2]

    # transformed: how the orientation step transformed the data position (on a vertical line)
    n = len(vertices[:,0])
    xp = np.zeros(n)
    yp = - np.sin(phi) * vertices[:,2]
    zp = + np.cos(phi) * vertices[:,2]

    xt = np.cos(theta) * xp - np.sin(theta) * yp
    yt = np.sin(theta) * xp + np.cos(theta) * yp
    zt = zp

    # adjust position according to the guide
    x += xg-xt
    y += yg-yt
    z += zg-zt
    
    vertices = np.transpose(np.vstack((x,y,z)))
    return pymesh.form_mesh(vertices, mesh.faces)

def parse_args():
    parser = argparse.ArgumentParser(description='Create a helicoidal triangle mesh from recatngle shape')

    parser.add_argument('--out', help='output file name', type=str, required=True)
    parser.add_argument('--pitch', type=float, default = 2.5)
    parser.add_argument('--nL', type=int, default = 32)
    parser.add_argument('--height', type=float, default = 5.0)
    parser.add_argument('--radius', type=float, default = 1.0)
    parser.add_argument('--rect_sizes', type=float, nargs=2, default = [0.1, 0.5])

    return parser.parse_args()

if __name__ == '__main__':
    from fix_mesh import fix_mesh_target_length
    args = parse_args()
    mesh = create_helix(args.height, args.nL, args.radius, args.pitch,
                        args.rect_sizes[0], args.rect_sizes[1])
    

    target_len = min(args.rect_sizes) * 0.6
    mesh = fix_mesh_target_length(mesh, target_len)
    #mesh = fix_mesh(mesh, "low")

    pymesh.save_mesh(args.out, mesh)
