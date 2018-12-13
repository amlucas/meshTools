#! /usr/bin/env python

import pymesh, argparse
import numpy as np
from fix_mesh import fix_mesh
import box

def create_helix(nL, L, R, pitch, nR, smallR):
    z = np.linspace(-L/2, L/2, nL)
    theta0 = np.pi * L / pitch + np.pi/4
    theta = z * (2 * np.pi / pitch)
    
    L0 = L/2-pitch/4 # start of decrease from 1
    L1 = L/2 # end of dcrease to 0
    dcenter = (z < L0) * 1 + ((z >= L0) * (z < L1)) * np.cos( (np.pi / (2 * (L1-L0))) * (z-L0) )

    x = R * np.cos(theta) * dcenter
    y = R * np.sin(theta) * dcenter
    
    vertices = np.transpose(np.vstack((x,y,z)))
    edges = np.transpose(np.vstack((range(nL-1), range(1,nL))))
    
    wire_network = pymesh.wires.WireNetwork.create_from_data(vertices, edges)
    
    inflator = pymesh.wires.Inflator(wire_network)
    
    inflator.set_profile(nR)
    inflator.set_refinement(2, "loop")
    inflator.inflate(smallR, per_vertex_thickness=True)

    mesh = inflator.mesh

    return mesh, vertices

def parse_args():
    parser = argparse.ArgumentParser(description='Create a helicoidal triangle mesh')

    parser.add_argument('--out', help='output file name', type=str, required=True)
    parser.add_argument('--pitch', type=float, default = 6.0)
    parser.add_argument('--height', type=float, default = 20.0)
    parser.add_argument('--nL', type=int, default = 64)
    parser.add_argument('--nR', type=int, default = 6)
    parser.add_argument('--radius', type=float, default = 3.0)
    parser.add_argument('--smallRadius', type=float, default = 1.0)

    parser.add_argument('--RectangleDims', type=float, nargs=3, default = [0.6, 6.0, 3.0])

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    alpha = 0.35
    ratio = 1.7
    
    R = args.radius - args.smallRadius/2
    L = args.height - args.RectangleDims[2] * (1-alpha) - args.smallRadius/2

    L = L / ratio
    
    Hmesh, bones = create_helix(args.nL, L, R, args.pitch/ratio,
                                args.nR, args.smallRadius)


    verts = np.array(np.transpose(Hmesh.vertices))
    verts[2,:] *= ratio
    Hmesh = pymesh.form_mesh(np.transpose(verts), Hmesh.faces)
    
    recte = np.array(args.RectangleDims)
    rectc = bones[-1]
    rectc[2] *= ratio
    rectc[2] += alpha * recte[2]
    
    Rmesh = box.create_box_simple(box_min = rectc - 0.5 * recte,
                                  box_max = rectc + 0.5 * recte)

    rect = np.array(args.RectangleDims)
    mesh = pymesh.boolean(Hmesh, Rmesh,
                          operation="union",
                          engine="igl")

    mesh = fix_mesh(mesh, "normal")

    pymesh.save_mesh(args.out, mesh)
