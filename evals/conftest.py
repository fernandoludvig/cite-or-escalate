def pytest_terminal_summary(terminalreporter):
    """Imprime a tabela das quatro métricas no fim da rodada."""
    from evals.test_evals import METRICS, RUNS, THRESHOLDS

    write = terminalreporter.write_line
    write("")
    write(f"métricas — {len(RUNS)} casos")
    for name, value in METRICS.items():
        limit = THRESHOLDS[name]
        comparison = "<=" if name == "action_promise_rate" else ">="
        ok = value <= limit if name == "action_promise_rate" else value >= limit
        write(f"  {'ok ' if ok else 'FAIL'} {name:<22} {value:>6.1%}  ({comparison} {limit:.0%})")
