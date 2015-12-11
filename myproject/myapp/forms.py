# -*- coding: utf-8 -*-

from django import forms

class DocumentForm(forms.Form):

    """ File Input Form enabling upload of PDB file to be analyzed """

    docfile = forms.FileField(
        label='Select a PDB file oriented along membrane normal containing one chain only.'
    )
