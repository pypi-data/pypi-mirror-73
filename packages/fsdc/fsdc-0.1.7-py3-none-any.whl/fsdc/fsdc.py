from filecmp import dircmp
import os
import argparse
import easygui
import pandas as pd
from pathlib import Path
import sys

def convert_bytes(num):
    #this function will convert bytes to MB.. GB.. etc
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:.3f} {x}'
        num /= 1024.0

def file_size(file_path):
    #this function will return the file size
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def already_in_df(df, temp_df):

	length = len(df)
	for x in range (0, length):
		filename = df.at[x, 'Filename']
		sizeA     = df.at[x, 'Size in Group A']
		pathA     = df.at[x, 'Path in Group A']
		sizeB     = df.at[x, 'Size in Group B']
		pathB     = df.at[x, 'Path in Group B']

		if filename == temp_df.at[0, 'Filename'] and sizeA == temp_df.at[0, 'Size in Group A'] and pathA == temp_df.at[0, 'Path in Group A']:
			if filename == temp_df.at[0, 'Filename'] and sizeB == temp_df.at[0, 'Size in Group B'] and pathB == temp_df.at[0, 'Path in Group B']:
				return True

	return False

def not_unique(df, file):
	length = len(df)
	for x in range (0, length):
		filename = df.at[x, 'Filename']

		if filename == file:
			return True
	
	return False

def get_files(folder):

	df = pd.DataFrame(columns=['Filename', 'Path', 'Size'])
	for root, dirs, file in os.walk(folder):
		for x in file:
			size = file_size(os.path.join(root, x))
			temp_df = pd.DataFrame([[x, root, size]], columns=['Filename', 'Path', 'Size'])
			df = df.append(temp_df, ignore_index=True)

	return df

def get_unique_files(list_of_folders_A, list_of_folders_B):

	dfA = pd.DataFrame(columns=['Filename', 'Path', 'Size'])
	dfB = pd.DataFrame(columns=['Filename', 'Path', 'Size'])

	for group_A in list_of_folders_A:
		dfA_tmp = get_files(group_A)
		dfA = dfA.append(dfA_tmp, ignore_index=True)
	for group_B in list_of_folders_B:
		dfB_tmp = get_files(group_B)
		dfB = dfB.append(dfB_tmp, ignore_index=True)

	filesA = dfA['Filename']
	filesB = dfB['Filename']
	for x in filesA.values:
		for y in filesB.values:
			if x == y:
				dfA = dfA.drop(dfA[dfA.Filename == x].index)
				dfB = dfB.drop(dfB[dfB.Filename == y].index)

	return dfA, dfB

def main():

	df = pd.DataFrame(columns=['Filename', 'Identical', 'Path in Group A',
							   'Size in Group A','Path in Group B', 
							   'Size in Group B'])
	
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--enable_gui", action="store_false", required=False,
					help="Input with easygui (you can only select one folder)")
	ap.add_argument("-t", "--terminal_output", action="store_true", required=False,
					help="Output in the terminal (default excel). There will be no file you can save.")
	args = vars(ap.parse_args())
	
	enable_gui = args['enable_gui']
	t_output = args['terminal_output']
	
	list_of_folders_A = []
	list_of_folders_B = []


	if enable_gui == False:

		A = easygui.diropenbox()
		list_of_folders_A = [A]
		B = easygui.diropenbox()
		list_of_folders_B = [B]
	
	else:
		list_of_folders_A = list(map(str, input('Give the path of the first foldergroup (you can input multiple paths): ').split()))

		list_of_folders_B = list(map(str, input('Give the path of the second foldergroup (you can input multiple paths): ').split()))
	
	print(list_of_folders_A)
	print(list_of_folders_B)

	for group_A in list_of_folders_A:
		for roota, dirsa, filesa in os.walk(group_A):
			for group_B in list_of_folders_B:
				for rootb, dirsb, filesb in os.walk(group_B):
					dc = dircmp(roota, rootb)
					if dc.same_files == []:
						pass
					else:

						for f in dc.same_files:
							sizea = file_size(os.path.join(roota, f))
							sizeb = file_size(os.path.join(rootb, f))
							temp_df = pd.DataFrame([[f, 'yes', roota, sizea, rootb, sizeb]], columns=['Filename', 'Identical', 'Path in Group A', 
																							   'Size in Group A','Path in Group B', 
																							   'Size in Group B'])
							df = df.append(temp_df, ignore_index=True)
		
					if dc.common_files == []:
						pass
					else:

						for f in dc.common_files:
							sizea = file_size(os.path.join(roota, f))
							sizeb = file_size(os.path.join(rootb, f))
							temp_df = pd.DataFrame([[f, 'no', roota, sizea, rootb, sizeb]], columns=['Filename', 'Identical', 'Path in Group A', 
																									'Size in Group A','Path in Group B', 
																									'Size in Group B'])
							if already_in_df(df, temp_df) == False:
								df = df.append(temp_df, ignore_index=True)
								
	#unique files
	a, b = get_unique_files(list_of_folders_A, list_of_folders_B)

	#output


	if t_output == True:

		print("common files:")
		print(df)
		print("##################################")
		print("Files unique to the first group")
		print(a)
		print("##################################")
		print("files unique to the second group")
		print(b)

	if t_output == False:

		if enable_gui == False:
				save_path = easygui.filesavebox(default="identical_files_from_")
		if enable_gui == True:
				save_path = input('Enter the path where you want to save the file: ')
				save_name = input('How do you want to name that file: ')
				save_path = save_path +'/'+ save_name +'.xlsx'

		with pd.ExcelWriter(save_path+'.xlsx') as writer:
			df.to_excel(writer, sheet_name='In both')
			a.to_excel(writer, sheet_name='Only in A')
			b.to_excel(writer, sheet_name='Only in B')


if __name__ == "__main__":
	main()