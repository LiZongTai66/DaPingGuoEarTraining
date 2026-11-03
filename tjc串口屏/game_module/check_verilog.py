from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '_tools'))
import pyslang

def check(name):
    tree = pyslang.syntax.SyntaxTree.fromText((ROOT / name).read_text(encoding='utf-8'), name=name)
    compilation = pyslang.ast.Compilation()
    compilation.addSyntaxTree(tree)
    diagnostics = compilation.getAllDiagnostics()
    engine = pyslang.DiagnosticEngine(compilation.sourceManager)
    client = pyslang.TextDiagnosticClient()
    engine.addClient(client)
    for diagnostic in diagnostics:
        engine.issue(diagnostic)
    text = client.getString()
    (ROOT / (name + '.diagnostics.txt')).write_text(text, encoding='utf-8')
    print(f'{name}: {engine.numErrors} errors, {engine.numWarnings} warnings')
    if engine.numErrors:
        print(text)
    return engine.numErrors

errors = check('original_gowin.v') + check('piano_game_complete.v')
sys.exit(bool(errors))
