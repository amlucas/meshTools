#! /usr/bin/env python

import pymesh, argparse
import numpy as np
import fix_mesh as FM
from helix import create_helix

def parse_args():
    parser = argparse.ArgumentParser(description='Create a helicoidal triangle mesh')

    parser.add_argument('--out', help='output file name', type=str)
    parser.add_argument('--pitch', type=float, default = 2.5)
    parser.add_argument('--height', type=float, default = 10.0)
    parser.add_argument('--nL', type=float, default = 64)
    parser.add_argument('--nR', type=float, default = 6)
    parser.add_argument('--radius', type=float, default = 1.0)
    parser.add_argument('--smallRadiusStart', type=float, default = 0.7)
    parser.add_argument('--smallRadiusEnd', type=float, default = 0.7)

    parser.add_argument('--sphereRadius', type=float, default = 1.5)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    Hmesh = create_helix(args.nL, args.height, args.radius, args.pitch,
                        args.nR, args.smallRadiusStart, args.smallRadiusEnd)

    R = args.sphereRadius
    H = args.height
    Smesh =  pymesh.generate_icosphere(R, [0.0, 0.0, H/2], refinement_order=2)

    mesh = pymesh.boolean(Hmesh, Smesh,
                          operation="union",
                          engine="igl")

    mesh = pymesh.subdivide(mesh, order=2, method="loop")
    #mesh = FM.fix_mesh(mesh, "low")
    mesh = FM.fix_mesh_target_length(mesh, 0.1)

    pymesh.save_mesh(args.out, mesh)
