import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from ipars import Pars


# --- exists ---

def test_exists_true(tmp_path):
    p = Pars()
    assert p.exists(str(tmp_path)) is True


def test_exists_false():
    p = Pars()
    assert p.exists('this_path_does_not_exist_xyz') is False


def test_exists_invalid_type():
    p = Pars()
    with pytest.raises(ValueError):
        p.exists(123)


# --- listdir ---

def test_listdir_returns_list(tmp_path):
    p = Pars()
    (tmp_path / 'a.txt').write_text('a')
    (tmp_path / 'b.txt').write_text('b')
    result = p.listdir(str(tmp_path))
    assert isinstance(result, list)
    assert 'a.txt' in result
    assert 'b.txt' in result


def test_listdir_invalid_type():
    p = Pars()
    with pytest.raises(ValueError):
        p.listdir(42)


# --- mkdir ---

def test_mkdir_creates_directory(tmp_path):
    p = Pars()
    new_dir = str(tmp_path / 'new_folder')
    p.mkdir(new_dir)
    assert (tmp_path / 'new_folder').exists()


def test_mkdir_does_not_raise_if_exists(tmp_path):
    p = Pars()
    existing = str(tmp_path)
    p.mkdir(existing)  # не должен бросать ошибку


def test_mkdir_invalid_type():
    p = Pars()
    with pytest.raises(ValueError):
        p.mkdir(99)


# --- returnBs4Object ---

def test_returnBs4Object(tmp_path):
    p = Pars()
    html_file = tmp_path / 'page.html'
    html_file.write_text('<html><body><h1>Hello</h1></body></html>', encoding='utf-8')

    soup = p.returnBs4Object(str(html_file))

    assert soup.find('h1').text == 'Hello'


def test_returnBs4Object_returns_beautifulsoup(tmp_path):
    p = Pars()
    html_file = tmp_path / 'page.html'
    html_file.write_text('<p>Test</p>', encoding='utf-8')

    result = p.returnBs4Object(str(html_file))

    assert isinstance(result, BeautifulSoup)


# --- getTexts ---

def _make_soup_elements(html: str) -> list:
    soup = BeautifulSoup(html, 'lxml')
    return soup.find_all('div')


def test_getTexts_basic():
    p = Pars()
    elements = _make_soup_elements('<div>Hello</div><div>World</div>')
    result = p.getTexts(elements)
    assert result == ['Hello', 'World']


def test_getTexts_needfix_strips_whitespace():
    p = Pars()
    elements = _make_soup_elements('<div>  Hello \n </div><div>\t World\t</div>')
    result = p.getTexts(elements, needFix=True)
    assert result == ['Hello', 'World']


def test_getTexts_returns_none_when_empty():
    p = Pars()
    elements = _make_soup_elements('<div></div>')
    result = p.getTexts(elements)
    assert result is None


def test_getTexts_invalid_type():
    p = Pars()
    with pytest.raises(ValueError):
        p.getTexts('not a list')


# --- getAttributes ---

def test_getAttributes_basic():
    p = Pars()
    soup = BeautifulSoup('<a href="http://a.com">1</a><a href="http://b.com">2</a>', 'lxml')
    elements = soup.find_all('a')
    result = p.getAttributes(elements, 'href')
    assert result == ['http://a.com', 'http://b.com']


def test_getAttributes_missing_attr():
    p = Pars()
    soup = BeautifulSoup('<div>no href</div>', 'lxml')
    elements = soup.find_all('div')
    result = p.getAttributes(elements, 'href')
    assert result is None


def test_getAttributes_invalid_type():
    p = Pars()
    with pytest.raises(ValueError):
        p.getAttributes('not a list', 'href')


# --- pprint ---

def test_pprint_does_not_raise(capsys):
    p = Pars()
    p.pprint({'key': 'value', 'list': [1, 2, 3]})
    captured = capsys.readouterr()
    assert 'key' in captured.out


# --- getStaticPage (с моком запроса) ---

def test_getStaticPage_saves_file(tmp_path):
    p = Pars()
    filepath = str(tmp_path / 'page.html')

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html><body>Mocked</body></html>'

    with patch('requests.get', return_value=mock_response):
        status = p.getStaticPage(filepath, 'http://example.com')

    assert status == 200
    assert (tmp_path / 'page.html').read_text(encoding='utf-8') == mock_response.text


def test_getStaticPage_binary_mode(tmp_path):
    p = Pars()
    filepath = str(tmp_path / 'image.png')

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'\x89PNG\r\n'

    with patch('requests.get', return_value=mock_response):
        status = p.getStaticPage(filepath, 'http://example.com/img.png', writeMethod='wb')

    assert status == 200
    assert (tmp_path / 'image.png').read_bytes() == mock_response.content


def test_getStaticPage_invalid_write_method(tmp_path):
    p = Pars()
    filepath = str(tmp_path / 'page.html')
    with pytest.raises(ValueError):
        p.getStaticPage(filepath, 'http://example.com', writeMethod='r')
