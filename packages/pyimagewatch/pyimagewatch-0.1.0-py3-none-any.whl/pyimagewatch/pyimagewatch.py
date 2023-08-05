"""
Image processing debugger similar to Image Watch for Visual Studio.
"""

from functools import wraps
from typing import Callable, Dict, Tuple

import cv2 as cv


# * ------------------------------------------------------------------------------ # *
# * COERCION * #


def is_even(value: int):
    """Check whether an integer is even."""
    is_even = not (value % 2)
    return is_even


def scale(
    range_in: Tuple[float, float], range_out: Tuple[float, float], value_in: float
):
    """Scale a value from an input range to an output range."""
    diff_in = range_in[1] - range_in[0]
    diff_value = value_in - range_in[0]
    diff_out = range_out[1] - range_out[0]
    scaling_factor = diff_out / diff_in
    value_out = range_out[0] + scaling_factor * diff_value
    return value_out


def default_coerce(track_range, arg_range, trackbar_pos):
    value = int(scale(track_range, arg_range, trackbar_pos))
    if is_even(value):
        value = value + 1
    return value


# * ------------------------------------------------------------------------------ # *
# * CLASS * #


class Checker:
    """Checker for OpenCV functions."""

    def __init__(self, cv_function_name: str):
        """Checker for OpenCV functions."""
        self.cv_function_name = cv_function_name
        self.cv_function = getattr(cv, cv_function_name)

    def start(self, decorator):
        """Starts checking the OpenCV function."""
        setattr(cv, self.cv_function_name, decorator())

    def stop(self):
        """Stops checking the OpenCV function."""
        setattr(cv, self.cv_function_name, self.cv_function)


class Watcher(Checker):
    """Watcher for OpenCV functions."""

    def watch(self):
        """Decorator to watch an OpenCV function."""

        @wraps(self.cv_function)
        def wrapper(*args, **kwargs):
            result = self.cv_function(*args, **kwargs)
            cv.imshow(self.cv_function_name, result)
            cv.waitKey()
            return result

        return wrapper

    def start(self):
        """Starts watching the OpenCV function."""
        super().start(self.watch)


class Tracker(Checker):
    """Tracker for OpenCV functions."""

    DEFAULT_TRACK_RANGE = (0, 10)

    def __init__(
        self,
        cv_function_name: str,
        args: Dict,
        track_arg: str,
        arg_range: Tuple[int, int],
        track_range: Tuple[int, int] = DEFAULT_TRACK_RANGE,
        coerce_function: Callable = default_coerce,
    ):
        """Tracker for OpenCV functions."""
        super().__init__(cv_function_name)
        self.args = args
        self.track_arg = track_arg
        self.arg_range = arg_range
        self.track_range = track_range
        self.coerce_function = coerce_function

    def trackbar(self, trackbar_pos):
        """Converts a trackbar input to an argument range."""
        value = self.coerce_function(self.track_range, self.arg_range, trackbar_pos)
        self.args[self.track_arg] = value
        result = self.cv_function(**self.args)
        cv.imshow(self.cv_function_name, result)
        return result

    def track(self):
        """Decorator to track an OpenCV function."""

        @wraps(self.cv_function)
        def wrapper(*args, **kwargs):
            track_init_value = int(
                scale(self.arg_range, self.track_range, self.arg_range[0])
            )
            cv.createTrackbar(
                self.track_arg,  # trackbarname
                self.cv_function_name,  # winname
                track_init_value,  # value: Initial slider position.
                self.track_range[-1],  # count: Maximal slider position.
                self.trackbar,  # TrackbarCallback
            )
            result = self.trackbar(track_init_value)
            cv.waitKey()
            return result

        return wrapper

    def start(self):
        """Starts watching the OpenCV function."""
        super().start(self.track)
