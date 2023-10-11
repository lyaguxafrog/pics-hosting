# -*- coding: utf-8 -*-

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField


from hosting import db

class Pictures(db.Model):
    """ Класс описывающий картинки """
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    pic_data = db.Column(db.LargeBinary)
    owner_id = db.Column(db.String)
    password = db.Column(db.String)
    is_one_view = db.Column(db.Boolean)
    view = db.Column(db.Integer)


class PicturesAdmin(ModelView):
    """ Класс описывающий поведение Pictures в админке """

    column_list = ('id', 'name', 'pic_data', 'pic_upload', 'owner_id', 'password', 'is_one_view', 'view')
    column_searchable_list = ('id', 'name', 'owner_id')
    form_columns = ('name', 'pic_data', 'pic_upload', 'owner_id', 'password', 'is_one_view')

    form_extra_fields = {
        'pic_upload': FileUploadField('Image', base_path='static/img', allow_overwrite=True)
    }

    def on_model_change(self, form, model, is_created):
        if form.pic_upload.data:
            # Сохраните данные изображения в поле pic_data
            model.pic_data = form.pic_upload.data.read()
