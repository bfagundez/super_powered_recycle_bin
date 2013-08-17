# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the 
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# Written by: David Lanstein ( dlanstein gmail com )


from base import SforceBaseClient
import ipdb
import string
import cProfile
import suds.sudsobject


class SforcePartnerClient(SforceBaseClient):
  def __init__(self, wsdl, *args, **kwargs):
    super(SforcePartnerClient, self).__init__(wsdl, *args, **kwargs)

  # Toolkit-specific calls
  # Added a sub record stringify (this allow inner query results)
  def _stringifySubRecord(self, rec):
      if rec:
        for k, v in rec:
          if k != 'type':
            # if is an EMPTY array, set as None
            if v != None:
              if v == []:
                setattr(rec, k, None)
              else:
                setattr(rec, k, v[0])  
          
          v = getattr(rec, k)

          if isinstance(v, suds.sudsobject.Object):

            v = self._stringifySubRecord(v)
            setattr(rec, k, v)

        return rec
      else:
        pass


  def _stringifyResultRecords(self, struct):
  
    if not isinstance(struct, list):
      struct = [struct]
      originallyList = False
    else:
      originallyList = True

    for record in struct:
      for k, v in record:
        # types are strings by default
        if k != 'type':
          # if is an EMPTY array, set as None
          if v != None:
            if v == []:
              setattr(record, k, None)
            else:
              setattr(record, k, v[0] )
        # refresh v
        v = getattr(record, k)
        
        if isinstance(v, suds.sudsobject.Object):
          
          if v.__contains__('size'):
            for item in v.records:
              item = self._stringifySubRecord(item)
          else:  
            v = self._stringifyResultRecords(v)

    if originallyList:
      return struct
    else:
      return struct[0]

  # Core calls

  def convertLead(self, leadConverts):
    xml = self._marshallSObjects(leadConverts)
    return super(SforcePartnerClient, self).convertLead(xml)

  def merge(self, sObjects):
    xml = self._marshallSObjects(sObjects)
    return super(SforcePartnerClient, self).merge(xml)

  def process(self, sObjects):
    xml = self._marshallSObjects(sObjects)
    return super(SforcePartnerClient, self).process(xml)

  def query(self, queryString):

    queryResult = super(SforcePartnerClient, self).query(queryString)
    if queryResult.size > 0:
      queryResult.records = self._stringifyResultRecords(queryResult.records)
    return queryResult

  def queryAll(self, queryString):
    queryResult = super(SforcePartnerClient, self).queryAll(queryString)
    if queryResult.size > 0:
      queryResult.records = self._stringifyResultRecords(queryResult.records)
    return queryResult
  
  def queryMore(self, queryLocator):
    queryResult = super(SforcePartnerClient, self).queryMore(queryLocator)
    if queryResult.size > 0:
      queryResult.records = self._stringifyResultRecords(queryResult.records)
    return queryResult
  
  def retrieve(self, fieldList, sObjectType, ids):
    sObjects = super(SforcePartnerClient, self).retrieve(fieldList, sObjectType, ids)
    sObjects = self._stringifyResultRecords(sObjects)
    return sObjects
  
  def search(self, searchString):
    searchResult = super(SforcePartnerClient, self).search(searchString)

    # HACK <result/> gets unmarshalled as '' instead of an empty SearchResult
    # return an empty SearchResult instead
    if searchResult == '':
      return self._sforce.factory.create('SearchResult')

    searchResult.searchRecords = self._stringifyResultRecords(searchResult.searchRecords)
    return searchResult

  # Utility calls

  def sendEmail(self, sObjects):
    xml = self._marshallSObjects(sObjects)
    return super(SforcePartnerClient, self).sendEmail(xml)

  # SOAP header-related calls

  def setCallOptions(self, header):
    '''
    This header is only applicable to the Partner WSDL
    '''
    self._callOptions = header
