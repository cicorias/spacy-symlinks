
import sys, os
from pathlib import Path

is_windows = sys.platform.startswith('win')
is_linux = sys.platform.startswith('linux')
is_osx = sys.platform == 'darwin'

# See: https://github.com/benjaminp/six/blob/master/six.py
is_python2 = sys.version_info[0] == 2
is_python3 = sys.version_info[0] == 3
is_python_pre_3_5 = is_python2 or (is_python3 and sys.version_info[1] < 5)

if is_python2:
  def path2str(path): return str(path).decode('utf8')

elif is_python3:
  def path2str(path): return str(path)


def symlink_to(link, target):
  if is_windows:
    import subprocess
    subprocess.call(['mklink', '/d', path2str(link),
                    path2str(target)], shell=True)
  else:
    link.symlink_to(target)


def symlink_remove(link):
  if(os.path.isdir( path2str(link))): # this should only be on Py2.7.
    os.rmdir( path2str(link))
  else:
    os.unlink(path2str(link))

  # if is_windows and is_python3:
  #   if link.exists() and link.is_symlink():
  #     link.unlink()
  # elif is_windows and link.exists(): # is_symlink fails on Py27
  #   os.rmdir( path2str(link) )
  #   link.unlink()
  # elif is_windows:
  #   raise NotImplementedError('cannot unlink as neither exists nor is symlink or not windows')
  # else:
  #   link.unlink()