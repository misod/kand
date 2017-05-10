from __future__ import unicode_literals
from fields import Fields
from django.contrib import admin
from import_export import resources
from flylogger.models import FlightData, Glider, TowPlane, Pilot
from flylogger.tables import LoggTable
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget






class FlightDataResource(resources.ModelResource):
    glider = fields.Field(
    column_name = 'glider',
    attribute = 'glider',
    widget =ForeignKeyWidget('Glider', 'glider_id'))

    towing = fields.Field(
    column_name = 'towing',
    attribute = 'towing',
    widget =ForeignKeyWidget('TowPlane', 'towing_id'))

    class Meta:
        model = FlightData
        exclude = ('flight_status')
        export_order= ('logged_date','flight_no','glider_pilot','glider','flight_type','takeoff','towing','towing_pilot','towing_landing','glider_landing','towing_height','towing_time','flight_time','notes','max_height')
        #fields = ('glider', 'towing',)



class FlightDataAdmin(ImportExportModelAdmin):
    resource_class = FlightDataResource


admin.site.register(FlightData, FlightDataAdmin)
admin.site.register(Glider)
admin.site.register(TowPlane)
admin.site.register(Pilot)

# Register your models here.
