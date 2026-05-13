# FinVision Backend - OpenRun (Clace) App Configuration
# Declares a containerized FastAPI app to be managed by the OpenRun server.
# OpenRun will handle: container build, lifecycle, reverse proxy, and TLS.

load("proxy.in", "proxy")
load("container.in", "container")

# App parameters (injected at deploy time via `openrun param set`)
app = ace.app(
    param.app_name if hasattr(param, "app_name") else "finvision-backend",
    routes=[
        ace.proxy("/", proxy.config(container.URL))
    ],
    container=container.config(
        container.AUTO,
        port=8080,
        health_url="/health",
    ),
    permissions=[
        ace.permission("proxy.in", "config", [container.URL]),
        ace.permission("container.in", "config", []),
    ]
)
