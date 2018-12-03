#! /usr/bin/env python

import pymesh, argparse

from fix_mesh import fix_mesh

def create_helix(L, nL, R, pitch, dr, dtheta):
    from box import create_box_simple
    import numpy as np

    box_min = [R-dr/2, -dtheta/2, -L/2]
    box_max = [R+dr/2,  dtheta/2,  L/2]

    mesh = create_box_simple(box_min, box_max)

    tol = min([box_max[0] - box_min[0],
               box_max[1] - box_min[1],
               box_max[2] - box_min[2]]) / 4

    for i in range(7):
        mesh  =  pymesh.subdivide(mesh, order=1, method="simple")
        mesh, __ = pymesh.collapse_short_edges(mesh, tol, preserve_feature=True)

    vertices = mesh.vertices
    z = vertices[:,2]
    theta = z * (2 * np.pi / pitch)

    x = np.cos(theta) * vertices[:,0] - np.sin(theta) * vertices[:,1]
    y = np.sin(theta) * vertices[:,0] + np.cos(theta) * vertices[:,1]

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
    args = parse_args()
    mesh = create_helix(args.height, args.nL, args.radius, args.pitch,
                        args.rect_sizes[0], args.rect_sizes[1])
    
    #mesh = fix_mesh(mesh, "normal")

    pymesh.save_mesh(args.out, mesh)
