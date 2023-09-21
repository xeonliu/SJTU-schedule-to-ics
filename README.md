# A simple script for generating .ics calendar file for SJTU students

## Dependencies
+ pysjtu
+ ics
+ dateutil

### Usage

```pythonr
python main.py [-h] [--output OUTPUT] username password year semester initial_date

positional arguments:
  username         jAccount username
  password         jAccount password
  year             The year you query for. Eg.If 2023-2024, then enter 2023
  semester         0/1/2
  initial_date     The first Monday of the semester. Eg.2023-09-11

options:
  -h, --help       show this help message and exit
  --output OUTPUT  your_location/your_name.ics
```

### External Links

icsx5 (for Android): https://icsx5.bitfire.at/

难蚌，pysjtu仓库里边有个export.py已经实现了该功能，自己丢人现眼了