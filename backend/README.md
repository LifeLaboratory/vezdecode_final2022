# vezdecode_final2022

Post-запрос set с тремя параметрами — исходным изображением, текстом в 
верхней части мема и текстом в нижней части мема. В ответ на этот запрос бэкенд должен возвращать число — 
идентификатор итогового мема.

Get-запрос get с одним параметром — идентификатором загруженного ранее мема. 
В ответ сервер должен возвращать изображение со встроенным текстом (!).

## Структура API
``` json
/set - POST
Входные:
image - text - изображение
text_up - text - текст сверху мема
text_down - text - текст снизу мемам 
Выходные: 
id_image - int


/get?<id:int> - GET
Выходные:
image - text - изображение 
```

## База данных
```
id_image - ID изображения
image_src - исходное изображение
text_full - полный текст
text_up - текст сверху мема
text_down - текст снизу мема
hash_image - хэш изображения для поиска одинаковых - 
```

## Логика работы
```
SET - пользователь загружает исходное изображение и текст, который хочет отобразить на изображение.
1. Если не задан параметр image - тогда находим готовые изображения с близким по смыслу текстом
2. Если не заданы параметры text_up/text_down - находим похожие изображения и возвращаем с готовым текстом

Потребуется:
1. Поиск по шаблону - https://www.tarantool.io/ru/doc/latest/tutorials/lua_tutorials/#indexed-pattern-search
1.1 https://www.tarantool.io/ru/doc/latest/tutorials/lua_tutorials/#c-lua-tutorial-indexed-pattern-search
2. Вывод данных - https://www.tarantool.io/ru/doc/latest/reference/reference_lua/box_space/select/#box-space-select
3. Поиск одинаковых изображений - https://wiki.programstore.ru/python-sravnenie-kartinok/
4. Добавление текста/картинки на изображение - https://fixmypc.ru/post/vstavka-teksta-i-izobrazheniia-v-kartinku-s-python-pillow-pil/
```