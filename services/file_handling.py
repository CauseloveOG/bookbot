import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

# Функция возвращает строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int] | None:
    symbols = (',', '.', '!', ':', ';', '?')
    txt = text[start:size + start]
    for i in range(len(txt) - 1, 0, -1):
        if txt[i] in symbols:
            if txt[i - 1] not in symbols:
                try:
                    if txt[i + 1] not in symbols:
                        txt = txt[:i + 1]
                        break
                finally:
                    txt = txt[:i + 1]
                    break
    return txt, len(txt)

# Функция формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as book_file:
        text = book_file.read()
    start = 0
    page = 1
    while start < len(text):
        page_text, cursor = _get_part_text(text, start, PAGE_SIZE)
        start += cursor
        if page_text.lstrip():
            book[page] = page_text.lstrip()
            page += 1

prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))