import csv 
import xml.etree.ElementTree as ET
import os, shutil
from pathlib import Path
import argparse

headers = [
		'file_path',
		'duration',
		'endOfFadeIn', 
		'startOfFadeOut', 
		'loudness', 
		'tempo',
		'tempoConfidence', 
		'timeSignature', 
		'timeSignatureConfidence',
		'key',
		'keyConfidence', 
		'mode', 
		'modeConfidence'
		]

keys = headers[1:]

def parse_xml(path):
	''' 
	Function to parse a single xml file
		Returns: 
			array: all row values retrieved from a single xml file
	'''
	pathname = path 
	tree = ET.parse(path)
	root = tree.getroot()
	row = []
	row.append(pathname) #append full_path name as string

	track_element = root.find('track')
	
	attributes = track_element.attrib # gets a dict of the atrributes

	for key in keys:
		val = attributes.get(key)
		row.append(val)

	return row

def create_csv():

	''' 
	Function to create CSV + column headers
		Returns: 
			csvwriter: writer object
			col_names: array of col_names
	'''

	xml_data = open('xml_data.csv', 'w', newline='', encoding = 'utf-8')
	csvwriter = csv.writer(xml_data)
	
	csvwriter.writerow(headers)
	return csvwriter

def get_files(src):

	path_list = []

	for path, dirs,files in os.walk(src):
		for file in files:
			if file.endswith(".xml"):
				file_path = os.path.join(path,file)
				path_list.append(file_path)
	
	return path_list

def main():
	parser = argparse.ArgumentParser(description="Program to extract relevant features from echo-nest XML files and write to a single CSV")
	parser.add_argument('-i', '--input-folder', required=True, type=str, help="The path to the folder that contains your xml files")
	args = parser.parse_args()
	src = args.input_folder

	path_list = get_files(src)
	csvwriter = create_csv()

	success = 0
	failed = 0
	failed_files = []

	print("Parsing files ...")

	for path in path_list:
		try :
			row = parse_xml(path)
			csvwriter.writerow(row)
			success += 1
			print("File Number {} parsed!".format(success))
		except:
			print("Could not parse {}".format(path))
			failed_files.append(path)
			failed += 1

	print("Successful writes = {}, Failed writes = {}".format(success, failed))

if __name__ == '__main__':
	main()
