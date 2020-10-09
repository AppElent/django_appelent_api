from django.core.management.base import BaseCommand
import random, os, json, re
from datetime import datetime
from dateutil import parser

def capitalizeFirst(key):
    key = key.replace('Serializer', '')
    return re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), key, 1)

class Command(BaseCommand):
    help = "seed database for testing and development."

    _COUNT = 0

    def get_template(self, name):
        return f"""
class {name}(serializers.Serializer):   
    \"\"\"  Description here \"\"\"
    """

    def add_arguments(self, parser):
        parser.add_argument('--string', type=str, help="JSON String")
        parser.add_argument('--application', type=str, help="Application name")

    def get_serializer_from_json(self, string, name):
        self._COUNT = self._COUNT + 1
        template = self.get_template(name)
        string = string.replace(': true', ': True')
        string = string.replace(': false', ': False')
        jsonobject = eval(string)
        if not isinstance(jsonobject, dict):
            return "Type of string is not dict but " + str(type(jsonobject))
        for key in jsonobject:
            value = jsonobject[key]
            #print(key, '->', jsonobject[key], type(jsonobject[key]))

            if isinstance(value, str):
                try:
                    d = parser.parse(value)
                except ValueError:
                    d = None
                if d is None:
                    template += f"\n    {key} = serializers.CharField()"
                else:
                    template += f"\n    {key} = serializers.DateTimeField()"
            elif isinstance(value, bool):
                template += f"\n    {key} = serializers.BooleanField()"
            elif isinstance(value, int):
                template += f"\n    {key} = serializers.IntegerField()"
            elif isinstance(value, list):
                first_element = value[0]
                if isinstance(first_element, str):
                    template += f"\n    {key} = serializers.ArrayField()"
                else:

                    newname = f"{capitalizeFirst(name)}{capitalizeFirst(key)}Serializer"
                    template += f"\n    {key} = {newname}()"
                    self.get_serializer_from_json(json.dumps(first_element), newname)
            elif isinstance(value, dict):
                newname = f"{capitalizeFirst(name)}{capitalizeFirst(key)}Serializer"
                template += f"\n    {key} = {newname}()"
                self.get_serializer_from_json(json.dumps(value), newname)
            else:
                raise Exception('Type niet herkend', key, value)
        print(template)

    def handle(self, *args, **options):
        string = options['string']
        name = options['application']
        if name is None:
            name = input('Enter name (e.g. ExampleSerializer)')
        if string is None:
            string = input('Enter JSON string')
        print('\n\nfrom rest_framework import serializers')
        self.get_serializer_from_json(string, name)

        #print(jsonobject['id'])


