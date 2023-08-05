# Copyright (c) 2017-2020 Fumito Hamamura <fumito.ham@gmail.com>

# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation version 3.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.

import pathlib
import zipfile
import tempfile
import io
import shutil
import locale
import os
import warnings


def get_archive_path(path: pathlib.Path, root: pathlib.Path):
    return str(path.resolve().relative_to(root).as_posix())


def make_parent_dir(path: pathlib.Path):

    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def make_root(root: pathlib.Path, is_zip: bool):
    if is_zip:
        with zipfile.ZipFile(root, "w"):
            pass
    else:
        root.mkdir(parents=True, exist_ok=True)


def find_zip_parent(path: pathlib.Path):
    """Return path to parent zip file.

    Check parent directories of a given path backwards and return
    a parent if its a path to a zip file. Returns :obj:`None`
    if no parent is a zip file.
    """
    p = path.resolve()
    while True:
        if p == p.parent:
            return None
        elif p.parent.exists():
            if p.parent.is_dir():
                p = p.parent
                continue
            elif zipfile.is_zipfile(p.parent):
                return p.parent
            else:
                raise ValueError("invalid path %s" % str(path))
        else:
            p = p.parent
            continue


def exists(path: pathlib.Path):

    root = find_zip_parent(path)

    if root:
        archive = get_archive_path(path, root)
        namelist = zipfile.ZipFile(root).namelist()
        if archive:
            if archive in namelist:
                return True
            elif archive + "/" in set(
                    n[:len(archive) + 1] for n in namelist):
                return True
            else:
                return False
        else:
            return True
    else:
        return path.exists()


def is_dir(path: pathlib.Path):

    root = find_zip_parent(path)

    if root:
        archive = get_archive_path(path, root)

        if archive:
            namelist = zipfile.ZipFile(root).namelist()
            if archive + "/" in set(
                    n[:len(archive) + 1] for n in namelist):
                return True
            else:
                return False
        else:
            return True
    else:
        return path.is_dir()


def _archive_exists(archive: str, file: zipfile.ZipFile):

    if archive not in file.namelist():
        return False
    else:
        warnings.warn(
            "'%s' already exists in %s" % (archive, str(file)))
        return True


def is_valid_archive_path(archive, file: zipfile.ZipFile):
    """Check archive is a valid file path

    Check if ``archive`` is not an existing dir in ``file``.
    Check if parents of ``archive`` are not paths to existing files.
    """
    archive = str(archive)

    if archive + "/" in set(n[:len(archive + "/")] for n in file.namelist()):
        return False

    for name in file.namelist():
        if name.split("/") == archive.split("/")[-1]:
            return False

    return True


def write_str(string: str, path: pathlib.Path,
                 encoding=None, newline=None):
    """Write string into a file under a directory or in a zip file."""

    write_file(lambda f: f.write(string), path, mode="t",
                 encoding=encoding, newline=newline)


def write_str_utf8(string: str, path: pathlib.Path):
    write_str(string, path, encoding="utf-8", newline="\n")


def pandas_to_pickle(obj, path: pathlib.Path):

    root = find_zip_parent(path)

    if root:
        with tempfile.TemporaryDirectory() as dirname:
            filepath = str(pathlib.Path(dirname).joinpath("temp"))
            obj.to_pickle(filepath)
            archive = get_archive_path(path, root)
            with zipfile.ZipFile(root, mode="a") as f:
                if not _archive_exists(archive, f):
                    if is_valid_archive_path(archive, f):
                        f.write(filepath, archive)
                    else:
                        raise ValueError("invalid archive '%s'" % archive)

    else:
        make_parent_dir(path)
        obj.to_pickle(str(path))


def write_file(callback, path: pathlib.Path, mode,
                 encoding=None, newline=None):

    if mode == "b":
        def encode(b): return b
    elif mode == "t":
        encoding = encoding or locale.getpreferredencoding()
        def encode(s): return s.encode(encoding)
    else:
        raise ValueError("invalid mode: %s" % mode)

    def get_io(mode):
        if mode == "b":
            return io.BytesIO()
        else:
            return io.StringIO(newline=newline or os.linesep)

    def open_path(mode):
        if mode == "b":
            return path.open("wb")
        else:
            return path.open("wt", encoding=encoding, newline=newline)

    root = find_zip_parent(path)

    if root:
        archive = get_archive_path(path, root)
        with get_io(mode) as buff:
            with zipfile.ZipFile(root, mode="a") as f:
                if not _archive_exists(archive, f):
                    if is_valid_archive_path(archive, f):
                        callback(buff)
                        buff.seek(0)
                        f.writestr(archive, encode(buff.read()))
                    else:
                        raise ValueError("invalid archive '%s'" % archive)

    else:
        make_parent_dir(path)
        with open_path(mode) as f:
            callback(f)


def copy_file(src, dst):

    root_src = find_zip_parent(src)
    root_dst = find_zip_parent(dst)

    if root_src and root_dst:

        arc_src = get_archive_path(src, root_src)
        arc_dst = get_archive_path(dst, root_dst)
        with zipfile.ZipFile(root_src, mode="r") as zip_src:
            with zip_src.open(arc_src, mode="r") as f_src:
                with zipfile.ZipFile(root_dst, mode="a") as zip_dst:
                    if not _archive_exists(arc_dst, zip_dst):
                        if is_valid_archive_path(arc_dst, zip_dst):
                            zip_dst.writestr(arc_dst, f_src.read())
                        else:
                            raise ValueError("invalid archive '%s'" % arc_dst)

    elif root_src and not root_dst:

        arc_src = get_archive_path(src, root_src)
        with zipfile.ZipFile(root_src, mode="r") as zip_src:
            with tempfile.TemporaryDirectory() as dirname:
                zip_src.extract(arc_src, path=dirname)
                make_parent_dir(dst)
                shutil.copyfile(
                    str(pathlib.Path(dirname) / arc_src),
                    str(pathlib.Path(dst))
                )

    elif not root_src and root_dst:

        arc_dst = get_archive_path(dst, root_dst)
        with zipfile.ZipFile(root_dst, mode="a") as zip_dst:
            if not _archive_exists(arc_dst, zip_dst):
                if is_valid_archive_path(arc_dst, zip_dst):
                    zip_dst.write(src, arc_dst)
                else:
                    raise ValueError("invalid archive '%s'" % arc_dst)

    elif not root_src and not root_dst:
        shutil.copyfile(str(src), str(dst))

    else:
        raise RuntimeError("must not happen")


def read_str(path: pathlib.Path, encoding=None, newline=None):

    return read_file(
        lambda f: f.read(), path, "t", encoding=encoding, newline=newline)


def read_str_utf8(path: pathlib.Path):
    return read_str(path, encoding="utf-8", newline="\n")


def read_file(callback, path: pathlib.Path, mode,
                encoding=None, newline=None):

    root = find_zip_parent(path)

    def open_path(mode):
        if mode == "b":
            return path.open("rb")
        else:
            return path.open("rt", encoding=encoding, newline=newline)

    if root:
        archive = get_archive_path(path, root)
        with zipfile.ZipFile(root, mode="r") as f_zip:
            with f_zip.open(archive, mode="r") as f_zipext:

                if mode == "t":
                    f = io.TextIOWrapper(
                        f_zipext, encoding=encoding,
                        newline=newline)
                else:
                    f = f_zipext

                return callback(f)
    else:
        with open_path(mode) as f:
            return callback(f)

