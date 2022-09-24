<#
This script is added to the windows registry to provide a context
menu for running PAT. See README for details
eg:
  "wt.exe powershell -noexit <path_to pat.ps1> %1"
#>
cd $PSScriptRoot
.venv/Scripts/activate.ps1
$script = $PSScriptRoot + "\project_archive_tool\pat-upload.py"
python $script "$args"
