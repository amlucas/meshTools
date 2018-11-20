#! /usr/bin/env python

import trimesh, argparse

parser = argparse.ArgumentParser(description='Create a sphere')

parser.add_argument('--subdivisions', help='Number of subdivisions from icosphere', type=int, default=2)
parser.add_argument('--radius', help='sphere radius', type=float, default=1.0)
parser.add_argument('--out', help='output file name', type=str)

args = parser.parse_args()

mesh = trimesh.creation.icosphere(args.subdivisions, args.radius)

mesh.export(args.out)
