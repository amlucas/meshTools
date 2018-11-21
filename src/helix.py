#! /usr/bin/env python

import pymesh, argparse
import numpy as np
from fix_mesh import fix_mesh

parser = argparse.ArgumentParser(description='Create a helicoidal triangle mesh')

parser.add_argument('--out', help='output file name', type=str)
parser.add_argument('--pitch', type=float, default = 2.5)
parser.add_argument('--height', type=float, default = 5.0)
parser.add_argument('--nsegments', type=float, default = 32)
parser.add_argument('--radius', type=float, default = 1.0)
parser.add_argument('--smallRadius', type=float, default = 0.5)

args = parser.parse_args()


n = args.nsegments
L = args.height
R = args.radius

R0 = args.smallRadius

z = np.linspace(-L/2, L/2, n)
theta = z * (2 * np.pi / args.pitch)
x = R * np.cos(theta)
y = R * np.sin(theta)

vertices = np.transpose(np.vstack((x,y,z)))
edges = np.transpose(np.vstack((range(n-1), range(1,n))))

wire_network = pymesh.wires.WireNetwork.create_from_data(vertices, edges)

inflator = pymesh.wires.Inflator(wire_network)

inflator.set_profile(6)
inflator.set_refinement(2, "loop")
inflator.inflate(R0, per_vertex_thickness=True)

mesh = inflator.mesh
mesh = fix_mesh(mesh, "low")

pymesh.save_mesh(args.out, mesh)
