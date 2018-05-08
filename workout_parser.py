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
    exercise_dict = {}

    for w in workouts:
        parsed_workouts.append(parse_workout(w, workout_dict, exercise_dict))

    # workout_dict is a dictionary
    # k = workout date
    # v = type of workout at date k
    print Counter(workout_dict.values())

    for date in exercise_dict.keys():
        print '%s : %s' % (date, exercise_dict[date])

def parse_workout(workout, workout_dict, exercise_dict):
    workout_lines = workout.split('\n')
    workout_lines = [line for line in workout_lines if line]

    date, muscle_group = parse_title_line(workout_lines[0])
    workout_dict[date] = muscle_group

    # all lines except title line
    exercise_lines = workout_lines[1:]
    
    # k = exercise name (including variation)
    # v = weight/rep single adjusted value
    exercises = { }

    for idx, line in enumerate(exercise_lines):
        if idx % 2 == 0:
            # exercise name
            exercise_name, exercise_variant = parse_exercise_name_line(line)
        else:
            chart_value = parse_reps_line(line, exercise_name)
            
            if chart_value == -1:
                continue

            exercises[exercise_name] = chart_value

    exercise_dict[date] = exercises

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

def parse_exercise_name_line(line):
    return get_exercise_name(line), get_exercise_variant(line)

def get_exercise_name(line):
    if '(' in line:
        # get the stuff except the parantheses
        return line[:line.find('(')].strip()

    else:
        return line

def get_exercise_variant(line):
    if '(' in line:
        # get the stuff inside the parantheses
        return line[line.find('(')+1:line.find(')')].capitalize()

    return 'Standard'

def parse_reps_line(line, exercise_name):
    # basically we have n expressions of the form
    # sets @ weight x reps,
    # separated by commas

    # pair (weight, reps)
    # weight = unweighted or a number
    # reps   = a number

    if 'cardio' in exercise_name.lower() or 'treadmill' in exercise_name.lower():
        print '[LOG] cardio parsing not yet implemented, so skipping'
        return -1

    else:
        sets = parse_sets(line)


    max_weight = 0
    max_weight_reps = 0

    for s in sets:
        if s[0] > max_weight:
            max_weight      = s[0]
            max_weight_reps = s[1]

    return get_weight_for_charting(exercise_name, max_weight, max_weight_reps)

def parse_sets(line):
    sets = []

    set_expressions = line.split(',')
    for set_expr in set_expressions:
        set_expr = set_expr.strip()
        is_pr = False

        if 'x' not in set_expr:
            print '[LOG] invalid set expression, missing weight-rep separator: %s' % set_expr
            continue

        if '//' in set_expr:
            print '[LOG] not sure how to parse supersets yet, so skipping'
            continue

        if 'drop' in set_expr:
            print '[LOG] not sure how to parse dropsets yet, so skipping'
            continue

        if '!' in set_expr:
            # TODO: do something with this?
            is_pr = True
            set_expr = set_expr.replace('!', '')

        if '@' in set_expr:
            # the thing to the direct left of the parantheses
            # is the number of sets
            try:
                num_sets = int(set_expr[set_expr.find('@')-1])
            except:
                print '[LOG] error parsing set expr: %s' % set_expr

            # modify the set expr for future parsing so that
            # its just weight x reps
            set_expr = set_expr[set_expr.find('@')+1:]

        else:
            num_sets = 1

        try:
            weight = set_expr[0:set_expr.find('x')]
            weight = int(weight)
        except:
            if weight.strip().lower() == 'unweighted' or weight.strip().lower() == 'warmup':
                weight = 0

            else:
                print '[LOG] could not parse weight from set expression: %s' % set_expr

        try:
            reps = int(set_expr[set_expr.find('x')+1:])

        except:
            print '[LOG] could not parse reps from set expression: %s' % set_expr

        for i in range(num_sets):
            sets.append((weight, reps))

    return sets

def get_weight_for_charting(exercise_name, max_weight, max_weight_reps):
    core_lifts = [
        'barbell bench',
        'deadlift',
        'squat'
    ]

    for lift in core_lifts:
        if lift in exercise_name.lower():
            return max_chart_convert(max_weight, max_weight_reps)

    return max_weight

def max_chart_convert(max_weight, max_weight_reps):
    chart_file_lines = open('max_chart_bench_squat_deadlift.txt', 'r').read().split('\n')

    reps_line = chart_file_lines[0]

    # the column to lookup in the chart
    # i.e. if you did 4 reps, look at column 3 in the grid
    chart_column = max_weight_reps - 1
    weights = [int(line.split()[0]) for line in chart_file_lines[1:]]

    for idx, w in enumerate(weights):
        if w == max_weight:
            adjusted_max = float(chart_file_lines[idx+1].split()[chart_column])
            return int(adjusted_max)

    # fail case - something went wrong
    print 'could not find max weight in chart'
    return max_weight

if __name__ == '__main__':
    main()