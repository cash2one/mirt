# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str


class FilterWidget(object):
    def __init__(self, url=None):
        self.url = url
        self.features_dict = {}

    def get_features(self):
        new_list = []
        for key, value in sorted(self.features_dict.iteritems(), key=lambda item: item[1].order):
            new_list.append(value)
        return new_list

    def update_feature(self, **kwargs):
        if "name" in kwargs:
            feature = self.Feature(**kwargs)
            self.features_dict.update({kwargs["name"]: feature})
            return bool(feature.widget.query_string)
        else:
            raise self.FeatureNameError()

    class FeatureNameError(Exception):
        def __init__(self):
            self.value = "Feature name must be specified!"

        def __str__(self):
            return repr(self.value)

    class Widget(object):
        types = ("fader_double",
                 "select_box",
                 "checkbox")

        def __init__(self, widget_type, **kwargs):
            self.type = widget_type
            self.query_string = ""
            if widget_type == "fader_double":
                self.min = kwargs.get('min', 0)
                self.max = kwargs.get('max', 1)
                has_cur_min = False
                self.current_min = kwargs.get('current_min', self.min)
                self.current_max = kwargs.get('current_max', self.max)
                if smart_str(self.min) != smart_str(self.current_min):
                    has_cur_min = True
                    self.query_string += ("%s min=%s" % (kwargs["name"], self.current_min))
                if smart_str(self.max) != smart_str(self.current_max):
                    if has_cur_min:
                        self.query_string += "&"
                    self.query_string += ("%s max=%s" % (kwargs["name"], self.current_max))
            elif widget_type == "select_box":
                self.values = []
                all_values = kwargs.get('values', [])
                with_labels = kwargs.get('with_labels', False)
                selected_values = kwargs.get('selected_values', [])

                value = lambda x: x[0] if with_labels else x
                selected = lambda x: True if value(x) in selected_values else False
                label = lambda x: x[1] if with_labels else x
                for index, val in enumerate(all_values):
                    self.values.append({"value": value(val), "label": label(val), "selected": selected(val)})
                    if selected(val):
                        self.query_string += "%s=%s" % (kwargs["name"], value(val))
                        if 0 < index < len(all_values):
                            self.query_string += "&"

            elif widget_type == "checkbox":
                self.checked = bool(kwargs.get("checked", None))
                if self.checked:
                    self.query_string = "%s=on" % kwargs["name"]


        def __str__(self):
            return self.type

    class Feature(object):
        class WidgetNoTypeError(Exception):
            def __init__(self):
                self.value = "Feature widget type must be specified! Available types are %s" % \
                             map(str, FilterWidget.Widget.types)

            def __str__(self):
                return repr(self.value)

        class WidgetWrongTypeError(Exception):
            def __init__(self):
                self.value = "Wrong widget type! Available types are %s" % \
                             map(str, FilterWidget.Widget.types)

            def __str__(self):
                return repr(self.value)

        def __init__(self, **kwargs):
            if "type" in kwargs:
                if kwargs["type"] in FilterWidget.Widget.types:
                    widget_type = kwargs["type"]
                    self.name = kwargs["name"]
                    self.order = kwargs.get("order", 0)
                    self.label = kwargs.get("label", self.name)
                    self.type = widget_type
                    self.widget = FilterWidget.Widget(widget_type, **kwargs)

                else:
                    raise self.WidgetWrongTypeError()
            else:
                raise self.WidgetNoTypeError()

        def __str__(self):
            return smart_str(self.name)