c.EnvironmentKernelSpecManager.conda_env_dirs=['~/.conda/envs']

import os
from subprocess import check_call

def post_save(model, os_path, contents_manager):
  if model['type'] != 'notebook':
    return
  d, fname = os.path.split(os_path)
  check_call(['jupyter', 'nbconvert', '--to', 'script', fname], cwd=d)
  check_call(['jupyter', 'nbconvert', '--to', 'html', fname], cwd=d)

c.FileContentsManager.post_save_hook = post_save
