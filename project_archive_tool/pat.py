import os
import tarfile
from types import SimpleNamespace
import argparse
from urllib.parse import urlparse
from pathlib import Path

import yaml
from tqdm import tqdm
import boto3
from botocore.exceptions import ClientError
from send2trash import send2trash

CONFIG_PATH = Path("./pat-config.yaml")
S3_CONSOLE_PATH = "https://s3.console.aws.amazon.com/s3/object/{bucket}?region={region}&prefix={key}"
script_path = Path(__file__).absolute()


def load_config():
  with open(CONFIG_PATH) as infile:
    config = yaml.safe_load(infile)
    return config


def get_upload_size(source_dir):
  root_directory = Path(source_dir)
  return sum(f.stat().st_size for f in root_directory.glob('**/*')
             if f.is_file())


def make_tarfile(source_dir):
  output_filename = f"{source_dir}.tar.gz"
  upload_size = get_upload_size(source_dir)
  with tqdm(total=upload_size) as pbar:

    def update_tar_progress(tar_info):
      pbar.update(tar_info.size)
      return tar_info

    with tarfile.open(output_filename, "w:gz") as tar:
      tar.add(source_dir,
              arcname=os.path.basename(source_dir),
              filter=update_tar_progress)
      return Path(tar.name)


def get_bucket_from_s3_url(s3_url):
  obj = urlparse(s3_url, allow_fragments=False)
  return obj.netloc


def upload_archive(config, archive_path):
  bucket = get_bucket_from_s3_url(config["project_dest"])
  s3 = boto3.client('s3')
  key = archive_path.parts[-1]
  filename = str(archive_path.resolve())
  file_size = os.stat(filename).st_size

  try:
    with tqdm(total=file_size, unit="B", unit_scale=True, desc=key) as pbar:
      response = s3.upload_file(
          Filename=filename,
          Bucket=bucket,
          Key=key,
          Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
      )
    region = s3.meta.region_name
    print("[SUCCESS] Archive available at:")
    print(S3_CONSOLE_PATH.format(bucket=bucket, key=key, region=region))
  except ClientError as e:
    print(e)
    return False
  return True


def main(project_path, do_clean):
  config = load_config()
  project_path = Path(project_path)

  if project_path is None:
    raise Exception("Invalid project name")

  print('Creating archive...')
  tar_path = make_tarfile(project_path)
  print('[SUCCESS] Archive created')
  upload_archive(config, tar_path)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="P.A.T. -  Project Archive Tool")
  parser.add_argument("project_path", type=str)
  parser.add_argument("--clean", action=argparse.BooleanOptionalAction)

  args = parser.parse_args()
  main(args.project_path, args.clean)
