#! /usr/bin/env python

import pymesh, argparse
import numpy as np
import fix_mesh as FM
from rect_helix import create_helix

def parse_args():
    parser = argparse.ArgumentParser(description='Create a sphere with rectangular-section helix')

    parser.add_argument('--out', help='output file name', type=str, required=True)
    parser.add_argument('--pitch', type=float, default = 2.5)
    parser.add_argument('--height', type=float, default = 10.0)
    parser.add_argument('--radius', type=float, default = 1.0)
    parser.add_argument('--rect_sizes', type=float, nargs=2, default = [0.3, 0.7])
    
    parser.add_argument('--sphereRadius', type=float, default = 1.5)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    Hmesh, _ = create_helix(args.height, args.radius, args.pitch,
                            args.rect_sizes[0], args.rect_sizes[1])

    R = args.sphereRadius
    H = args.height
    Smesh =  pymesh.generate_icosphere(R, [0.0, 0.0, H/2], refinement_order=2)

    mesh = pymesh.boolean(Hmesh, Smesh,
                          operation="union",
                          engine="igl")

    mesh = pymesh.subdivide(mesh, order=2, method="simple")
    #mesh = FM.fix_mesh(mesh, "low")
    mesh = FM.fix_mesh_target_length(mesh, 0.1)

    pymesh.save_mesh(args.out, mesh)
