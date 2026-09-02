import json

with open("user_actions.json", encoding="utf-8") as f:
    d = json.load(f)

print("FLOW_ID =", d[0].get("flow_id"))
print("CANTIDAD =", len(d))
print()

for i, a in enumerate(d[:40]):
    print(
        f"{i+1:03} | "
        f"tipo={a.get('tipo')} | "
        f"logico={a.get('tipo_logico')} | "
        f"componente={a.get('tipo_componente')} | "
        f"tag={a.get('tag')} | "
        f"texto={a.get('texto')} | "
        f"valor={a.get('valor')} | "
        f"field={a.get('field')} | "
        f"locator={a.get('playwright_locator')} | "
        f"score={a.get('locator_score')}"
    )