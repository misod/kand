import django_tables2 as tables
from .models import Person

class PersonTable(tables.Table):
    class Meta:
        model = Person
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}

#class PersonTable(tables.Table):
#    class Meta:
#        model = Person


#class PersonList(SingleTableView):
#    model = Person
#    table_class = PersonTable
