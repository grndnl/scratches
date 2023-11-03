import argparse
import os
import math
import sys
import time
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--model-dir', type=str, default='input/')
parser.add_argument('--output-dir', type=str, default='output/')
parser.add_argument('--environment', type=str, default='abandoned_church')
# parser.add_argument('--material', type=str, default='Prism-113')
parser.add_argument('--material', type=str, default='Prism-2050')
parser.add_argument('--camera', type=str, default='0')
parser.add_argument('--model', type=str, default='')
parser.add_argument('--tmp-dir', type=str, default='tmp/')
parser.add_argument('--preview', type=bool, default=True)
parser.add_argument('--batch-file', type=str, default='')
parser.add_argument('--upload', type=bool, default=False)
parser.add_argument('--s3-bucket', type=str, default='s3://auto3d-datasets/ShapeNet/images')


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]




class Renderer:
    def __init__(self, model_dir, output_dir, tmp_dir):
        self.model_dir = model_dir
        self.output_dir = output_dir
        self.tmp_dir = tmp_dir

    def updateSPD(self, material, environment, model):
        inputPath = os.path.join(self.model_dir, model)
        outputPath = os.path.join(self.tmp_dir, model)
        os.system('./spd_xml_dump64 -r ' + inputPath)
        with open('__spd_index__.xml', 'r') as f:
            content = f.read()
            content = content.replace('#EnvironmentLibrary#studio_02', 'EnvironmentLibrary#' + environment)
            content = content.replace('Prism-113', material)
            with open('__spd_index__.xml', 'w') as f:
                f.write(content)

        os.system('./spd_xml_update64 ' + inputPath + ' __spd_index__.xml -o ' + outputPath)
        return outputPath

    def render(self, batchID, camera, material, environment, model):
        path = self.updateSPD(material, environment, model)
        output = os.path.join(self.output_dir, batchID,
                              model.split('.')[0] + '#' + camera + '#' + material + '#' + environment + '.exr')
        camera = float(camera)
        x = math.cos(camera)
        y = math.sin(camera)
        os.system(
            f'./vxrt --spp 180 --width=150 --height=150 --quality 35 --use-filter --auto-expose --scale-eye-distance --recenter --camera-override --camera-up="0 0 1" --camera-eye="{x} {y} 0.2" ' + path + ' --outfile ' + output)


def mkdir(path):
    print(f'make dir {path}')
    if not os.path.exists(path):
        os.system(f'mkdir {path}')


def upload(s3_bucket, output_dir, category):
    if s3_bucket != '':
        zipFile = os.path.join(output_dir, category)
        shutil.make_archive(zipFile, 'zip', outputPath)
        os.system(f'aws s3 cp {zipFile}.zip {s3_bucket}/{currentBatch}/')


if __name__ == '__main__':
    args = parser.parse_args()

    renderer = Renderer(args.model_dir, args.output_dir, args.tmp_dir)


    mkdir(args.output_dir)
    mkdir(args.tmp_dir)

    models = get_all_files(args.model_dir, "*.spd")
    print(models)

    for model in models:
        model = model.name

        if args.preview:
            renderer.render('', args.camera, args.material, args.environment, model)
        else:
            if args.batch_file == '':
                print('batch file cannot be empty')
            currentBatch = ''
            category = os.path.basename(args.model_dir)
            with open(args.batch_file, 'r') as f:
                for line in f:
                    batch, camera, material, environment, model = line[:-1].split(',')
                    if batch != currentBatch:
                        if currentBatch != '' and args.upload:
                            upload(args.s3_bucket, args.output_dir, category)
                        currentBatch = batch
                        outputPath = os.path.join(args.output_dir, currentBatch)
                        mkdir(outputPath)
                    renderer.render(batch, camera, material, environment, model)
            if currentBatch != '' and args.upload:
                upload(args.s3_bucket, args.output_dir, category)




