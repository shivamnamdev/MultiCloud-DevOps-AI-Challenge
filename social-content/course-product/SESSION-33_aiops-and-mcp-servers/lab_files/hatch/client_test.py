import asyncio, os, json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(command="python", args=["hatch.py"], env={**os.environ, "PROM_URL": "http://det-prom:9090"})

def show(label, res):
    text = "".join(c.text for c in res.content if getattr(c, "text", None))
    print(f"[{label}] isError={res.isError} :: {text[:230].replace(chr(10), ' | ')}")

async def main():
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            print("server:", init.serverInfo.name, "| protocol:", init.protocolVersion)
            tools = await s.list_tools()
            for t in tools.tools:
                print("tool:", t.name, "| inputs:", list(t.inputSchema["properties"]), "|", (t.description or "")[:60])
            show("list_pods atithi", await s.call_tool("list_pods", {"namespace": "atithi"}))
            show("list_pods kube-system", await s.call_tool("list_pods", {"namespace": "kube-system"}))
            show("list_pods monitoring", await s.call_tool("list_pods", {"namespace": "monitoring"}))
            show("logs semicolon name", await s.call_tool("get_pod_logs", {"namespace": "atithi", "pod": "x; rm -rf /"}))
            show("logs $(subst) name", await s.call_tool("get_pod_logs", {"namespace": "atithi", "pod": "$(id)"}))
            res = await s.call_tool("get_pod_logs", {"namespace": "atithi", "pod": "logdemo", "tail": 100000})
            txt = res.content[0].text
            print(f"[logs tail=100000] lines returned: {len(txt.splitlines()) - 1} (cap 200) | starts with: {txt.splitlines()[0]!r}")
            print("   secret redacted:", "abc123" not in txt and "sk-FAKE" not in txt, "| injection line still present (only labelled untrusted):", "ignore your earlier instructions" in txt)
            show("logs of a pod in a forbidden ns", await s.call_tool("get_pod_logs", {"namespace": "kube-system", "pod": "coredns-x"}))
            show("logs missing pod", await s.call_tool("get_pod_logs", {"namespace": "atithi", "pod": "nope"}))
            show("prom ok", await s.call_tool("query_prometheus", {"promql": "up"}))
            show("prom bad promql", await s.call_tool("query_prometheus", {"promql": "sum(("}))
            show("prom 301 chars", await s.call_tool("query_prometheus", {"promql": "a" * 301}))
            show("prom empty", await s.call_tool("query_prometheus", {"promql": "  "}))
asyncio.run(main())
