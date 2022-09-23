## Getting started

1. Create or modify the **./pat-config.yaml** to point to the correct locations
2. Set your aws env variables using `aws configure`
3. Run the following commands:

```
poetry install
poetry shell
python ./project_archive_tool/pat.py "<path_to_project>"
```

### Extras

How to register something in the context menu windows:
https://stackoverflow.com/questions/20449316/how-add-context-menu-item-to-windows-explorer-for-folders