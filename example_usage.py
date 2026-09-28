from client import SymbolicExecutionEngine

engine = SymbolicExecutionEngine()
branches = engine.execute_simple_branch("account_balance", 1000)
for idx, branch in enumerate(branches):
    print(f"Branch {idx}: Variables={branch.sym_vars}, Conditions={branch.path_condition}")
