import os
from pathlib import Path
from utils.symlinks import symlink_to, symlink_remove

import pytest

def target_local_path():
  return './foo-target'

def link_local_path():
  return './foo-symlink'


@pytest.fixture(scope='function')
def setup_target(request):
  target = Path(target_local_path())
  if target.exists():
    print('target exists skipping mkdir')
  else:
    print('creating temp dir for test')
    os.mkdir(target)
    target.exists()

  # yield -- need to cleanup even if assertion fails
  # https://github.com/pytest-dev/pytest/issues/2508#issuecomment-309934240
  def cleanup():  
    symlink_remove(Path(link_local_path()))
    print('removing target link')
    os.rmdir(target)
    print('done')

  request.addfinalizer(cleanup)


def test_create_symlink_windows(setup_target):
  target = Path(target_local_path())
  link = Path(link_local_path())
  assert target.exists()

  symlink_to(link, target)

  assert link.exists()
  assert link.is_symlink()
