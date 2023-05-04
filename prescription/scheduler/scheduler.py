from ..models import Prescription , Booking
import threading
import schedule
import time

class ExampleThread(threading.Thread):
    def __init__(self):
        prescriptions = Prescription.objects.filter(cancelation_date=None)
        bookings = Booking.objects.all()
        self.prescription = [p for p in prescriptions]
        self.booking = [b for b in bookings]
        self._stop_event = threading.Event()  # initialize the stop event
        threading.Thread.__init__(self)

    def stop(self):
        self._stop_event.set()  # set the stop event flag

    def run(self):
        try:
            # run this job every 24 hours
            for p in self.prescription:
                schedule.every().day.at("00:00").do(p.isCanceled)

            for b in self.booking:
                schedule.every(1).minutes.do(b.isExpired)
                schedule.every().day.at("00:00").do(b.isExpired)

            while not self._stop_event.is_set():  # check the stop event flag
                schedule.run_pending()
                time.sleep(5)

        except Exception as e:
            print(e)
