
synoFileCheck
=============

**synoFileCheck** is a small stand-alone application to support data migration from one file server to another. It was developed for Synology DS or RS systems, but should run with any server mapping drives via SMB. It supports the check of completeness and especially the handling of too long filenames, if the target folder is encrypted.

The application consists of two components:

**synoFileCheck.py** is a Python program (testet with 3.10.0). It is not ready to use but has to be adapted to the server and folder names of the environment to operate in. The program compares the two servers and generates a json output file with all results.

**synoFileCheck.html** is a HTML+CSS+JS program (testet with Google Chrome 98.0.4758.102 and Firefox 97.0.1). After reading in the json file produced by synoFileCheck.py there are two pages prepared: one with a complete listing of the comparison results and one to step through all files with too long filenames and the possibility to manually change the names. As a result a .bat file is generated with all appropriate copy commands. The filenames on the old server are kept, whereas the filenames on the new server are shortened.

## Installation
* An installation is not needed
* Copy the two files to any folder

## Technical Prerequisites
* Python3
* Actual browser
* no further software is required

## Customization of synoFileCheck.py
1. Nodenames of old (=source) and new (=target) file servers
2. Shared folders with same name on old and new system as list elements
3. Folders with different names or tree positions (one function call per folder)
4. Output directory for results in json file

## Customization of synoFileCheck.html
* No customization needed, you'll be asked for locations of json file and bat output file
* The program can be run locally from any directory, no web server needed

## Shortening of filenames
Using folders with encryption on Synology servers has the restriction, that filenames with more than 143 characters are not allowed. Copying from a folder without encryption to a folder with encryption will fail in such cases.

A typical way to handle this, especially with large numbers of such files, is to shorten the filenames programmatically via script. If filenames differ only beyond position 143 the algorithm nedded may become complicated and comprehensive testing is needed.

If brute-force cutted filenames are not accepted and the number of such files is in a range that manual processing is a valid option, the procedure built in synoFileCheck.html may be userful. The folders are copied from source to destination system accepting copy errors for files with too long filenames. Unfortunately this cannot be done with Synologies File Station, because it stops after the first error and leaves the target folder in an unpredictable state. So copy with a Linux or Windows script is necessary.

After copying synoFileCheck.py is run resulting in a json result file. synoFileCheck.html can read this file, present the results of the comparison and offer a possibility to manually shorten filenames.

The screen should be self-explaining:
* to navigate use the arrow buttons or enter the record number
* Max length of filename may be changed, this leads to a reload of the json file and all manually entered data is lost
* The command in the bat file can be edited with the following replacements
    - $A = source folder
	- $B = destination folder
	- $old = filename in source
	- $new = filename in destination (shortened)
* with the checkbox Enable it is possible to exclude files from being copied (e.g. temp files)
* the new filename is shortened by the loading script as proposal, after leaving the field, the length is updated
* with the Generate ommands button a .bat file is created that can be executed
* it is proposed to manually append a pause statement at the end of the bat file, so that copy errors can be checked afterwards

