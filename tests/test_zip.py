import zipfile
import pytest
from ipars import ZipManager


def test_zipfile_creates_archive(tmp_path):
    zm = ZipManager()
    source = tmp_path / 'hello.txt'
    source.write_text('hello world')
    zip_path = str(tmp_path / 'output.zip')

    zm.zipFile(str(source), zip_path)

    assert (tmp_path / 'output.zip').exists()
    with zipfile.ZipFile(zip_path, 'r') as zf:
        assert 'hello.txt' in zf.namelist()


def test_zipfile_content_is_correct(tmp_path):
    zm = ZipManager()
    source = tmp_path / 'data.txt'
    source.write_text('test content')
    zip_path = str(tmp_path / 'output.zip')

    zm.zipFile(str(source), zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        content = zf.read('data.txt').decode('utf-8')
    assert content == 'test content'


def test_zipfolder_creates_archive(tmp_path):
    zm = ZipManager()
    folder = tmp_path / 'myfolder'
    folder.mkdir()
    (folder / 'a.txt').write_text('aaa')
    (folder / 'b.txt').write_text('bbb')
    zip_path = str(tmp_path / 'folder.zip')

    zm.zipFolder(str(folder), zip_path)

    assert (tmp_path / 'folder.zip').exists()
    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()
    assert any('a.txt' in n for n in names)
    assert any('b.txt' in n for n in names)


def test_zipfolder_nested(tmp_path):
    zm = ZipManager()
    folder = tmp_path / 'root'
    folder.mkdir()
    sub = folder / 'sub'
    sub.mkdir()
    (sub / 'deep.txt').write_text('deep')
    zip_path = str(tmp_path / 'nested.zip')

    zm.zipFolder(str(folder), zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()
    assert any('deep.txt' in n for n in names)


def test_set_compression_none():
    zm = ZipManager('none')
    assert zm.compression == zipfile.ZIP_STORED


def test_set_compression_normal():
    zm = ZipManager('normal')
    assert zm.compression == zipfile.ZIP_DEFLATED


def test_set_compression_hard():
    zm = ZipManager('hard')
    assert zm.compression == zipfile.ZIP_BZIP2


def test_set_compression_maximum():
    zm = ZipManager('maximum')
    assert zm.compression == zipfile.ZIP_LZMA


def test_invalid_compression_raises():
    with pytest.raises(ValueError):
        ZipManager('ultra')
