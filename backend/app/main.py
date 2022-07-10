import tornado.ioloop
import tornado.web
import string
import random
import asynctnt
from tornado.template import Loader
from base64 import b64encode
from io import BytesIO
import cv2
from PIL import Image, ImageDraw, ImageFont
import io
import difflib


HOST = '37.139.42.4'
HOST_TARANTOOL = 'tarantool20_1'
SCHEMA = 'service_tarantool'
HOST_TARANTOOL = '127.0.0.1'


class ShortGenerator(tornado.web.RequestHandler):
    def get(self):
        # loader = Loader('template')
        # self.write(loader.load('index.html').generate(short_url=None, image=None))
        pass

    async def CalcImageHash(self, img):
        '''
        Метод вычисления уникального хэша изображения
        :param FileName:
        :return:
        '''
        with open('1.f', 'wb') as f:
            f.write(img)
        image = cv2.imread('1.f')
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        avg = gray_image.mean()
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)

        _hash = ""
        for x in range(8):
            for y in range(8):
                val = threshold_image[x, y]
                if val == 255:
                    _hash = _hash + "1"
                else:
                    _hash = _hash + "0"

        return _hash

    async def CompareHash(self, hash1, hash2):
        """
        Метод расчитывает расстояние Хемминга
        :param hash1:
        :param hash2:
        :return:
        """
        l = len(hash1)
        i = 0
        count = 0
        while i < l:
            if hash1[i] != hash2[i]:
                count = count + 1
            i = i + 1
        return count

    async def search_compare_image(self, img):
        """
        Метод сравнивает входное изображение со всем множеством хэшей в БД и находит ближайшее изображение
        Возвращает наиболее подходящее изображение
        :param img:
        :return:
        """
        conn = asynctnt.Connection(host=HOST_TARANTOOL, port=3301)
        await conn.connect()
        data = await conn.select(SCHEMA)
        img_hash = await self.CalcImageHash(img)
        min_compare = {'distance': 1000, 'id_image': -1, 'image': None, 'text_up': None, 'text_down': None}
        for values in data:
            compare_hash = await self.CompareHash(list(img_hash), list(values.get('hash_image')))
            if compare_hash < min_compare.get('distance'):
                min_compare['distance'] = compare_hash
                min_compare['id_image'] = values.get('id_image')
                min_compare['image'] = values.get('image_src')
                min_compare['text_up'] = values.get('text_up')
                min_compare['text_down'] = values.get('text_down')
            if min_compare.get('distance') == 0:
                break
        return min_compare.get('image').encode('latin-1'), min_compare.get('text_up'), min_compare.get('text_down')

    async def search_compare_text(self, text_up, text_down):
        """
        Метод сравнивает входной текст со всем множеством хэшей в БД и находит ближайшее изображение
        Возвращает наиболее подходящее изображение
        :param img:
        :return:
        """
        conn = asynctnt.Connection(host=HOST_TARANTOOL, port=3301)
        await conn.connect()
        search_1 = await conn.eval(f'''return indexed_pattern_search("service_tarantool", 3, "{text_up}")''')
        search_1_result = search_1.body[0]
        search_2 = await conn.eval(f'''return indexed_pattern_search("service_tarantool", 4, "{text_down}")''')
        search_2_result = search_2.body[0]
        await conn.disconnect()
        return search_1_result.get('image_src') or search_2_result.get('image_src'), text_up, text_down

    async def generate_random_meme(self):
        """
        Метод выбирает 2 рандомных мема в коллекции и создает новый
        :param img:
        :return:
        """
        conn = asynctnt.Connection(host=HOST_TARANTOOL, port=3301)
        await conn.connect()
        id_image = await conn.eval(f'''return box.space.service_tarantool:len()''')
        id_image = id_image.body[0]
        obj1 = await conn.select(SCHEMA, [random.randint(1, id_image)], index='pk')
        obj2 = await conn.select(SCHEMA, [random.randint(1, id_image)], index='pk')
        await conn.disconnect()
        return obj1[0].get('image_src').encode('latin-1'), obj2[0].get('text_up'), obj2[0].get('text_down')

    async def save_image(self, image, text_up, text_down):
        """
        метод сохранения изображений в БД
        :param image:
        :param text_up:
        :param text_down:
        :return:
        """
        conn = asynctnt.Connection(host=HOST_TARANTOOL, port=3301)
        await conn.connect()
        id_image = await conn.eval(f'''return box.space.service_tarantool:len()''')
        id_image = id_image.body[0] + 1
        image_hash = await self.CalcImageHash(image)
        await conn.insert(SCHEMA, [id_image, image.decode('latin-1'), f'{text_up} {text_down}', text_up, text_down, image_hash])
        await conn.disconnect()
        return id_image

    async def switch_set(self, image, text_up, text_down):
        if image and not text_up and not text_down:
            # Поиск по хэшу картинки
            image, text_up, text_down = await self.search_compare_image(image)
            # await self.save_image(image, text_up, text_down)
        elif not image and (text_up or text_down):
            # Поиск по тексту
            image, text_up, text_down = await self.search_compare_text(text_up, text_down)
            pass
        elif not image and not(text_up or text_down):
            # генерация рандомного мема
            image, text_up, text_down = await self.generate_random_meme()
        elif image and text_up and text_down:
            # проверяем если уже имеется, возвращаем ID иначе записываем:
            pass
        id_image = await self.save_image(image, text_up, text_down)
        return id_image

    async def post(self):
        image = self.request.arguments.get('image')[0] if self.request.arguments.get('image') else None
        text_up = self.request.arguments.get('text_up')[0].decode() if self.request.arguments.get('text_up') else ''
        text_down = self.request.arguments.get('text_down')[0].decode() if self.request.arguments.get('text_down') else ''
        data = await self.switch_set(image, text_up, text_down)
        conn = asynctnt.Connection(host=HOST_TARANTOOL, port=3301)
        await conn.connect()
        self.write(str(data))


class ImageReader(tornado.web.RequestHandler):
    async def get(self, id_image):
        """
        Метод получает из БД выбранное изображение и возвращает в API

        :param id_image:
        :return:
        """
        conn = asynctnt.Connection(host=HOST_TARANTOOL, port=3301)
        await conn.connect()
        data = await conn.select(SCHEMA, [int(id_image)], index='pk')
        await conn.disconnect()
        image = await self.add_text_in_image(data[0].get('image_src'), data[0].get('text_up'), data[0].get('text_down'))

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        b64 = b64encode(buffered.getvalue())
        self.write(f'<img src="data:image/png;base64, {b64.decode()}">')  # возможно нужно вернуть данные изображения

    async def add_text_in_image(self, img, text_up, text_down):
        """
        Метод добавляет водяной знак команды + текст снизу и сверху
        :param img:
        :return:
        """
        def add_text(img_src, text, width=150, height=200):
            draw_text = ImageDraw.Draw(img_src)
            position = (img_src.width - width,
                        img_src.height - height)
            font = ImageFont.truetype('1.ttf', size=22)
            draw_text.text(
                position,
                text,
                font=font
                # fill='#1C0606'
            )

        with open('2.f', 'wb') as f:
            f.write(img.encode('latin-1'))
        im = Image.open('2.f')
        add_text(im, '[LIFE] Laboratory', im.width * 0.4, im.height * 0.95)
        if text_up:
            add_text(im, text_up, im.width * 0.6, im.height * 0.3)
        if text_down:
            add_text(im, text_down, im.width * 0.6, im.height * 0.85)
        return im


def make_app():
    return tornado.web.Application([
        (r"/", ShortGenerator),
        (r"/get/(.*)", ImageReader),
        (r"/set", ShortGenerator),
    ])


def _create_database():
    import tarantool
    conn = tarantool.Connection(host=HOST_TARANTOOL, port=3301)
    conn.connect()
    try:
        conn.eval('''box.schema.space.create('service_tarantool')''')
        conn.eval('''
box.space.service_tarantool:format({
  { name = 'id_image', type = 'number'}, 
  {name = 'image_src', type = 'string'}, 
  {name = 'text_full', type = 'string'}, 
  {name = 'text_up', type = 'string'}, 
  {name = 'text_down', type = 'string'}, 
  {name = 'hash_image', type = 'string'}
})''')
        conn.eval('''
box.space.service_tarantool:create_index('pk', {
  type = 'tree',
  parts = {
   { field = 'id_image', type = 'number'}
  }
})''')

        conn.eval('''
box.space.service_tarantool:create_index('hash_search', {
  type = 'tree', 
  parts = {'hash'}
})''')
        conn.eval('''
-- поиск по шаблону текста
function indexed_pattern_search(space_name, field_no, pattern)
  -- СМ. ПРИМЕЧАНИЕ №1 "ПОИСК НУЖНОГО ИНДЕКСА"
  if (box.space[space_name] == nil) then
    print("Error: Failed to find the specified space")
    return nil
  end
  local index_no = -1
  for i=0,box.schema.INDEX_MAX,1 do
    if (box.space[space_name].index[i] == nil) then break end
    if (box.space[space_name].index[i].type == "TREE"
        and box.space[space_name].index[i].parts[1].fieldno == field_no
        and (box.space[space_name].index[i].parts[1].type == "scalar"
        or box.space[space_name].index[i].parts[1].type == "string")) then
      index_no = i
      break
    end
  end
  if (index_no == -1) then
    print("Error: Failed to find an appropriate index")
    return nil
  end
  -- СМ. ПРИМЕЧАНИЕ №2 "ПОЛУЧЕНИЕ КЛЮЧА ИНДЕКСНОГО ПОИСКА ИЗ ШАБЛОНА"
  local index_search_key = ""
  local index_search_key_length = 0
  local last_character = ""
  local c = ""
  local c2 = ""
  for i=1,string.len(pattern),1 do
    c = string.sub(pattern, i, i)
    if (last_character ~= "%") then
      if (c == '^' or c == "$" or c == "(" or c == ")" or c == "."
                   or c == "[" or c == "]" or c == "*" or c == "+"
                   or c == "-" or c == "?") then
        break
      end
      if (c == "%") then
        c2 = string.sub(pattern, i + 1, i + 1)
        if (string.match(c2, "%p") == nil) then break end
        index_search_key = index_search_key .. c2
      else
        index_search_key = index_search_key .. c
      end
    end
    last_character = c
  end
  index_search_key_length = string.len(index_search_key)
  if (index_search_key_length < 3) then
    print("Error: index search key " .. index_search_key .. " is too short")
    return nil
  end
  -- СМ. ПРИМЕЧАНИЕ №3 "ВНЕШНИЙ ЦИКЛ: НАЧАЛО"
  local result_set = {}
  local number_of_tuples_in_result_set = 0
  local previous_tuple_field = ""
  while true do
    local number_of_tuples_since_last_yield = 0
    local is_time_for_a_yield = false
    -- СМ. ПРИМЕЧАНИЕ №4 "ВНУТРЕННИЙ ЦИКЛ: ИТЕРАТОР"
    for _,tuple in box.space[space_name].index[index_no]:
    pairs(index_search_key,{iterator = box.index.GE}) do
      -- СМ. ПРИМЕЧАНИЕ №5 "ВНУТРЕННИЙ ЦИКЛ: ПРЕРЫВАНИЕ, ЕСЛИ КЛЮЧ ИНДЕКСА СЛИШКОМ БОЛЬШОЙ"
      if (string.sub(tuple[field_no], 1, index_search_key_length)
      > index_search_key) then
        break
      end
      -- СМ. ПРИМЕЧАНИЕ №6 "ВНУТРЕННИЙ ЦИКЛ: ПРЕРЫВАНИЕ ПОСЛЕ КАЖДЫХ ДЕСЯТИ КОРТЕЖЕЙ -- ВОЗМОЖНО"
      number_of_tuples_since_last_yield = number_of_tuples_since_last_yield + 1
      if (number_of_tuples_since_last_yield >= 10
          and tuple[field_no] ~= previous_tuple_field) then
        index_search_key = tuple[field_no]
        is_time_for_a_yield = true
        break
        end
      previous_tuple_field = tuple[field_no]
      -- СМ. ПРИМЕЧАНИЕ №7 "ВНУТРЕННИЙ ЦИКЛ: ДОБАВЛЕНИЕ В РЕЗУЛЬТАТ, ЕСЛИ ШАБЛОН СОВПАДЕТ"
      if (string.match(tuple[field_no], pattern) ~= nil) then
        number_of_tuples_in_result_set = number_of_tuples_in_result_set + 1
        result_set[number_of_tuples_in_result_set] = tuple
        return result_set
      end
    end
    -- СМ. ПРИМЕЧАНИЕ №8 "ВНЕШНИЙ ЦИКЛ: ПРЕРЫВАНИЕ ИЛИ ПЕРЕДАЧА УПРАВЛЕНИЯ И ПРОДОЛЖЕНИЕ"
    if (is_time_for_a_yield ~= true) then
      break
    end
    require('fiber').yield()
  end
  return result_set
end''')
        conn.eval('''box.space.service_20:create_index('url', {type = 'tree', parts = {'url'}});''')
        conn.eval('''box.space.service_20:create_index('short', {type = 'tree', parts = {'short_url'}});''')
    except:
        pass
    conn.eval('''
    -- поиск по шаблону текста
    function indexed_pattern_search(space_name, field_no, pattern)
      -- СМ. ПРИМЕЧАНИЕ №1 "ПОИСК НУЖНОГО ИНДЕКСА"
      if (box.space[space_name] == nil) then
        print("Error: Failed to find the specified space")
        return nil
      end
      local index_no = -1
      for i=0,box.schema.INDEX_MAX,1 do
        if (box.space[space_name].index[i] == nil) then break end
        if (box.space[space_name].index[i].type == "TREE"
            and box.space[space_name].index[i].parts[1].fieldno == field_no
            and (box.space[space_name].index[i].parts[1].type == "scalar"
            or box.space[space_name].index[i].parts[1].type == "string")) then
          index_no = i
          break
        end
      end
      if (index_no == -1) then
        print("Error: Failed to find an appropriate index")
        return nil
      end
      -- СМ. ПРИМЕЧАНИЕ №2 "ПОЛУЧЕНИЕ КЛЮЧА ИНДЕКСНОГО ПОИСКА ИЗ ШАБЛОНА"
      local index_search_key = ""
      local index_search_key_length = 0
      local last_character = ""
      local c = ""
      local c2 = ""
      for i=1,string.len(pattern),1 do
        c = string.sub(pattern, i, i)
        if (last_character ~= "%") then
          if (c == '^' or c == "$" or c == "(" or c == ")" or c == "."
                       or c == "[" or c == "]" or c == "*" or c == "+"
                       or c == "-" or c == "?") then
            break
          end
          if (c == "%") then
            c2 = string.sub(pattern, i + 1, i + 1)
            if (string.match(c2, "%p") == nil) then break end
            index_search_key = index_search_key .. c2
          else
            index_search_key = index_search_key .. c
          end
        end
        last_character = c
      end
      index_search_key_length = string.len(index_search_key)
      if (index_search_key_length < 3) then
        print("Error: index search key " .. index_search_key .. " is too short")
        return nil
      end
      -- СМ. ПРИМЕЧАНИЕ №3 "ВНЕШНИЙ ЦИКЛ: НАЧАЛО"
      local result_set = {}
      local number_of_tuples_in_result_set = 0
      local previous_tuple_field = ""
      while true do
        local number_of_tuples_since_last_yield = 0
        local is_time_for_a_yield = false
        -- СМ. ПРИМЕЧАНИЕ №4 "ВНУТРЕННИЙ ЦИКЛ: ИТЕРАТОР"
        for _,tuple in box.space[space_name].index[index_no]:
        pairs(index_search_key,{iterator = box.index.GE}) do
          -- СМ. ПРИМЕЧАНИЕ №5 "ВНУТРЕННИЙ ЦИКЛ: ПРЕРЫВАНИЕ, ЕСЛИ КЛЮЧ ИНДЕКСА СЛИШКОМ БОЛЬШОЙ"
          if (string.sub(tuple[field_no], 1, index_search_key_length)
          > index_search_key) then
            break
          end
          -- СМ. ПРИМЕЧАНИЕ №6 "ВНУТРЕННИЙ ЦИКЛ: ПРЕРЫВАНИЕ ПОСЛЕ КАЖДЫХ ДЕСЯТИ КОРТЕЖЕЙ -- ВОЗМОЖНО"
          number_of_tuples_since_last_yield = number_of_tuples_since_last_yield + 1
          if (number_of_tuples_since_last_yield >= 10
              and tuple[field_no] ~= previous_tuple_field) then
            index_search_key = tuple[field_no]
            is_time_for_a_yield = true
            break
            end
          previous_tuple_field = tuple[field_no]
          -- СМ. ПРИМЕЧАНИЕ №7 "ВНУТРЕННИЙ ЦИКЛ: ДОБАВЛЕНИЕ В РЕЗУЛЬТАТ, ЕСЛИ ШАБЛОН СОВПАДЕТ"
          if (string.match(tuple[field_no], pattern) ~= nil) then
            number_of_tuples_in_result_set = number_of_tuples_in_result_set + 1
            result_set[number_of_tuples_in_result_set] = tuple
            return result_set
          end
        end
        -- СМ. ПРИМЕЧАНИЕ №8 "ВНЕШНИЙ ЦИКЛ: ПРЕРЫВАНИЕ ИЛИ ПЕРЕДАЧА УПРАВЛЕНИЯ И ПРОДОЛЖЕНИЕ"
        if (is_time_for_a_yield ~= true) then
          break
        end
        require('fiber').yield()
      end
      return result_set
    end''')


if __name__ == "__main__":
    _create_database()
    app = make_app()
    app.listen(12342, address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()


'''
s = box.schema.space.create('service_20')
s:format({{name = 'id', type = 'int'}, {name = 'url', type = 'string'}, {name = 'short_url', type = 'string'}})
s:create_index('short_url', {type = 'tree', parts = {'url'}})
s:create_index('short_url', {type = 'tree', parts = {'short_url'}})
'''

'''
s = box.schema.space.create('service_tarantool')
s:format({
  { name = 'id_image', type = 'number'}, 
  {name = 'image_src', type = 'string'}, 
  {name = 'text_full', type = 'string'}, 
  {name = 'text_up', type = 'string'}, 
  {name = 'text_down', type = 'string'}, 
  {name = 'hash_image', type = 'string'}
})
s:create_index('pk', {
  type = 'tree',
  parts = {
   { field = 'id_image', type = 'number'}
  }
}) 

s:create_index('text_full_search', {
  type = 'tree', 
  parts = {
    {'text_up'},
    {'text_down'}
  }
})

s:create_index('hash_search', {
  type = 'tree', 
  parts = {'hash'}
})

indexed_pattern_search("service_tarantool", 3, "TEXT")

-- поиск по шаблону текста
function indexed_pattern_search(space_name, field_no, pattern)
  -- СМ. ПРИМЕЧАНИЕ №1 "ПОИСК НУЖНОГО ИНДЕКСА"
  if (box.space[space_name] == nil) then
    print("Error: Failed to find the specified space")
    return nil
  end
  local index_no = -1
  for i=0,box.schema.INDEX_MAX,1 do
    if (box.space[space_name].index[i] == nil) then break end
    if (box.space[space_name].index[i].type == "TREE"
        and box.space[space_name].index[i].parts[1].fieldno == field_no
        and (box.space[space_name].index[i].parts[1].type == "scalar"
        or box.space[space_name].index[i].parts[1].type == "string")) then
      index_no = i
      break
    end
  end
  if (index_no == -1) then
    print("Error: Failed to find an appropriate index")
    return nil
  end
  -- СМ. ПРИМЕЧАНИЕ №2 "ПОЛУЧЕНИЕ КЛЮЧА ИНДЕКСНОГО ПОИСКА ИЗ ШАБЛОНА"
  local index_search_key = ""
  local index_search_key_length = 0
  local last_character = ""
  local c = ""
  local c2 = ""
  for i=1,string.len(pattern),1 do
    c = string.sub(pattern, i, i)
    if (last_character ~= "%") then
      if (c == '^' or c == "$" or c == "(" or c == ")" or c == "."
                   or c == "[" or c == "]" or c == "*" or c == "+"
                   or c == "-" or c == "?") then
        break
      end
      if (c == "%") then
        c2 = string.sub(pattern, i + 1, i + 1)
        if (string.match(c2, "%p") == nil) then break end
        index_search_key = index_search_key .. c2
      else
        index_search_key = index_search_key .. c
      end
    end
    last_character = c
  end
  index_search_key_length = string.len(index_search_key)
  if (index_search_key_length < 3) then
    print("Error: index search key " .. index_search_key .. " is too short")
    return nil
  end
  -- СМ. ПРИМЕЧАНИЕ №3 "ВНЕШНИЙ ЦИКЛ: НАЧАЛО"
  local result_set = {}
  local number_of_tuples_in_result_set = 0
  local previous_tuple_field = ""
  while true do
    local number_of_tuples_since_last_yield = 0
    local is_time_for_a_yield = false
    -- СМ. ПРИМЕЧАНИЕ №4 "ВНУТРЕННИЙ ЦИКЛ: ИТЕРАТОР"
    for _,tuple in box.space[space_name].index[index_no]:
    pairs(index_search_key,{iterator = box.index.GE}) do
      -- СМ. ПРИМЕЧАНИЕ №5 "ВНУТРЕННИЙ ЦИКЛ: ПРЕРЫВАНИЕ, ЕСЛИ КЛЮЧ ИНДЕКСА СЛИШКОМ БОЛЬШОЙ"
      if (string.sub(tuple[field_no], 1, index_search_key_length)
      > index_search_key) then
        break
      end
      -- СМ. ПРИМЕЧАНИЕ №6 "ВНУТРЕННИЙ ЦИКЛ: ПРЕРЫВАНИЕ ПОСЛЕ КАЖДЫХ ДЕСЯТИ КОРТЕЖЕЙ -- ВОЗМОЖНО"
      number_of_tuples_since_last_yield = number_of_tuples_since_last_yield + 1
      if (number_of_tuples_since_last_yield >= 10
          and tuple[field_no] ~= previous_tuple_field) then
        index_search_key = tuple[field_no]
        is_time_for_a_yield = true
        break
        end
      previous_tuple_field = tuple[field_no]
      -- СМ. ПРИМЕЧАНИЕ №7 "ВНУТРЕННИЙ ЦИКЛ: ДОБАВЛЕНИЕ В РЕЗУЛЬТАТ, ЕСЛИ ШАБЛОН СОВПАДЕТ"
      if (string.match(tuple[field_no], pattern) ~= nil) then
        number_of_tuples_in_result_set = number_of_tuples_in_result_set + 1
        result_set[number_of_tuples_in_result_set] = tuple
      end
    end
    -- СМ. ПРИМЕЧАНИЕ №8 "ВНЕШНИЙ ЦИКЛ: ПРЕРЫВАНИЕ ИЛИ ПЕРЕДАЧА УПРАВЛЕНИЯ И ПРОДОЛЖЕНИЕ"
    if (is_time_for_a_yield ~= true) then
      break
    end
    require('fiber').yield()
  end
  return result_set
end
'''
