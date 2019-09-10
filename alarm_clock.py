# Jeff Bromen

"""Simple Python script to set an alarm for a specific time.
   When the alarm goes off, a random youtube video will be opened.
   The possible youtube video URLs are taken from "youtube_alarm_videos.txt"
   With snooze option and wake up text added by Franek
"""

import datetime
import os
import time
import random
import webbrowser

# If video URL file does not exist, create one
if not os.path.isfile("youtube_alarm_videos.txt"):
    print('Creating "youtube_alarm_videos.txt"...')
    with open("youtube_alarm_videos.txt", "w") as alarm_file:
        alarm_file.write("https://www.youtube.com/watch?v=anM6uIZvx74")


def check_alarm_input(alarm_time):
    """Checks to see if the user has entered in a valid alarm time"""
    if len(alarm_time) == 1:  # [Hour] Format
        if 24 > alarm_time[0] >= 0:
            return True
    elif len(alarm_time) == 2:  # [Hour:Minute] Format
        if 24 > alarm_time[0] >= 0 and \
                60 > alarm_time[1] >= 0:
            return True
    elif len(alarm_time) == 3:  # [Hour:Minute:Second] Format
        if 24 > alarm_time[0] >= 0 and \
                60 > alarm_time[1] >= 0 and \
                60 > alarm_time[2] >= 0:
            return True
    else:
        return False


def wake_up_now():
    """Opens random video on YouTube to wake up"""
    if display_message:
        print(message)
    else:
        print("Wake Up!")

    # Load list of possible video URLs
    with open("youtube_alarm_videos.txt", "r") as alarm_file:
        videos = alarm_file.readlines()

    # Open a random video from the list
    webbrowser.open(random.choice(videos))


# Get user input for the alarm time
print("Set a time for the alarm (Ex. 06:30 or 18:30:00)")
while True:
    alarm_input = input(">> ")
    try:
        alarm_time = [int(n) for n in alarm_input.split(":")]
        if check_alarm_input(alarm_time):
            break
        else:
            raise ValueError
    except ValueError:
        print("ERROR: Enter time in HH:MM or HH:MM:SS format")

# asking for alarm text
print("Do you want to display a message during an alarm? Write \"yes\" if you do, press Enter if not ")
ask_for_message = input(">> ")

if ask_for_message == "yes" or ask_for_message == "Yes":
    display_message = True
    message = input("Your message: ")
else:
    display_message = False

# Convert the alarm time from [H:M] or [H:M:S] to seconds
seconds_hms = [3600, 60, 1]  # Number of seconds in an Hour, Minute, and Second
alarm_seconds = sum([a * b for a, b in zip(seconds_hms[:len(alarm_time)], alarm_time)])

# Get the current time of day in seconds
now = datetime.datetime.now()
current_time_seconds = sum([a * b for a, b in zip(seconds_hms, [now.hour, now.minute, now.second])])

# Calculate the number of seconds until alarm goes off
time_diff_seconds = alarm_seconds - current_time_seconds

# If time difference is negative, set alarm for next day
if time_diff_seconds < 0:
    time_diff_seconds += 86400  # number of seconds in a day

# Display the amount of time until the alarm goes off
print("Alarm set to go off in %s" % datetime.timedelta(seconds=time_diff_seconds))

# Sleep until the alarm goes off
time.sleep(time_diff_seconds)

# Time for the alarm to go off
wake_up_now()


def snooze_input(answer):
    """checks user's input to turn on a snooze"""
    if answer == "yes" or answer == "Yes":
        return True
    else:
        return False


# repeating snooze until user stops it
while True:
    print("Do you want to set a snooze? Write \"yes\" if you do, press Enter if not")
    snooze_answer = input(">> ")

    if snooze_input(snooze_answer):

        snooze_time_seconds = 60 * int(input("snooze time in minutes: "))
        print("Alarm set to go off in %s" % datetime.timedelta(seconds=snooze_time_seconds))
        time.sleep(snooze_time_seconds)
        wake_up_now()

    else:
        break
