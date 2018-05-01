from datetime import datetime
from collections import Counter

def main():
    workout_file_lines = open('workout_log.txt', 'r').read().split('\n')

    workouts = ['' for _ in range(1000)]
    workout_number = 0

    for line in workout_file_lines:
        if '===' in line:
            workout_number += 1

        else:
            workouts[workout_number] += (line + '\n')


    workouts = [w for w in workouts if w]
    parsed_workouts = []
    workout_dict = {}

    for w in workouts:
        parsed_workouts.append(parse_workout(w, workout_dict))

    # workout_dict is a dictionary
    # k = workout date
    # v = type of workout at date k
    print Counter(workout_dict.values())

def parse_workout(workout, workout_dict):
    workout_lines = workout.split('\n')
    workout_lines = [line for line in workout_lines if line]

    date, muscle_group = parse_title_line(workout_lines[0])
    workout_dict[date] = muscle_group

    # all lines except title line
    exercise_lines = workout_lines[1:]

    for idx, line in enumerate(exercise_lines):
        if idx % 2 == 0:
            # exercise name
        else:
            # rep results


def parse_title_line(title_line):
    date_slash = title_line.find('/')
    month = title_line[date_slash-2:date_slash]

    try:
        month = int(month)
    except:
        print '[LOG] could not parse month as two-digit integer... trying one-digit month'

    month = title_line[date_slash-1:date_slash]

    try:
        month = int(month)
    except:
        print '[LOG] could not parse month as one-digit integer... could not find workout date'

    string_after_slash = title_line[date_slash+1:]
    day = string_after_slash[:string_after_slash.find(' ')]

    try:
        day = int(day)
    except:
        print '[LOG] could not parse day. Title line: \n%s\n' % title_line

    dt = datetime(2018, month, day)
    muscle_group = title_line.split('-')[1].lstrip().rstrip().upper()

    return dt, muscle_group

if __name__ == '__main__':
    main()