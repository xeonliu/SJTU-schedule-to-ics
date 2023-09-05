# This is a sample Python script.
import pysjtu
import datetime
from dateutil import tz
from ics import Calendar, Event
import argparse


def serial2time(start, end):
    startTimeISO = ['08:00', '08:55', '10:00', '10:55', '12:00', '12:55', '14:00', '14:55', '16:00', '16:55', '18:00',
                    '18:55']
    # No.14 is a virtual class
    endTimeISO = ['08:45', '09:40', '10:45', '11:40', '12:45', '13:40', '14:45', '15:40', '16:45', '17:40', '18:45',
                  '19:40', '20:20', '20:20']
    return datetime.time.fromisoformat(startTimeISO[start - 1]), datetime.time.fromisoformat(endTimeISO[end - 1])


def serial2date(initDay, week, day):
    dt = datetime.timedelta(weeks=week - 1, days=day - 1)
    outputDay = initDay + dt
    return outputDay


def login(name, passwd):
    return pysjtu.create_client(username=name, password=passwd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script for generating ics file for SJTUer's timetable.")
    parser.add_argument('username', type=str, help='jAccount username')
    parser.add_argument('password', type=str,help='jAccount password')
    parser.add_argument('year', type=int,help='The year you query for. Eg.If 2023-2024, then enter 2023')
    parser.add_argument('semester',type=int,help='0/1/2')
    parser.add_argument('initial_date', type=str,help='The first Monday of the semester. Eg.2023-09-11')
    parser.add_argument('--output',type=str,default='sjtu.ics',help='your_location/your_name.ics')
    args=parser.parse_args()

    c = login(args.username, args.password)
    # create a calendar
    currCal = Calendar()
    timeZone = tz.gettz('Asia/Shanghai')
    # 学年，学期
    schedules = c.schedule(args.year, args.semester)
    # 开学第一周周一
    # initDay = datetime.date(2023, 9, 11)
    initDay = datetime.date.fromisoformat(args.initial_date)
    # for each single class
    for s in schedules:
        # name
        className = s.name
        print(s.name)

        # location
        classLocation = s.location

        # time
        startTime, endTime = serial2time(s.time[0], s.time[-1])

        # days of the week
        dayOfWeek = s.day

        # generate an array with the weeks
        weekNumArray = []
        for week in s.week:
            if isinstance(week, range):
                weekNumArray.extend(week)
            else:
                weekNumArray.append(week)

        # a datetime array for current class
        dateTimeArray = []
        for week in weekNumArray:
            outputDay = serial2date(initDay, week, dayOfWeek)
            startDateTime = datetime.datetime.combine(outputDay, startTime, tzinfo=timeZone)
            endDateTime = datetime.datetime.combine(outputDay, endTime, tzinfo=timeZone)
            dateTimeArray.append(outputDay)
            print("开始时间：", startDateTime.isoformat(' '))
            print("结束时间：", endDateTime.isoformat(' '))

            # event
            e = Event(name=className, begin=startDateTime, end=endDateTime, location=classLocation,
                      description=s.class_name)
            currCal.events.add(e)

    with open(args.output, 'w', encoding="utf-8") as f:
        f.writelines(currCal.serialize_iter())