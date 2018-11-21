#! /usr/bin/env python

import pymesh, argparse
import numpy as np

parser = argparse.ArgumentParser(description='Create a helicoidal triangle mesh')

parser.add_argument('--out', help='output file name', type=str)

args = parser.parse_args()

n = 32
L0 = 5.0
R0 = 0.5
R = 1.0
P = L0 / 3

z = np.linspace(-L0/2, L0/2, n)
theta = z * (2 * np.pi / P)
x = R * np.cos(theta)
y = R * np.sin(theta)

vertices = np.transpose(np.vstack((x,y,z)))
edges = np.transpose(np.vstack((range(n-1), range(1,n))))

wire_network = pymesh.wires.WireNetwork.create_from_data(vertices, edges)

inflator = pymesh.wires.Inflator(wire_network)

inflator.set_profile(6)
inflator.inflate(R0, per_vertex_thickness=True)

mesh = inflator.mesh

pymesh.save_mesh(args.out, mesh)
