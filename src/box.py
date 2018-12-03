#! /usr/bin/env python

import pymesh, argparse

def create_box_simple(box_min, box_max):
    import numpy as np
    
    vertices = np.array([
        [box_min[0], box_min[1], box_min[2]],
        [box_max[0], box_min[1], box_min[2]],
        [box_max[0], box_max[1], box_min[2]],
        [box_min[0], box_max[1], box_min[2]],
        [box_min[0], box_min[1], box_max[2]],
        [box_max[0], box_min[1], box_max[2]],
        [box_max[0], box_max[1], box_max[2]],
        [box_min[0], box_max[1], box_max[2]]])
    
    faces = np.array([
        [0, 2, 1],
        [0, 3, 2],
        [0, 1, 4],
        [1, 5, 4],
        [0, 7, 3],
        [0, 4, 7],
        [3, 7, 6],
        [3, 6, 2],
        [2, 6, 5],
        [2, 5, 1],
        [4, 5, 6],
        [4, 6, 7]])

    mesh = pymesh.form_mesh(vertices, faces)
    return mesh


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='create a simple recatangel mesh')
    parser.add_argument('--out', help='output file name', type=str, required=True)
    parser.add_argument('--box_min', type=float, nargs=3, default = [-1, -2, -3])
    parser.add_argument('--box_max', type=float, nargs=3, default = [ 1,  2,  3])
    args = parser.parse_args()

    mesh = create_box_simple(args.box_min, args.box_max)

    pymesh.save_mesh(args.out, mesh)
