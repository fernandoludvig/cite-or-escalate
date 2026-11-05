"""Tracing OpenTelemetry do agente e do portão.

Três propriedades deliberadas:

1. **Sem SDK instalado, tudo vira no-op.** O pytest e o CI avaliam respostas
   gravadas e não podem passar a depender do OTel — o portão tem que rodar de
   graça em qualquer clone. Por isso o import é preguiçoso e `span()` cede
   `None` quando o SDK não está lá.
2. **Console por padrão.** Sem variável de ambiente nenhuma, os spans saem no
   terminal. Dá para ver o trace sem criar conta em nenhum SaaS.
3. **OTLP quando o ambiente pede.** Com `OTEL_EXPORTER_OTLP_ENDPOINT` definido,
   o exportador padrão do SDK lê endpoint e headers do próprio ambiente — é o
   que faz o mesmo trace servir Langfuse, LangSmith ou Arize sem código novo.

Atributos seguem as convenções semânticas `gen_ai.*`, não nomes inventados: é o
que torna o trace legível em qualquer um desses backends.

    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http

Langfuse (confirmado na doc em 05/11/2026):

    OTEL_EXPORTER_OTLP_ENDPOINT=https://cloud.langfuse.com/api/public/otel
    OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic $(printf '%s' "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" | base64),x-langfuse-ingestion-version=4"

LangSmith (idem; workspace por projeto):

    OTEL_EXPORTER_OTLP_ENDPOINT=https://api.smith.langchain.com/otel
    OTEL_EXPORTER_OTLP_HEADERS="x-api-key=$LANGSMITH_API_KEY,Langsmith-Project=cite-or-escalate"
"""

import os
from contextlib import contextmanager

SERVICE = "cite-or-escalate"

_tracer = False  # False = ainda não tentou; None = SDK ausente


def tracer():
    global _tracer
    if _tracer is False:
        _tracer = _build()
    return _tracer


def _build():
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        return None

    provider = TracerProvider(resource=Resource.create({"service.name": SERVICE}))
    provider.add_span_processor(BatchSpanProcessor(_exporter()))
    trace.set_tracer_provider(provider)
    return provider.get_tracer(SERVICE)


def _exporter():
    if os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"):
        # Lê endpoint e headers do ambiente. Atenção: endpoint errado falha em
        # silêncio — o SDK engole o erro de export e o trace simplesmente não
        # aparece no backend.
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        return OTLPSpanExporter()

    from opentelemetry.sdk.trace.export import ConsoleSpanExporter

    return ConsoleSpanExporter()


@contextmanager
def span(name: str, **attributes):
    """Abre um span, ou não faz nada se o SDK não estiver instalado."""
    current = tracer()
    if current is None:
        yield None
        return
    with current.start_as_current_span(name) as active:
        for key, value in attributes.items():
            active.set_attribute(key, value)
        yield active


def trace_id(active) -> str:
    """Id do trace em hex, ou string vazia quando não há span."""
    return format(active.get_span_context().trace_id, "032x") if active else ""


if __name__ == "__main__":
    # Auto-checagem: exercita o caminho inteiro sem gastar chamada de API.
    with span("self-check", **{"gen_ai.operation.name": "chat"}) as parent:
        parent_id = trace_id(parent)
        with span("child") as child:
            assert trace_id(child) == parent_id, "filho deveria herdar o trace do pai"
    if tracer() is None:
        print("SDK do OTel ausente — span() virou no-op, como previsto.")
    else:
        assert len(parent_id) == 32, parent_id
        print(f"\ntrace_id: {parent_id}")
