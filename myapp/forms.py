# -*- coding: utf-8 -*-

from django import forms

FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)

class TMProteinFileForm(forms.Form):

    """ File Input Form enabling upload of PDB file to be analyzed """

    tmproteinfile = forms.FileField(
        label='Select a PDB file oriented along membrane normal containing one chain only.'
    )
#    BordersOfThinSlices = forms.CharField()

#    favorite_colors = forms.MultipleChoiceField(required=False, \
#    widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)

class ParametersForm(forms.Form):

    """ File Input Form enabling upload of PDB file to be analyzed """

    BordersOfThinSlices = forms.CharField()


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    favorite_colors = forms.MultipleChoiceField(required=False, \
    widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)