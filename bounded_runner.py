"""Replay recorded adapter events with a hard attempt budget and explicit fallback."""
import argparse, json, math


def run(events, max_attempts=3, fallback=None):
    if (
        isinstance(max_attempts, bool)
        or not isinstance(max_attempts, int)
        or max_attempts < 1
    ):
        raise ValueError("max_attempts must be a positive integer")
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    trace = []
    cost = 0.0

    def consume(event, source):
        nonlocal cost
        if not isinstance(event, dict):
            raise ValueError("event must be an object")
        value = event.get("reported_cost")
        if value is not None and (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
        ):
            raise ValueError("reported_cost must be finite nonnegative or null")
        if value is not None:
            cost += value
        status = event.get("status")
        if status not in ["ok", "timeout", "error", "invalid"]:
            raise ValueError("invalid event status")
        accepted = (
            status == "ok"
            and isinstance(event.get("payload"), dict)
            and bool(event["payload"])
        )
        trace.append(
            {
                "attempt": len(trace) + 1,
                "source": source,
                "status": status if status != "ok" or accepted else "invalid",
                "reported_cost": value,
            }
        )
        return event["payload"] if accepted else None

    budget = max_attempts - (1 if fallback is not None else 0)
    for event in events[:budget]:
        result = consume(event, "primary")
        if result is not None:
            break
    else:
        result = None
    if result is None and fallback is not None and len(trace) < max_attempts:
        result = consume(fallback, "fallback")
    known = all(e["reported_cost"] is not None for e in trace)
    return {
        "mode": "offline_event_replay",
        "status": "accepted" if result is not None else "needs_review",
        "result": result,
        "attempts": len(trace),
        "max_attempts": max_attempts,
        "reported_cost_total": cost if known else None,
        "reported_cost_known_subtotal": cost,
        "trace": trace,
        "external_actions_executed": 0,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("config")
    a = p.parse_args()
    try:
        with open(a.config, encoding="utf-8-sig") as f:
            c = json.load(f)
        print(
            json.dumps(
                run(c["events"], c.get("max_attempts", 3), c.get("fallback")),
                indent=2,
                ensure_ascii=False,
                allow_nan=False,
            )
        )
    except (ValueError, KeyError) as e:
        p.error(str(e))


if __name__ == "__main__":
    main()
