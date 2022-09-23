cd $PSScriptRoot
.venv/Scripts/activate.ps1
$script = $PSScriptRoot + "\project_archive_tool\pat.py"
python $script "$args"
