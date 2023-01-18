from env import DEVICE_ID

import tinytuya
import datetime
import numpy as np
import time

class Bulb(tinytuya.BulbDevice):
    def __init__(self, device_id, wakeup_time="0700"):
        super().__init__(dev_id=device_id)
        self.wakeup_time = wakeup_time
        
    @staticmethod
    def minute_delay(delay):
        time.sleep(int(delay * 60))
    
    def light_percentage_sequence_exponential(self, min_before_wakeup=30, delay=1, a = None):
        time = np.arange(0, min_before_wakeup + delay, delay)
        if a is None:
            a = 4.8 if min_before_wakeup ==30 else 3.1
        percentages = 100 * np.exp((time - min_before_wakeup) / a)
        return percentages
    
    def wakeup_sequence(self, min_before_wakeup=30, delay=1, a = None):
        self.set_brightness_percentage(0)
        self.set_colourtemp_percentage(0)
        self.turn_on()
        light_percentages = self.light_percentage_sequence_exponential(min_before_wakeup, delay, a)
        for percent in light_percentages:
            self.set_colourtemp_percentage(percent)
            self.set_brightness_percentage(percent)
            self.minute_delay(delay)

    def flash_n_times(self, n, wait):
        for i in range(n):
            self.turn_off()
            time.sleep(wait)
            self.turn_on()
            time.sleep(wait)
    
    def basic_time_check_alarm(self, hour, minute, min_before_wakeup=30, delay=1, loop_delay=1, flash_times=10, flash_wait=0.25):
        self.turn_off()
        while True:
            time_now = datetime.datetime.now()
            if (time_now.hour == hour) & (time_now.minute == minute):
                print("Starting Sequence")
                self.wakeup_sequence(min_before_wakeup, delay)
                self.flash_n_times(flash_times, flash_wait)
                print("Sequence Complete")
                print(f"Time Taken: {datetime.datetime.now() - time_now}")
                break
            else:
                print(f"Time Now: {time_now.strftime('%H:%M')}")
                self.minute_delay(loop_delay)

def main():
    bulb = Bulb(device_id=DEVICE_ID)
    bulb.basic_time_check_alarm(12, 58, 1, 0.1, .5)
    
if __name__ == "__main__":
    main()