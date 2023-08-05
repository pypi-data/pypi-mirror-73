"""
Image processing debugger similar to Image Watch for Visual Studio.
"""

from functools import wraps
from typing import Callable, Dict, List, Optional, Tuple

import cv2 as cv


# * ------------------------------------------------------------------------------ # *
# * BASE CLASS * #


class Checker:
    """Checker for OpenCV functions."""

    def __init__(self, cv_function_name: str):
        """Checker for OpenCV functions."""
        cv.namedWindow(cv_function_name)
        self.cv_function_name = cv_function_name
        self.cv_function = getattr(cv, cv_function_name)

    def start(self, decorator):
        """Starts checking the OpenCV function."""
        setattr(cv, self.cv_function_name, decorator())

    def stop(self):
        """Stops checking the OpenCV function."""
        setattr(cv, self.cv_function_name, self.cv_function)


# * ------------------------------------------------------------------------------ # *
# * FUNCTION WATCHING * #


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


# * ------------------------------------------------------------------------------ # *
# * FUNCTION TRACKING * #


class Tracker(Checker):
    """Tracker for OpenCV functions."""

    TRACKBAR_MAX = 1000

    def __init__(
        self,
        cv_function_name: str,
        arg_to_track: str,
        arg_range: Tuple[int, int],
        coercion_function: Optional[Callable] = None,
        trackbar_max: int = TRACKBAR_MAX,
    ):
        """Tracker for OpenCV functions."""
        super().__init__(cv_function_name)
        self.master_callback = True
        self.arg_to_track = arg_to_track
        self.arg_range = arg_range
        self.trackbar_range = (0, trackbar_max)
        self.coercion_function = coercion_function
        self.cv_function_kwargs: Dict = {}

    def track(self):
        """Decorator to track an OpenCV function."""

        @wraps(self.cv_function)
        def wrapper(**kwargs):  # this wrapper only supports kwargs, no positional args

            # capture the `kwargs` passed to OpenCV
            self.cv_function_kwargs.update(kwargs)

            # get the current value of the argument to be tracked
            self.arg_current_value = self.cv_function_kwargs[self.arg_to_track]
            self.trackbar_pos = int(
                self.scale(
                    range_in=self.arg_range,
                    range_out=self.trackbar_range,
                    value_in=self.arg_current_value,
                )
            )

            # create a trackbar with the slider in the right position
            cv.createTrackbar(
                self.arg_to_track,  # trackbarname
                self.cv_function_name,  # winname
                self.trackbar_pos,  # value: Initial slider position.
                self.trackbar_range[-1],  # count: Maximal slider position.
                self.trackbar_callback,  # TrackbarCallback
            )

            # begin the callback, OpenCV will re-run it on trackbar position change
            result = self.trackbar_callback(self.trackbar_pos)
            if self.master_callback:
                cv.waitKey()

            return result

        return wrapper

    def start(self):
        """Starts tracking the OpenCV function."""
        super().start(self.track)

    def trackbar_callback(self, trackbar_pos: int):
        """The callback that updates the argument when the trackbar position changes."""
        self.trackbar_pos = trackbar_pos
        self.update_kwargs()
        result = self.cv_function(**self.cv_function_kwargs)

        self.preview(result)
        return result

    def update_kwargs(self):
        """Update the current value of the argument being controlled by the trackbar."""
        self.arg_current_value = self.scale(
            range_in=self.trackbar_range,
            range_out=self.arg_range,
            value_in=self.trackbar_pos,
        )
        if self.coercion_function is not None:
            self.arg_current_value = self.coercion_function(self.arg_current_value)
        self.cv_function_kwargs[self.arg_to_track] = self.arg_current_value

    def preview(self, result):
        """Preview the result of an OpenCV function."""

        FONT = cv.FONT_HERSHEY_SIMPLEX
        FONT_SCALE = 0.5
        THICKNESS = 1
        PAD = 5
        X = 0

        # convert unknown color space to color to facilitate placing elements
        preview = cv.cvtColor(result, cv.COLOR_GRAY2RGB)
        # prepare the text, get the text size
        text = f"{self.arg_to_track} = {self.arg_current_value:g}"
        (width, height) = cv.getTextSize(
            text, FONT, fontScale=FONT_SCALE, thickness=THICKNESS
        )[0]
        # get rectangle coordinates and bottom-left corner of text
        Y = height + 2 * PAD
        pt1 = (X, Y)
        pt2 = (X + width + 2 * PAD, 0)
        org = (X + PAD, Y - PAD)
        # print a rectangle, then the text, then show the result
        cv.rectangle(
            img=preview, pt1=pt1, pt2=pt2, color=(255, 255, 255), thickness=cv.FILLED
        )
        cv.putText(
            img=preview,
            text=text,
            org=org,
            fontFace=FONT,
            fontScale=FONT_SCALE,
            color=(0, 0, 255),
            thickness=1,
        )
        cv.imshow(self.cv_function_name, preview)

    @staticmethod
    def scale(
        range_in: Tuple[float, float], range_out: Tuple[float, float], value_in: float,
    ) -> float:
        """Scale a value from an input range to an output range."""
        diff_in = range_in[1] - range_in[0]
        diff_value = value_in - range_in[0]
        diff_out = range_out[1] - range_out[0]
        scaling_factor = diff_out / diff_in
        value_out = range_out[0] + scaling_factor * diff_value
        return value_out


class Trackers:
    """Track multiple arguments in one OpenCV function."""

    def __init__(
        self,
        cv_function_name: str,
        args_to_track: List[str],
        arg_ranges: List[Tuple[int, int]],
        coercion_functions: List[Optional[Callable]] = None,
    ):
        """Track multiple arguments in one OpenCV function."""

        # reverse args so they are arranged top-to-bottom when tracked
        args_to_track.reverse()
        arg_ranges.reverse()

        # assign attributes
        self.cv_function_name = cv_function_name
        self.args_to_track = args_to_track
        self.arg_ranges = arg_ranges
        if coercion_functions is not None:
            coercion_functions.reverse()  # reverse to match args order
            self.coercion_functions = coercion_functions
        else:
            self.coercion_functions = [None] * len(args_to_track)
        self.cv_function_kwargs_shared: Dict = {}
        self.trackers: List[Tracker] = []

    def start(self):
        for arg_to_track, arg_range, coercion_function in zip(
            self.args_to_track, self.arg_ranges, self.coercion_functions
        ):
            """Starts tracking the OpenCV function."""
            tracker = Tracker(
                self.cv_function_name, arg_to_track, arg_range, coercion_function,
            )
            tracker.cv_function_kwargs = self.cv_function_kwargs_shared
            tracker.master_callback = False
            tracker.start()
            self.trackers.append(tracker)
        self.trackers[-1].master_callback = True

    def stop(self):
        """Stops tracking the OpenCV function."""
        [tracker.stop() for tracker in self.trackers]
        self.trackers = []
