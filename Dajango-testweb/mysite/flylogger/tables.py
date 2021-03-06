import django_tables2 as tables
from django_tables2_reports.tables import TableReport
from django_tables2_reports.views import ReportTableView
from .models import FlightData
from .models import (Glider, TowPlane)

#class PersonTable(tables.Table):
#        name = tables.Column()
#        age = tables.Column()
#        class Meta:
#        model = Person
#        # add class="paleblue" to <table> tag
#        attrs = {'class': 'paleblue'}

class LoggTable(TableReport):
    glider = tables.Column(accessor = 'glider.glider_id')
    towing = tables.Column(accessor = 'towing.towing_id')
    glider_pilot = tables.Column(verbose_name ='Glider Pilot', accessor = 'glider_pilot.name')
    towing_pilot = tables.Column(verbose_name ='Towing Pilot',accessor = 'towing_pilot.name')

    #def render_glider(self,record):
    #    if record.glider.exists():
    #            return str([p.pk for p in record.glider.all()])
    class Meta :
        model = FlightData
        #model = Glider
        #exclude = ('max_height')
        attrs = {'class': 'paleblue'}

class GliderTable(tables.Table):
    class Meta:
        model = Glider
        attrs = {'class': 'paleblue'}


#class PersonTable(tables.Table):
#    class Meta:
#        model = Person


#class PersonList(SingleTableView):
#    model = Person
#    table_class = PersonTable
