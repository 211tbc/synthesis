#!/usr/bin/env python

#import sys
import os
#import glob
import string
#import copy
import pickle

class XMLUtilities:
			
	
	def __init__(self):
		print "XMLUtilities initialized..."
		# initialize the dictionary of sequences
		self.IDNumberSequences = {}
		# get the serialized sequence stored on the Hard drive to init the number generator
		self.cacheFile = 'sequences.dat'
		self.IDNumberSequences = self.getSequenceCache()
		self.IDNumberSequences = {}
		
		self.systemID = 0
		self.recordID = 0
		
		self.recIDLookup = {'client':'c', 'need':'n', 'service':'s', 'goal':'g', 'action_step':'as', 'entry_exit':'ee', 'info_release':'ir', 'household':'h', 'member':'m'}
	
	def setrecordID(self, precordID):
		self.recordID = precordID
		
	def getrecordID(self):
		return self.recordID
	
	def setsystemID(self, psystemID):
		self.systemID = psystemID
		
	def getsystemID(self):
		return self.systemID
	
	def setIDNumberSequence(self, psequenceID, pIDNumber):
		self.IDNumberSequences[psequenceID] = pIDNumber

	def getSequenceCache(self):
		
		if os.path.isfile(os.path.join(os.getcwd(), self.cacheFile)):
			cacheFile = open(self.cacheFile, 'rb')

			cacheData = pickle.load(self.cacheFile)
		
			cacheFile.close()
		else:
			cacheData = {}
	
		return cacheData
	
	def generateRecID(self, sequenceID):
		
		# check if the dictionary has the key, if so, get the current sequence number, increment it, store it, and return the value
		if self.IDNumberSequences.has_key(sequenceID):
			number = self.IDNumberSequences[sequenceID] + 1
		else:
			number = 1
			
		if sequenceID == "system":
			self.setsystemID(number)
		else:	
			self.setrecordID(number)
		
		# store the new key value for that sequence.
		#self.IDNumberSequences[sequenceID] = number
		self.setIDNumberSequence(sequenceID, number)
		
		IDNumber = "%s%010d" % (sequenceID, number)
		
		return IDNumber
	
	def generateSysID(self, sequenceName):
		IDNumber = "%s%010da" % (self.recIDLookup[sequenceName], self.getsystemID())
		return IDNumber
	
	# SBB20071021 Added new function to take the "RowID" from the database and stuff into the XML system_id field
	def generateSysID2(self, sequenceName, keyValue):
		IDNumber = "%s%010da" % (self.recIDLookup[sequenceName], keyValue)
		return IDNumber
		
	def generateSystemID(self, systemID):
		systemID = self.generateRecID(systemID)
		#self.setsystemID(systemID)
		return systemID
	
	def initializeSystemID(self, puserID):
		self.setsystemID(puserID)
		
	def cacheSequences(self):
				
		selfref_list = [1, 2, 3]
		selfref_list.append(selfref_list)
		
		output = open(self.cacheFile, 'wb')
		
		# Pickle dictionary using protocol 0.
		pickle.dump(self.IDNumberSequences, output)
		
		output.close()
	
if __name__ == "__main__":
	xmlU = XMLUtilities()
	sequences = ["need", "client", "service", "goal", 'entry_exit']
	
	print "SystemID is: %s" % xmlU.generateSystemID("system")
	
	for seq in sequences:
		
		for ID in range(10):
			#idNumber = xmlU.generateID(seq)
			idNumber = xmlU.generateSysID(seq)
			print "Sequence: %s Generated system_id: %s" % (seq, idNumber)
	
	print "SystemID is: %s" % xmlU.generateSystemID("system")
	
	for seq in sequences:
		for ID in range(10):
			idNumber = xmlU.generateRecID(seq)
			print "Sequence: %s Generated rec_id: %s" % (seq, idNumber)