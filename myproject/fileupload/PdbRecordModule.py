################################################################################################

class PdbRecord(object):                                          # any record in PDB file

      """ stores record from PDB file """

      def __init__(self, *args, **kwargs):

          """ constructs record from input string """

          self.s = str(*args, **kwargs)

      def Type(self):

          """ constructs record from input string """

          return self.s[(1-1):(6)]

