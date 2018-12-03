#! /usr/bin/env python

import pymesh, argparse
import numpy as np
import fix_mesh as FM
from circ_helix import create_helix

def parse_args():
    parser = argparse.ArgumentParser(description='Create a helix with rectangle at the end')

    parser.add_argument('--out', help='output file name', type=str, required=True)
    parser.add_argument('--pitch', type=float, default = 2.5)
    parser.add_argument('--height', type=float, default = 10.0)
    parser.add_argument('--nL', type=float, default = 64)
    parser.add_argument('--nR', type=float, default = 6)
    parser.add_argument('--radius', type=float, default = 1.0)
    parser.add_argument('--smallRadiusStart', type=float, default = 0.7)
    parser.add_argument('--smallRadiusEnd', type=float, default = 0.7)

    parser.add_argument('--RectangleDims', type=float, nargs=3, default = [1.0, 1.5, 0.5])

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    Hmesh, bones = create_helix(args.nL, args.height, args.radius, args.pitch,
                                args.nR, args.smallRadiusStart, args.smallRadiusEnd)

    H = args.height
    rect = np.array(args.RectangleDims)
    Rmesh =  pymesh.generate_box_mesh(box_min = -0.5 * rect,
                                      box_max =  0.5 * rect,
                                      subdiv_order=1)

    rcenter = bones[-2]
    rorient = rcenter - bones[-3]
    
    q = pymesh.Quaternion.fromData([0, 1, 0], rorient)
    q.normalize()
    verts = Rmesh.vertices

    def transform(v):
        if np.linalg.norm(v) < 1e-8:
            return rcenter
        return q.rotate(v) + rcenter
    
    verts = [transform(v) for v in verts]
    
    Rmesh = pymesh.form_mesh(np.array(verts), Rmesh.faces)
    
    mesh = pymesh.boolean(Hmesh, Rmesh,
                          operation="union",
                          engine="igl")

    #mesh = pymesh.subdivide(mesh, order=2, method="loop")
    #mesh = FM.fix_mesh(mesh, "low")
    mesh = FM.fix_mesh_target_length(mesh, 0.1)

    pymesh.save_mesh(args.out, mesh)
