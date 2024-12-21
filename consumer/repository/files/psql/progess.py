import sys
import os
import threading

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount  # Zwiększenie ilości przesyłanych bajtów
            percentage = (self._seen_so_far / self._size) * 100  # Obliczenie procentowego postępu
            print(f"Przesłano: {self._seen_so_far:.2f}/{self._size:.2f} bajtów ({percentage:.2f}%)", end="\r")
            sys.stdout.flush()  # Upewniamy się, że tekst jest natychmiast wyświetlany
            if self._seen_so_far == self._size:
                print(f"\n{self._filename} - przesyłanie zakończone.")
