import os
from glob import glob
import filecmp


def _generate_file_name(name, ext='split', pad=4):
    """
    Yield new file string.

    Parameters
    ----------
    name : str
        Base name of the file.
    ext : str, optional
        Desired extension of the file name. Default is 'split'.
    pad : int, optional
        Desired zero-padding that will be added to the incremental file names.
        Default is 4.

    Returns
    -------
    generator
    """

    i = 0
    while True:
        old_name, old_ext = os.path.splitext(name)
        file_name = f'{old_name}{i:0{pad}d}{old_ext}.{ext}'
        i += 1
        yield file_name


def split(src, dst_dir=None, size=100000000):
    """
    Split file into smaller chunks and save to file.
    Parameters
    ----------
    src
    dst_dir
    size

    Returns
    -------
    None
    """

    src = os.path.realpath(src)
    if not os.path.exists(src):
        raise FileExistsError(src)

    f_name = os.path.basename(src)
    file_name = _generate_file_name(f_name)

    if dst_dir is not None:
        _, src_ext = os.path.splitext(src)
    else:
        dst_dir = os.path.dirname(src)

    file_counter = 0
    with open(src, 'rb') as infile:
        while True:
            chunk = infile.read(size)
            if chunk == b'':
                break
            else:
                file_counter += 1
            dst = os.path.realpath(os.path.join(dst_dir, next(file_name)))
            with open(dst, 'wb') as outfile:
                outfile.write(chunk)
                print(f'Data written to {dst}')

    print(f'{file_counter} file(s) written.')


def unsplit(search_pattern, dst, validate=False, orig_src=None):

    src_dir = os.path.realpath(os.path.dirname(search_pattern))
    if not os.path.exists(src_dir):
        raise NotADirectoryError(src_dir)

    search_pattern = os.path.realpath(search_pattern)
    if '*' not in search_pattern:
        raise ValueError(search_pattern)

    file_list = glob(search_pattern)

    if len(file_list) <= 0:
        raise FileNotFoundError(f'No files were found at {search_pattern}')

    # Extrapolate destination file name
    if not os.path.isfile(dst) and os.path.isdir(dst):
        dst_name = os.path.splitext(os.path.basename(search_pattern))[0].replace('*', '')
        dst_ext = os.path.splitext(os.path.splitext(os.path.basename(file_list[0]))[0])[-1]
        dst_name += '(unsplit)' + dst_ext
        dst = os.path.realpath(os.path.join(dst, dst_name))

    with open(dst, 'wb') as dst_file:
        for src in file_list:
            with open(src, 'rb') as src_file:
                data = src_file.read()
                dst_file.write(data)

    if validate:
        orig_src = os.path.realpath(orig_src)
        no_loss = filecmp.cmp(dst, orig_src)
        print(f'File reconstructed without loss: {no_loss}')

    print(f'File written to {dst}')
    return dst


__all__ = ['split', 'unsplit']

if __name__ == '__main__':
    src = 'C:/Users/markt/OneDrive/School/SDASL/Eglin_Summer_2020/EglinSummer2020/data/20200706/large/dataset.npz'
    dst_dir = 'C:/Users/markt/OneDrive/School/SDASL/Eglin_Summer_2020/EglinSummer2020/data/20200706/'
    split(src, dst_dir)

    recon_src = 'C:/Users/markt/OneDrive/School/SDASL/Eglin_Summer_2020/EglinSummer2020/data/20200706/dataset*.split'
    recon_dst = dst_dir
    unsplit(recon_src, recon_dst, validate=True, orig_src=src)
