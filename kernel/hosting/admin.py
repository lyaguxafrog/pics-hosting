# -*- coding: utf-8 -*-

from flask import Flask

from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from flask_admin.menu import MenuLink

from flask_admin import expose
from flask_admin.model.template import macro

import os
from dotenv import load_dotenv, find_dotenv

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from hosting import app
from hosting import db
from hosting import login_manager

from hosting.models import (TelegramUser,
                        TelegramUserAdmin, Bot,
                        BotAdmin,Admins, AdminsAdmin,
                        Pictures, PicturesAdmin)


@login_manager.user_loader
def load_user(user_id):
    return Admins.query.get(int(user_id))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

class ImageView(PicturesAdmin):
    @expose('/view-image/<int:id>/')
    def view_image(self, id):
        picture = self.get_one(id)
        if picture:
            return self.render(
                'admin/view_image.html',
                picture=picture,
                macro=macro
            )


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(AdminsAdmin(Admins, db.session))
admin.add_view(TelegramUserAdmin(TelegramUser, db.session, name="Users"))
admin.add_view(ImageView(Pictures, db.session, name="Pictures"))
admin.add_view(BotAdmin(Bot, db.session, name="Bots"))


login_manager.init_app(app)
