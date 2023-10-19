# -*- coding: utf-8 -*-

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField

import os
import random
import string
from PIL import Image
from io import BytesIO

from sqlalchemy.ext.declarative import declared_attr

from hosting import db

def random_string(length=8):
    """Генерация случайной строки заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

class Pictures(db.Model):
    """ Класс описывающий картинки """
    
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pic_data = db.Column(db.LargeBinary)
    file_path = db.Column(db.String)
    owner_id = db.Column(db.String)
    password = db.Column(db.String)
    is_one_view = db.Column(db.Boolean)
    view = db.Column(db.Integer, default=0)

class PicturesAdmin(ModelView):
    """ Класс описывающий поведение Pictures в админке """

    column_list = ('id', 'name', 'owner_id', 'password', 'is_one_view', 'view')
    column_searchable_list = ('id', 'name', 'owner_id')
    form_columns = ('name', 'pic_upload', 'owner_id', 'password', 'is_one_view')

    form_extra_fields = {
        'pic_upload': FileUploadField('Image', base_path='static/img', allow_overwrite=True)
    }

    def on_model_change(self, form, model, is_created):
        if form.pic_upload.data:
            try:
                # Прочтите загруженное изображение с использованием Pillow
                image = Image.open(form.pic_upload.data)
                
                # Создайте пустой буфер для сохранения изображения в формате PNG
                image_buffer = BytesIO()
                
                # Сохраните изображение в формате PNG в буфер
                image.save(image_buffer, format="PNG")
                
                # Сгенерируйте случайное имя файла
                random_filename = random_string() + '.png'
                
                # Сохраните данные изображения и новое имя файла в модели
                model.pic_data = image_buffer.getvalue()

                db.session.commit()
            except Exception as e:
                print(f"Ошибка при загрузке и обработке изображения: {str(e)}")
