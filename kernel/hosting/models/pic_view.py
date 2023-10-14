# -*- coding: utf-8 -*-


from flask_admin import expose
from flask_admin.model.template import macro



from hosting.models import PicturesAdmin


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
