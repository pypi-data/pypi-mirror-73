from procmon_parser.logs import *
from procmon_parser.logs_format import *
from procmon_parser import *
from procmon_parser.logs import EventClass


# with open(r"C:\temp\Logfile - Copy.PML", "rb") as f:
#     data = f.read()

f = open(r"C:\Temp\LogfileTests32bitUTC.PML", "rb")
logs_reader = ProcmonLogsReader(f)
first_event = next(logs_reader)
print(first_event.get_compatible_csv_info())
for event in logs_reader:
    print(event.get_compatible_csv_info(first_event.date))


# f = open(r"C:\temp\Logfile34.PML", "rb")
# logs_reader = ProcmonLogsReader(f)
# for event in logs_reader:
#     if event.event_class == EventClass.PROCESS:
#         print(event)


