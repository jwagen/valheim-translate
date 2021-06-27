# Translation patch for valheim. WORK IN PROGRESS


## Usage
To extract a .po file from valheim run the following
```
python extract.py -e valheim_out.po <C:\path\to\valheim_Data>
```

This .po file can then be opened in `poedit` or simmilar program to do the acctual translation. 
When the file has been translated the new translation can be patched in.

```
python extract.py -p valheim_out.po <C:\path\to\valheim_Data>
```