"""Code analysis utilities"""

import enum
from typing import overload

import pyslang
import pyslang.ast


class DriverKind(enum.Enum):
    Procedural = 0

    Continuous = 1

class DriverSource(enum.Enum):
    Initial = 0

    Final = 1

    Always = 2

    AlwaysComb = 3

    AlwaysLatch = 4

    AlwaysFF = 5

    Subroutine = 6

    Other = 7

class DriverFlags(enum.IntEnum):
    InputPort = 1

    OutputPort = 2

    ClockVar = 4

    Initializer = 8

    FromSideEffect = 16

    HasOverrideRange = 32

    ViaIndirectPort = 64

class AnalysisFlags(enum.IntEnum):
    CheckUnused = 1

    FullCaseUniquePriority = 2

    FullCaseFourState = 4

    AllowMultiDrivenLocals = 8

    AllowDupInitialDrivers = 16

    CheckShadow = 32

    InlineContAssignFunctionReads = 64

    AlwaysStarUsesLSPs = 128

    ContAssignUsesLSPs = 256

class AnalysisOptions:
    def __init__(self) -> None: ...

    @property
    def flags(self) -> AnalysisFlags: ...

    @flags.setter
    def flags(self, arg: AnalysisFlags, /) -> None: ...

    @property
    def maxCaseAnalysisSteps(self) -> int: ...

    @maxCaseAnalysisSteps.setter
    def maxCaseAnalysisSteps(self, arg: int, /) -> None: ...

    @property
    def maxLoopAnalysisSteps(self) -> int: ...

    @maxLoopAnalysisSteps.setter
    def maxLoopAnalysisSteps(self, arg: int, /) -> None: ...

class AnalyzedScope:
    @property
    def scope(self) -> pyslang.ast.Scope: ...

    @property
    def procedures(self) -> list[AnalyzedProcedure]: ...

class ValueDriver:
    @property
    def path(self) -> pyslang.ast.ValuePath: ...

    @property
    def containingSymbol(self) -> pyslang.ast.Symbol: ...

    @property
    def flags(self) -> DriverFlags: ...

    @property
    def kind(self) -> DriverKind: ...

    @property
    def source(self) -> DriverSource: ...

    @property
    def symbol(self) -> pyslang.ast.ValueSymbol: ...

    @property
    def bounds(self) -> tuple[int, int]: ...

    @property
    def sourceRange(self) -> pyslang.SourceRange: ...

    @property
    def overrideRange(self) -> pyslang.SourceRange: ...

    @property
    def isInputPort(self) -> bool: ...

    @property
    def isUnidirectionalPort(self) -> bool: ...

    @property
    def isClockVar(self) -> bool: ...

    @property
    def isInSingleDriverProcedure(self) -> bool: ...

class AnalysisManager:
    def __init__(self, options: AnalysisOptions = ...) -> None: ...

    def addProcListener(self, listener: object) -> None: ...

    def addScopeListener(self, listener: object) -> None: ...

    def addAssertionListener(self, listener: object) -> None: ...

    def analyze(self, compilation: pyslang.ast.Compilation) -> None: ...

    def getDrivers(self, symbol: pyslang.ast.ValueSymbol) -> list[ValueDriver]: ...

    def getDiagnostics(self) -> pyslang.Diagnostics: ...

    def getAnalyzedScope(self, scope: pyslang.ast.Scope) -> AnalyzedScope: ...

    def getAnalyzedSubroutine(self, symbol: pyslang.ast.SubroutineSymbol) -> AnalyzedProcedure: ...

    def getAnalyzedAssertions(self, symbol: pyslang.ast.Symbol) -> list[AnalyzedAssertion]: ...

    @property
    def options(self) -> AnalysisOptions: ...

class ReadRange:
    @property
    def symbol(self) -> pyslang.ast.ValueSymbol: ...

    @property
    def bitRange(self) -> tuple[int, int]: ...

class SensitivityListKind(enum.Enum):
    Explicit = 1

    Implicit = 2

    Dynamic = 3

class SensitivityList:
    @property
    def kind(self) -> SensitivityListKind: ...

    @property
    def timingControl(self) -> pyslang.ast.TimingControl: ...

    @property
    def reads(self) -> span[ReadRange]: ...

class ImplicitEventReadSet:
    @property
    def statement(self) -> pyslang.ast.Statement: ...

    @property
    def reads(self) -> span[ReadRange]: ...

class AnalyzedProcedure:
    @property
    def analyzedSymbol(self) -> pyslang.ast.Symbol: ...

    @property
    def parentProcedure(self) -> AnalyzedProcedure: ...

    @property
    def inferredClock(self) -> pyslang.ast.TimingControl: ...

    @property
    def drivers(self) -> span[ValueDriver]: ...

    @property
    def callExpressions(self) -> span[pyslang.ast.CallExpression]: ...

    @property
    def timingControls(self) -> span[pyslang.ast.Statement]: ...

    @property
    def readSet(self) -> span[ReadRange]: ...

    @property
    def implicitEventReadSets(self) -> span[ImplicitEventReadSet]: ...

    @property
    def sensitivityList(self) -> SensitivityList: ...

class AnalyzedAssertion:
    @property
    def containingSymbol(self) -> pyslang.ast.Symbol: ...

    @property
    def procedure(self) -> AnalyzedProcedure: ...

    @property
    def astNode(self) -> pyslang.ast.ConcurrentAssertionStatement | pyslang.ast.AssertionInstanceExpression: ...

    @property
    def semanticLeadingClock(self) -> pyslang.ast.TimingControl: ...

    @property
    def root(self) -> pyslang.ast.AssertionExpr: ...

    def getClock(self, expr: pyslang.ast.AssertionExpr) -> pyslang.ast.TimingControl: ...

class FlowAnalysis:
    """
    A flow analysis visitor that walks statements with proper control flow handling.

    Set callback attributes before calling run():
    - onAssignment: called for each assignment expression
    - onVariableRef: called for each variable reference (NamedValueExpression)
    - onCallExpression: called for each function/task call
    - onConditionalBegin: called when entering an if/else
    - onCaseBegin: called when entering a case statement
    - onLoopBegin: called when entering any loop statement
    - onBranchMerge: called when control flow paths merge (state1, state2) -> merged_state
    - onStateCopy: called to copy state when forking (state) -> copied_state
    - createTopState: called to create initial state () -> state
    """

    def __init__(self, symbol: pyslang.ast.Symbol, options: AnalysisOptions = ...) -> None:
        """
        Create a flow analysis for the given symbol (procedural block, subroutine, etc.)
        """

    @overload
    def run(self, stmt: pyslang.ast.Statement) -> None:
        """Run the analysis on a statement"""

    @overload
    def run(self, expr: pyslang.ast.Expression) -> None:
        """Run the analysis on an expression"""

    @property
    def currentState(self) -> object:
        """The current flow state's user data"""

    @currentState.setter
    def currentState(self, arg: object, /) -> None: ...

    @property
    def bad(self) -> bool:
        """True if the analysis detected an error"""

    @property
    def evalContext(self) -> pyslang.ast.EvalContext:
        """The evaluation context for use during analysis"""

    @property
    def onAssignment(self) -> object:
        """Callback for assignment expressions: (AssignmentExpression) -> None"""

    @onAssignment.setter
    def onAssignment(self, arg: object, /) -> None: ...

    @property
    def onVariableRef(self) -> object:
        """Callback for variable references: (NamedValueExpression) -> None"""

    @onVariableRef.setter
    def onVariableRef(self, arg: object, /) -> None: ...

    @property
    def onCallExpression(self) -> object:
        """Callback for function/task calls: (CallExpression) -> None"""

    @onCallExpression.setter
    def onCallExpression(self, arg: object, /) -> None: ...

    @property
    def onConditionalBegin(self) -> object:
        """Callback when entering conditional: (ConditionalStatement) -> None"""

    @onConditionalBegin.setter
    def onConditionalBegin(self, arg: object, /) -> None: ...

    @property
    def onCaseBegin(self) -> object:
        """Callback when entering case: (CaseStatement) -> None"""

    @onCaseBegin.setter
    def onCaseBegin(self, arg: object, /) -> None: ...

    @property
    def onLoopBegin(self) -> object:
        """Callback when entering any loop: (Statement) -> None"""

    @onLoopBegin.setter
    def onLoopBegin(self, arg: object, /) -> None: ...

    @property
    def onBranchMerge(self) -> object:
        """Callback when branches merge: (state1, state2) -> merged_state"""

    @onBranchMerge.setter
    def onBranchMerge(self, arg: object, /) -> None: ...

    @property
    def onStateCopy(self) -> object:
        """Callback to copy state: (state) -> copied_state"""

    @onStateCopy.setter
    def onStateCopy(self, arg: object, /) -> None: ...

    @property
    def createTopState(self) -> object:
        """Callback to create initial state: () -> state"""

    @createTopState.setter
    def createTopState(self, arg: object, /) -> None: ...
