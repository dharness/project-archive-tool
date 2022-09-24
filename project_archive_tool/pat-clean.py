from pathlib import Path
import argparse


def get_blend1_files(project_path):
  for path in Path(project_path).rglob('*.blend1'):
    print(path)


def get_ae_files(project_path):
  for path in Path(project_path).rglob('**/Adobe After Effects Auto-Save/*'):
    print(path)

def get_pr_files(project_path):
  for path in Path(project_path).rglob('**/Adobe Premiere Pro Auto-Save/*'):
    print(path)
  for path in Path(project_path).rglob('**/Adobe Premiere Pro Audio Previews/*'):
    print(path)

def main(project_path):
  # files = get_blend1_files(project_path)
  # files = get_ae_files(project_path)
  files = get_pr_files(project_path)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="P.A.T. -  Project Archive Tool")
  parser.add_argument("project_path", type=str)

  args = parser.parse_args()
  main(args.project_path)
