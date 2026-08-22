# __tests__/__init__.py:5
__all__ = ["asyncfrace_memory"]
import logging
import tracemalloc
from functools import wraps

 # plus (bellow)
log = logging.getLogger(__name__)
def asyncfrace_memory(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not tracemalloc.is_tracing():
            tracemalloc.start(50)
        snapshot_on_start = tracemalloc.take_snapshot()
        result = await func(*args, **kwargs)
        snapshot_on_end = tracemalloc.take_snapshot()

        # Analysis
        top_starts = snapshot_on_end.compare_to(snapshot_on_start, 'traceback') #  lineno
        # Filter
        top_starts_list = [start for start in top_starts if start.size_diff >= 1024 * 300]
        # Publication
        log.debug(f"{'='*60}")
        log.debug(f"Memory usage for {func.__name__}")
        for ind, start in enumerate(top_starts_list):
            size_diff_kb = start.size_diff / 1024
            size_kb = start.size / 1024
            direction = "🔺 +" if start.size_diff > 0 else "🔻 "
            log.debug(f"{ind}. {direction}{abs(size_diff_kb):.1f}: {size_kb} (total: {size_kb:.1f} KiB)")
            log.debug(f"   Count diff:{start.count_diff:+d} (total: {start.count})")
            log.debug(f"   Traceback:")
            for frame in start.traceback:
                log.debug(f"        {frame.filename}:{frame.lineno}")
            if len(start.traceback) > 5:
                log.debug(f"     ... and {len(start.traceback) - 5} more frames")
        current, peak = tracemalloc.get_traced_memory()
        log.debug(f"📈 Current memory usage: {current / 1024:.1f} KiB")
        log.debug(f"📈 Peak memory usage: {peak / 1024:.1f} KiB")
        log.debug(f"{'='*60}\n")

        return result

    return wrapper

def frace_memory(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not tracemalloc.is_tracing():
            tracemalloc.start(50)
        snapshot_on_start = tracemalloc.take_snapshot()
        result = func(*args, **kwargs)
        snapshot_on_end = tracemalloc.take_snapshot()

        # Analysis
        top_starts = snapshot_on_end.compare_to(snapshot_on_start, 'traceback') #  lineno
        # Filter
        top_starts_list = [start for start in top_starts if start.size_diff >= 1024 * 300]
        # Publication
        log.debug(f"\n{'='*60}")
        log.debug(f"\nMemory usage for {func.__name__}")
        for ind, start in enumerate(top_starts_list):
            size_diff_kb = start.size_diff / 1024
            size_kb = start.size / 1024
            direction = "🔺 +" if start.size_diff > 0 else "🔻 "
            log.debug(f"{ind}. {direction}{abs(size_diff_kb):.1f}: {size_kb} (total: {size_kb:.1f} KiB)")
            log.debug(f"   Count diff:{start.count_diff:+d} (total: {start.count})")
            log.debug(f"   Traceback:")
            for frame in start.traceback:
                log.debug(f"        {frame.filename}:{frame.lineno}")
            if len(start.traceback) > 5:
                log.debug(f"     ... and {len(start.traceback) - 5} more frames")
        current, peak = tracemalloc.get_traced_memory()
        log.debug(f"📈 Current memory usage: {current / 1024:.1f} KiB")
        log.debug(f"📈 Peak memory usage: {peak / 1024:.1f} KiB")
        log.debug(f"{'='*60}\n")

        return result
    return wrapper
