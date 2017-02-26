# coding: utf-8
import json
import geojson
from geojson import Feature, Point, FeatureCollection, Polygon
import os
import numpy as np
from json import encoder
import math

# encoder.FLOAT_REPR = lambda o: format(o, '.6f')
gjindex = -len('.geojson')
num_feats = 5000

def remove_zetas(m):
    try:
        return np.array(m)[:, :, :2].tolist()
    except:
        new_m = []
        for i in np.array(m):
            new_m.append(np.array(i)[:, :2].tolist())
        return new_m


def parse_geojson(fname):
    print fname
    with open(fname, 'r') as f:
        fc = geojson.load(f)

    fc.keys()

    fc['type']



    id_feat = str(fc).count('"id":')-1

    def fix_props(props, z):
        props['height'] = z
        props['base_height'] = 0
        props['level'] = 1
        props['name'] = props['name'] if 'name' in props else ''

        if 'fill' in props:
            props['color'] = props['fill']
        elif 'stroke' in props:
            props['color'] = 'white'

        # del props['stroke-opacity']
        # del props['stroke-width']
        # del props['styleHash']
        # del props['styleMapHash']
        # del props['styleUrl']
        return props
    for file_number in range(int(math.ceil(len(fc.features)/float(num_feats)))):
        newgj = FeatureCollection([])
        print file_number

        for f in fc.features[file_number*num_feats:(file_number+1)*num_feats]:
            if f.geometry.type == 'GeometryCollection':
                for p in f.geometry.geometries:
                    newprops = fix_props(f.properties, p['coordinates'][0][0][2])
                    newfeat = {"type": "Feature",
                               'id': id_feat,
                               'properties': newprops,
                               'geometry': p}
                    p['coordinates'] = remove_zetas(p['coordinates'])
                    newgj.features.append(newfeat)
                    id_feat += 1

            else:
                f.properties = fix_props(
                    f.properties, f.geometry['coordinates'][0][0][2])
                # f.geometry['coordinates'] = remove_zetas(f.geometry['coordinates'])
                newgj.features.append(f)

        with open('new/' + fname[:gjindex] + fname[gjindex:], 'w') as outfile:
            json.dump(newgj, outfile) #, separators=(',', ':'))


def main():
    for fname in [f for f in os.listdir('.') if ('dismesso' in f or 'obsoleto' in f)]:
        parse_geojson(fname)

if __name__ == '__main__':
    main()
