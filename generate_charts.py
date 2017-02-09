#!/usr/bin/python

import datetime
import json
import os
import subprocess
import sys

dates = []
enrolment_data = {}

def get_json_files(dir_path):
    """
    Returns a list of JSON file names in the given directory path.

    (str) -> [str]
    """
    return [f for f in os.listdir(dir_path) if f.endswith('.json')]

def file_name_to_iso(file_name):
    """

    """
    epoch = int(file_name.split('.json')[0])
    iso_date = datetime.datetime.fromtimestamp(epoch).isoformat()
    return iso_date.split('T')[0]

def parse_file(file_path):
    """
    Parses a JSON file, tracking the enrolment count for each course/meeting.

    (str) -> None
    """
    # This is a SINGLE day's worth of data
    with open(file_path) as data_file:
        data = json.load(data_file)

        # Every course
        for course_id, course_data in data.items():
            # Ensure subdirectory exists for department
            # if not os.path.exists(args.output):
            #     os.makedirs(args.output)

            # Fetch all enrolment data for each meeting section
            for meeting_id, meeting_data in course_data['meetings'].items():
                if not 'actualEnrolment' in meeting_data:
                    continue

                if not course_id in enrolment_data:
                    enrolment_data[course_id] = {}

                if not meeting_id in enrolment_data[course_id]:
                    enrolment_data[course_id][meeting_id] = []

                enrolment = int(meeting_data['actualEnrolment'])
                enrolment_data[course_id][meeting_id].append(enrolment)

def gnuplot_exec(cmds, data):
    """
    Runs gnuplot with the given commands.

    [str] -> subprocess
    """
    args = ['gnuplot', '-e', (';'.join([str(c) for c in cmds]))]
    program = subprocess.Popen(args, stdin=subprocess.PIPE)
    for line in data:
        program.stdin.write(str(line) + os.linesep)

    return program

def plot_course(course_id, meetings, output_dir):
    """
    Plots the given course data with gnuplot.
    """
    cmds = [
        'set grid',
        'set title "{0} ({1} - {2})"'.format(course_id, dates[0], dates[-1]),
        'set xdata time',
        'set timefmt "%Y-%m-%d"',
        'set ylabel "Enrolment"',
        'set logscale y 2',
        'set key below',
        'set term jpeg small size 800,450',
        'set output "{0}/{1}.jpg"'.format(output_dir, course_id)
    ]

    # Each meeting section is a new plot
    plots = []
    for meeting_id, meeting_data in meetings:
        plots.append('"-" u 1:2 t "{0}" w lp'.format(meeting_id))

    cmds.append('plot ' + ', '.join(plots))

    data = []
    for meeting_id, meeting_data in meetings:
        for i in range(len(meeting_data)):
            if sum(meeting_data) != 0:
                data.append('{0} {1}'.format(dates[i], meeting_data[i]))
        data.append('e')

    if len(data) > 0:
        gnuplot_exec(cmds, data)


if __name__ == '__main__':
    if 2 > len(sys.argv) or len(sys.argv) > 3:
        print('Usage: %s <JSON data directory> [output directory]' % sys.argv[0])
        exit(1)

    folder = sys.argv[1]
    output = './charts'
    if len(sys.argv) == 3:
        output = sys.argv[2]

    # Ensure output directory exists
    if not os.path.exists(output):
        os.makedirs(output)

    # Aggregate enrolment counts for each date for every course
    file_names = get_json_files(folder)
    for file_name in file_names:
        # Date
        dates.append(file_name_to_iso(file_name))

        # Course data
        file_path = os.path.join(folder, file_name)
        parse_file(file_path)

    # Generate some charts with the enrolment data
    for course_id, course_data in enrolment_data.items():
        plot_course(course_id, course_data.items(), output)
