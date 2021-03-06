#! /usr/bin/env python

import pymesh, argparse
import numpy as np
from fix_mesh import fix_mesh

def create_helix(nL, L, R, pitch, nR, RStart, REnd):
    z = np.linspace(-L/2, L/2, nL)
    theta = z * (2 * np.pi / pitch)
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    
    vertices = np.transpose(np.vstack((x,y,z)))
    edges = np.transpose(np.vstack((range(nL-1), range(1,nL))))
    
    wire_network = pymesh.wires.WireNetwork.create_from_data(vertices, edges)
    
    inflator = pymesh.wires.Inflator(wire_network)
    
    inflator.set_profile(nR)
    inflator.set_refinement(2, "loop")
    thickness = np.arange(wire_network.num_vertices) /  wire_network.num_vertices * (RStart-REnd) + REnd
    inflator.inflate(thickness, per_vertex_thickness=True)

    mesh = inflator.mesh

    return mesh, vertices

def parse_args():
    parser = argparse.ArgumentParser(description='Create a helicoidal triangle mesh')

    parser.add_argument('--out', help='output file name', type=str, required=True)
    parser.add_argument('--pitch', type=float, default = 2.5)
    parser.add_argument('--height', type=float, default = 5.0)
    parser.add_argument('--nL', type=float, default = 32)
    parser.add_argument('--nR', type=float, default = 6)
    parser.add_argument('--radius', type=float, default = 1.0)
    parser.add_argument('--smallRadiusStart', type=float, default = 0.5)
    parser.add_argument('--smallRadiusEnd', type=float, default = 0.5)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    mesh, _ = create_helix(args.nL, args.height, args.radius, args.pitch,
                           args.nR, args.smallRadiusStart, args.smallRadiusEnd)
    
    mesh = fix_mesh(mesh, "low")

    pymesh.save_mesh(args.out, mesh)
