"""AST types: symbols, expressions, statements, types"""

from collections.abc import Callable, Iterator, Sequence, Set
import enum
from typing import Final, overload

import pyslang
import pyslang.parsing
import pyslang.syntax


class PatternKind(enum.Enum):
    Invalid = 0

    Wildcard = 1

    Constant = 2

    Variable = 3

    Tagged = 4

    Structure = 5

class TimingControlKind(enum.Enum):
    Invalid = 0

    Delay = 1

    SignalEvent = 2

    EventList = 3

    ImplicitEvent = 4

    RepeatedEvent = 5

    Delay3 = 6

    OneStepDelay = 7

    CycleDelay = 8

    BlockEventList = 9

class ConstraintKind(enum.Enum):
    Invalid = 0

    List = 1

    Expression = 2

    Implication = 3

    Conditional = 4

    Uniqueness = 5

    DisableSoft = 6

    SolveBefore = 7

    Foreach = 8

class AssertionExprKind(enum.Enum):
    Invalid = 0

    Simple = 1

    SequenceConcat = 2

    SequenceWithMatch = 3

    Unary = 4

    Binary = 5

    FirstMatch = 6

    Clocking = 7

    StrongWeak = 8

    Abort = 9

    Conditional = 10

    Case = 11

    DisableIff = 12

class UnaryAssertionOperator(enum.Enum):
    Not = 0

    NextTime = 1

    SNextTime = 2

    Always = 3

    SAlways = 4

    Eventually = 5

    SEventually = 6

class BinaryAssertionOperator(enum.Enum):
    And = 0

    Or = 1

    Intersect = 2

    Throughout = 3

    Within = 4

    Iff = 5

    Until = 6

    SUntil = 7

    UntilWith = 8

    SUntilWith = 9

    Implies = 10

    OverlappedImplication = 11

    NonOverlappedImplication = 12

    OverlappedFollowedBy = 13

    NonOverlappedFollowedBy = 14

class BinsSelectExprKind(enum.Enum):
    Invalid = 0

    Condition = 1

    Unary = 2

    Binary = 3

    SetExpr = 4

    WithFilter = 5

    CrossId = 6

class DimensionKind(enum.Enum):
    Unknown = 0

    Range = 1

    AbbreviatedRange = 2

    Dynamic = 3

    Associative = 4

    Queue = 5

    DPIOpenArray = 6

class ValueRangeKind(enum.Enum):
    Simple = 0

    AbsoluteTolerance = 1

    RelativeTolerance = 2

class VisitAction(enum.Enum):
    Advance = 0

    Skip = 1

    Interrupt = 2

class EvalFlags(enum.IntEnum):
    IsScript = 1

    CacheResults = 2

    SpecparamsAllowed = 4

    AllowUnboundedPlaceholder = 8

class EvalContext:
    @overload
    def __init__(self, astCtx: ASTContext, flags: EvalFlags = EvalFlags.None_) -> None: ...

    @overload
    def __init__(self, symbol: Symbol, flags: EvalFlags = EvalFlags.None_) -> None: ...

    @property
    def flags(self) -> EvalFlags: ...

    def createLocal(self, symbol: ValueSymbol, value: pyslang.ConstantValue | None = None) -> pyslang.ConstantValue: ...

    def findLocal(self, symbol: ValueSymbol) -> pyslang.ConstantValue: ...

    def deleteLocal(self, symbol: ValueSymbol) -> None: ...

    def pushFrame(self, subroutine: SubroutineSymbol, callLocation: pyslang.SourceLocation, lookupLocation: LookupLocation) -> bool: ...

    def pushEmptyFrame(self) -> None: ...

    def popFrame(self) -> None: ...

    def pushLValue(self, lval: LValue) -> None: ...

    def popLValue(self) -> None: ...

    def step(self, loc: pyslang.SourceLocation) -> bool: ...

    def setDisableTarget(self, arg0: Symbol, arg1: pyslang.SourceRange, /) -> None: ...

    def dumpStack(self) -> str: ...

    @property
    def topLValue(self) -> LValue: ...

    @property
    def inFunction(self) -> bool: ...

    @property
    def cacheResults(self) -> bool: ...

    @property
    def topFrame(self) -> EvalContext.Frame: ...

    @property
    def disableTarget(self) -> Symbol: ...

    @property
    def disableRange(self) -> pyslang.SourceRange: ...

    @property
    def diagnostics(self) -> pyslang.Diagnostics: ...

    @property
    def queueTarget(self) -> pyslang.ConstantValue: ...

    @queueTarget.setter
    def queueTarget(self, arg: pyslang.ConstantValue, /) -> None: ...

    class Frame:
        @property
        def temporaries(self) -> "std::map<slang::ast::ValueSymbol const * __ptr64,slang::ConstantValue,std::less<slang::ast::ValueSymbol const * __ptr64>,std::allocator<std::pair<slang::ast::ValueSymbol const * __ptr64 const,slang::ConstantValue> > >": ...

        @property
        def subroutine(self) -> SubroutineSymbol: ...

        @property
        def callLocation(self) -> pyslang.SourceLocation: ...

        @property
        def lookupLocation(self) -> LookupLocation: ...

class LValue:
    def __init__(self) -> None: ...

    def bad(self) -> bool: ...

    def resolve(self) -> pyslang.ConstantValue: ...

    def load(self) -> pyslang.ConstantValue: ...

    def store(self, value: pyslang.ConstantValue) -> None: ...

class ASTFlags(enum.IntEnum):
    InsideConcatenation = 1

    UnevaluatedBranch = 2

    AllowDataType = 4

    AssignmentAllowed = 8

    AssignmentDisallowed = 16

    NonProcedural = 32

    StaticInitializer = 64

    StreamingAllowed = 128

    TopLevelStatement = 256

    AllowUnboundedLiteral = 512

    AllowUnboundedLiteralArithmetic = 1024

    Function = 2048

    Final = 4096

    NonBlockingTimingControl = 8192

    EventExpression = 16384

    AllowTypeReferences = 32768

    AssertionExpr = 65536

    AllowClockingBlock = 131072

    AssertionInstanceArgCheck = 262144

    AssertionDelayOrRepetition = 524288

    LValue = 1048576

    PropertyNegation = 2097152

    PropertyTimeAdvance = 4194304

    RecursivePropertyArg = 8388608

    ConcurrentAssertActionBlock = 16777216

    AllowCoverageSampleFormal = 33554432

    AllowCoverpoint = 67108864

    AllowNetType = 134217728

    OutputArg = 268435456

    AllowInterconnect = 536870912

    StreamingWithRange = 1073741824

    SpecifyBlock = 2147483648

    SpecparamInitializer = 4294967296

    DPIArg = 8589934592

    AssertionDefaultArg = 17179869184

    LAndRValue = 34359738368

    NoReference = 68719476736

    ConfigParam = 137438953472

    TypeOperator = 274877906944

    ForkJoinAnyNone = 549755813888

    DisallowUDNT = 1099511627776

    BindInstantiation = 2199023255552

    WildcardPortConn = 4398046511104

class EvaluatedDimension:
    @property
    def kind(self) -> DimensionKind: ...

    @property
    def range(self) -> pyslang.ConstantRange: ...

    @property
    def associativeType(self) -> Type: ...

    @property
    def queueMaxSize(self) -> int: ...

    @property
    def leftExpr(self) -> Expression: ...

    @property
    def rightExpr(self) -> Expression: ...

    @property
    def isRange(self) -> bool: ...

class ASTContext:
    def __init__(self, scope: Scope, lookupLocation: LookupLocation, flags: ASTFlags = ASTFlags.None_) -> None: ...

    @property
    def scope(self) -> Scope: ...

    @property
    def lookupIndex(self) -> "slang::ast::SymbolIndex": ...

    @property
    def flags(self) -> ASTFlags: ...

    @property
    def getCompilation(self) -> Compilation: ...

    @property
    def getLocation(self) -> LookupLocation: ...

    @property
    def inUnevaluatedBranch(self) -> bool: ...

    @property
    def getInstance(self) -> InstanceSymbolBase: ...

    @property
    def getProceduralBlock(self) -> ProceduralBlockSymbol: ...

    @property
    def inAlwaysCombLatch(self) -> bool: ...

    @overload
    def addDiag(self, code: pyslang.DiagCode, location: pyslang.SourceLocation) -> pyslang.Diagnostic: ...

    @overload
    def addDiag(self, code: pyslang.DiagCode, sourceRange: pyslang.SourceRange) -> pyslang.Diagnostic: ...

    @overload
    def requireIntegral(self, expr: Expression) -> bool: ...

    @overload
    def requireIntegral(self, cv: pyslang.ConstantValue, range: pyslang.SourceRange) -> bool: ...

    def requireNoUnknowns(self, value: pyslang.SVInt, range: pyslang.SourceRange) -> bool: ...

    @overload
    def requirePositive(self, value: pyslang.SVInt, range: pyslang.SourceRange) -> bool: ...

    @overload
    def requirePositive(self, value: int | None, range: pyslang.SourceRange) -> bool: ...

    def requireGtZero(self, value: int | None, range: pyslang.SourceRange) -> bool: ...

    def requireBooleanConvertible(self, expr: Expression) -> bool: ...

    @overload
    def requireValidBitWidth(self, width: int, range: pyslang.SourceRange) -> bool: ...

    @overload
    def requireValidBitWidth(self, value: pyslang.SVInt, range: pyslang.SourceRange) -> int | None: ...

    def eval(self, expr: Expression, extraFlags: EvalFlags = ASTFlags.None_) -> pyslang.ConstantValue: ...

    def tryEval(self, expr: Expression) -> pyslang.ConstantValue: ...

    @overload
    def evalInteger(self, syntax: pyslang.syntax.ExpressionSyntax, extraFlags: ASTFlags = ASTFlags.None_) -> int | None: ...

    @overload
    def evalInteger(self, expr: Expression, extraFlags: EvalFlags = ASTFlags.None_) -> int | None: ...

    def evalDimension(self, syntax: pyslang.syntax.VariableDimensionSyntax, requireRange: bool, isPacked: bool) -> EvaluatedDimension: ...

    @overload
    def evalPackedDimension(self, syntax: pyslang.syntax.VariableDimensionSyntax) -> EvaluatedDimension: ...

    @overload
    def evalPackedDimension(self, syntax: pyslang.syntax.ElementSelectSyntax) -> EvaluatedDimension: ...

    def evalUnpackedDimension(self, syntax: pyslang.syntax.VariableDimensionSyntax) -> EvaluatedDimension: ...

    @overload
    def requireSimpleExpr(self, expr: pyslang.syntax.PropertyExprSyntax) -> pyslang.syntax.ExpressionSyntax: ...

    @overload
    def requireSimpleExpr(self, expr: pyslang.syntax.PropertyExprSyntax, code: pyslang.DiagCode) -> pyslang.syntax.ExpressionSyntax: ...

    def getRandMode(self, symbol: Symbol) -> RandMode: ...

    def addAssertionBacktrace(self, diag: pyslang.Diagnostic) -> None: ...

    def resetFlags(self, addedFlags: ASTFlags) -> ASTContext: ...

class ValuePath:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, expr: Expression, evalContext: EvalContext) -> None: ...

    @property
    def rootExpr(self) -> Expression: ...

    @property
    def fullExpr(self) -> Expression: ...

    @property
    def lsp(self) -> Expression: ...

    @property
    def lspBounds(self) -> tuple[int, int]: ...

    @property
    def rootSymbol(self) -> ValueSymbol: ...

    @property
    def empty(self) -> bool: ...

    @property
    def isFullyStatic(self) -> bool: ...

    def toString(self, evalContext: EvalContext) -> str: ...

    def overlaps(self, other: ValuePath) -> bool: ...

    def __iter__(self) -> Iterator[Expression]: ...

    def expandIndirectRefs(self, alloc: pyslang.BumpAllocator, evalContext: EvalContext, callback: Callable) -> None: ...

    @staticmethod
    def visitPaths(expr: Expression, evalContext: EvalContext, callback: Callable, skipSelectors: bool = False) -> None: ...

class Pattern:
    @property
    def kind(self) -> PatternKind: ...

    @property
    def syntax(self) -> pyslang.syntax.SyntaxNode: ...

    @property
    def sourceRange(self) -> pyslang.SourceRange: ...

    @property
    def bad(self) -> bool: ...

    def eval(self, context: EvalContext, value: pyslang.ConstantValue, conditionKind: CaseStatementCondition) -> pyslang.ConstantValue: ...

    def isEquivalentTo(self, other: Pattern) -> bool: ...

    def __repr__(self) -> str: ...

class InvalidPattern(Pattern):
    pass

class WildcardPattern(Pattern):
    pass

class ConstantPattern(Pattern):
    @property
    def expr(self) -> Expression: ...

class VariablePattern(Pattern):
    @property
    def variable(self) -> PatternVarSymbol: ...

class TaggedPattern(Pattern):
    @property
    def valuePattern(self) -> Pattern: ...

    @property
    def member(self) -> FieldSymbol: ...

class StructurePattern(Pattern):
    @property
    def patterns(self) -> span[StructurePattern.FieldPattern]: ...

    class FieldPattern:
        @property
        def field(self) -> FieldSymbol: ...

        @property
        def pattern(self) -> Pattern: ...

class TimingControl:
    @property
    def kind(self) -> TimingControlKind: ...

    @property
    def syntax(self) -> pyslang.syntax.SyntaxNode: ...

    @property
    def sourceRange(self) -> pyslang.SourceRange: ...

    @property
    def bad(self) -> bool: ...

    def isEquivalentTo(self, other: TimingControl) -> bool: ...

    def visit(self, f: object | None = None, lookup_table: object | None = None) -> None:
        """
        Visit a pyslang object with a callback function `f` or a `lookup_table` dict.

        At least one of `f` or `lookup_table` must be provided (both default to `None`). If both are provided, 'lookup_table' will be used to decide which callback to use.

        When `f` is provided without `lookup_table`, it is called for every node visited. The callback should take a single argument (the current node). Its return value controls traversal: `pyslang.VisitAction.Interrupt` aborts the visit, `pyslang.VisitAction.Skip` skips child nodes, and any other return value (including `pyslang.VisitAction.Advance` or `None`) continues normally.

        When `lookup_table` is provided, it should be a dict mapping node kind enum values to handler functions. The C++ side checks each node's kind before crossing the Python boundary, calling only the matching handler. Nodes not in the table are traversed without invoking Python. `f` is not called in this mode.

        The `lookup_table` is compiled into native lookups when the visit begins and must not be mutated during traversal.
        """

    def __repr__(self) -> str: ...

class InvalidTimingControl(TimingControl):
    pass

class ImplicitEventControl(TimingControl):
    pass

class OneStepDelayControl(TimingControl):
    pass

class DelayControl(TimingControl):
    @property
    def expr(self) -> Expression: ...

class Delay3Control(TimingControl):
    @property
    def expr1(self) -> Expression: ...

    @property
    def expr2(self) -> Expression: ...

    @property
    def expr3(self) -> Expression: ...

class SignalEventControl(TimingControl):
    @property
    def expr(self) -> Expression: ...

    @property
    def iffCondition(self) -> Expression: ...

    @property
    def edge(self) -> EdgeKind: ...

class EventListControl(TimingControl):
    @property
    def events(self) -> span[TimingControl]: ...

class RepeatedEventControl(TimingControl):
    @property
    def expr(self) -> Expression: ...

    @property
    def event(self) -> TimingControl: ...

class CycleDelayControl(TimingControl):
    @property
    def expr(self) -> Expression: ...

class BlockEventListControl(TimingControl):
    @property
    def events(self) -> span[BlockEventListControl.Event]: ...

    class Event:
        @property
        def target(self) -> Expression: ...

        @property
        def isBegin(self) -> bool: ...

class Constraint:
    @property
    def kind(self) -> ConstraintKind: ...

    @property
    def syntax(self) -> pyslang.syntax.ConstraintItemSyntax: ...

    @property
    def bad(self) -> bool: ...

    def isEquivalentTo(self, other: Constraint) -> bool: ...

    def __repr__(self) -> str: ...

class InvalidConstraint(Constraint):
    pass

class ConstraintList(Constraint):
    @property
    def list(self) -> span[Constraint]: ...

class ExpressionConstraint(Constraint):
    @property
    def isSoft(self) -> bool: ...

    @property
    def expr(self) -> Expression: ...

class ImplicationConstraint(Constraint):
    @property
    def predicate(self) -> Expression: ...

    @property
    def body(self) -> Constraint: ...

class ConditionalConstraint(Constraint):
    @property
    def predicate(self) -> Expression: ...

    @property
    def ifBody(self) -> Constraint: ...

    @property
    def elseBody(self) -> Constraint: ...

class UniquenessConstraint(Constraint):
    @property
    def items(self) -> span[Expression]: ...

class DisableSoftConstraint(Constraint):
    @property
    def target(self) -> Expression: ...

class SolveBeforeConstraint(Constraint):
    @property
    def solve(self) -> span[Expression]: ...

    @property
    def after(self) -> span[Expression]: ...

class ForeachConstraint(Constraint):
    @property
    def arrayRef(self) -> Expression: ...

    @property
    def body(self) -> Constraint: ...

    @property
    def loopDims(self) -> span[ForeachLoopStatement.LoopDim]: ...

class AssertionExpr:
    @property
    def kind(self) -> AssertionExprKind: ...

    @property
    def syntax(self) -> pyslang.syntax.SyntaxNode: ...

    @property
    def bad(self) -> bool: ...

    def isEquivalentTo(self, other: AssertionExpr) -> bool: ...

    def __repr__(self) -> str: ...

class InvalidAssertionExpr(AssertionExpr):
    pass

class SequenceRange:
    @property
    def min(self) -> int: ...

    @property
    def max(self) -> int | None: ...

class SequenceRepetition:
    @property
    def kind(self) -> SequenceRepetition.Kind: ...

    @property
    def range(self) -> SequenceRange: ...

    class Kind(enum.Enum):
        Consecutive = 0

        Nonconsecutive = 1

        GoTo = 2

    Consecutive: SequenceRepetition.Kind = SequenceRepetition.Kind.Consecutive

    Nonconsecutive: SequenceRepetition.Kind = SequenceRepetition.Kind.Nonconsecutive

    GoTo: SequenceRepetition.Kind = SequenceRepetition.Kind.GoTo

class SimpleAssertionExpr(AssertionExpr):
    @property
    def expr(self) -> Expression: ...

    @property
    def repetition(self) -> SequenceRepetition | None: ...

class SequenceConcatExpr(AssertionExpr):
    @property
    def elements(self) -> span[SequenceConcatExpr.Element]: ...

    class Element:
        @property
        def delay(self) -> SequenceRange: ...

        @property
        def sequence(self) -> AssertionExpr: ...

class SequenceWithMatchExpr(AssertionExpr):
    @property
    def expr(self) -> AssertionExpr: ...

    @property
    def repetition(self) -> SequenceRepetition | None: ...

    @property
    def matchItems(self) -> span[Expression]: ...

class UnaryAssertionExpr(AssertionExpr):
    @property
    def expr(self) -> AssertionExpr: ...

    @property
    def op(self) -> UnaryAssertionOperator: ...

    @property
    def range(self) -> SequenceRange | None: ...

class BinaryAssertionExpr(AssertionExpr):
    @property
    def left(self) -> AssertionExpr: ...

    @property
    def right(self) -> AssertionExpr: ...

    @property
    def op(self) -> BinaryAssertionOperator: ...

class FirstMatchAssertionExpr(AssertionExpr):
    @property
    def seq(self) -> AssertionExpr: ...

    @property
    def matchItems(self) -> span[Expression]: ...

class ClockingAssertionExpr(AssertionExpr):
    @property
    def clocking(self) -> TimingControl: ...

    @property
    def expr(self) -> AssertionExpr: ...

class StrongWeakAssertionExpr(AssertionExpr):
    @property
    def expr(self) -> AssertionExpr: ...

    @property
    def strength(self) -> StrongWeakAssertionExpr.Strength: ...

    class Strength(enum.Enum):
        Strong = 0

        Weak = 1

    Strong: StrongWeakAssertionExpr.Strength = StrongWeakAssertionExpr.Strength.Strong

    Weak: StrongWeakAssertionExpr.Strength = StrongWeakAssertionExpr.Strength.Weak

class AbortAssertionExpr(AssertionExpr):
    @property
    def condition(self) -> Expression: ...

    @property
    def expr(self) -> AssertionExpr: ...

    @property
    def action(self) -> AbortAssertionExpr.Action: ...

    @property
    def isSync(self) -> bool: ...

    class Action(enum.Enum):
        Accept = 0

        Reject = 1

    Accept: AbortAssertionExpr.Action = AbortAssertionExpr.Action.Accept

    Reject: AbortAssertionExpr.Action = AbortAssertionExpr.Action.Reject

class ConditionalAssertionExpr(AssertionExpr):
    @property
    def condition(self) -> Expression: ...

    @property
    def ifExpr(self) -> AssertionExpr: ...

    @property
    def elseExpr(self) -> AssertionExpr: ...

class CaseAssertionExpr(AssertionExpr):
    @property
    def expr(self) -> Expression: ...

    @property
    def items(self) -> span[CaseAssertionExpr.ItemGroup]: ...

    @property
    def defaultCase(self) -> AssertionExpr: ...

    class ItemGroup:
        @property
        def expressions(self) -> span[Expression]: ...

        @property
        def body(self) -> AssertionExpr: ...

class DisableIffAssertionExpr(AssertionExpr):
    @property
    def condition(self) -> Expression: ...

    @property
    def expr(self) -> AssertionExpr: ...

class BinsSelectExpr:
    @property
    def kind(self) -> BinsSelectExprKind: ...

    @property
    def syntax(self) -> pyslang.syntax.SyntaxNode: ...

    @property
    def bad(self) -> bool: ...

    def __repr__(self) -> str: ...

class InvalidBinsSelectExpr(BinsSelectExpr):
    pass

class CrossIdBinsSelectExpr(BinsSelectExpr):
    pass

class ConditionBinsSelectExpr(BinsSelectExpr):
    @property
    def target(self) -> Symbol: ...

    @property
    def intersects(self) -> span[Expression]: ...

class UnaryBinsSelectExpr(BinsSelectExpr):
    @property
    def expr(self) -> BinsSelectExpr: ...

    @property
    def op(self) -> UnaryBinsSelectExpr.Op: ...

    class Op(enum.Enum):
        Negation = 0

    Negation: UnaryBinsSelectExpr.Op = UnaryBinsSelectExpr.Op.Negation

class BinaryBinsSelectExpr(BinsSelectExpr):
    @property
    def left(self) -> BinsSelectExpr: ...

    @property
    def right(self) -> BinsSelectExpr: ...

    @property
    def op(self) -> BinaryBinsSelectExpr.Op: ...

    class Op(enum.Enum):
        And = 0

        Or = 1

    And: BinaryBinsSelectExpr.Op = BinaryBinsSelectExpr.Op.And

    Or: BinaryBinsSelectExpr.Op = BinaryBinsSelectExpr.Op.Or

class SetExprBinsSelectExpr(BinsSelectExpr):
    @property
    def expr(self) -> Expression: ...

    @property
    def matchesExpr(self) -> Expression: ...

class BinSelectWithFilterExpr(BinsSelectExpr):
    @property
    def expr(self) -> BinsSelectExpr: ...

    @property
    def filter(self) -> Expression: ...

    @property
    def matchesExpr(self) -> Expression: ...

class VariableLifetime(enum.Enum):
    Automatic = 0

    Static = 1

class Visibility(enum.Enum):
    Public = 0

    Protected = 1

    Local = 2

class ArgumentDirection(enum.Enum):
    In = 0

    Out = 1

    InOut = 2

    Ref = 3

class ProceduralBlockKind(enum.Enum):
    Initial = 0

    Final = 1

    Always = 2

    AlwaysComb = 3

    AlwaysLatch = 4

    AlwaysFF = 5

class StatementBlockKind(enum.Enum):
    Sequential = 0

    JoinAll = 1

    JoinAny = 2

    JoinNone = 3

class DefinitionKind(enum.Enum):
    Module = 0

    Interface = 1

    Program = 2

class UnconnectedDrive(enum.Enum):
    Pull0 = 1

    Pull1 = 2

class EdgeKind(enum.Enum):
    PosEdge = 1

    NegEdge = 2

    BothEdges = 3

class SubroutineKind(enum.Enum):
    Function = 0

    Task = 1

class AssertionKind(enum.Enum):
    Assert = 0

    Assume = 1

    CoverProperty = 2

    CoverSequence = 3

    Restrict = 4

    Expect = 5

class ElabSystemTaskKind(enum.Enum):
    Fatal = 0

    Error = 1

    Warning = 2

    Info = 3

    StaticAssert = 4

class RandMode(enum.Enum):
    Rand = 1

    RandC = 2

class PrimitivePortDirection(enum.Enum):
    In = 0

    Out = 1

    OutReg = 2

    InOut = 3

class MinTypMax(enum.Enum):
    Min = 0

    Typ = 1

    Max = 2

class CompilationFlags(enum.IntEnum):
    AllowHierarchicalConst = 1

    RelaxEnumConversions = 2

    AllowUseBeforeDeclare = 4

    AllowTopLevelIfacePorts = 8

    LintMode = 16

    IgnoreUnknownModules = 32

    RelaxStringConversions = 64

    AllowRecursiveImplicitCall = 128

    AllowBareValParamAssignment = 256

    AllowSelfDeterminedStreamConcat = 512

    AllowMergingAnsiPorts = 1024

    DisableInstanceCaching = 2048

    DisallowRefsToUnknownInstances = 4096

    AllowUnnamedGenerate = 8192

    AllowVirtualIfaceWithOverride = 16384

    AllowArrayConcatAssignPattern = 32768

    AllowCrossAutoBinMax = 262144

    AllowInvalidTop = 1048576

    CheckUninstantiated = 2097152

class CompilationOptions:
    def __init__(self) -> None: ...

    @property
    def flags(self) -> CompilationFlags: ...

    @flags.setter
    def flags(self, arg: CompilationFlags, /) -> None: ...

    @property
    def maxInstanceDepth(self) -> int: ...

    @maxInstanceDepth.setter
    def maxInstanceDepth(self, arg: int, /) -> None: ...

    @property
    def maxCheckerInstanceDepth(self) -> int: ...

    @maxCheckerInstanceDepth.setter
    def maxCheckerInstanceDepth(self, arg: int, /) -> None: ...

    @property
    def maxGenerateSteps(self) -> int: ...

    @maxGenerateSteps.setter
    def maxGenerateSteps(self, arg: int, /) -> None: ...

    @property
    def maxConstexprDepth(self) -> int: ...

    @maxConstexprDepth.setter
    def maxConstexprDepth(self, arg: int, /) -> None: ...

    @property
    def maxConstexprSteps(self) -> int: ...

    @maxConstexprSteps.setter
    def maxConstexprSteps(self, arg: int, /) -> None: ...

    @property
    def maxConstantSize(self) -> int: ...

    @maxConstantSize.setter
    def maxConstantSize(self, arg: int, /) -> None: ...

    @property
    def maxConstexprBacktrace(self) -> int: ...

    @maxConstexprBacktrace.setter
    def maxConstexprBacktrace(self, arg: int, /) -> None: ...

    @property
    def maxDefParamSteps(self) -> int: ...

    @maxDefParamSteps.setter
    def maxDefParamSteps(self, arg: int, /) -> None: ...

    @property
    def maxDefParamBlocks(self) -> int: ...

    @maxDefParamBlocks.setter
    def maxDefParamBlocks(self, arg: int, /) -> None: ...

    @property
    def maxInstanceArray(self) -> int: ...

    @maxInstanceArray.setter
    def maxInstanceArray(self, arg: int, /) -> None: ...

    @property
    def maxEnumValues(self) -> int: ...

    @maxEnumValues.setter
    def maxEnumValues(self, arg: int, /) -> None: ...

    @property
    def maxRecursiveClassSpecialization(self) -> int: ...

    @maxRecursiveClassSpecialization.setter
    def maxRecursiveClassSpecialization(self, arg: int, /) -> None: ...

    @property
    def maxUDPCoverageNotes(self) -> int: ...

    @maxUDPCoverageNotes.setter
    def maxUDPCoverageNotes(self, arg: int, /) -> None: ...

    @property
    def errorLimit(self) -> int: ...

    @errorLimit.setter
    def errorLimit(self, arg: int, /) -> None: ...

    @property
    def typoCorrectionLimit(self) -> int: ...

    @typoCorrectionLimit.setter
    def typoCorrectionLimit(self, arg: int, /) -> None: ...

    @property
    def minTypMax(self) -> MinTypMax: ...

    @minTypMax.setter
    def minTypMax(self, arg: MinTypMax, /) -> None: ...

    @property
    def languageVersion(self) -> pyslang.LanguageVersion: ...

    @languageVersion.setter
    def languageVersion(self, arg: pyslang.LanguageVersion, /) -> None: ...

    @property
    def defaultTimeScale(self) -> pyslang.TimeScale | None: ...

    @defaultTimeScale.setter
    def defaultTimeScale(self, arg: pyslang.TimeScale | None, /) -> None: ...

    @property
    def topModules(self) -> set[str]: ...

    @topModules.setter
    def topModules(self, arg: Set[str], /) -> None: ...

    @property
    def paramOverrides(self) -> list[str]: ...

    @paramOverrides.setter
    def paramOverrides(self, arg: Sequence[str], /) -> None: ...

    @property
    def defaultLiblist(self) -> list[str]: ...

    @defaultLiblist.setter
    def defaultLiblist(self, arg: Sequence[str], /) -> None: ...

class Compilation:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, options: pyslang.Bag) -> None: ...

    def __repr__(self) -> str: ...

    @property
    def options(self) -> CompilationOptions: ...

    @property
    def isFinalized(self) -> bool: ...

    @property
    def isElaborated(self) -> bool: ...

    @property
    def sourceManager(self) -> pyslang.SourceManager: ...

    @property
    def defaultLibrary(self) -> pyslang.SourceLibrary: ...

    def addSyntaxTree(self, tree: pyslang.syntax.SyntaxTree) -> None: ...

    def getSyntaxTrees(self) -> span[pyslang.syntax.SyntaxTree]: ...

    def getRoot(self) -> RootSymbol: ...

    def addSystemSubroutine(self, subroutine: object) -> None: ...

    def addSystemMethod(self, typeKind: SymbolKind, method: object) -> None: ...

    def getSystemSubroutine(self, name: str) -> SystemSubroutine: ...

    def getSystemMethod(self, typeKind: SymbolKind, name: str) -> SystemSubroutine: ...

    def parseName(self, name: str) -> pyslang.syntax.NameSyntax: ...

    def tryParseName(self, name: str, diags: pyslang.Diagnostics) -> pyslang.syntax.NameSyntax: ...

    def createScriptScope(self) -> CompilationUnitSymbol: ...

    def getParseDiagnostics(self) -> pyslang.Diagnostics: ...

    def getSemanticDiagnostics(self) -> pyslang.Diagnostics: ...

    def getAllDiagnostics(self) -> pyslang.Diagnostics: ...

    def addDiagnostics(self, diagnostics: pyslang.Diagnostics) -> None: ...

    def getCompilationUnit(self, syntax: pyslang.syntax.CompilationUnitSyntax) -> CompilationUnitSymbol: ...

    def getCompilationUnits(self) -> span[CompilationUnitSymbol]: ...

    def getSourceLibrary(self, name: str) -> pyslang.SourceLibrary: ...

    def tryGetDefinition(self, name: str, scope: Scope) -> Compilation.DefinitionLookupResult: ...

    def getDefinitions(self) -> list[Symbol]: ...

    def getPackage(self, name: str) -> PackageSymbol: ...

    def getStdPackage(self) -> PackageSymbol: ...

    def getPackages(self) -> list[PackageSymbol]: ...

    def getGateType(self, name: str) -> PrimitiveSymbol: ...

    def getDPIExports(self) -> list: ...

    @overload
    def getAttributes(self, symbol: Symbol) -> span[AttributeSymbol]: ...

    @overload
    def getAttributes(self, stmt: Statement) -> span[AttributeSymbol]: ...

    @overload
    def getAttributes(self, expr: Expression) -> span[AttributeSymbol]: ...

    @overload
    def getAttributes(self, conn: PortConnection) -> span[AttributeSymbol]: ...

    def getType(self, kind: pyslang.syntax.SyntaxKind) -> Type: ...

    def getNetType(self, kind: pyslang.parsing.TokenKind) -> NetType: ...

    def freeze(self) -> None: ...

    def unfreeze(self) -> None: ...

    @property
    def defaultTimeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def bitType(self) -> Type: ...

    @property
    def logicType(self) -> Type: ...

    @property
    def intType(self) -> Type: ...

    @property
    def byteType(self) -> Type: ...

    @property
    def integerType(self) -> Type: ...

    @property
    def realType(self) -> Type: ...

    @property
    def shortRealType(self) -> Type: ...

    @property
    def stringType(self) -> Type: ...

    @property
    def voidType(self) -> Type: ...

    @property
    def errorType(self) -> Type: ...

    @property
    def unsignedIntType(self) -> Type: ...

    @property
    def nullType(self) -> Type: ...

    @property
    def unboundedType(self) -> Type: ...

    @property
    def typeRefType(self) -> Type: ...

    @property
    def wireNetType(self) -> NetType: ...

    @property
    def hasIssuedErrors(self) -> bool: ...

    @property
    def hasFatalErrors(self) -> bool: ...

    class DefinitionLookupResult:
        def __init__(self) -> None: ...

        @property
        def definition(self) -> Symbol: ...

        @definition.setter
        def definition(self, arg: Symbol, /) -> None: ...

        @property
        def configRoot(self) -> ConfigBlockSymbol: ...

        @configRoot.setter
        def configRoot(self, arg: ConfigBlockSymbol, /) -> None: ...

        @property
        def configRule(self) -> "slang::ast::ConfigRule": ...

        @configRule.setter
        def configRule(self, arg: "slang::ast::ConfigRule", /) -> None: ...

    class DPIExport:
        @property
        def subroutine(self) -> SubroutineSymbol: ...

        @property
        def cIdentifier(self) -> str: ...

        @property
        def syntax(self) -> pyslang.syntax.DPIExportSyntax: ...

class ScriptSession:
    def __init__(self) -> None: ...

    @property
    def compilation(self) -> Compilation: ...

    def eval(self, text: str) -> pyslang.ConstantValue: ...

    def evalExpression(self, expr: pyslang.syntax.ExpressionSyntax) -> pyslang.ConstantValue: ...

    def evalStatement(self, expr: pyslang.syntax.StatementSyntax) -> None: ...

    def getDiagnostics(self) -> pyslang.Diagnostics: ...

class SystemSubroutine:
    def __init__(self, name: str, kind: SubroutineKind) -> None: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def kind(self) -> SubroutineKind: ...

    @kind.setter
    def kind(self, arg: SubroutineKind, /) -> None: ...

    @property
    def knownNameId(self) -> pyslang.parsing.KnownSystemName: ...

    @knownNameId.setter
    def knownNameId(self, arg: pyslang.parsing.KnownSystemName, /) -> None: ...

    @property
    def hasOutputArgs(self) -> bool: ...

    @hasOutputArgs.setter
    def hasOutputArgs(self, arg: bool, /) -> None: ...

    @property
    def withClauseMode(self) -> SystemSubroutine.WithClauseMode: ...

    @withClauseMode.setter
    def withClauseMode(self, arg: SystemSubroutine.WithClauseMode, /) -> None: ...

    def allowEmptyArgument(self, argIndex: int) -> bool: ...

    def allowClockingArgument(self, argIndex: int) -> bool: ...

    def bindArgument(self, argIndex: int, context: ASTContext, syntax: pyslang.syntax.ExpressionSyntax, previousArgs: span[Expression]) -> Expression: ...

    def checkArguments(self, context: ASTContext, args: span[Expression], range: pyslang.SourceRange, iterOrThis: Expression) -> Type: ...

    def eval(self, context: EvalContext, args: span[Expression], range: pyslang.SourceRange, callInfo: CallExpression.SystemCallInfo) -> pyslang.ConstantValue: ...

    def badArg(self, context: ASTContext, arg: Expression) -> Type: ...

    def checkArgCount(self, context: ASTContext, isMethod: bool, args: span[Expression], callRange: pyslang.SourceRange, min: int, max: int) -> bool: ...

    def kindStr(self) -> str: ...

    def noHierarchical(self, context: EvalContext, expr: Expression) -> bool: ...

    def notConst(self, context: EvalContext, range: pyslang.SourceRange) -> bool: ...

    @staticmethod
    def unevaluatedContext(sourceContext: ASTContext) -> ASTContext: ...

    def __repr__(self) -> str: ...

    class WithClauseMode(enum.Enum):
        Iterator = 1

        Randomize = 2

class SimpleSystemSubroutine(SystemSubroutine):
    def __init__(self, name: str, kind: SubroutineKind, requiredArgs: int, argTypes: Sequence[Type], returnType: Type, isMethod: bool, isFirstArgLValue: bool = False) -> None: ...

class NonConstantFunction(SimpleSystemSubroutine):
    def __init__(self, name: str, returnType: Type, requiredArgs: int = 0, argTypes: Sequence[Type] = [], isMethod: bool = False) -> None: ...

class ExpressionKind(enum.Enum):
    Invalid = 0

    IntegerLiteral = 1

    RealLiteral = 2

    TimeLiteral = 3

    UnbasedUnsizedIntegerLiteral = 4

    NullLiteral = 5

    UnboundedLiteral = 6

    StringLiteral = 7

    NamedValue = 8

    HierarchicalValue = 9

    UnaryOp = 10

    BinaryOp = 11

    ConditionalOp = 12

    Inside = 13

    Assignment = 14

    Concatenation = 15

    Replication = 16

    Streaming = 17

    ElementSelect = 18

    RangeSelect = 19

    MemberAccess = 20

    Call = 21

    Conversion = 22

    DataType = 23

    TypeReference = 24

    ArbitrarySymbol = 25

    LValueReference = 26

    SimpleAssignmentPattern = 27

    StructuredAssignmentPattern = 28

    ReplicatedAssignmentPattern = 29

    EmptyArgument = 30

    ValueRange = 31

    Dist = 32

    NewArray = 33

    NewClass = 34

    NewCovergroup = 35

    CopyClass = 36

    MinTypMax = 37

    ClockingEvent = 38

    AssertionInstance = 39

    TaggedUnion = 40

class UnaryOperator(enum.Enum):
    Plus = 0

    Minus = 1

    BitwiseNot = 2

    BitwiseAnd = 3

    BitwiseOr = 4

    BitwiseXor = 5

    BitwiseNand = 6

    BitwiseNor = 7

    BitwiseXnor = 8

    LogicalNot = 9

    Preincrement = 10

    Predecrement = 11

    Postincrement = 12

    Postdecrement = 13

class BinaryOperator(enum.Enum):
    Add = 0

    Subtract = 1

    Multiply = 2

    Divide = 3

    Mod = 4

    BinaryAnd = 5

    BinaryOr = 6

    BinaryXor = 7

    BinaryXnor = 8

    Equality = 9

    Inequality = 10

    CaseEquality = 11

    CaseInequality = 12

    GreaterThanEqual = 13

    GreaterThan = 14

    LessThanEqual = 15

    LessThan = 16

    WildcardEquality = 17

    WildcardInequality = 18

    LogicalAnd = 19

    LogicalOr = 20

    LogicalImplication = 21

    LogicalEquivalence = 22

    LogicalShiftLeft = 23

    LogicalShiftRight = 24

    ArithmeticShiftLeft = 25

    ArithmeticShiftRight = 26

    Power = 27

class RangeSelectionKind(enum.Enum):
    Simple = 0

    IndexedUp = 1

    IndexedDown = 2

class ConversionKind(enum.Enum):
    Implicit = 0

    Propagated = 1

    StreamingConcat = 2

    Explicit = 3

    BitstreamCast = 4

class Expression:
    @property
    def kind(self) -> ExpressionKind: ...

    @property
    def type(self) -> Type: ...

    @property
    def syntax(self) -> pyslang.syntax.ExpressionSyntax: ...

    @property
    def sourceRange(self) -> pyslang.SourceRange: ...

    @property
    def constant(self) -> pyslang.ConstantValue: ...

    @property
    def bad(self) -> bool: ...

    @property
    def isImplicitString(self) -> bool: ...

    @property
    def isUnsizedInteger(self) -> bool: ...

    @property
    def effectiveWidth(self) -> int | None: ...

    @property
    def hasHierarchicalReference(self) -> bool: ...

    def eval(self, context: EvalContext) -> pyslang.ConstantValue: ...

    def evalLValue(self, context: EvalContext) -> LValue: ...

    def isImplicitlyAssignableTo(self, compilation: Compilation, type: Type) -> bool: ...

    def getSymbolReference(self, allowPacked: bool = True) -> Symbol: ...

    def isEquivalentTo(self, other: Expression) -> bool: ...

    def visit(self, f: object | None = None, lookup_table: object | None = None) -> None:
        """
        Visit a pyslang object with a callback function `f` or a `lookup_table` dict.

        At least one of `f` or `lookup_table` must be provided (both default to `None`). If both are provided, 'lookup_table' will be used to decide which callback to use.

        When `f` is provided without `lookup_table`, it is called for every node visited. The callback should take a single argument (the current node). Its return value controls traversal: `pyslang.VisitAction.Interrupt` aborts the visit, `pyslang.VisitAction.Skip` skips child nodes, and any other return value (including `pyslang.VisitAction.Advance` or `None`) continues normally.

        When `lookup_table` is provided, it should be a dict mapping node kind enum values to handler functions. The C++ side checks each node's kind before crossing the Python boundary, calling only the matching handler. Nodes not in the table are traversed without invoking Python. `f` is not called in this mode.

        The `lookup_table` is compiled into native lookups when the visit begins and must not be mutated during traversal.
        """

    def __repr__(self) -> str: ...

class InvalidExpression(Expression):
    pass

class AssignmentExpression(Expression):
    @property
    def op(self) -> BinaryOperator | None: ...

    @property
    def timingControl(self) -> TimingControl: ...

    @property
    def isCompound(self) -> bool: ...

    @property
    def isNonBlocking(self) -> bool: ...

    @property
    def isLValueArg(self) -> bool: ...

    @property
    def left(self) -> Expression: ...

    @property
    def right(self) -> Expression: ...

class ConversionExpression(Expression):
    @property
    def conversionKind(self) -> ConversionKind: ...

    @property
    def isConstCast(self) -> bool: ...

    @property
    def isImplicit(self) -> bool: ...

    @property
    def operand(self) -> Expression: ...

class NewArrayExpression(Expression):
    @property
    def sizeExpr(self) -> Expression: ...

    @property
    def initExpr(self) -> Expression: ...

class NewClassExpression(Expression):
    @property
    def isSuperClass(self) -> bool: ...

    @property
    def constructorCall(self) -> Expression: ...

class NewCovergroupExpression(Expression):
    @property
    def arguments(self) -> span[Expression]: ...

class AssignmentPatternExpressionBase(Expression):
    @property
    def elements(self) -> span[Expression]: ...

class SimpleAssignmentPatternExpression(AssignmentPatternExpressionBase):
    pass

class StructuredAssignmentPatternExpression(AssignmentPatternExpressionBase):
    @property
    def memberSetters(self) -> span[StructuredAssignmentPatternExpression.MemberSetter]: ...

    @property
    def typeSetters(self) -> span[StructuredAssignmentPatternExpression.TypeSetter]: ...

    @property
    def indexSetters(self) -> span[StructuredAssignmentPatternExpression.IndexSetter]: ...

    @property
    def defaultSetter(self) -> Expression: ...

    class MemberSetter:
        @property
        def member(self) -> Symbol: ...

        @property
        def expr(self) -> Expression: ...

    class TypeSetter:
        @property
        def type(self) -> Type: ...

        @property
        def expr(self) -> Expression: ...

    class IndexSetter:
        @property
        def index(self) -> Expression: ...

        @property
        def expr(self) -> Expression: ...

class ReplicatedAssignmentPatternExpression(AssignmentPatternExpressionBase):
    @property
    def count(self) -> Expression: ...

class CallExpression(Expression):
    @property
    def subroutine(self) -> SubroutineSymbol | CallExpression.SystemCallInfo: ...

    @property
    def thisClass(self) -> Expression: ...

    @property
    def arguments(self) -> span[Expression]: ...

    @property
    def isSystemCall(self) -> bool: ...

    @property
    def subroutineName(self) -> str: ...

    @property
    def subroutineKind(self) -> SubroutineKind: ...

    class IteratorCallInfo:
        @property
        def iterExpr(self) -> Expression: ...

        @property
        def iterVar(self) -> ValueSymbol: ...

    class RandomizeCallInfo:
        @property
        def inlineConstraints(self) -> Constraint: ...

        @property
        def constraintRestrictions(self) -> span[str]: ...

    class SystemCallInfo:
        @property
        def subroutine(self) -> SystemSubroutine: ...

        @property
        def scope(self) -> Scope: ...

        @property
        def extraInfo(self) -> None | CallExpression.IteratorCallInfo | CallExpression.RandomizeCallInfo: ...

class IntegerLiteral(Expression):
    @property
    def isDeclaredUnsized(self) -> bool: ...

    @property
    def value(self) -> pyslang.SVInt: ...

class RealLiteral(Expression):
    @property
    def value(self) -> float: ...

class TimeLiteral(Expression):
    @property
    def value(self) -> float: ...

    @property
    def scale(self) -> pyslang.TimeScale: ...

class UnbasedUnsizedIntegerLiteral(Expression):
    @property
    def literalValue(self) -> pyslang.logic_t: ...

    @property
    def value(self) -> pyslang.SVInt: ...

class NullLiteral(Expression):
    pass

class UnboundedLiteral(Expression):
    pass

class StringLiteral(Expression):
    @property
    def rawValue(self) -> str: ...

    @property
    def intValue(self) -> pyslang.ConstantValue: ...

    @property
    def value(self) -> str: ...

class ValueExpressionBase(Expression):
    @property
    def symbol(self) -> ValueSymbol: ...

class NamedValueExpression(ValueExpressionBase):
    pass

class HierarchicalValueExpression(ValueExpressionBase):
    pass

class DataTypeExpression(Expression):
    pass

class LValueReferenceExpression(Expression):
    pass

class EmptyArgumentExpression(Expression):
    pass

class TypeReferenceExpression(Expression):
    @property
    def targetType(self) -> Type: ...

class ArbitrarySymbolExpression(Expression):
    @property
    def symbol(self) -> Symbol: ...

class ClockingEventExpression(Expression):
    @property
    def timingControl(self) -> TimingControl: ...

class AssertionInstanceExpression(Expression):
    @property
    def symbol(self) -> Symbol: ...

    @property
    def body(self) -> AssertionExpr: ...

    @property
    def arguments(self) -> span["std::tuple<slang::ast::AssertionPortSymbol const * __ptr64,std::variant<slang::ast::Expression const * __ptr64,slang::ast::AssertionExpr const * __ptr64,slang::ast::TimingControl const * __ptr64> >"]: ...

    @property
    def localVars(self) -> span[LocalAssertionVarSymbol]: ...

    @property
    def isRecursiveProperty(self) -> bool: ...

class MinTypMaxExpression(Expression):
    @property
    def min(self) -> Expression: ...

    @property
    def typ(self) -> Expression: ...

    @property
    def max(self) -> Expression: ...

    @property
    def selected(self) -> Expression: ...

class CopyClassExpression(Expression):
    @property
    def sourceExpr(self) -> Expression: ...

class DistExpression(Expression):
    @property
    def left(self) -> Expression: ...

    @property
    def items(self) -> span[DistExpression.DistItem]: ...

    @property
    def defaultWeight(self) -> DistExpression.DistWeight: ...

    class DistWeight:
        @property
        def kind(self) -> DistExpression.DistWeight.Kind: ...

        @property
        def expr(self) -> Expression: ...

        class Kind(enum.Enum):
            PerValue = 0

            PerRange = 1

        PerValue: DistExpression.DistWeight.Kind = DistExpression.DistWeight.Kind.PerValue

        PerRange: DistExpression.DistWeight.Kind = DistExpression.DistWeight.Kind.PerRange

    class DistItem:
        @property
        def weight(self) -> DistExpression.DistWeight | None: ...

        @property
        def value(self) -> Expression: ...

class TaggedUnionExpression(Expression):
    @property
    def member(self) -> Symbol: ...

    @property
    def valueExpr(self) -> Expression: ...

class UnaryExpression(Expression):
    @property
    def operand(self) -> Expression: ...

    @property
    def op(self) -> UnaryOperator: ...

class BinaryExpression(Expression):
    @property
    def left(self) -> Expression: ...

    @property
    def right(self) -> Expression: ...

    @property
    def op(self) -> BinaryOperator: ...

class ConditionalExpression(Expression):
    @property
    def left(self) -> Expression: ...

    @property
    def right(self) -> Expression: ...

    @property
    def conditions(self) -> span[ConditionalExpression.Condition]: ...

    class Condition:
        @property
        def expr(self) -> Expression: ...

        @property
        def pattern(self) -> Pattern: ...

class InsideExpression(Expression):
    @property
    def left(self) -> Expression: ...

    @property
    def rangeList(self) -> span[Expression]: ...

class ConcatenationExpression(Expression):
    @property
    def operands(self) -> span[Expression]: ...

class ReplicationExpression(Expression):
    @property
    def count(self) -> Expression: ...

    @property
    def concat(self) -> Expression: ...

class StreamingConcatenationExpression(Expression):
    @property
    def sliceSize(self) -> int: ...

    @property
    def isFixedSize(self) -> bool: ...

    @property
    def bitstreamWidth(self) -> int: ...

    @property
    def streams(self) -> span[StreamingConcatenationExpression.StreamExpression]: ...

    class StreamExpression:
        @property
        def operand(self) -> Expression: ...

        @property
        def withExpr(self) -> Expression: ...

        @property
        def constantWithWidth(self) -> int | None: ...

class ValueRangeExpression(Expression):
    @property
    def left(self) -> Expression: ...

    @property
    def right(self) -> Expression: ...

class ElementSelectExpression(Expression):
    @property
    def value(self) -> Expression: ...

    @property
    def selector(self) -> Expression: ...

class RangeSelectExpression(Expression):
    @property
    def selectionKind(self) -> RangeSelectionKind: ...

    @property
    def value(self) -> Expression: ...

    @property
    def left(self) -> Expression: ...

    @property
    def right(self) -> Expression: ...

class MemberAccessExpression(Expression):
    @property
    def value(self) -> Expression: ...

    @property
    def member(self) -> Symbol: ...

class StatementKind(enum.Enum):
    Invalid = 0

    Empty = 1

    List = 2

    Block = 3

    ExpressionStatement = 4

    VariableDeclaration = 5

    Return = 6

    Continue = 7

    Break = 8

    Disable = 9

    Conditional = 10

    Case = 11

    PatternCase = 12

    ForLoop = 13

    RepeatLoop = 14

    ForeachLoop = 15

    WhileLoop = 16

    DoWhileLoop = 17

    ForeverLoop = 18

    Timed = 19

    ImmediateAssertion = 20

    ConcurrentAssertion = 21

    DisableFork = 22

    Wait = 23

    WaitFork = 24

    WaitOrder = 25

    EventTrigger = 26

    ProceduralAssign = 27

    ProceduralDeassign = 28

    RandCase = 29

    RandSequence = 30

    ProceduralChecker = 31

class CaseStatementCondition(enum.Enum):
    Normal = 0

    WildcardXOrZ = 1

    WildcardJustZ = 2

    Inside = 3

class UniquePriorityCheck(enum.Enum):
    Unique = 1

    Unique0 = 2

    Priority = 3

class Statement:
    @property
    def kind(self) -> StatementKind: ...

    @property
    def syntax(self) -> pyslang.syntax.StatementSyntax: ...

    @property
    def sourceRange(self) -> pyslang.SourceRange: ...

    @property
    def bad(self) -> bool: ...

    def eval(self, context: EvalContext) -> EvalResult: ...

    def visit(self, f: object | None = None, lookup_table: object | None = None) -> None:
        """
        Visit a pyslang object with a callback function `f` or a `lookup_table` dict.

        At least one of `f` or `lookup_table` must be provided (both default to `None`). If both are provided, 'lookup_table' will be used to decide which callback to use.

        When `f` is provided without `lookup_table`, it is called for every node visited. The callback should take a single argument (the current node). Its return value controls traversal: `pyslang.VisitAction.Interrupt` aborts the visit, `pyslang.VisitAction.Skip` skips child nodes, and any other return value (including `pyslang.VisitAction.Advance` or `None`) continues normally.

        When `lookup_table` is provided, it should be a dict mapping node kind enum values to handler functions. The C++ side checks each node's kind before crossing the Python boundary, calling only the matching handler. Nodes not in the table are traversed without invoking Python. `f` is not called in this mode.

        The `lookup_table` is compiled into native lookups when the visit begins and must not be mutated during traversal.
        """

    def __repr__(self) -> str: ...

class EvalResult(enum.Enum):
    Fail = 0

    Success = 1

    Return = 2

    Break = 3

    Continue = 4

    Disable = 5

class InvalidStatement(Statement):
    pass

class EmptyStatement(Statement):
    pass

class BreakStatement(Statement):
    pass

class ContinueStatement(Statement):
    pass

class DisableForkStatement(Statement):
    pass

class WaitForkStatement(Statement):
    pass

class StatementList(Statement):
    @property
    def list(self) -> span[Statement]: ...

class BlockStatement(Statement):
    @property
    def blockSymbol(self) -> StatementBlockSymbol: ...

    @property
    def blockKind(self) -> StatementBlockKind: ...

    @property
    def body(self) -> Statement: ...

class ReturnStatement(Statement):
    @property
    def expr(self) -> Expression: ...

class DisableStatement(Statement):
    @property
    def target(self) -> Expression: ...

class VariableDeclStatement(Statement):
    @property
    def symbol(self) -> VariableSymbol: ...

class ConditionalStatement(Statement):
    @property
    def conditions(self) -> span[ConditionalStatement.Condition]: ...

    @property
    def check(self) -> UniquePriorityCheck: ...

    @property
    def ifFalse(self) -> Statement: ...

    @property
    def ifTrue(self) -> Statement: ...

    class Condition:
        @property
        def expr(self) -> Expression: ...

        @property
        def pattern(self) -> Pattern: ...

class CaseStatement(Statement):
    @property
    def items(self) -> span[CaseStatement.ItemGroup]: ...

    @property
    def defaultCase(self) -> Statement: ...

    @property
    def condition(self) -> CaseStatementCondition: ...

    @property
    def check(self) -> UniquePriorityCheck: ...

    @property
    def expr(self) -> Expression: ...

    class ItemGroup:
        @property
        def expressions(self) -> span[Expression]: ...

        @property
        def stmt(self) -> Statement: ...

class PatternCaseStatement(Statement):
    @property
    def items(self) -> span[PatternCaseStatement.ItemGroup]: ...

    @property
    def defaultCase(self) -> Statement: ...

    @property
    def condition(self) -> CaseStatementCondition: ...

    @property
    def check(self) -> UniquePriorityCheck: ...

    @property
    def expr(self) -> Expression: ...

    class ItemGroup:
        @property
        def pattern(self) -> Pattern: ...

        @property
        def filter(self) -> Expression: ...

        @property
        def stmt(self) -> Statement: ...

class ForLoopStatement(Statement):
    @property
    def initializers(self) -> span[Expression]: ...

    @property
    def loopVars(self) -> span[VariableSymbol]: ...

    @property
    def stopExpr(self) -> Expression: ...

    @property
    def steps(self) -> span[Expression]: ...

    @property
    def body(self) -> Statement: ...

class ForeachLoopStatement(Statement):
    @property
    def loopDims(self) -> span[ForeachLoopStatement.LoopDim]: ...

    @property
    def arrayRef(self) -> Expression: ...

    @property
    def body(self) -> Statement: ...

    class LoopDim:
        @property
        def range(self) -> pyslang.ConstantRange | None: ...

        @property
        def loopVar(self) -> IteratorSymbol: ...

class RepeatLoopStatement(Statement):
    @property
    def count(self) -> Expression: ...

    @property
    def body(self) -> Statement: ...

class WhileLoopStatement(Statement):
    @property
    def cond(self) -> Expression: ...

    @property
    def body(self) -> Statement: ...

class DoWhileLoopStatement(Statement):
    @property
    def cond(self) -> Expression: ...

    @property
    def body(self) -> Statement: ...

class ForeverLoopStatement(Statement):
    @property
    def body(self) -> Statement: ...

class ExpressionStatement(Statement):
    @property
    def expr(self) -> Expression: ...

class TimedStatement(Statement):
    @property
    def timing(self) -> TimingControl: ...

    @property
    def stmt(self) -> Statement: ...

class ImmediateAssertionStatement(Statement):
    @property
    def cond(self) -> Expression: ...

    @property
    def ifTrue(self) -> Statement: ...

    @property
    def ifFalse(self) -> Statement: ...

    @property
    def assertionKind(self) -> AssertionKind: ...

    @property
    def isDeferred(self) -> bool: ...

    @property
    def isFinal(self) -> bool: ...

class ConcurrentAssertionStatement(Statement):
    @property
    def propertySpec(self) -> AssertionExpr: ...

    @property
    def ifTrue(self) -> Statement: ...

    @property
    def ifFalse(self) -> Statement: ...

    @property
    def assertionKind(self) -> AssertionKind: ...

class WaitStatement(Statement):
    @property
    def cond(self) -> Expression: ...

    @property
    def stmt(self) -> Statement: ...

class WaitOrderStatement(Statement):
    @property
    def ifTrue(self) -> Statement: ...

    @property
    def ifFalse(self) -> Statement: ...

    @property
    def events(self) -> span[Expression]: ...

class EventTriggerStatement(Statement):
    @property
    def target(self) -> Expression: ...

    @property
    def timing(self) -> TimingControl: ...

    @property
    def isNonBlocking(self) -> bool: ...

class ProceduralAssignStatement(Statement):
    @property
    def assignment(self) -> Expression: ...

    @property
    def isForce(self) -> bool: ...

class ProceduralDeassignStatement(Statement):
    @property
    def lvalue(self) -> Expression: ...

    @property
    def isRelease(self) -> bool: ...

class RandCaseStatement(Statement):
    @property
    def items(self) -> span[RandCaseStatement.Item]: ...

    class Item:
        @property
        def expr(self) -> Expression: ...

        @property
        def stmt(self) -> Statement: ...

class RandSequenceStatement(Statement):
    @property
    def firstProduction(self) -> RandSeqProductionSymbol: ...

class ProceduralCheckerStatement(Statement):
    @property
    def instances(self) -> span[Symbol]: ...

class SymbolKind(enum.Enum):
    Unknown = 0

    Root = 1

    Definition = 2

    CompilationUnit = 3

    DeferredMember = 4

    TransparentMember = 5

    EmptyMember = 6

    PredefinedIntegerType = 7

    ScalarType = 8

    FloatingType = 9

    EnumType = 10

    EnumValue = 11

    PackedArrayType = 12

    FixedSizeUnpackedArrayType = 13

    DynamicArrayType = 14

    DPIOpenArrayType = 15

    AssociativeArrayType = 16

    QueueType = 17

    PackedStructType = 18

    UnpackedStructType = 19

    PackedUnionType = 20

    UnpackedUnionType = 21

    ClassType = 22

    CovergroupType = 23

    VoidType = 24

    NullType = 25

    CHandleType = 26

    StringType = 27

    EventType = 28

    UnboundedType = 29

    TypeRefType = 30

    UntypedType = 31

    SequenceType = 32

    PropertyType = 33

    VirtualInterfaceType = 34

    TypeAlias = 35

    ErrorType = 36

    ForwardingTypedef = 37

    NetType = 38

    Parameter = 39

    TypeParameter = 40

    Port = 41

    MultiPort = 42

    InterfacePort = 43

    Modport = 44

    ModportPort = 45

    ModportClocking = 46

    Instance = 47

    InstanceBody = 48

    InstanceArray = 49

    Package = 50

    ExplicitImport = 51

    WildcardImport = 52

    Attribute = 53

    Genvar = 54

    GenerateBlock = 55

    GenerateBlockArray = 56

    ProceduralBlock = 57

    StatementBlock = 58

    Net = 59

    Variable = 60

    FormalArgument = 61

    Field = 62

    ClassProperty = 63

    Subroutine = 64

    ContinuousAssign = 65

    ElabSystemTask = 66

    GenericClassDef = 67

    MethodPrototype = 68

    UninstantiatedDef = 69

    Iterator = 70

    PatternVar = 71

    ConstraintBlock = 72

    DefParam = 73

    Specparam = 74

    Primitive = 75

    PrimitivePort = 76

    PrimitiveInstance = 77

    SpecifyBlock = 78

    Sequence = 79

    Property = 80

    AssertionPort = 81

    ClockingBlock = 82

    ClockVar = 83

    LocalAssertionVar = 84

    LetDecl = 85

    Checker = 86

    CheckerInstance = 87

    CheckerInstanceBody = 88

    RandSeqProduction = 89

    CovergroupBody = 90

    Coverpoint = 91

    CoverCross = 92

    CoverCrossBody = 93

    CoverageBin = 94

    TimingPath = 95

    PulseStyle = 96

    SystemTimingCheck = 97

    AnonymousProgram = 98

    NetAlias = 99

    ConfigBlock = 100

class PulseStyleKind(enum.Enum):
    OnEvent = 0

    OnDetect = 1

    ShowCancelled = 2

    NoShowCancelled = 3

class SystemTimingCheckKind(enum.Enum):
    Unknown = 0

    Setup = 1

    Hold = 2

    SetupHold = 3

    Recovery = 4

    Removal = 5

    RecRem = 6

    Skew = 7

    TimeSkew = 8

    FullSkew = 9

    Period = 10

    Width = 11

    NoChange = 12

class LookupFlags(enum.IntEnum):
    Type = 1

    AllowDeclaredAfter = 2

    DisallowWildcardImport = 4

    NoUndeclaredError = 8

    NoUndeclaredErrorIfUninstantiated = 16

    AllowIncompleteForwardTypedefs = 32

    NoSelectors = 64

    AllowRoot = 128

    AllowUnit = 256

    IfacePortConn = 512

    StaticInitializer = 1024

    ForceHierarchical = 18

    TypeReference = 2048

    AlwaysAllowUpward = 4096

    DisallowUnitReferences = 8192

    AllowUnnamedGenerate = 16384

class LookupResultFlags(enum.IntEnum):
    WasImported = 1

    IsHierarchical = 2

    SuppressUndeclared = 4

    FromTypeParam = 8

    FromForwardTypedef = 16

class LookupLocation:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, scope: Scope, index: int) -> None: ...

    @property
    def scope(self) -> Scope: ...

    @property
    def index(self) -> "slang::ast::SymbolIndex": ...

    @staticmethod
    def before(symbol: Symbol) -> LookupLocation: ...

    @staticmethod
    def after(symbol: Symbol) -> LookupLocation: ...

    max: Final[LookupLocation] = ...
    """(arg: object, /) -> pyslang.ast.LookupLocation"""

    min: Final[LookupLocation] = ...
    """(arg: object, /) -> pyslang.ast.LookupLocation"""

    def __eq__(self, arg: LookupLocation, /) -> bool: ...

    def __ne__(self, arg: LookupLocation, /) -> bool: ...

class LookupResult:
    def __init__(self) -> None: ...

    @property
    def found(self) -> Symbol: ...

    @property
    def systemSubroutine(self) -> SystemSubroutine: ...

    @property
    def upwardCount(self) -> int: ...

    @property
    def flags(self) -> LookupResultFlags: ...

    @property
    def selectors(self) -> "slang::SmallVector<std::variant<slang::syntax::ElementSelectSyntax const * __ptr64,slang::ast::LookupResult::MemberSelector>,4>": ...

    @property
    def diagnostics(self) -> pyslang.Diagnostics: ...

    @property
    def hasError(self) -> bool: ...

    def clear(self) -> None: ...

    def reportDiags(self, context: ASTContext) -> None: ...

    def errorIfSelectors(self, context: ASTContext) -> None: ...

    class MemberSelector:
        @property
        def name(self) -> str: ...

        @property
        def dotLocation(self) -> pyslang.SourceLocation: ...

        @property
        def nameRange(self) -> pyslang.SourceRange: ...

class Lookup:
    @staticmethod
    def name(syntax: pyslang.syntax.NameSyntax, context: ASTContext, flags: LookupFlags, result: LookupResult) -> None: ...

    @staticmethod
    def unqualified(scope: Symbol, name: str, flags: LookupFlags = LookupFlags.None_) -> object: ...

    @staticmethod
    def unqualifiedAt(scope: Symbol, name: str, location: LookupLocation, sourceRange: pyslang.SourceRange, flags: LookupFlags = LookupFlags.None_) -> object: ...

    @staticmethod
    def findClass(name: pyslang.syntax.NameSyntax, context: ASTContext, requireInterfaceClass: pyslang.DiagCode | None = None) -> ClassType: ...

    @staticmethod
    def getContainingClass(scope: Symbol) -> object: ...

    @staticmethod
    def getVisibility(symbol: Symbol) -> Visibility: ...

    @staticmethod
    def isVisibleFrom(symbol: Symbol, scope: Scope) -> bool: ...

    @staticmethod
    def isAccessibleFrom(target: Symbol, sourceScope: Symbol) -> bool: ...

    @staticmethod
    def ensureVisible(symbol: Symbol, context: ASTContext, sourceRange: pyslang.SourceRange | None) -> bool: ...

    @staticmethod
    def ensureAccessible(symbol: Symbol, context: ASTContext, sourceRange: pyslang.SourceRange | None) -> bool: ...

    @staticmethod
    def findTempVar(scope: Scope, symbol: TempVarSymbol, name: pyslang.syntax.NameSyntax, result: LookupResult) -> bool: ...

    @staticmethod
    def withinClassRandomize(context: ASTContext, syntax: pyslang.syntax.NameSyntax, flags: LookupFlags, result: LookupResult) -> bool: ...

    @staticmethod
    def findAssertionLocalVar(context: ASTContext, name: pyslang.syntax.NameSyntax, result: LookupResult) -> bool: ...

class Symbol:
    @property
    def kind(self) -> SymbolKind: ...

    @property
    def name(self) -> str: ...

    @property
    def location(self) -> pyslang.SourceLocation: ...

    @property
    def parentScope(self) -> Scope: ...

    @property
    def syntax(self) -> pyslang.syntax.SyntaxNode: ...

    @property
    def isScope(self) -> bool: ...

    @property
    def isType(self) -> bool: ...

    @property
    def isValue(self) -> bool: ...

    @property
    def declaredType(self) -> DeclaredType: ...

    @property
    def declaringDefinition(self) -> DefinitionSymbol: ...

    @property
    def randMode(self) -> RandMode: ...

    @property
    def nextSibling(self) -> Symbol: ...

    @property
    def sourceLibrary(self) -> pyslang.SourceLibrary: ...

    @property
    def hierarchicalPath(self) -> str: ...

    @property
    def lexicalPath(self) -> str: ...

    @overload
    def isDeclaredBefore(self, target: Symbol) -> bool | None: ...

    @overload
    def isDeclaredBefore(self, location: LookupLocation) -> bool | None: ...

    def visit(self, f: object | None = None, lookup_table: object | None = None) -> None:
        """
        Visit a pyslang object with a callback function `f` or a `lookup_table` dict.

        At least one of `f` or `lookup_table` must be provided (both default to `None`). If both are provided, 'lookup_table' will be used to decide which callback to use.

        When `f` is provided without `lookup_table`, it is called for every node visited. The callback should take a single argument (the current node). Its return value controls traversal: `pyslang.VisitAction.Interrupt` aborts the visit, `pyslang.VisitAction.Skip` skips child nodes, and any other return value (including `pyslang.VisitAction.Advance` or `None`) continues normally.

        When `lookup_table` is provided, it should be a dict mapping node kind enum values to handler functions. The C++ side checks each node's kind before crossing the Python boundary, calling only the matching handler. Nodes not in the table are traversed without invoking Python. `f` is not called in this mode.

        The `lookup_table` is compiled into native lookups when the visit begins and must not be mutated during traversal.
        """

    def __eq__(self, arg: Symbol, /) -> bool: ...

    def __hash__(self) -> int: ...

    def __repr__(self) -> str: ...

class Scope:
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def __eq__(self, arg: Scope, /) -> bool: ...

    def __hash__(self) -> int: ...

    def __repr__(self) -> str: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

class AttributeSymbol(Symbol):
    @property
    def value(self) -> pyslang.ConstantValue: ...

class CompilationUnitSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

class PackageSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def defaultLifetime(self) -> VariableLifetime: ...

    @property
    def hasExportAll(self) -> bool: ...

    def findForImport(self, name: str) -> Symbol: ...

class RootSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def topInstances(self) -> span[InstanceSymbol]: ...

    @property
    def compilationUnits(self) -> span[CompilationUnitSymbol]: ...

class DefinitionSymbol(Symbol):
    @property
    def definitionKind(self) -> DefinitionKind: ...

    @property
    def defaultLifetime(self) -> VariableLifetime: ...

    @property
    def unconnectedDrive(self) -> UnconnectedDrive: ...

    @property
    def cellDefine(self) -> bool: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def instanceCount(self) -> int: ...

    def getKindString(self) -> str: ...

    def getArticleKindString(self) -> str: ...

    def __repr__(self) -> str: ...

class ValueSymbol(Symbol):
    @property
    def type(self) -> Type: ...

    @property
    def initializer(self) -> Expression: ...

class EnumValueSymbol(ValueSymbol):
    @property
    def value(self) -> pyslang.ConstantValue: ...

class ParameterSymbolBase:
    @property
    def isLocalParam(self) -> bool: ...

    @property
    def isPortParam(self) -> bool: ...

    @property
    def isBodyParam(self) -> bool: ...

class ParameterSymbol(ValueSymbol):
    @property
    def isLocalParam(self) -> bool: ...

    @property
    def isPortParam(self) -> bool: ...

    @property
    def isBodyParam(self) -> bool: ...

    @property
    def value(self) -> pyslang.ConstantValue: ...

    @property
    def isOverridden(self) -> bool: ...

class TypeParameterSymbol(Symbol):
    @property
    def isLocalParam(self) -> bool: ...

    @property
    def isPortParam(self) -> bool: ...

    @property
    def isBodyParam(self) -> bool: ...

    @property
    def targetType(self) -> DeclaredType: ...

    @property
    def typeAlias(self) -> Type: ...

    @property
    def isOverridden(self) -> bool: ...

class DefParamSymbol(Symbol):
    @property
    def target(self) -> Symbol: ...

    @property
    def initializer(self) -> Expression: ...

    @property
    def value(self) -> pyslang.ConstantValue: ...

class SpecparamSymbol(ValueSymbol):
    @property
    def isPathPulse(self) -> bool: ...

    @property
    def value(self) -> pyslang.ConstantValue: ...

    @property
    def pulseRejectLimit(self) -> pyslang.ConstantValue: ...

    @property
    def pulseErrorLimit(self) -> pyslang.ConstantValue: ...

    @property
    def pathSource(self) -> Symbol: ...

    @property
    def pathDest(self) -> Symbol: ...

class VariableFlags(enum.IntEnum):
    Const = 1

    CompilerGenerated = 2

    ImmutableCoverageOption = 4

    CoverageSampleFormal = 8

    CheckerFreeVariable = 16

    RefStatic = 32

class VariableSymbol(ValueSymbol):
    @property
    def lifetime(self) -> VariableLifetime: ...

    @property
    def flags(self) -> VariableFlags: ...

class FormalArgumentSymbol(VariableSymbol):
    @property
    def direction(self) -> ArgumentDirection: ...

    @property
    def defaultValue(self) -> Expression: ...

class FieldSymbol(VariableSymbol):
    @property
    def bitOffset(self) -> int: ...

    @property
    def fieldIndex(self) -> int: ...

    @property
    def randMode(self) -> RandMode: ...

class NetSymbol(ValueSymbol):
    @property
    def expansionHint(self) -> NetSymbol.ExpansionHint: ...

    @property
    def isImplicit(self) -> bool: ...

    @property
    def netType(self) -> NetType: ...

    @property
    def delay(self) -> TimingControl: ...

    @property
    def chargeStrength(self) -> "slang::ast::ChargeStrength" | None: ...

    @property
    def driveStrength(self) -> tuple["slang::ast::DriveStrength" | None, "slang::ast::DriveStrength" | None]: ...

    class ExpansionHint(enum.Enum):
        Vectored = 1

        Scalared = 2

    Vectored: NetSymbol.ExpansionHint = NetSymbol.ExpansionHint.Vectored

    Scalared: NetSymbol.ExpansionHint = NetSymbol.ExpansionHint.Scalared

class TempVarSymbol(VariableSymbol):
    pass

class IteratorSymbol(TempVarSymbol):
    pass

class PatternVarSymbol(TempVarSymbol):
    pass

class LocalAssertionVarSymbol(VariableSymbol):
    pass

class ClockingSkew:
    @property
    def edge(self) -> EdgeKind: ...

    @property
    def delay(self) -> TimingControl: ...

    @property
    def hasValue(self) -> bool: ...

class ClockVarSymbol(VariableSymbol):
    @property
    def direction(self) -> ArgumentDirection: ...

    @property
    def inputSkew(self) -> ClockingSkew: ...

    @property
    def outputSkew(self) -> ClockingSkew: ...

class ClassPropertySymbol(VariableSymbol):
    @property
    def visibility(self) -> Visibility: ...

    @property
    def randMode(self) -> RandMode: ...

class MethodFlags(enum.IntEnum):
    Virtual = 1

    Pure = 2

    Static = 4

    Constructor = 8

    InterfaceExtern = 16

    ModportImport = 32

    ModportExport = 64

    DPIImport = 128

    DPIContext = 256

    BuiltIn = 512

    Randomize = 1024

    ForkJoin = 2048

    DefaultedSuperArg = 4096

    Initial = 8192

    Extends = 16384

    Final = 32768

class SubroutineSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def defaultLifetime(self) -> VariableLifetime: ...

    @property
    def subroutineKind(self) -> SubroutineKind: ...

    @property
    def visibility(self) -> Visibility: ...

    @property
    def flags(self) -> MethodFlags: ...

    @property
    def thisVar(self) -> VariableSymbol: ...

    @property
    def returnValVar(self) -> VariableSymbol: ...

    @property
    def arguments(self) -> span[FormalArgumentSymbol]: ...

    @property
    def body(self) -> Statement: ...

    @property
    def returnType(self) -> Type: ...

    @property
    def override(self) -> SubroutineSymbol: ...

    @property
    def prototype(self) -> MethodPrototypeSymbol: ...

    @property
    def isVirtual(self) -> bool: ...

class MethodPrototypeSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def subroutineKind(self) -> SubroutineKind: ...

    @property
    def visibility(self) -> Visibility: ...

    @property
    def flags(self) -> MethodFlags: ...

    @property
    def arguments(self) -> span[FormalArgumentSymbol]: ...

    @property
    def returnType(self) -> Type: ...

    @property
    def override(self) -> Symbol: ...

    @property
    def subroutine(self) -> SubroutineSymbol: ...

    @property
    def isVirtual(self) -> bool: ...

    @property
    def firstExternImpl(self) -> MethodPrototypeSymbol.ExternImpl: ...

    class ExternImpl:
        @property
        def impl(self) -> SubroutineSymbol: ...

        @property
        def nextImpl(self) -> MethodPrototypeSymbol.ExternImpl: ...

class PortSymbol(Symbol):
    @property
    def internalSymbol(self) -> Symbol: ...

    @property
    def externalLoc(self) -> pyslang.SourceLocation: ...

    @property
    def direction(self) -> ArgumentDirection: ...

    @property
    def isNullPort(self) -> bool: ...

    @property
    def isAnsiPort(self) -> bool: ...

    @property
    def type(self) -> Type: ...

    @property
    def initializer(self) -> Expression: ...

    @property
    def internalExpr(self) -> Expression: ...

    @property
    def isNetPort(self) -> bool: ...

class MultiPortSymbol(Symbol):
    @property
    def ports(self) -> span[PortSymbol]: ...

    @property
    def direction(self) -> ArgumentDirection: ...

    @property
    def isNullPort(self) -> bool: ...

    @property
    def type(self) -> Type: ...

    @property
    def initializer(self) -> Expression: ...

class InterfacePortSymbol(Symbol):
    @property
    def interfaceDef(self) -> DefinitionSymbol: ...

    @property
    def modport(self) -> str: ...

    @property
    def isGeneric(self) -> bool: ...

    @property
    def declaredRange(self) -> span[pyslang.ConstantRange] | None: ...

    @property
    def connection(self) -> tuple[Symbol, ModportSymbol]: ...

    @property
    def isInvalid(self) -> bool: ...

class PortConnection:
    @property
    def ifaceConn(self) -> tuple[Symbol, ModportSymbol]: ...

    @property
    def expression(self) -> Expression: ...

    @property
    def port(self) -> Symbol: ...

class InstanceSymbolBase(Symbol):
    @property
    def arrayPath(self) -> span[int]: ...

    @property
    def arrayName(self) -> str: ...

class InstanceSymbol(InstanceSymbolBase):
    @property
    def definition(self) -> DefinitionSymbol: ...

    @property
    def isModule(self) -> bool: ...

    @property
    def isInterface(self) -> bool: ...

    @property
    def portConnections(self) -> span[PortConnection]: ...

    @property
    def body(self) -> InstanceBodySymbol: ...

    @property
    def canonicalBody(self) -> InstanceBodySymbol: ...

    @overload
    def getPortConnection(self, port: PortSymbol) -> PortConnection: ...

    @overload
    def getPortConnection(self, port: InterfacePortSymbol) -> PortConnection: ...

class InstanceBodySymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def parentInstance(self) -> InstanceSymbol: ...

    @property
    def parameters(self) -> list: ...

    @property
    def portList(self) -> span[Symbol]: ...

    @property
    def definition(self) -> DefinitionSymbol: ...

    def findPort(self, portName: str) -> Symbol: ...

    def hasSameType(self, other: InstanceBodySymbol) -> bool: ...

class InstanceArraySymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def elements(self) -> span[Symbol]: ...

    @property
    def range(self) -> pyslang.ConstantRange: ...

    @property
    def arrayName(self) -> str: ...

class UninstantiatedDefSymbol(Symbol):
    @property
    def definitionName(self) -> str: ...

    @property
    def paramExpressions(self) -> span[Expression]: ...

    @property
    def portConnections(self) -> span[AssertionExpr]: ...

    @property
    def portNames(self) -> span[str]: ...

    @property
    def isChecker(self) -> bool: ...

class PrimitiveInstanceSymbol(InstanceSymbolBase):
    @property
    def primitiveType(self) -> PrimitiveSymbol: ...

    @property
    def portConnections(self) -> span[Expression]: ...

    @property
    def delay(self) -> TimingControl: ...

    @property
    def driveStrength(self) -> tuple["slang::ast::DriveStrength" | None, "slang::ast::DriveStrength" | None]: ...

class CheckerInstanceSymbol(InstanceSymbolBase):
    @property
    def body(self) -> CheckerInstanceBodySymbol: ...

    @property
    def portConnections(self) -> span[CheckerInstanceSymbol.Connection]: ...

    class Connection:
        @property
        def formal(self) -> Symbol: ...

        @property
        def outputInitialExpr(self) -> Expression: ...

        @property
        def actual(self) -> Expression | AssertionExpr | TimingControl: ...

        @property
        def attributes(self) -> span[AttributeSymbol]: ...

class CheckerInstanceBodySymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def parentInstance(self) -> CheckerInstanceSymbol: ...

    @property
    def checker(self) -> CheckerSymbol: ...

class StatementBlockSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def blockKind(self) -> StatementBlockKind: ...

    @property
    def defaultLifetime(self) -> VariableLifetime: ...

class ProceduralBlockSymbol(Symbol):
    @property
    def procedureKind(self) -> ProceduralBlockKind: ...

    @property
    def isSingleDriverBlock(self) -> bool: ...

    @property
    def body(self) -> Statement: ...

    @property
    def blocks(self) -> span[StatementBlockSymbol]: ...

class GenerateBranchKind(enum.Enum):
    IfTrue = 0

    IfFalse = 1

    CaseItem = 2

    CaseDefault = 3

    LoopIteration = 4

    IllegalUnconditional = 5

class GenerateBlockSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def constructIndex(self) -> int: ...

    @property
    def branchKind(self) -> GenerateBranchKind: ...

    @property
    def caseItemExpressions(self) -> span[Expression]: ...

    @property
    def arrayIndex(self) -> pyslang.SVInt: ...

    @property
    def conditionExpression(self) -> Expression: ...

    @property
    def externalName(self) -> str: ...

class GenerateBlockArraySymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def constructIndex(self) -> int: ...

    @property
    def entries(self) -> span[GenerateBlockSymbol]: ...

    @property
    def valid(self) -> bool: ...

    @property
    def initialExpression(self) -> Expression: ...

    @property
    def stopExpression(self) -> Expression: ...

    @property
    def iterExpression(self) -> Expression: ...

    @property
    def loopVariable(self) -> VariableSymbol: ...

    @property
    def externalName(self) -> str: ...

class EmptyMemberSymbol(Symbol):
    pass

class GenvarSymbol(Symbol):
    pass

class SpecifyBlockSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

class AnonymousProgramSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

class NetAliasSymbol(Symbol):
    @property
    def netReferences(self) -> span[Expression]: ...

class TransparentMemberSymbol(Symbol):
    @property
    def wrapped(self) -> Symbol: ...

class ExplicitImportSymbol(Symbol):
    @property
    def packageName(self) -> str: ...

    @property
    def importName(self) -> str: ...

    @property
    def package(self) -> PackageSymbol: ...

    @property
    def importedSymbol(self) -> Symbol: ...

class WildcardImportSymbol(Symbol):
    @property
    def packageName(self) -> str: ...

    @property
    def package(self) -> PackageSymbol: ...

class ModportPortSymbol(ValueSymbol):
    @property
    def direction(self) -> ArgumentDirection: ...

    @property
    def internalSymbol(self) -> Symbol: ...

    @property
    def explicitConnection(self) -> Expression: ...

class ModportClockingSymbol(Symbol):
    @property
    def target(self) -> Symbol: ...

class ModportSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def hasExports(self) -> bool: ...

class ContinuousAssignSymbol(Symbol):
    @property
    def assignment(self) -> Expression: ...

    @property
    def delay(self) -> TimingControl: ...

    @property
    def driveStrength(self) -> tuple["slang::ast::DriveStrength" | None, "slang::ast::DriveStrength" | None]: ...

class ElabSystemTaskSymbol(Symbol):
    @property
    def taskKind(self) -> ElabSystemTaskKind: ...

    @property
    def message(self) -> str | None: ...

    @property
    def assertCondition(self) -> Expression: ...

class PrimitivePortSymbol(ValueSymbol):
    @property
    def direction(self) -> PrimitivePortDirection: ...

class PrimitiveSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def ports(self) -> span[PrimitivePortSymbol]: ...

    @property
    def initVal(self) -> pyslang.ConstantValue: ...

    @property
    def primitiveKind(self) -> PrimitiveSymbol.PrimitiveKind: ...

    @property
    def isSequential(self) -> bool: ...

    @property
    def table(self) -> span[PrimitiveSymbol.TableEntry]: ...

    class PrimitiveKind(enum.Enum):
        UserDefined = 0

        Fixed = 1

        NInput = 2

        NOutput = 3

    UserDefined: PrimitiveSymbol.PrimitiveKind = PrimitiveSymbol.PrimitiveKind.UserDefined

    Fixed: PrimitiveSymbol.PrimitiveKind = PrimitiveSymbol.PrimitiveKind.Fixed

    NInput: PrimitiveSymbol.PrimitiveKind = PrimitiveSymbol.PrimitiveKind.NInput

    NOutput: PrimitiveSymbol.PrimitiveKind = PrimitiveSymbol.PrimitiveKind.NOutput

    class TableEntry:
        @property
        def inputs(self) -> str: ...

        @property
        def state(self) -> str: ...

        @property
        def output(self) -> str: ...

class AssertionPortSymbol(Symbol):
    @property
    def direction(self) -> ArgumentDirection | None: ...

    @property
    def isLocalVar(self) -> bool: ...

    @property
    def type(self) -> Type: ...

class SequenceSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def ports(self) -> span[AssertionPortSymbol]: ...

class PropertySymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def ports(self) -> span[AssertionPortSymbol]: ...

class LetDeclSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def ports(self) -> span[AssertionPortSymbol]: ...

class CheckerSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def ports(self) -> span[AssertionPortSymbol]: ...

class ClockingBlockSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def event(self) -> TimingControl: ...

    @property
    def defaultInputSkew(self) -> ClockingSkew: ...

    @property
    def defaultOutputSkew(self) -> ClockingSkew: ...

class RandSeqProductionSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def arguments(self) -> span[FormalArgumentSymbol]: ...

    @property
    def rules(self) -> span[RandSeqProductionSymbol.Rule]: ...

    @property
    def returnType(self) -> Type: ...

    class ProdKind(enum.Enum):
        Item = 0

        CodeBlock = 1

        IfElse = 2

        Repeat = 3

        Case = 4

    class ProdBase:
        @property
        def kind(self) -> RandSeqProductionSymbol.ProdKind: ...

    class ProdItem(RandSeqProductionSymbol.ProdBase):
        @property
        def target(self) -> RandSeqProductionSymbol: ...

        @property
        def args(self) -> span[Expression]: ...

    class CodeBlockProd(RandSeqProductionSymbol.ProdBase):
        @property
        def block(self) -> StatementBlockSymbol: ...

    class IfElseProd(RandSeqProductionSymbol.ProdBase):
        @property
        def expr(self) -> Expression: ...

        @property
        def ifItem(self) -> RandSeqProductionSymbol.ProdItem: ...

        @property
        def elseItem(self) -> RandSeqProductionSymbol.ProdItem | None: ...

    class RepeatProd(RandSeqProductionSymbol.ProdBase):
        @property
        def expr(self) -> Expression: ...

        @property
        def item(self) -> RandSeqProductionSymbol.ProdItem: ...

    class CaseItem:
        @property
        def expressions(self) -> span[Expression]: ...

        @property
        def item(self) -> RandSeqProductionSymbol.ProdItem: ...

    class CaseProd(RandSeqProductionSymbol.ProdBase):
        @property
        def expr(self) -> Expression: ...

        @property
        def items(self) -> span[RandSeqProductionSymbol.CaseItem]: ...

        @property
        def defaultItem(self) -> RandSeqProductionSymbol.ProdItem | None: ...

    class Rule:
        @property
        def ruleBlock(self) -> StatementBlockSymbol: ...

        @property
        def prods(self) -> span[RandSeqProductionSymbol.ProdBase]: ...

        @property
        def weightExpr(self) -> Expression: ...

        @property
        def randJoinExpr(self) -> Expression: ...

        @property
        def codeBlock(self) -> RandSeqProductionSymbol.CodeBlockProd | None: ...

        @property
        def isRandJoin(self) -> bool: ...

class TimingPathSymbol(Symbol):
    @property
    def connectionKind(self) -> TimingPathSymbol.ConnectionKind: ...

    @property
    def polarity(self) -> TimingPathSymbol.Polarity: ...

    @property
    def edgePolarity(self) -> TimingPathSymbol.Polarity: ...

    @property
    def edgeIdentifier(self) -> EdgeKind: ...

    @property
    def isStateDependent(self) -> bool: ...

    @property
    def edgeSourceExpr(self) -> Expression: ...

    @property
    def conditionExpr(self) -> Expression: ...

    @property
    def inputs(self) -> span[Expression]: ...

    @property
    def outputs(self) -> span[Expression]: ...

    @property
    def delays(self) -> span[Expression]: ...

    class ConnectionKind(enum.Enum):
        Full = 0

        Parallel = 1

    class Polarity(enum.Enum):
        Unknown = 0

        Positive = 1

        Negative = 2

class PulseStyleSymbol(Symbol):
    @property
    def pulseStyleKind(self) -> PulseStyleKind: ...

    @property
    def terminals(self) -> span[Expression]: ...

class SystemTimingCheckSymbol(Symbol):
    @property
    def timingCheckKind(self) -> SystemTimingCheckKind: ...

    @property
    def arguments(self) -> span[SystemTimingCheckSymbol.Arg]: ...

    class Arg:
        @property
        def expr(self) -> Expression: ...

        @property
        def condition(self) -> Expression: ...

        @property
        def edge(self) -> EdgeKind: ...

        @property
        def edgeDescriptors(self) -> span["std::array<char,2>"]: ...

class CoverageOptionSetter:
    @property
    def isTypeOption(self) -> bool: ...

    @property
    def name(self) -> str: ...

    @property
    def expression(self) -> Expression: ...

class CovergroupBodySymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def options(self) -> span[CoverageOptionSetter]: ...

class CoverageBinSymbol(Symbol):
    @property
    def binsKind(self) -> CoverageBinSymbol.BinKind: ...

    @property
    def isArray(self) -> bool: ...

    @property
    def isWildcard(self) -> bool: ...

    @property
    def isDefault(self) -> bool: ...

    @property
    def isDefaultSequence(self) -> bool: ...

    @property
    def iffExpr(self) -> Expression: ...

    @property
    def numberOfBinsExpr(self) -> Expression: ...

    @property
    def setCoverageExpr(self) -> Expression: ...

    @property
    def withExpr(self) -> Expression: ...

    @property
    def crossSelectExpr(self) -> BinsSelectExpr: ...

    @property
    def values(self) -> span[Expression]: ...

    class TransRangeList:
        @property
        def items(self) -> span[Expression]: ...

        @property
        def repeatFrom(self) -> Expression: ...

        @property
        def repeatTo(self) -> Expression: ...

        @property
        def repeatKind(self) -> CoverageBinSymbol.TransRangeList.RepeatKind: ...

        class RepeatKind(enum.Enum):
            """enum.Enum"""

            Consecutive = 1

            Nonconsecutive = 2

            GoTo = 3

        Consecutive: CoverageBinSymbol.TransRangeList.RepeatKind = CoverageBinSymbol.TransRangeList.RepeatKind.Consecutive

        Nonconsecutive: CoverageBinSymbol.TransRangeList.RepeatKind = CoverageBinSymbol.TransRangeList.RepeatKind.Nonconsecutive

        GoTo: CoverageBinSymbol.TransRangeList.RepeatKind = CoverageBinSymbol.TransRangeList.RepeatKind.GoTo

    class BinKind(enum.Enum):
        Bins = 0

        IllegalBins = 1

        IgnoreBins = 2

    Bins: CoverageBinSymbol.BinKind = CoverageBinSymbol.BinKind.Bins

    IllegalBins: CoverageBinSymbol.BinKind = CoverageBinSymbol.BinKind.IllegalBins

    IgnoreBins: CoverageBinSymbol.BinKind = CoverageBinSymbol.BinKind.IgnoreBins

class CoverpointSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def options(self) -> span[CoverageOptionSetter]: ...

    @property
    def type(self) -> Type: ...

    @property
    def coverageExpr(self) -> Expression: ...

    @property
    def iffExpr(self) -> Expression: ...

class CoverCrossBodySymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def crossQueueType(self) -> Type: ...

class CoverCrossSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def options(self) -> span[CoverageOptionSetter]: ...

    @property
    def targets(self) -> span[CoverpointSymbol]: ...

    @property
    def iffExpr(self) -> Expression: ...

class ConfigBlockSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

class IntegralFlags(enum.IntEnum):
    Unsigned = 0

    TwoState = 0

    Signed = 1

    FourState = 2

    Reg = 4

class Type(Symbol):
    @property
    def canonicalType(self) -> Type: ...

    @property
    def bitWidth(self) -> int: ...

    @property
    def bitstreamWidth(self) -> int: ...

    @property
    def selectableWidth(self) -> int: ...

    @property
    def isSigned(self) -> bool: ...

    @property
    def isFourState(self) -> bool: ...

    @property
    def isAggregate(self) -> bool: ...

    @property
    def isSingular(self) -> bool: ...

    @property
    def isIntegral(self) -> bool: ...

    @property
    def isScalar(self) -> bool: ...

    @property
    def isPredefinedInteger(self) -> bool: ...

    @property
    def isSimpleBitVector(self) -> bool: ...

    @property
    def hasFixedRange(self) -> bool: ...

    @property
    def isBooleanConvertible(self) -> bool: ...

    @property
    def isArray(self) -> bool: ...

    @property
    def isStruct(self) -> bool: ...

    @property
    def isFixedSize(self) -> bool: ...

    @property
    def isSimpleType(self) -> bool: ...

    @property
    def isByteArray(self) -> bool: ...

    @property
    def isNumeric(self) -> bool: ...

    @property
    def isPackedArray(self) -> bool: ...

    @property
    def isUnpackedArray(self) -> bool: ...

    @property
    def isDynamicallySizedArray(self) -> bool: ...

    @property
    def isTaggedUnion(self) -> bool: ...

    @property
    def isUnpackedStruct(self) -> bool: ...

    @property
    def isPackedUnion(self) -> bool: ...

    @property
    def isUnpackedUnion(self) -> bool: ...

    @property
    def isAssociativeArray(self) -> bool: ...

    @property
    def isQueue(self) -> bool: ...

    @property
    def isEnum(self) -> bool: ...

    @property
    def isClass(self) -> bool: ...

    @property
    def isCovergroup(self) -> bool: ...

    @property
    def isFloating(self) -> bool: ...

    @property
    def isVoid(self) -> bool: ...

    @property
    def isNull(self) -> bool: ...

    @property
    def isCHandle(self) -> bool: ...

    @property
    def isString(self) -> bool: ...

    @property
    def isEvent(self) -> bool: ...

    @property
    def isUnbounded(self) -> bool: ...

    @property
    def isTypeRefType(self) -> bool: ...

    @property
    def isUntypedType(self) -> bool: ...

    @property
    def isSequenceType(self) -> bool: ...

    @property
    def isPropertyType(self) -> bool: ...

    @property
    def isVirtualInterface(self) -> bool: ...

    @property
    def isHandleType(self) -> bool: ...

    @property
    def isObjectHandleType(self) -> bool: ...

    @property
    def isAlias(self) -> bool: ...

    @property
    def isError(self) -> bool: ...

    def isMatching(self, rhs: Type) -> bool: ...

    def isEquivalent(self, rhs: Type) -> bool: ...

    def isAssignmentCompatible(self, rhs: Type) -> bool: ...

    def isCastCompatible(self, rhs: Type) -> bool: ...

    def isBitstreamCastable(self, rhs: Type) -> bool: ...

    def isBitstreamType(self, destination: bool = False) -> bool: ...

    def isDerivedFrom(self, rhs: Type) -> bool: ...

    def implements(self, rhs: Type) -> bool: ...

    def isValidForRand(self, mode: RandMode, languageVersion: pyslang.LanguageVersion) -> bool: ...

    def coerceValue(self, value: pyslang.ConstantValue) -> pyslang.ConstantValue: ...

    @staticmethod
    def getCommonBase(left: Type, right: Type) -> Type: ...

    @property
    def integralFlags(self) -> IntegralFlags: ...

    @property
    def defaultValue(self) -> pyslang.ConstantValue: ...

    @property
    def fixedRange(self) -> pyslang.ConstantRange: ...

    @property
    def arrayElementType(self) -> Type: ...

    @property
    def associativeIndexType(self) -> Type: ...

    @property
    def canBeStringLike(self) -> bool: ...

    @property
    def isIterable(self) -> bool: ...

    @property
    def isValidForDPIReturn(self) -> bool: ...

    @property
    def isValidForDPIArg(self) -> bool: ...

    @property
    def isValidForSequence(self) -> bool: ...

    def __eq__(self, arg: Type, /) -> bool: ...

    def __hash__(self) -> int: ...

    def __repr__(self) -> str: ...

class NetType(Symbol):
    @property
    def declaredType(self) -> DeclaredType: ...

    @property
    def netKind(self) -> NetType.NetKind: ...

    @property
    def resolutionFunction(self) -> SubroutineSymbol: ...

    @property
    def isError(self) -> bool: ...

    @property
    def isBuiltIn(self) -> bool: ...

    @staticmethod
    def getSimulatedNetType(internal: NetType, external: NetType, shouldWarn: bool) -> NetType: ...

    class NetKind(enum.Enum):
        Unknown = 0

        Wire = 1

        WAnd = 2

        WOr = 3

        Tri = 4

        TriAnd = 5

        TriOr = 6

        Tri0 = 7

        Tri1 = 8

        TriReg = 9

        Supply0 = 10

        Supply1 = 11

        UWire = 12

        Interconnect = 13

        UserDefined = 14

    Unknown: NetType.NetKind = NetType.NetKind.Unknown

    Wire: NetType.NetKind = NetType.NetKind.Wire

    WAnd: NetType.NetKind = NetType.NetKind.WAnd

    WOr: NetType.NetKind = NetType.NetKind.WOr

    Tri: NetType.NetKind = NetType.NetKind.Tri

    TriAnd: NetType.NetKind = NetType.NetKind.TriAnd

    TriOr: NetType.NetKind = NetType.NetKind.TriOr

    Tri0: NetType.NetKind = NetType.NetKind.Tri0

    Tri1: NetType.NetKind = NetType.NetKind.Tri1

    TriReg: NetType.NetKind = NetType.NetKind.TriReg

    Supply0: NetType.NetKind = NetType.NetKind.Supply0

    Supply1: NetType.NetKind = NetType.NetKind.Supply1

    UWire: NetType.NetKind = NetType.NetKind.UWire

    Interconnect: NetType.NetKind = NetType.NetKind.Interconnect

    UserDefined: NetType.NetKind = NetType.NetKind.UserDefined

class TypePrintingOptions:
    @property
    def quoteChar(self) -> str | None: ...

    @quoteChar.setter
    def quoteChar(self, arg: str | None, /) -> None: ...

    @property
    def elideScopeNames(self) -> bool: ...

    @elideScopeNames.setter
    def elideScopeNames(self, arg: bool, /) -> None: ...

    @property
    def printAKA(self) -> bool: ...

    @printAKA.setter
    def printAKA(self, arg: bool, /) -> None: ...

    @property
    def skipScopedTypeNames(self) -> bool: ...

    @skipScopedTypeNames.setter
    def skipScopedTypeNames(self, arg: bool, /) -> None: ...

    @property
    def skipTypeDefs(self) -> bool: ...

    @skipTypeDefs.setter
    def skipTypeDefs(self, arg: bool, /) -> None: ...

    @property
    def fullEnumType(self) -> bool: ...

    @fullEnumType.setter
    def fullEnumType(self, arg: bool, /) -> None: ...

    @property
    def typedefsAsLinks(self) -> bool: ...

    @typedefsAsLinks.setter
    def typedefsAsLinks(self, arg: bool, /) -> None: ...

    @property
    def enumsAsLinks(self) -> bool: ...

    @enumsAsLinks.setter
    def enumsAsLinks(self, arg: bool, /) -> None: ...

    @property
    def classesAsLinks(self) -> bool: ...

    @classesAsLinks.setter
    def classesAsLinks(self, arg: bool, /) -> None: ...

    @property
    def printIntegralRange(self) -> bool: ...

    @printIntegralRange.setter
    def printIntegralRange(self, arg: bool, /) -> None: ...

    @property
    def anonymousTypeStyle(self) -> TypePrintingOptions.AnonymousTypeStyle: ...

    @anonymousTypeStyle.setter
    def anonymousTypeStyle(self, arg: TypePrintingOptions.AnonymousTypeStyle, /) -> None: ...

    @property
    def friendlyMemberCharLimit(self) -> int: ...

    @friendlyMemberCharLimit.setter
    def friendlyMemberCharLimit(self, arg: int, /) -> None: ...

    class AnonymousTypeStyle(enum.Enum):
        SystemName = 0

        FriendlyName = 1

    SystemName: TypePrintingOptions.AnonymousTypeStyle = TypePrintingOptions.AnonymousTypeStyle.SystemName

    FriendlyName: TypePrintingOptions.AnonymousTypeStyle = TypePrintingOptions.AnonymousTypeStyle.FriendlyName

class TypePrinter:
    def __init__(self) -> None: ...

    @property
    def options(self) -> TypePrintingOptions: ...

    @options.setter
    def options(self, arg: TypePrintingOptions, /) -> None: ...

    def append(self, type: Type) -> None: ...

    def clear(self) -> None: ...

    def toString(self) -> str: ...

class DeclaredType:
    @property
    def type(self) -> Type: ...

    @property
    def typeSyntax(self) -> pyslang.syntax.DataTypeSyntax: ...

    @property
    def initializer(self) -> Expression: ...

    @property
    def initializerSyntax(self) -> pyslang.syntax.ExpressionSyntax: ...

    @property
    def initializerLocation(self) -> pyslang.SourceLocation: ...

    @property
    def isEvaluating(self) -> bool: ...

    @property
    def resolvedDimensions(self) -> list[EvaluatedDimension]: ...

class IntegralType(Type):
    def getBitVectorRange(self) -> pyslang.ConstantRange: ...

    def isDeclaredReg(self) -> bool: ...

class ScalarType(IntegralType):
    @property
    def scalarKind(self) -> ScalarType.Kind: ...

    class Kind(enum.Enum):
        Bit = 0

        Logic = 1

        Reg = 2

    Bit: ScalarType.Kind = ScalarType.Kind.Bit

    Logic: ScalarType.Kind = ScalarType.Kind.Logic

    Reg: ScalarType.Kind = ScalarType.Kind.Reg

class PredefinedIntegerType(IntegralType):
    @property
    def integerKind(self) -> PredefinedIntegerType.Kind: ...

    class Kind(enum.Enum):
        ShortInt = 0

        Int = 1

        LongInt = 2

        Byte = 3

        Integer = 4

        Time = 5

    ShortInt: PredefinedIntegerType.Kind = PredefinedIntegerType.Kind.ShortInt

    Int: PredefinedIntegerType.Kind = PredefinedIntegerType.Kind.Int

    LongInt: PredefinedIntegerType.Kind = PredefinedIntegerType.Kind.LongInt

    Byte: PredefinedIntegerType.Kind = PredefinedIntegerType.Kind.Byte

    Integer: PredefinedIntegerType.Kind = PredefinedIntegerType.Kind.Integer

    Time: PredefinedIntegerType.Kind = PredefinedIntegerType.Kind.Time

class FloatingType(Type):
    @property
    def floatKind(self) -> FloatingType.Kind: ...

    class Kind(enum.Enum):
        Real = 0

        ShortReal = 1

        RealTime = 2

    Real: FloatingType.Kind = FloatingType.Kind.Real

    ShortReal: FloatingType.Kind = FloatingType.Kind.ShortReal

    RealTime: FloatingType.Kind = FloatingType.Kind.RealTime

class EnumType(IntegralType):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def baseType(self) -> Type: ...

    @property
    def systemId(self) -> int: ...

class PackedArrayType(IntegralType):
    @property
    def elementType(self) -> Type: ...

    @property
    def range(self) -> pyslang.ConstantRange: ...

class FixedSizeUnpackedArrayType(Type):
    @property
    def elementType(self) -> Type: ...

    @property
    def range(self) -> pyslang.ConstantRange: ...

class DynamicArrayType(Type):
    @property
    def elementType(self) -> Type: ...

class DPIOpenArrayType(Type):
    @property
    def isPacked(self) -> bool: ...

    @property
    def elementType(self) -> Type: ...

class AssociativeArrayType(Type):
    @property
    def elementType(self) -> Type: ...

    @property
    def indexType(self) -> Type: ...

class QueueType(Type):
    @property
    def elementType(self) -> Type: ...

    @property
    def maxBound(self) -> int: ...

class PackedStructType(IntegralType):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def systemId(self) -> int: ...

class UnpackedStructType(Type):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def systemId(self) -> int: ...

class PackedUnionType(IntegralType):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def systemId(self) -> int: ...

    @property
    def isTagged(self) -> bool: ...

    @property
    def isSoft(self) -> bool: ...

    @property
    def tagBits(self) -> int: ...

class UnpackedUnionType(Type):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def systemId(self) -> int: ...

    @property
    def isTagged(self) -> bool: ...

class VoidType(Type):
    pass

class NullType(Type):
    pass

class CHandleType(Type):
    pass

class StringType(Type):
    pass

class EventType(Type):
    pass

class UnboundedType(Type):
    pass

class TypeRefType(Type):
    pass

class UntypedType(Type):
    pass

class SequenceType(Type):
    pass

class PropertyType(Type):
    pass

class ErrorType(Type):
    pass

class VirtualInterfaceType(Type):
    @property
    def iface(self) -> InstanceSymbol: ...

    @property
    def modport(self) -> ModportSymbol: ...

class ForwardTypeRestriction(enum.Enum):
    Enum = 1

    Struct = 2

    Union = 3

    Class = 4

    InterfaceClass = 5

class ForwardingTypedefSymbol(Symbol):
    @property
    def typeRestriction(self) -> ForwardTypeRestriction: ...

    @property
    def visibility(self) -> Visibility | None: ...

    @property
    def nextForwardDecl(self) -> ForwardingTypedefSymbol: ...

class TypeAliasType(Type):
    @property
    def targetType(self) -> DeclaredType: ...

    @property
    def visibility(self) -> Visibility: ...

    @property
    def firstForwardDecl(self) -> ForwardingTypedefSymbol: ...

class ClassType(Type):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def genericClass(self) -> GenericClassDefSymbol: ...

    @property
    def isAbstract(self) -> bool: ...

    @property
    def isInterface(self) -> bool: ...

    @property
    def isFinal(self) -> bool: ...

    @property
    def thisVar(self) -> VariableSymbol: ...

    @property
    def baseClass(self) -> Type: ...

    @property
    def implementedInterfaces(self) -> span[Type]: ...

    @property
    def baseConstructorCall(self) -> Expression: ...

    @property
    def constructor(self) -> SubroutineSymbol: ...

    @property
    def firstForwardDecl(self) -> ForwardingTypedefSymbol: ...

    @property
    def properties(self) -> list: ...

class GenericClassDefSymbol(Symbol):
    @property
    def isInterface(self) -> bool: ...

    @property
    def defaultSpecialization(self, arg: Scope, /) -> Type: ...

    @property
    def invalidSpecialization(self) -> Type: ...

    @property
    def firstForwardDecl(self) -> ForwardingTypedefSymbol: ...

class ConstraintBlockFlags(enum.IntEnum):
    Pure = 2

    Static = 4

    Extern = 8

    ExplicitExtern = 16

    Initial = 32

    Extends = 64

    Final = 128

class ConstraintBlockSymbol(Symbol):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def thisVar(self) -> VariableSymbol: ...

    @property
    def flags(self) -> ConstraintBlockFlags: ...

    @property
    def constraints(self) -> Constraint: ...

class CovergroupType(Type):
    @property
    def compilation(self) -> Compilation: ...

    @property
    def defaultNetType(self) -> NetType: ...

    @property
    def timeScale(self) -> pyslang.TimeScale | None: ...

    @property
    def isProceduralContext(self) -> bool: ...

    @property
    def containingInstance(self) -> InstanceBodySymbol: ...

    @property
    def compilationUnit(self) -> CompilationUnitSymbol: ...

    @property
    def isUninstantiated(self) -> bool: ...

    def find(self, arg: str, /) -> Symbol: ...

    def lookupName(self, name: str, location: LookupLocation = ..., flags: LookupFlags = LookupFlags.None_) -> Symbol: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Symbol]: ...

    @property
    def arguments(self) -> span[FormalArgumentSymbol]: ...

    @property
    def body(self) -> CovergroupBodySymbol: ...

    @property
    def baseGroup(self) -> Type: ...

    @property
    def coverageEvent(self) -> TimingControl: ...
