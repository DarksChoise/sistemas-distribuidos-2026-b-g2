"""Two metrics of the enroll-student saga, exposed on /metrics in the Prometheus text format."""

from prometheus_client import CollectorRegistry, Counter, Histogram

REGISTRY = CollectorRegistry()

SAGA_REQUESTS = Counter(
    "workflow_saga_requests_total",
    "enroll-student sagas by outcome",
    ["saga", "outcome"],
    registry=REGISTRY,
)

# Buckets around what a student waits for in the enrollment page: under 1 s is fine, 3 s is the
# billing timeout, 10 s is the most the portal shows "Enrolling..." before it gives up.
SAGA_DURATION = Histogram(
    "workflow_saga_duration_seconds",
    "Time from the POST of the saga to its final state",
    ["saga", "outcome"],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0),
    registry=REGISTRY,
)
