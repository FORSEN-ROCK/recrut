from django.forms.widgets import MultiWidget, SelectMultiple, TextInput


class ManyToManyWidget(MultiWidget):
    template_name = 'widgets/many_to_many_widget.html'

    def __init__(self, choice_list=[], selected=[], attrs=None):
        widgets = [SelectMultiple(attrs={'size': 5,
                                         'maxlength': 50,
                                         'class': 'many_many'},
                                  choices=choice_list),
                   SelectMultiple(attrs={'size': 5,
                                         'maxlength': 50,
                                         'class': 'many_many'},
                                  choices=selected)
        ]
        super(ManyToManyWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.code, value.number]
        else:
            return ['', '']

class CalendarWidget(TextInput):

    def __init__(self, attrs={}):
        widgets = [TextInput(attrs={'class': 'vDateField'})]
        super(CalendarWidget, self).__init__(attrs={'class': 'vDateField',
                                                    'size': '10',
                                                    'type': 'date'})

    def format_output(self, rendered_widgets):
        return mark_safe(u'%s<br />%s' % (rendered_widgets[0]))