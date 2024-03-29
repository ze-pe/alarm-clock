import subprocess
import time
import threading

'''
CLEAR and CLEAR_AND_RETURN are escape sequences in ANSI-compatible terminals that can be used to control the terminal display. These sequences are used to clear the terminal screen and reset the cursor position to the top-left corner.
'''
CLEAR = "\033[2J" # clears the entire terminal screen
CLEAR_AND_RETURN = "\033[H" # moves the cursor to the top-left corner of the terminal screen

running = True # variable to control the loop state

def key_listener():
    global running
    while True:
        key = input("Press Enter to pause/resume the alarm.")
        if key == '':
            running = not running
            if running:
                print("Resumed...")
            else:
                print("Paused...")

def alarm(seconds):
    global running
    time_elapsed = 0

    print(CLEAR)
    while time_elapsed < seconds:
        if running:
            time.sleep(1)
            time_elapsed += 1

            time_remaining = seconds - time_elapsed
            minutes_remaining = time_remaining // 60
            seconds_remaining = time_remaining % 60

            print(f"{CLEAR_AND_RETURN}Alarm will sound in: {minutes_remaining:02d}:{seconds_remaining:02d}")
                
            print(CLEAR)
            print(f"{CLEAR_AND_RETURN}Alarm complete.")
        else:
            time.sleep(0)

    # audio file source: https://orangefreesounds.com/clock-gong-sound/
    audio_file = "alarm.mp3"

    '''
    The Popen() method is called to start the VLC player in the background and play the audio file. The command "vlc" is passed as the first argument to Popen(), which starts the VLC media player. The --intf dummy option is used to specify that the player should not show a GUI interface, and --play-and-exit is used to ensure that the media player exits once the audio has finished playing. Finally, the audio_file variable is passed as the last argument, which tells the media player which file to play.
    '''
    # Start the media player in the background and play the audio file
    player = subprocess.Popen(["vlc", "--intf", "dummy", "--play-and-exit", audio_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    '''
    After starting the media player, the code waits for the audio to finish playing before continuing. The communicate() method on the player object waits for the process to finish and returns the output streams as byte strings. The stdout and stderr streams are captured in the stdout and stderr variables respectively. Since the media player is set to exit once the audio is finished playing, the communicate() method call blocks until the media player has finished playing the audio file, at which point it returns the output streams and the program continues.
    '''
    # Wait for the audio to finish playing
    stdout, stderr = player.communicate()

# User inputs for minutes and seconds for alarm countdown
while True:
    try:
        minutes = int(input("Set the number of minutes for the alarm: "))
        if minutes >= 0:
            break
        else:
            print("Please enter a positive integer value.")
    except ValueError:
        print("Please enter a positive integer value.")

while True:
    try:
        seconds = int(input("Set the number of seconds for the alarm: "))
        if 0 <= seconds < 60:
            break
        else:
            print("Please enter a valid integer (0-59).")
    except ValueError:
        print("Please enter a valid integer (0-59).")

total_seconds = minutes * 60 + seconds

# Start the key listener thread
thread = threading.Thread(target=key_listener)
thread.daemon = True
thread.start()

alarm(total_seconds)