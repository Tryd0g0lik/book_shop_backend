# """
# persons/forms/widget/radio_field.py:1
# """
# from  typing import TypedDict
# from django import forms
#
# class DictForFieldHelpText(TypedDict):
#     choice_help_text: str
#
# class RadioFieldWithHelpText(forms.RadioSelect):
#     option_template_name = "templates/forms/multiple_radio.html"
#     def __init__(self, *args, **kwargs):
#         self.choice_help_text: dict | DictForFieldHelpText  = kwargs.pop("choice_help_text", {})
#         super().__init__(*args, **kwargs)
#
#
#     def create_option(self,  name, value, label, selected, index, subindex=None, attrs=None):
#         option = super().create_option( name, value, label, selected, index, subindex, attrs)
#         help_text = self.choice_help_text.get(value,None)
#         if help_text:
#             option['help_text'] = help_text
#         return option
#
