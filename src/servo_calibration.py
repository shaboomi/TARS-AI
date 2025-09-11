import time

import Adafruit_PCA9685


# Default pulse range used by the existing servo tester
DEFAULT_MIN = 0
DEFAULT_MAX = 600
STEP = 5


def set_pulse(pwm, channel, pulse):
    """Send a pulse to the servo on ``channel``."""
    pwm.set_pwm(channel, 0, pulse)
    print(f"Channel {channel} -> {pulse}")


def calibrate_channel(channel: int):
    """Interactively adjust and record min/max pulse widths for ``channel``."""
    pwm = Adafruit_PCA9685.PCA9685(busnum=1)
    pwm.set_pwm_freq(50)

    pulse = (DEFAULT_MIN + DEFAULT_MAX) // 2
    set_pulse(pwm, channel, pulse)

    min_val = None
    max_val = None

    print("\nControls: [a] decrease, [d] increase, [s] save min, [w] save max, [q] quit")

    while True:
        cmd = input(": ").strip().lower()
        if cmd == "a":
            pulse = max(DEFAULT_MIN, pulse - STEP)
            set_pulse(pwm, channel, pulse)
        elif cmd == "d":
            pulse = min(DEFAULT_MAX, pulse + STEP)
            set_pulse(pwm, channel, pulse)
        elif cmd == "s":
            min_val = pulse
            print(f"\nRecorded min pulse: {min_val}")
        elif cmd == "w":
            max_val = pulse
            print(f"\nRecorded max pulse: {max_val}")
        elif cmd == "q":
            break

    print("\nCalibration complete")
    print(f"Channel {channel} -> min: {min_val}, max: {max_val}")


if __name__ == "__main__":
    try:
        ch = int(input("Servo channel (0-15): "))
    except ValueError:
        print("Invalid channel")
        raise SystemExit(1)
    calibrate_channel(ch)
