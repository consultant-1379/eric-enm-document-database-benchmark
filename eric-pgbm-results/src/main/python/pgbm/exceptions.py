"""
This custom defined exception is raised when the benchmark job status
returns as "Failed" (see init_wait_pgbm.wait_for_benchmark() for usage).
The exception is then handled in the main script (see result_service.py)
where the overall exit status is handled (once an exception is thrown).
"""


class PgBenchmarkError(Exception):
    pass
