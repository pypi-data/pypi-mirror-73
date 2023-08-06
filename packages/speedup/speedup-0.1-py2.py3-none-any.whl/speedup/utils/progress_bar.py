import progressbar
import time


def duration_progress(activity, duration, is_done):
    def progress(activity, iterations=100):
        bar = progressbar.ProgressBar(
            widgets=[activity, ' ', progressbar.Bar(),
                     ' (', progressbar.ETA(), ') ', ])
        return bar(range(iterations))

    if duration is not None:
        iterations = 100
        time_per_iteration = float(duration) / float(iterations)

        bar = progress(activity, iterations)
        cursor = 0
        for cursor in range(iterations):
            bar.next()
            time.sleep(time_per_iteration)

            # If done early.
            if is_done():
                bar.update(100)
                break

    if not is_done():
        # if still not done.
        bar = progressbar.ProgressBar(
            widgets=[activity, ' ', progressbar.RotatingMarker(),
                     ' (', progressbar.Timer(), ') ', ],
            max_value=progressbar.UnknownLength)
        i = 0
        while not is_done():
            bar.update(i)
            i += 1

    print("")
