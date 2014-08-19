from django.contrib import admin
from pms_app.models import Position, PositionInstrument, PositionStock, PositionOption


# Register your models here.
admin.site.register(Position)
admin.site.register(PositionInstrument)
admin.site.register(PositionStock)
admin.site.register(PositionOption)