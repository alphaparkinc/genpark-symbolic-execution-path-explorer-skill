import sys
import json
from client import SymbolicExecutionEngine

engine = SymbolicExecutionEngine()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "symbolic_branch_explore",
                        "description": "Bifurcate symbolic state on comparison predicate",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "var_name": {"type": "string"},
                                "threshold": {"type": "number"}
                            },
                            "required": ["var_name", "threshold"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "symbolic_branch_explore":
            states = engine.execute_simple_branch(args["var_name"], args["threshold"])
            res = [{"variables": s.sym_vars, "path_condition": s.path_condition} for s in states]
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"branches": res})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
