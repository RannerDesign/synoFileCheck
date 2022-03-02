#   synoFileCheck.py
#
#   26.02.2022 RB
#   Compare folders after data migration of file servers
#   Installation specific adjustments need to be entered at the
#   beginning of the main program below
#
import os.path, json, time, filecmp
from datetime import datetime
#
#   ------------------------------------------------------------
#   Functions definitions
#   ------------------------------------------------------------
#
def compareFolders(A, B):
    result = {}
    result['only_left_folders'] = []
    result['only_left_files'] = []
    result['only_left_errors'] = []
    result['only_right_folders'] = []
    result['only_right_files'] = []
    result['only_right_errors'] = []
    result['funny_names'] = []
    result['diff_files'] = []
    result['error_files'] = []
    folderDifference(A, B, result)
    return result
#   ------------------------------------------------------------
def folderDifference(A, B, result):
    dirs_cmp = filecmp.dircmp(A, B)
    if len(dirs_cmp.left_only) > 0:
        for x in dirs_cmp.left_only:
            y = os.path.join(A, x)
            if os.path.isdir(y):
                result['only_left_folders'].append({'left': A, 'right': B, 'name': x})
            elif os.path.isfile(y):
                result['only_left_files'].append({'left': A, 'right': B, 'name': x})
            else:
                result['only_left_errors'].append({'left': A, 'right': B, 'name': x})
    if len(dirs_cmp.right_only) > 0:
        for x in dirs_cmp.right_only:
            y = os.path.join(B, x)
            if os.path.isdir(y):
                result['only_right_folders'].append({'left': A, 'right': B, 'name': x})
            elif os.path.isfile(y):
                result['only_right_files'].append({'left': A, 'right': B, 'name': x})
            else:
                result['only_right_errors'].append({'left': A, 'right': B, 'name': x})
    if len(dirs_cmp.common_funny) > 0:
        for x in dirs_cmp.common_funny:
            result['funny_names'].append({'left': A, 'right': B, 'name': x})
    if len(dirs_cmp.diff_files) > 0:
        for x in dirs_cmp.diff_files:
            result['diff_files'].append({'left': A, 'right': B, 'name': x})
    if len(dirs_cmp.funny_files) > 0:
        for x in dirs_cmp.funny_files:
            result['error_files'].append({'left': A, 'right': B, 'name': x})

    for common_dir in dirs_cmp.common_dirs:
        folderDifference(os.path.join(A, common_dir), os.path.join(B, common_dir), result)
#   ------------------------------------------------------------
def cleanFileName(raw):
    forbidden = "/\\"
    out = ""
    for c in raw:
        if c in forbidden:
            out += ""
        else:
            out += c
    return out
#   ------------------------------------------------------------
def shortenFilename(name, maxlen):
    parts = name.rsplit('.', 1)
    return parts[0][:maxlen-len(parts[1])-1] + '.' + parts[1]
#   ------------------------------------------------------------
def singlecheck(folderA, folderB, R):
    if not os.path.isdir(folderA):
        print("Folder A not existing: " + folderA)
        return R
    if not os.path.isdir(folderB):
        print("Folder B not existing: " + folderB)
        return R
    starttime = time.time()
    curtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(curtime + " - singleCheck comparing " + folderA + " with " + folderB)
    
    results = compareFolders(folderA, folderB)

    endtime = time.time()
    print('singleCheck ending after {:.0f} seconds'.format(endtime-starttime))

    return mergeResults(R, results)
#   ------------------------------------------------------------
def mergeResults(A, B):
    keysA = A.keys()
    keysB = B.keys()
    out = {}
    for a in keysA:
        if a in keysB:
            out[a] = A[a] + B[a]
        else:
            out[a] = A[a]
    for b in keysB:
        if not b in keysA:
            out[b] = B[b]
    return out
#   ------------------------------------------------------------
def prepareResults(results, topA, topB, outFolder):
    daytag = datetime.now().strftime("%y%m%d")
    outFilename = cleanFileName(daytag + " compare " + topA + " " + topB + '.json')
    with open(os.path.join(outFolder, outFilename), "w") as outfile:
        json.dump(results, outfile)
#
#   ============================================================
#   Main program
#   ============================================================
#
print("synoFileCheck starting ...")

#   Customizing 1:
#   Nodenames of old and new file server
topA = "\\\\oldSyno\\"
topB = "\\\\newSyno\\"

#   Customizing 2:
#   Shared folders with same name on old and new system
folders = ['Data1', 'Data3', 'homes', 'music', 'photo', 'video', 'web']

results = {}

#   Process shared folders with same name 
for folder in folders:
    results = singlecheck(topA + folder, topB + folder, results)

#   Customizing 3:
#   Process folders with different names
results = singlecheck("\\\\oldSyno\\Data2\\special", "\\\\newSyno\\Data2\\special", results)

#   Customizing 4:
#   Change output folder for results (last parameter, optional)
#   if kept empty string, output goes to the same folder as this script
prepareResults(results, topA, topB, '')

print("synoFileCheck ending")

