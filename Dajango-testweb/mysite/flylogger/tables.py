import django_tables2 as tables
from .models import FlightData

#class PersonTable(tables.Table):
#        name = tables.Column()
#        age = tables.Column()
#        class Meta:
#        model = Person
#        # add class="paleblue" to <table> tag
#        attrs = {'class': 'paleblue'}

class LoggTable(tables.Table):
    flight_no = tables.Column()
    class Meta :
        model = FlightData
        attrs = {'class': 'paleblue'}



#class PersonTable(tables.Table):
#    class Meta:
#        model = Person


#class PersonList(SingleTableView):
#    model = Person
#    table_class = PersonTable
