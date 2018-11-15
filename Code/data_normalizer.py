import pandas
import re


def convert(location_list):
# Function to convert and numerize co-ordinates

        if location_list[5] != 'E':
            location_list[4] = - location_list[4]       #to negate longitudinal value
        if location_list[3] != 'N':
            location_list[2] = - location_list[2]       #to negate latitudinal value
        if location_list[1] != '0':
            location_list[0] = - location_list[0]       #to negate altitude value
        return location_list

def match_patterns(raw_input):
# Function to extract meaningful information from EXIF meta data

        #Normalizing altitude
        split_string = raw_input[0].split('/')
        raw_input[0] = float(split_string[0])/float(split_string[1])
        raw_input[0] = float(raw_input[0])

        #Normalizing latitude
        split_string=raw_input[2][1:-1].replace(" ","").split(',')
        raw_input[2] = float(split_string[0])+float(split_string[1])/60.0
        split_string[2] = split_string[2].split('/')
        raw_input[2] += float(split_string[2][0])/(float(split_string[2][1])*3600.0)

        #Normalizing longitude
        split_string = raw_input[4][1:-1].replace(" ","").split(',')
        raw_input[4] = float(split_string[0])+float(split_string[1])/60.0
        split_string[2] = split_string[2].split('/')
        raw_input[4] += float(split_string[2][0])/(float(split_string[2][1])*3600.0)

        clean_output= raw_input

        return clean_output




