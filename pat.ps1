<#
This script is added to the windows registry to provide a context
menu for running PAT. See README for details
#>
cd $PSScriptRoot
.venv/Scripts/activate.ps1
$script = $PSScriptRoot + "\project_archive_tool\pat.py"
python $script "$args"
