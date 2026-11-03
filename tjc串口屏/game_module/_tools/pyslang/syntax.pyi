"""Syntax tree nodes and utilities"""

from collections.abc import Iterator
import enum
from typing import overload

import pyslang
import pyslang.parsing


class SyntaxKind(enum.Enum):
    Unknown = 0

    AcceptOnPropertyExpr = 1

    ActionBlock = 2

    AddAssignmentExpression = 3

    AddExpression = 4

    AlwaysBlock = 5

    AlwaysCombBlock = 6

    AlwaysFFBlock = 7

    AlwaysLatchBlock = 8

    AndAssignmentExpression = 9

    AndPropertyExpr = 10

    AndSequenceExpr = 11

    AnonymousProgram = 12

    AnsiPortList = 13

    AnsiUdpPortList = 14

    ArgumentList = 15

    ArithmeticLeftShiftAssignmentExpression = 16

    ArithmeticRightShiftAssignmentExpression = 17

    ArithmeticShiftLeftExpression = 18

    ArithmeticShiftRightExpression = 19

    ArrayAndMethod = 20

    ArrayOrMethod = 21

    ArrayOrRandomizeMethodExpression = 22

    ArrayUniqueMethod = 23

    ArrayXorMethod = 24

    AscendingRangeSelect = 25

    AssertPropertyStatement = 26

    AssertionItemPort = 27

    AssertionItemPortList = 28

    AssignmentExpression = 29

    AssignmentPatternExpression = 30

    AssignmentPatternItem = 31

    AssumePropertyStatement = 32

    AttributeInstance = 33

    AttributeSpec = 34

    BadExpression = 35

    BeginKeywordsDirective = 36

    BinSelectWithFilterExpr = 37

    BinaryAndExpression = 38

    BinaryBinsSelectExpr = 39

    BinaryBlockEventExpression = 40

    BinaryConditionalDirectiveExpression = 41

    BinaryEventExpression = 42

    BinaryOrExpression = 43

    BinaryXnorExpression = 44

    BinaryXorExpression = 45

    BindDirective = 46

    BindTargetList = 47

    BinsSelectConditionExpr = 48

    BinsSelection = 49

    BitSelect = 50

    BitType = 51

    BlockCoverageEvent = 52

    BlockingEventTriggerStatement = 53

    ByteType = 54

    CHandleType = 55

    CaseEqualityExpression = 56

    CaseGenerate = 57

    CaseInequalityExpression = 58

    CasePropertyExpr = 59

    CaseStatement = 60

    CastExpression = 61

    CellConfigRule = 62

    CellDefineDirective = 63

    ChargeStrength = 64

    CheckerDataDeclaration = 65

    CheckerDeclaration = 66

    CheckerInstanceStatement = 67

    CheckerInstantiation = 68

    ClassDeclaration = 69

    ClassMethodDeclaration = 70

    ClassMethodPrototype = 71

    ClassName = 72

    ClassPropertyDeclaration = 73

    ClassSpecifier = 74

    ClockingDeclaration = 75

    ClockingDirection = 76

    ClockingItem = 77

    ClockingPropertyExpr = 78

    ClockingSequenceExpr = 79

    ClockingSkew = 80

    ColonExpressionClause = 81

    CompilationUnit = 82

    ConcatenationExpression = 83

    ConcurrentAssertionMember = 84

    ConditionalConstraint = 85

    ConditionalExpression = 86

    ConditionalPathDeclaration = 87

    ConditionalPattern = 88

    ConditionalPredicate = 89

    ConditionalPropertyExpr = 90

    ConditionalStatement = 91

    ConfigCellIdentifier = 92

    ConfigDeclaration = 93

    ConfigInstanceIdentifier = 94

    ConfigLiblist = 95

    ConfigUseClause = 96

    ConstraintBlock = 97

    ConstraintDeclaration = 98

    ConstraintPrototype = 99

    ConstructorName = 100

    ContinuousAssign = 101

    CopyClassExpression = 102

    CoverCross = 103

    CoverPropertyStatement = 104

    CoverSequenceStatement = 105

    CoverageBins = 106

    CoverageBinsArraySize = 107

    CoverageIffClause = 108

    CoverageOption = 109

    CovergroupDeclaration = 110

    Coverpoint = 111

    CycleDelay = 112

    DPIExport = 113

    DPIImport = 114

    DataDeclaration = 115

    Declarator = 116

    DefParam = 117

    DefParamAssignment = 118

    DefaultCaseItem = 119

    DefaultClockingReference = 120

    DefaultConfigRule = 121

    DefaultCoverageBinInitializer = 122

    DefaultDecayTimeDirective = 123

    DefaultDisableDeclaration = 124

    DefaultDistItem = 125

    DefaultExtendsClauseArg = 126

    DefaultFunctionPort = 127

    DefaultNetTypeDirective = 128

    DefaultPatternKeyExpression = 129

    DefaultPropertyCaseItem = 130

    DefaultRsCaseItem = 131

    DefaultSkewItem = 132

    DefaultTriregStrengthDirective = 133

    DeferredAssertion = 134

    DefineDirective = 135

    Delay3 = 136

    DelayControl = 137

    DelayModeDistributedDirective = 138

    DelayModePathDirective = 139

    DelayModeUnitDirective = 140

    DelayModeZeroDirective = 141

    DelayedSequenceElement = 142

    DelayedSequenceExpr = 143

    DescendingRangeSelect = 144

    DisableConstraint = 145

    DisableForkStatement = 146

    DisableIff = 147

    DisableStatement = 148

    DistConstraintList = 149

    DistItem = 150

    DistWeight = 151

    DivideAssignmentExpression = 152

    DivideExpression = 153

    DividerClause = 154

    DoWhileStatement = 155

    DotMemberClause = 156

    DriveStrength = 157

    EdgeControlSpecifier = 158

    EdgeDescriptor = 159

    EdgeSensitivePathSuffix = 160

    ElabSystemTask = 161

    ElementSelect = 162

    ElementSelectExpression = 163

    ElsIfDirective = 164

    ElseClause = 165

    ElseConstraintClause = 166

    ElseDirective = 167

    ElsePropertyClause = 168

    EmptyArgument = 169

    EmptyIdentifierName = 170

    EmptyMember = 171

    EmptyNonAnsiPort = 172

    EmptyPortConnection = 173

    EmptyQueueExpression = 174

    EmptyStatement = 175

    EmptyTimingCheckArg = 176

    EndCellDefineDirective = 177

    EndIfDirective = 178

    EndKeywordsDirective = 179

    EndProtectDirective = 180

    EndProtectedDirective = 181

    EnumType = 182

    EqualityExpression = 183

    EqualsAssertionArgClause = 184

    EqualsTypeClause = 185

    EqualsValueClause = 186

    EventControl = 187

    EventControlWithExpression = 188

    EventType = 189

    ExpectPropertyStatement = 190

    ExplicitAnsiPort = 191

    ExplicitNonAnsiPort = 192

    ExpressionConstraint = 193

    ExpressionCoverageBinInitializer = 194

    ExpressionOrDist = 195

    ExpressionPattern = 196

    ExpressionStatement = 197

    ExpressionTimingCheckArg = 198

    ExtendsClause = 199

    ExternInterfaceMethod = 200

    ExternModuleDecl = 201

    ExternUdpDecl = 202

    FilePathSpec = 203

    FinalBlock = 204

    FirstMatchSequenceExpr = 205

    FollowedByPropertyExpr = 206

    ForLoopStatement = 207

    ForVariableDeclaration = 208

    ForeachLoopList = 209

    ForeachLoopStatement = 210

    ForeverStatement = 211

    ForwardTypeRestriction = 212

    ForwardTypedefDeclaration = 213

    FunctionDeclaration = 214

    FunctionPort = 215

    FunctionPortList = 216

    FunctionPrototype = 217

    GenerateBlock = 218

    GenerateRegion = 219

    GenvarDeclaration = 220

    GreaterThanEqualExpression = 221

    GreaterThanExpression = 222

    HierarchicalInstance = 223

    HierarchyInstantiation = 224

    IdWithExprCoverageBinInitializer = 225

    IdentifierName = 226

    IdentifierSelectName = 227

    IfDefDirective = 228

    IfGenerate = 229

    IfNDefDirective = 230

    IfNonePathDeclaration = 231

    IffEventClause = 232

    IffPropertyExpr = 233

    ImmediateAssertStatement = 234

    ImmediateAssertionMember = 235

    ImmediateAssumeStatement = 236

    ImmediateCoverStatement = 237

    ImplementsClause = 238

    ImplicationConstraint = 239

    ImplicationPropertyExpr = 240

    ImplicitAnsiPort = 241

    ImplicitEventControl = 242

    ImplicitNonAnsiPort = 243

    ImplicitType = 244

    ImpliesPropertyExpr = 245

    IncludeDirective = 246

    InequalityExpression = 247

    InitialBlock = 248

    InsideExpression = 249

    InstanceConfigRule = 250

    InstanceName = 251

    IntType = 252

    IntegerLiteralExpression = 253

    IntegerType = 254

    IntegerVectorExpression = 255

    InterfaceDeclaration = 256

    InterfaceHeader = 257

    InterfacePortHeader = 258

    IntersectClause = 259

    IntersectSequenceExpr = 260

    InvocationExpression = 261

    JumpStatement = 262

    LessThanEqualExpression = 263

    LessThanExpression = 264

    LetDeclaration = 265

    LibraryDeclaration = 266

    LibraryIncDirClause = 267

    LibraryIncludeStatement = 268

    LibraryMap = 269

    LineDirective = 270

    LocalScope = 271

    LocalVariableDeclaration = 272

    LogicType = 273

    LogicalAndExpression = 274

    LogicalEquivalenceExpression = 275

    LogicalImplicationExpression = 276

    LogicalLeftShiftAssignmentExpression = 277

    LogicalOrExpression = 278

    LogicalRightShiftAssignmentExpression = 279

    LogicalShiftLeftExpression = 280

    LogicalShiftRightExpression = 281

    LongIntType = 282

    LoopConstraint = 283

    LoopGenerate = 284

    LoopStatement = 285

    MacroActualArgument = 286

    MacroActualArgumentList = 287

    MacroArgumentDefault = 288

    MacroFormalArgument = 289

    MacroFormalArgumentList = 290

    MacroUsage = 291

    MatchesClause = 292

    MemberAccessExpression = 293

    MinTypMaxExpression = 294

    ModAssignmentExpression = 295

    ModExpression = 296

    ModportClockingPort = 297

    ModportDeclaration = 298

    ModportExplicitPort = 299

    ModportItem = 300

    ModportNamedPort = 301

    ModportSimplePortList = 302

    ModportSubroutinePort = 303

    ModportSubroutinePortList = 304

    ModuleDeclaration = 305

    ModuleHeader = 306

    MultipleConcatenationExpression = 307

    MultiplyAssignmentExpression = 308

    MultiplyExpression = 309

    NameValuePragmaExpression = 310

    NamedArgument = 311

    NamedBlockClause = 312

    NamedConditionalDirectiveExpression = 313

    NamedLabel = 314

    NamedParamAssignment = 315

    NamedPortConnection = 316

    NamedStructurePatternMember = 317

    NamedType = 318

    NetAlias = 319

    NetDeclaration = 320

    NetPortHeader = 321

    NetTypeDeclaration = 322

    NewArrayExpression = 323

    NewClassExpression = 324

    NoUnconnectedDriveDirective = 325

    NonAnsiPortList = 326

    NonAnsiUdpPortList = 327

    NonblockingAssignmentExpression = 328

    NonblockingEventTriggerStatement = 329

    NullLiteralExpression = 330

    NumberPragmaExpression = 331

    OneStepDelay = 332

    OrAssignmentExpression = 333

    OrPropertyExpr = 334

    OrSequenceExpr = 335

    OrderedArgument = 336

    OrderedParamAssignment = 337

    OrderedPortConnection = 338

    OrderedStructurePatternMember = 339

    PackageDeclaration = 340

    PackageExportAllDeclaration = 341

    PackageExportDeclaration = 342

    PackageHeader = 343

    PackageImportDeclaration = 344

    PackageImportItem = 345

    ParallelBlockStatement = 346

    ParameterDeclaration = 347

    ParameterDeclarationStatement = 348

    ParameterPortList = 349

    ParameterValueAssignment = 350

    ParenExpressionList = 351

    ParenPragmaExpression = 352

    ParenthesizedBinsSelectExpr = 353

    ParenthesizedConditionalDirectiveExpression = 354

    ParenthesizedEventExpression = 355

    ParenthesizedExpression = 356

    ParenthesizedPattern = 357

    ParenthesizedPropertyExpr = 358

    ParenthesizedSequenceExpr = 359

    PathDeclaration = 360

    PathDescription = 361

    PatternCaseItem = 362

    PortConcatenation = 363

    PortDeclaration = 364

    PortReference = 365

    PostdecrementExpression = 366

    PostincrementExpression = 367

    PowerExpression = 368

    PragmaDirective = 369

    PrimaryBlockEventExpression = 370

    PrimitiveInstantiation = 371

    ProceduralAssignStatement = 372

    ProceduralDeassignStatement = 373

    ProceduralForceStatement = 374

    ProceduralReleaseStatement = 375

    Production = 376

    ProgramDeclaration = 377

    ProgramHeader = 378

    PropertyDeclaration = 379

    PropertySpec = 380

    PropertyType = 381

    ProtectDirective = 382

    ProtectedDirective = 383

    PullStrength = 384

    PulseStyleDeclaration = 385

    QueueDimensionSpecifier = 386

    RandCaseItem = 387

    RandCaseStatement = 388

    RandJoinClause = 389

    RandSequenceStatement = 390

    RangeCoverageBinInitializer = 391

    RangeDimensionSpecifier = 392

    RangeList = 393

    RealLiteralExpression = 394

    RealTimeType = 395

    RealType = 396

    RegType = 397

    RepeatedEventControl = 398

    ReplicatedAssignmentPattern = 399

    ResetAllDirective = 400

    RestrictPropertyStatement = 401

    ReturnStatement = 402

    RootScope = 403

    RsCase = 404

    RsCodeBlock = 405

    RsElseClause = 406

    RsIfElse = 407

    RsProdItem = 408

    RsRepeat = 409

    RsRule = 410

    RsWeightClause = 411

    SUntilPropertyExpr = 412

    SUntilWithPropertyExpr = 413

    ScopedName = 414

    SequenceDeclaration = 415

    SequenceMatchList = 416

    SequenceRepetition = 417

    SequenceType = 418

    SequentialBlockStatement = 419

    ShortIntType = 420

    ShortRealType = 421

    SignalEventExpression = 422

    SignedCastExpression = 423

    SimpleAssignmentPattern = 424

    SimpleBinsSelectExpr = 425

    SimplePathSuffix = 426

    SimplePragmaExpression = 427

    SimplePropertyExpr = 428

    SimpleRangeSelect = 429

    SimpleSequenceExpr = 430

    SolveBeforeConstraint = 431

    SpecifyBlock = 432

    SpecparamDeclaration = 433

    SpecparamDeclarator = 434

    StandardCaseItem = 435

    StandardPropertyCaseItem = 436

    StandardRsCaseItem = 437

    StreamExpression = 438

    StreamExpressionWithRange = 439

    StreamingConcatenationExpression = 440

    StringLiteralExpression = 441

    StringType = 442

    StrongWeakPropertyExpr = 443

    StructType = 444

    StructUnionMember = 445

    StructurePattern = 446

    StructuredAssignmentPattern = 447

    SubtractAssignmentExpression = 448

    SubtractExpression = 449

    SuperHandle = 450

    SuperNewDefaultedArgsExpression = 451

    SystemName = 452

    SystemTimingCheck = 453

    TaggedPattern = 454

    TaggedUnionExpression = 455

    TaskDeclaration = 456

    ThisHandle = 457

    ThroughoutSequenceExpr = 458

    TimeLiteralExpression = 459

    TimeScaleDirective = 460

    TimeType = 461

    TimeUnitsDeclaration = 462

    TimingCheckEventArg = 463

    TimingCheckEventCondition = 464

    TimingControlExpression = 465

    TimingControlStatement = 466

    TransListCoverageBinInitializer = 467

    TransRange = 468

    TransRepeatRange = 469

    TransSet = 470

    TypeAssignment = 471

    TypeParameterDeclaration = 472

    TypeReference = 473

    TypedefDeclaration = 474

    UdpBody = 475

    UdpDeclaration = 476

    UdpEdgeField = 477

    UdpEntry = 478

    UdpInitialStmt = 479

    UdpInputPortDecl = 480

    UdpOutputPortDecl = 481

    UdpSimpleField = 482

    UnaryBinsSelectExpr = 483

    UnaryBitwiseAndExpression = 484

    UnaryBitwiseNandExpression = 485

    UnaryBitwiseNorExpression = 486

    UnaryBitwiseNotExpression = 487

    UnaryBitwiseOrExpression = 488

    UnaryBitwiseXnorExpression = 489

    UnaryBitwiseXorExpression = 490

    UnaryConditionalDirectiveExpression = 491

    UnaryLogicalNotExpression = 492

    UnaryMinusExpression = 493

    UnaryPlusExpression = 494

    UnaryPredecrementExpression = 495

    UnaryPreincrementExpression = 496

    UnaryPropertyExpr = 497

    UnarySelectPropertyExpr = 498

    UnbasedUnsizedLiteralExpression = 499

    UnconnectedDriveDirective = 500

    UndefDirective = 501

    UndefineAllDirective = 502

    UnionType = 503

    UniquenessConstraint = 504

    UnitScope = 505

    UntilPropertyExpr = 506

    UntilWithPropertyExpr = 507

    Untyped = 508

    UserDefinedNetDeclaration = 509

    ValueRangeExpression = 510

    VariableDimension = 511

    VariablePattern = 512

    VariablePortHeader = 513

    VirtualInterfaceType = 514

    VoidCastedCallStatement = 515

    VoidType = 516

    WaitForkStatement = 517

    WaitOrderStatement = 518

    WaitStatement = 519

    WildcardDimensionSpecifier = 520

    WildcardEqualityExpression = 521

    WildcardInequalityExpression = 522

    WildcardLiteralExpression = 523

    WildcardPattern = 524

    WildcardPortConnection = 525

    WildcardPortList = 526

    WildcardUdpPortList = 527

    WithClause = 528

    WithFunctionClause = 529

    WithFunctionSample = 530

    WithinSequenceExpr = 531

    XorAssignmentExpression = 532

class CSTJsonMode(enum.Enum):
    Full = 0

    NoWhitespace = 1

    SimpleTrivia = 2

    NoTrivia = 3

    SimpleTokens = 4

class SyntaxNode:
    @property
    def parent(self) -> SyntaxNode: ...

    @property
    def kind(self) -> SyntaxKind: ...

    def getFirstToken(self) -> pyslang.parsing.Token: ...

    def getLastToken(self) -> pyslang.parsing.Token: ...

    def isEquivalentTo(self, other: SyntaxNode) -> bool: ...

    def visit(self, f: object | None = None, lookup_table: object | None = None) -> None:
        """
        Visit a pyslang object with a callback function `f` or a `lookup_table` dict.

        At least one of `f` or `lookup_table` must be provided (both default to `None`). If both are provided, 'lookup_table' will be used to decide which callback to use.

        When `f` is provided without `lookup_table`, it is called for every node visited. The callback should take a single argument (the current node). Its return value controls traversal: `pyslang.VisitAction.Interrupt` aborts the visit, `pyslang.VisitAction.Skip` skips child nodes, and any other return value (including `pyslang.VisitAction.Advance` or `None`) continues normally.

        When `lookup_table` is provided, it should be a dict mapping node kind enum values to handler functions. The C++ side checks each node's kind before crossing the Python boundary, calling only the matching handler. Nodes not in the table are traversed without invoking Python. `f` is not called in this mode.

        The `lookup_table` is compiled into native lookups when the visit begins and must not be mutated during traversal.
        """

    @property
    def sourceRange(self) -> pyslang.SourceRange: ...

    def __getitem__(self, arg: int, /) -> object: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[object]: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    def to_json(self, mode: CSTJsonMode = CSTJsonMode.Full, sourceManager: pyslang.SourceManager | None = None) -> str:
        """
        Convert this syntax node to JSON string with optional formatting mode and source manager
        """

class IncludeMetadata:
    def __init__(self) -> None: ...

    @property
    def syntax(self) -> IncludeDirectiveSyntax: ...

    @property
    def path(self) -> str: ...

    @property
    def buffer(self) -> pyslang.SourceBuffer: ...

    @property
    def isSystem(self) -> bool: ...

class SyntaxTree:
    @property
    def isLibraryUnit(self) -> bool: ...

    @overload
    @staticmethod
    def fromFile(path: str) -> SyntaxTree: ...

    @overload
    @staticmethod
    def fromFile(path: str, sourceManager: pyslang.SourceManager, options: pyslang.Bag = ...) -> SyntaxTree: ...

    @overload
    @staticmethod
    def fromFiles(paths: span[str]) -> SyntaxTree: ...

    @overload
    @staticmethod
    def fromFiles(paths: span[str], sourceManager: pyslang.SourceManager, options: pyslang.Bag = ...) -> SyntaxTree: ...

    @overload
    @staticmethod
    def fromText(text: str, name: str = 'source', path: str = '') -> SyntaxTree: ...

    @overload
    @staticmethod
    def fromText(text: str, sourceManager: pyslang.SourceManager, name: str = 'source', path: str = '', options: pyslang.Bag = ..., library: pyslang.SourceLibrary | None = None) -> SyntaxTree: ...

    @staticmethod
    def fromFileInMemory(text: str, sourceManager: pyslang.SourceManager, name: str = 'source', path: str = '', options: pyslang.Bag = ...) -> SyntaxTree: ...

    @staticmethod
    def fromBuffer(buffer: pyslang.SourceBuffer, sourceManager: pyslang.SourceManager, options: pyslang.Bag = ..., inheritedMacros: span[DefineDirectiveSyntax] = []) -> SyntaxTree: ...

    @staticmethod
    def fromBuffers(buffers: span[pyslang.SourceBuffer], sourceManager: pyslang.SourceManager, options: pyslang.Bag = ..., inheritedMacros: span[DefineDirectiveSyntax] = []) -> SyntaxTree: ...

    @staticmethod
    def fromLibraryMapFile(path: str, sourceManager: pyslang.SourceManager, options: pyslang.Bag = ...) -> SyntaxTree: ...

    @staticmethod
    def fromLibraryMapText(text: str, sourceManager: pyslang.SourceManager, name: str = 'source', path: str = '', options: pyslang.Bag = ...) -> SyntaxTree: ...

    @staticmethod
    def fromLibraryMapBuffer(buffer: pyslang.SourceBuffer, sourceManager: pyslang.SourceManager, options: pyslang.Bag = ...) -> SyntaxTree: ...

    @property
    def diagnostics(self) -> pyslang.Diagnostics: ...

    @property
    def sourceManager(self) -> pyslang.SourceManager: ...

    @property
    def root(self) -> SyntaxNode: ...

    @property
    def options(self) -> pyslang.Bag: ...

    @property
    def sourceLibrary(self) -> pyslang.SourceLibrary: ...

    def getIncludeDirectives(self) -> span[IncludeMetadata]: ...

    @staticmethod
    def getDefaultSourceManager() -> pyslang.SourceManager: ...

    def validate(self) -> bool: ...

    def to_json(self, mode: CSTJsonMode = CSTJsonMode.Full) -> str:
        """Convert this syntax tree to JSON string with optional formatting mode"""

class CommentHandler:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, kind: CommentHandler.Kind, endRegion: str) -> None: ...

    @property
    def kind(self) -> CommentHandler.Kind: ...

    @kind.setter
    def kind(self, arg: CommentHandler.Kind, /) -> None: ...

    @property
    def endRegion(self) -> str: ...

    @endRegion.setter
    def endRegion(self, arg: str, /) -> None: ...

    class Kind(enum.Enum):
        Protect = 0

        TranslateOff = 1

        LintOn = 2

        LintOff = 3

        LintSave = 4

        LintRestore = 5

    Protect: CommentHandler.Kind = CommentHandler.Kind.Protect

    TranslateOff: CommentHandler.Kind = CommentHandler.Kind.TranslateOff

    LintOn: CommentHandler.Kind = CommentHandler.Kind.LintOn

    LintOff: CommentHandler.Kind = CommentHandler.Kind.LintOff

    LintSave: CommentHandler.Kind = CommentHandler.Kind.LintSave

    LintRestore: CommentHandler.Kind = CommentHandler.Kind.LintRestore

class SyntaxPrinter:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, sourceManager: pyslang.SourceManager) -> None: ...

    def append(self, text: str) -> SyntaxPrinter: ...

    @overload
    def print(self, trivia: pyslang.parsing.Trivia) -> SyntaxPrinter: ...

    @overload
    def print(self, token: pyslang.parsing.Token) -> SyntaxPrinter: ...

    @overload
    def print(self, node: SyntaxNode) -> SyntaxPrinter: ...

    @overload
    def print(self, tree: SyntaxTree) -> SyntaxPrinter: ...

    def setIncludeTrivia(self, include: bool) -> SyntaxPrinter: ...

    def setIncludeMissing(self, include: bool) -> SyntaxPrinter: ...

    def setIncludeSkipped(self, include: bool) -> SyntaxPrinter: ...

    def setIncludeDirectives(self, include: bool) -> SyntaxPrinter: ...

    def setExpandMacros(self, expand: bool) -> SyntaxPrinter: ...

    def setExpandIncludes(self, expand: bool) -> SyntaxPrinter: ...

    def setIncludeComments(self, include: bool) -> SyntaxPrinter: ...

    def setSquashNewlines(self, include: bool) -> SyntaxPrinter: ...

    def str(self) -> str: ...

    @staticmethod
    def printFile(tree: SyntaxTree) -> str: ...

class SyntaxRewriter:
    def remove(self, arg: SyntaxNode, /) -> None: ...

    def replace(self, oldNode: SyntaxNode, newNode: SyntaxNode, preserveTrivia: bool = False) -> None: ...

    def insertBefore(self, arg0: SyntaxNode, arg1: SyntaxNode, /) -> None: ...

    def insertAfter(self, arg0: SyntaxNode, arg1: SyntaxNode, /) -> None: ...

    @overload
    def insertAtFront(self, list: SyntaxList, newNode: SyntaxNode, separator: pyslang.parsing.Token = ...) -> None: ...

    @overload
    def insertAtFront(self, list: SeparatedSyntaxList, newNode: SyntaxNode, separator: pyslang.parsing.Token = ...) -> None: ...

    @overload
    def insertAtBack(self, list: SyntaxList, newNode: SyntaxNode, separator: pyslang.parsing.Token = ...) -> None: ...

    @overload
    def insertAtBack(self, list: SeparatedSyntaxList, newNode: SyntaxNode, separator: pyslang.parsing.Token = ...) -> None: ...

    @property
    def factory(self) -> SyntaxFactory:
        """Get the SyntaxFactory for creating new syntax nodes"""

    @property
    def alloc(self) -> pyslang.BumpAllocator:
        """Get the allocator for creating tokens and trivia"""

    @overload
    def makeToken(self, kind: pyslang.parsing.TokenKind, text: str, trivia: span[pyslang.parsing.Trivia] = []) -> pyslang.parsing.Token:
        """Create a new token with the given kind and text"""

    @overload
    def makeToken(self, kind: pyslang.parsing.TokenKind, trivia: span[pyslang.parsing.Trivia] = []) -> pyslang.parsing.Token:
        """Create a token with text inferred from kind (for keywords/punctuation)"""

    def makeId(self, text: str, trivia: span[pyslang.parsing.Trivia] = []) -> pyslang.parsing.Token:
        """Create an identifier token"""

    def makeComma(self) -> pyslang.parsing.Token:
        """Create a comma token"""

    def makeTrivia(self, kind: pyslang.parsing.TriviaKind, text: str) -> pyslang.parsing.Trivia:
        """Create a trivia with text allocated in the rewriter's allocator"""

    def clone(self, node: SyntaxNode) -> SyntaxNode:
        """Create a shallow clone of the given syntax node"""

    def deepClone(self, node: SyntaxNode) -> SyntaxNode:
        """Create a deep clone of the given syntax node and all its children"""

    def makeList(self, items: list) -> SyntaxList:
        """Create a SyntaxList from a list of syntax nodes"""

    def makeSeparatedList(self, items: list) -> SeparatedSyntaxList:
        """
        Create a SeparatedSyntaxList from a list of syntax nodes and separator tokens
        """

    def makeTokenList(self, items: list) -> TokenList:
        """Create a TokenList from a list of tokens"""

def rewrite(tree: SyntaxTree, handler: object) -> SyntaxTree: ...

def clone(node: SyntaxNode, alloc: pyslang.BumpAllocator) -> SyntaxNode:
    """Create a shallow clone of the given syntax node"""

def deepClone(node: SyntaxNode, alloc: pyslang.BumpAllocator) -> SyntaxNode:
    """Create a deep clone of the given syntax node and all its children"""

class ExpressionSyntax(SyntaxNode):
    pass

class DataTypeSyntax(ExpressionSyntax):
    pass

class TimingControlSyntax(SyntaxNode):
    pass

class SequenceExprSyntax(SyntaxNode):
    pass

class PropertyExprSyntax(SyntaxNode):
    pass

class EqualsValueClauseSyntax(SyntaxNode):
    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class AttributeSpecSyntax(SyntaxNode):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def value(self) -> EqualsValueClauseSyntax: ...

    @value.setter
    def value(self, arg: EqualsValueClauseSyntax, /) -> None: ...

class AttributeInstanceSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openStar(self) -> pyslang.parsing.Token: ...

    @openStar.setter
    def openStar(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def specs(self) -> SeparatedSyntaxList: ...

    @specs.setter
    def specs(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeStar(self) -> pyslang.parsing.Token: ...

    @closeStar.setter
    def closeStar(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class NamedLabelSyntax(SyntaxNode):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

class StatementSyntax(SyntaxNode):
    @property
    def label(self) -> NamedLabelSyntax: ...

    @label.setter
    def label(self, arg: NamedLabelSyntax, /) -> None: ...

    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

class MemberSyntax(SyntaxNode):
    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

class ArgumentSyntax(SyntaxNode):
    pass

class EmptyArgumentSyntax(ArgumentSyntax):
    @property
    def placeholder(self) -> pyslang.parsing.Token: ...

    @placeholder.setter
    def placeholder(self, arg: pyslang.parsing.Token, /) -> None: ...

class OrderedArgumentSyntax(ArgumentSyntax):
    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class NamedArgumentSyntax(ArgumentSyntax):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ArgumentListSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def parameters(self) -> SeparatedSyntaxList: ...

    @parameters.setter
    def parameters(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ParamAssignmentSyntax(SyntaxNode):
    pass

class OrderedParamAssignmentSyntax(ParamAssignmentSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class NamedParamAssignmentSyntax(ParamAssignmentSyntax):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ParameterValueAssignmentSyntax(SyntaxNode):
    @property
    def hash(self) -> pyslang.parsing.Token: ...

    @hash.setter
    def hash(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def parameters(self) -> SeparatedSyntaxList: ...

    @parameters.setter
    def parameters(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class PatternSyntax(SyntaxNode):
    pass

class ParenthesizedPatternSyntax(PatternSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def pattern(self) -> PatternSyntax: ...

    @pattern.setter
    def pattern(self, arg: PatternSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class VariablePatternSyntax(PatternSyntax):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def variableName(self) -> pyslang.parsing.Token: ...

    @variableName.setter
    def variableName(self, arg: pyslang.parsing.Token, /) -> None: ...

class WildcardPatternSyntax(PatternSyntax):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def star(self) -> pyslang.parsing.Token: ...

    @star.setter
    def star(self, arg: pyslang.parsing.Token, /) -> None: ...

class ExpressionPatternSyntax(PatternSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class TaggedPatternSyntax(PatternSyntax):
    @property
    def tagged(self) -> pyslang.parsing.Token: ...

    @tagged.setter
    def tagged(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def memberName(self) -> pyslang.parsing.Token: ...

    @memberName.setter
    def memberName(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def pattern(self) -> PatternSyntax: ...

    @pattern.setter
    def pattern(self, arg: PatternSyntax, /) -> None: ...

class StructurePatternMemberSyntax(SyntaxNode):
    pass

class OrderedStructurePatternMemberSyntax(StructurePatternMemberSyntax):
    @property
    def pattern(self) -> PatternSyntax: ...

    @pattern.setter
    def pattern(self, arg: PatternSyntax, /) -> None: ...

class NamedStructurePatternMemberSyntax(StructurePatternMemberSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def pattern(self) -> PatternSyntax: ...

    @pattern.setter
    def pattern(self, arg: PatternSyntax, /) -> None: ...

class StructurePatternSyntax(PatternSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SeparatedSyntaxList: ...

    @members.setter
    def members(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class MatchesClauseSyntax(SyntaxNode):
    @property
    def matchesKeyword(self) -> pyslang.parsing.Token: ...

    @matchesKeyword.setter
    def matchesKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def pattern(self) -> PatternSyntax: ...

    @pattern.setter
    def pattern(self, arg: PatternSyntax, /) -> None: ...

class ConditionalPatternSyntax(SyntaxNode):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def matchesClause(self) -> MatchesClauseSyntax: ...

    @matchesClause.setter
    def matchesClause(self, arg: MatchesClauseSyntax, /) -> None: ...

class ConditionalPredicateSyntax(SyntaxNode):
    @property
    def conditions(self) -> SeparatedSyntaxList: ...

    @conditions.setter
    def conditions(self, arg: SeparatedSyntaxList, /) -> None: ...

class AssignmentPatternSyntax(SyntaxNode):
    pass

class SimpleAssignmentPatternSyntax(AssignmentPatternSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class AssignmentPatternItemSyntax(SyntaxNode):
    @property
    def key(self) -> ExpressionSyntax: ...

    @key.setter
    def key(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class StructuredAssignmentPatternSyntax(AssignmentPatternSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class ReplicatedAssignmentPatternSyntax(AssignmentPatternSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def countExpr(self) -> ExpressionSyntax: ...

    @countExpr.setter
    def countExpr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def innerOpenBrace(self) -> pyslang.parsing.Token: ...

    @innerOpenBrace.setter
    def innerOpenBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def innerCloseBrace(self) -> pyslang.parsing.Token: ...

    @innerCloseBrace.setter
    def innerCloseBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class BadExpressionSyntax(ExpressionSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class PrimaryExpressionSyntax(ExpressionSyntax):
    pass

class PrefixUnaryExpressionSyntax(ExpressionSyntax):
    @property
    def operatorToken(self) -> pyslang.parsing.Token: ...

    @operatorToken.setter
    def operatorToken(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def operand(self) -> ExpressionSyntax: ...

    @operand.setter
    def operand(self, arg: ExpressionSyntax, /) -> None: ...

class PostfixUnaryExpressionSyntax(ExpressionSyntax):
    @property
    def operand(self) -> ExpressionSyntax: ...

    @operand.setter
    def operand(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def operatorToken(self) -> pyslang.parsing.Token: ...

    @operatorToken.setter
    def operatorToken(self, arg: pyslang.parsing.Token, /) -> None: ...

class BinaryExpressionSyntax(ExpressionSyntax):
    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def operatorToken(self) -> pyslang.parsing.Token: ...

    @operatorToken.setter
    def operatorToken(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def right(self) -> ExpressionSyntax: ...

    @right.setter
    def right(self, arg: ExpressionSyntax, /) -> None: ...

class MinTypMaxExpressionSyntax(ExpressionSyntax):
    @property
    def min(self) -> ExpressionSyntax: ...

    @min.setter
    def min(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def colon1(self) -> pyslang.parsing.Token: ...

    @colon1.setter
    def colon1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def typ(self) -> ExpressionSyntax: ...

    @typ.setter
    def typ(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def colon2(self) -> pyslang.parsing.Token: ...

    @colon2.setter
    def colon2(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def max(self) -> ExpressionSyntax: ...

    @max.setter
    def max(self, arg: ExpressionSyntax, /) -> None: ...

class TaggedUnionExpressionSyntax(ExpressionSyntax):
    @property
    def tagged(self) -> pyslang.parsing.Token: ...

    @tagged.setter
    def tagged(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def member(self) -> pyslang.parsing.Token: ...

    @member.setter
    def member(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class ValueRangeExpressionSyntax(ExpressionSyntax):
    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> ExpressionSyntax: ...

    @right.setter
    def right(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

class RangeListSyntax(SyntaxNode):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def valueRanges(self) -> SeparatedSyntaxList: ...

    @valueRanges.setter
    def valueRanges(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class InsideExpressionSyntax(ExpressionSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def inside(self) -> pyslang.parsing.Token: ...

    @inside.setter
    def inside(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ranges(self) -> RangeListSyntax: ...

    @ranges.setter
    def ranges(self, arg: RangeListSyntax, /) -> None: ...

class ConditionalExpressionSyntax(ExpressionSyntax):
    @property
    def predicate(self) -> ConditionalPredicateSyntax: ...

    @predicate.setter
    def predicate(self, arg: ConditionalPredicateSyntax, /) -> None: ...

    @property
    def question(self) -> pyslang.parsing.Token: ...

    @question.setter
    def question(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> ExpressionSyntax: ...

    @right.setter
    def right(self, arg: ExpressionSyntax, /) -> None: ...

class AssignmentPatternExpressionSyntax(PrimaryExpressionSyntax):
    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def pattern(self) -> AssignmentPatternSyntax: ...

    @pattern.setter
    def pattern(self, arg: AssignmentPatternSyntax, /) -> None: ...

class SelectorSyntax(SyntaxNode):
    pass

class BitSelectSyntax(SelectorSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class RangeSelectSyntax(SelectorSyntax):
    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def range(self) -> pyslang.parsing.Token: ...

    @range.setter
    def range(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> ExpressionSyntax: ...

    @right.setter
    def right(self, arg: ExpressionSyntax, /) -> None: ...

class ElementSelectSyntax(SyntaxNode):
    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def selector(self) -> SelectorSyntax: ...

    @selector.setter
    def selector(self, arg: SelectorSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

class NameSyntax(ExpressionSyntax):
    pass

class IdentifierNameSyntax(NameSyntax):
    @property
    def identifier(self) -> pyslang.parsing.Token: ...

    @identifier.setter
    def identifier(self, arg: pyslang.parsing.Token, /) -> None: ...

class SystemNameSyntax(NameSyntax):
    @property
    def systemIdentifier(self) -> pyslang.parsing.Token: ...

    @systemIdentifier.setter
    def systemIdentifier(self, arg: pyslang.parsing.Token, /) -> None: ...

class IdentifierSelectNameSyntax(NameSyntax):
    @property
    def identifier(self) -> pyslang.parsing.Token: ...

    @identifier.setter
    def identifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def selectors(self) -> SyntaxList: ...

    @selectors.setter
    def selectors(self, arg: SyntaxList, /) -> None: ...

class EmptyIdentifierNameSyntax(NameSyntax):
    @property
    def placeholder(self) -> pyslang.parsing.Token: ...

    @placeholder.setter
    def placeholder(self, arg: pyslang.parsing.Token, /) -> None: ...

class KeywordNameSyntax(NameSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

class ClassNameSyntax(NameSyntax):
    @property
    def identifier(self) -> pyslang.parsing.Token: ...

    @identifier.setter
    def identifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def parameters(self) -> ParameterValueAssignmentSyntax: ...

    @parameters.setter
    def parameters(self, arg: ParameterValueAssignmentSyntax, /) -> None: ...

class ScopedNameSyntax(NameSyntax):
    @property
    def left(self) -> NameSyntax: ...

    @left.setter
    def left(self, arg: NameSyntax, /) -> None: ...

    @property
    def separator(self) -> pyslang.parsing.Token: ...

    @separator.setter
    def separator(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> NameSyntax: ...

    @right.setter
    def right(self, arg: NameSyntax, /) -> None: ...

class LiteralExpressionSyntax(PrimaryExpressionSyntax):
    @property
    def literal(self) -> pyslang.parsing.Token: ...

    @literal.setter
    def literal(self, arg: pyslang.parsing.Token, /) -> None: ...

class IntegerVectorExpressionSyntax(PrimaryExpressionSyntax):
    @property
    def size(self) -> pyslang.parsing.Token: ...

    @size.setter
    def size(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def base(self) -> pyslang.parsing.Token: ...

    @base.setter
    def base(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def value(self) -> pyslang.parsing.Token: ...

    @value.setter
    def value(self, arg: pyslang.parsing.Token, /) -> None: ...

class EmptyQueueExpressionSyntax(PrimaryExpressionSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConcatenationExpressionSyntax(PrimaryExpressionSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expressions(self) -> SeparatedSyntaxList: ...

    @expressions.setter
    def expressions(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class MultipleConcatenationExpressionSyntax(PrimaryExpressionSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expression(self) -> ExpressionSyntax: ...

    @expression.setter
    def expression(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def concatenation(self) -> ConcatenationExpressionSyntax: ...

    @concatenation.setter
    def concatenation(self, arg: ConcatenationExpressionSyntax, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class StreamExpressionWithRangeSyntax(SyntaxNode):
    @property
    def withKeyword(self) -> pyslang.parsing.Token: ...

    @withKeyword.setter
    def withKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def range(self) -> ElementSelectSyntax: ...

    @range.setter
    def range(self, arg: ElementSelectSyntax, /) -> None: ...

class StreamExpressionSyntax(SyntaxNode):
    @property
    def expression(self) -> ExpressionSyntax: ...

    @expression.setter
    def expression(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def withRange(self) -> StreamExpressionWithRangeSyntax: ...

    @withRange.setter
    def withRange(self, arg: StreamExpressionWithRangeSyntax, /) -> None: ...

class StreamingConcatenationExpressionSyntax(PrimaryExpressionSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def operatorToken(self) -> pyslang.parsing.Token: ...

    @operatorToken.setter
    def operatorToken(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def sliceSize(self) -> ExpressionSyntax: ...

    @sliceSize.setter
    def sliceSize(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def innerOpenBrace(self) -> pyslang.parsing.Token: ...

    @innerOpenBrace.setter
    def innerOpenBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expressions(self) -> SeparatedSyntaxList: ...

    @expressions.setter
    def expressions(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def innerCloseBrace(self) -> pyslang.parsing.Token: ...

    @innerCloseBrace.setter
    def innerCloseBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class ParenthesizedExpressionSyntax(PrimaryExpressionSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expression(self) -> ExpressionSyntax: ...

    @expression.setter
    def expression(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class NewArrayExpressionSyntax(ExpressionSyntax):
    @property
    def newKeyword(self) -> NameSyntax: ...

    @newKeyword.setter
    def newKeyword(self, arg: NameSyntax, /) -> None: ...

    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def sizeExpr(self) -> ExpressionSyntax: ...

    @sizeExpr.setter
    def sizeExpr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def initializer(self) -> ParenthesizedExpressionSyntax: ...

    @initializer.setter
    def initializer(self, arg: ParenthesizedExpressionSyntax, /) -> None: ...

class NewClassExpressionSyntax(ExpressionSyntax):
    @property
    def scopedNew(self) -> NameSyntax: ...

    @scopedNew.setter
    def scopedNew(self, arg: NameSyntax, /) -> None: ...

    @property
    def argList(self) -> ArgumentListSyntax: ...

    @argList.setter
    def argList(self, arg: ArgumentListSyntax, /) -> None: ...

class CopyClassExpressionSyntax(ExpressionSyntax):
    @property
    def scopedNew(self) -> NameSyntax: ...

    @scopedNew.setter
    def scopedNew(self, arg: NameSyntax, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class SuperNewDefaultedArgsExpressionSyntax(ExpressionSyntax):
    @property
    def scopedNew(self) -> NameSyntax: ...

    @scopedNew.setter
    def scopedNew(self, arg: NameSyntax, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ElementSelectExpressionSyntax(ExpressionSyntax):
    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def select(self) -> ElementSelectSyntax: ...

    @select.setter
    def select(self, arg: ElementSelectSyntax, /) -> None: ...

class MemberAccessExpressionSyntax(ExpressionSyntax):
    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

class InvocationExpressionSyntax(ExpressionSyntax):
    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def arguments(self) -> ArgumentListSyntax: ...

    @arguments.setter
    def arguments(self, arg: ArgumentListSyntax, /) -> None: ...

class CastExpressionSyntax(ExpressionSyntax):
    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def apostrophe(self) -> pyslang.parsing.Token: ...

    @apostrophe.setter
    def apostrophe(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> ParenthesizedExpressionSyntax: ...

    @right.setter
    def right(self, arg: ParenthesizedExpressionSyntax, /) -> None: ...

class SignedCastExpressionSyntax(ExpressionSyntax):
    @property
    def signing(self) -> pyslang.parsing.Token: ...

    @signing.setter
    def signing(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def apostrophe(self) -> pyslang.parsing.Token: ...

    @apostrophe.setter
    def apostrophe(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def inner(self) -> ParenthesizedExpressionSyntax: ...

    @inner.setter
    def inner(self, arg: ParenthesizedExpressionSyntax, /) -> None: ...

class DelaySyntax(TimingControlSyntax):
    @property
    def hash(self) -> pyslang.parsing.Token: ...

    @hash.setter
    def hash(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delayValue(self) -> ExpressionSyntax: ...

    @delayValue.setter
    def delayValue(self, arg: ExpressionSyntax, /) -> None: ...

class Delay3Syntax(TimingControlSyntax):
    @property
    def hash(self) -> pyslang.parsing.Token: ...

    @hash.setter
    def hash(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delay1(self) -> ExpressionSyntax: ...

    @delay1.setter
    def delay1(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def comma1(self) -> pyslang.parsing.Token: ...

    @comma1.setter
    def comma1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delay2(self) -> ExpressionSyntax: ...

    @delay2.setter
    def delay2(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def comma2(self) -> pyslang.parsing.Token: ...

    @comma2.setter
    def comma2(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delay3(self) -> ExpressionSyntax: ...

    @delay3.setter
    def delay3(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class OneStepDelaySyntax(TimingControlSyntax):
    @property
    def hash(self) -> pyslang.parsing.Token: ...

    @hash.setter
    def hash(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def oneStep(self) -> pyslang.parsing.Token: ...

    @oneStep.setter
    def oneStep(self, arg: pyslang.parsing.Token, /) -> None: ...

class EventControlSyntax(TimingControlSyntax):
    @property
    def at(self) -> pyslang.parsing.Token: ...

    @at.setter
    def at(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def eventName(self) -> ExpressionSyntax: ...

    @eventName.setter
    def eventName(self, arg: ExpressionSyntax, /) -> None: ...

class IffEventClauseSyntax(SyntaxNode):
    @property
    def iff(self) -> pyslang.parsing.Token: ...

    @iff.setter
    def iff(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class EventExpressionSyntax(SequenceExprSyntax):
    pass

class SignalEventExpressionSyntax(EventExpressionSyntax):
    @property
    def edge(self) -> pyslang.parsing.Token: ...

    @edge.setter
    def edge(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def iffClause(self) -> IffEventClauseSyntax: ...

    @iffClause.setter
    def iffClause(self, arg: IffEventClauseSyntax, /) -> None: ...

class BinaryEventExpressionSyntax(EventExpressionSyntax):
    @property
    def left(self) -> EventExpressionSyntax: ...

    @left.setter
    def left(self, arg: EventExpressionSyntax, /) -> None: ...

    @property
    def operatorToken(self) -> pyslang.parsing.Token: ...

    @operatorToken.setter
    def operatorToken(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> EventExpressionSyntax: ...

    @right.setter
    def right(self, arg: EventExpressionSyntax, /) -> None: ...

class ParenthesizedEventExpressionSyntax(EventExpressionSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> EventExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: EventExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ImplicitEventControlSyntax(TimingControlSyntax):
    @property
    def at(self) -> pyslang.parsing.Token: ...

    @at.setter
    def at(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def star(self) -> pyslang.parsing.Token: ...

    @star.setter
    def star(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class EventControlWithExpressionSyntax(TimingControlSyntax):
    @property
    def at(self) -> pyslang.parsing.Token: ...

    @at.setter
    def at(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> EventExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: EventExpressionSyntax, /) -> None: ...

class RepeatedEventControlSyntax(TimingControlSyntax):
    @property
    def repeat(self) -> pyslang.parsing.Token: ...

    @repeat.setter
    def repeat(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def eventControl(self) -> TimingControlSyntax: ...

    @eventControl.setter
    def eventControl(self, arg: TimingControlSyntax, /) -> None: ...

class TimingControlExpressionSyntax(ExpressionSyntax):
    @property
    def timing(self) -> TimingControlSyntax: ...

    @timing.setter
    def timing(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class DimensionSpecifierSyntax(SyntaxNode):
    pass

class RangeDimensionSpecifierSyntax(DimensionSpecifierSyntax):
    @property
    def selector(self) -> SelectorSyntax: ...

    @selector.setter
    def selector(self, arg: SelectorSyntax, /) -> None: ...

class WildcardDimensionSpecifierSyntax(DimensionSpecifierSyntax):
    @property
    def star(self) -> pyslang.parsing.Token: ...

    @star.setter
    def star(self, arg: pyslang.parsing.Token, /) -> None: ...

class ColonExpressionClauseSyntax(SyntaxNode):
    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class QueueDimensionSpecifierSyntax(DimensionSpecifierSyntax):
    @property
    def dollar(self) -> pyslang.parsing.Token: ...

    @dollar.setter
    def dollar(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def maxSizeClause(self) -> ColonExpressionClauseSyntax: ...

    @maxSizeClause.setter
    def maxSizeClause(self, arg: ColonExpressionClauseSyntax, /) -> None: ...

class VariableDimensionSyntax(SyntaxNode):
    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def specifier(self) -> DimensionSpecifierSyntax: ...

    @specifier.setter
    def specifier(self, arg: DimensionSpecifierSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

class DeclaratorSyntax(SyntaxNode):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dimensions(self) -> SyntaxList: ...

    @dimensions.setter
    def dimensions(self, arg: SyntaxList, /) -> None: ...

    @property
    def initializer(self) -> EqualsValueClauseSyntax: ...

    @initializer.setter
    def initializer(self, arg: EqualsValueClauseSyntax, /) -> None: ...

class DataDeclarationSyntax(MemberSyntax):
    @property
    def modifiers(self) -> TokenList: ...

    @modifiers.setter
    def modifiers(self, arg: TokenList, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ForwardTypeRestrictionSyntax(SyntaxNode):
    @property
    def keyword1(self) -> pyslang.parsing.Token: ...

    @keyword1.setter
    def keyword1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def keyword2(self) -> pyslang.parsing.Token: ...

    @keyword2.setter
    def keyword2(self, arg: pyslang.parsing.Token, /) -> None: ...

class TypedefDeclarationSyntax(MemberSyntax):
    @property
    def typedefKeyword(self) -> pyslang.parsing.Token: ...

    @typedefKeyword.setter
    def typedefKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dimensions(self) -> SyntaxList: ...

    @dimensions.setter
    def dimensions(self, arg: SyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ForwardTypedefDeclarationSyntax(MemberSyntax):
    @property
    def typedefKeyword(self) -> pyslang.parsing.Token: ...

    @typedefKeyword.setter
    def typedefKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def typeRestriction(self) -> ForwardTypeRestrictionSyntax: ...

    @typeRestriction.setter
    def typeRestriction(self, arg: ForwardTypeRestrictionSyntax, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class NetStrengthSyntax(SyntaxNode):
    pass

class ChargeStrengthSyntax(NetStrengthSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def strength(self) -> pyslang.parsing.Token: ...

    @strength.setter
    def strength(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class DriveStrengthSyntax(NetStrengthSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def strength0(self) -> pyslang.parsing.Token: ...

    @strength0.setter
    def strength0(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def comma(self) -> pyslang.parsing.Token: ...

    @comma.setter
    def comma(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def strength1(self) -> pyslang.parsing.Token: ...

    @strength1.setter
    def strength1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class PullStrengthSyntax(NetStrengthSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def strength(self) -> pyslang.parsing.Token: ...

    @strength.setter
    def strength(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class NetDeclarationSyntax(MemberSyntax):
    @property
    def netType(self) -> pyslang.parsing.Token: ...

    @netType.setter
    def netType(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def strength(self) -> NetStrengthSyntax: ...

    @strength.setter
    def strength(self, arg: NetStrengthSyntax, /) -> None: ...

    @property
    def expansionHint(self) -> pyslang.parsing.Token: ...

    @expansionHint.setter
    def expansionHint(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def delay(self) -> TimingControlSyntax: ...

    @delay.setter
    def delay(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class UserDefinedNetDeclarationSyntax(MemberSyntax):
    @property
    def netType(self) -> pyslang.parsing.Token: ...

    @netType.setter
    def netType(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delay(self) -> TimingControlSyntax: ...

    @delay.setter
    def delay(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class WithFunctionClauseSyntax(SyntaxNode):
    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

class NetTypeDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def withFunction(self) -> WithFunctionClauseSyntax: ...

    @withFunction.setter
    def withFunction(self, arg: WithFunctionClauseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PackageImportItemSyntax(SyntaxNode):
    @property
    def package(self) -> pyslang.parsing.Token: ...

    @package.setter
    def package(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def doubleColon(self) -> pyslang.parsing.Token: ...

    @doubleColon.setter
    def doubleColon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def item(self) -> pyslang.parsing.Token: ...

    @item.setter
    def item(self, arg: pyslang.parsing.Token, /) -> None: ...

class PackageImportDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PackageExportDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PackageExportAllDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def star1(self) -> pyslang.parsing.Token: ...

    @star1.setter
    def star1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def doubleColon(self) -> pyslang.parsing.Token: ...

    @doubleColon.setter
    def doubleColon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def star2(self) -> pyslang.parsing.Token: ...

    @star2.setter
    def star2(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ParameterDeclarationBaseSyntax(SyntaxNode):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

class ParameterDeclarationSyntax(ParameterDeclarationBaseSyntax):
    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

class EqualsTypeClauseSyntax(SyntaxNode):
    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

class TypeAssignmentSyntax(SyntaxNode):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def assignment(self) -> EqualsTypeClauseSyntax: ...

    @assignment.setter
    def assignment(self, arg: EqualsTypeClauseSyntax, /) -> None: ...

class TypeParameterDeclarationSyntax(ParameterDeclarationBaseSyntax):
    @property
    def typeKeyword(self) -> pyslang.parsing.Token: ...

    @typeKeyword.setter
    def typeKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def typeRestriction(self) -> ForwardTypeRestrictionSyntax: ...

    @typeRestriction.setter
    def typeRestriction(self, arg: ForwardTypeRestrictionSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

class ParameterDeclarationStatementSyntax(MemberSyntax):
    @property
    def parameter(self) -> ParameterDeclarationBaseSyntax: ...

    @parameter.setter
    def parameter(self, arg: ParameterDeclarationBaseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PortHeaderSyntax(SyntaxNode):
    pass

class PortDeclarationSyntax(MemberSyntax):
    @property
    def header(self) -> PortHeaderSyntax: ...

    @header.setter
    def header(self, arg: PortHeaderSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class GenvarDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def identifiers(self) -> SeparatedSyntaxList: ...

    @identifiers.setter
    def identifiers(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class FunctionPortBaseSyntax(SyntaxNode):
    pass

class DefaultFunctionPortSyntax(FunctionPortBaseSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

class FunctionPortSyntax(FunctionPortBaseSyntax):
    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def constKeyword(self) -> pyslang.parsing.Token: ...

    @constKeyword.setter
    def constKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def direction(self) -> pyslang.parsing.Token: ...

    @direction.setter
    def direction(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def staticKeyword(self) -> pyslang.parsing.Token: ...

    @staticKeyword.setter
    def staticKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def varKeyword(self) -> pyslang.parsing.Token: ...

    @varKeyword.setter
    def varKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dataType(self) -> DataTypeSyntax: ...

    @dataType.setter
    def dataType(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def declarator(self) -> DeclaratorSyntax: ...

    @declarator.setter
    def declarator(self, arg: DeclaratorSyntax, /) -> None: ...

class FunctionPortListSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> SeparatedSyntaxList: ...

    @ports.setter
    def ports(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class IntegerTypeSyntax(DataTypeSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def signing(self) -> pyslang.parsing.Token: ...

    @signing.setter
    def signing(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dimensions(self) -> SyntaxList: ...

    @dimensions.setter
    def dimensions(self, arg: SyntaxList, /) -> None: ...

class KeywordTypeSyntax(DataTypeSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

class NamedTypeSyntax(DataTypeSyntax):
    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

class StructUnionMemberSyntax(SyntaxNode):
    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def randomQualifier(self) -> pyslang.parsing.Token: ...

    @randomQualifier.setter
    def randomQualifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class StructUnionTypeSyntax(DataTypeSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def taggedOrSoft(self) -> pyslang.parsing.Token: ...

    @taggedOrSoft.setter
    def taggedOrSoft(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def packed(self) -> pyslang.parsing.Token: ...

    @packed.setter
    def packed(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def signing(self) -> pyslang.parsing.Token: ...

    @signing.setter
    def signing(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dimensions(self) -> SyntaxList: ...

    @dimensions.setter
    def dimensions(self, arg: SyntaxList, /) -> None: ...

class EnumTypeSyntax(DataTypeSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def baseType(self) -> DataTypeSyntax: ...

    @baseType.setter
    def baseType(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SeparatedSyntaxList: ...

    @members.setter
    def members(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dimensions(self) -> SyntaxList: ...

    @dimensions.setter
    def dimensions(self, arg: SyntaxList, /) -> None: ...

class TypeReferenceSyntax(DataTypeSyntax):
    @property
    def typeKeyword(self) -> pyslang.parsing.Token: ...

    @typeKeyword.setter
    def typeKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class DotMemberClauseSyntax(SyntaxNode):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def member(self) -> pyslang.parsing.Token: ...

    @member.setter
    def member(self, arg: pyslang.parsing.Token, /) -> None: ...

class VirtualInterfaceTypeSyntax(DataTypeSyntax):
    @property
    def virtualKeyword(self) -> pyslang.parsing.Token: ...

    @virtualKeyword.setter
    def virtualKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def interfaceKeyword(self) -> pyslang.parsing.Token: ...

    @interfaceKeyword.setter
    def interfaceKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def parameters(self) -> ParameterValueAssignmentSyntax: ...

    @parameters.setter
    def parameters(self, arg: ParameterValueAssignmentSyntax, /) -> None: ...

    @property
    def modport(self) -> DotMemberClauseSyntax: ...

    @modport.setter
    def modport(self, arg: DotMemberClauseSyntax, /) -> None: ...

class ImplicitTypeSyntax(DataTypeSyntax):
    @property
    def signing(self) -> pyslang.parsing.Token: ...

    @signing.setter
    def signing(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dimensions(self) -> SyntaxList: ...

    @dimensions.setter
    def dimensions(self, arg: SyntaxList, /) -> None: ...

    @property
    def placeholder(self) -> pyslang.parsing.Token: ...

    @placeholder.setter
    def placeholder(self, arg: pyslang.parsing.Token, /) -> None: ...

class DeferredAssertionSyntax(SyntaxNode):
    @property
    def hash(self) -> pyslang.parsing.Token: ...

    @hash.setter
    def hash(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def zero(self) -> pyslang.parsing.Token: ...

    @zero.setter
    def zero(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def finalKeyword(self) -> pyslang.parsing.Token: ...

    @finalKeyword.setter
    def finalKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

class ElseClauseSyntax(SyntaxNode):
    @property
    def elseKeyword(self) -> pyslang.parsing.Token: ...

    @elseKeyword.setter
    def elseKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def clause(self) -> SyntaxNode: ...

    @clause.setter
    def clause(self, arg: SyntaxNode, /) -> None: ...

class ActionBlockSyntax(SyntaxNode):
    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

    @property
    def elseClause(self) -> ElseClauseSyntax: ...

    @elseClause.setter
    def elseClause(self, arg: ElseClauseSyntax, /) -> None: ...

class ImmediateAssertionStatementSyntax(StatementSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delay(self) -> DeferredAssertionSyntax: ...

    @delay.setter
    def delay(self, arg: DeferredAssertionSyntax, /) -> None: ...

    @property
    def expr(self) -> ParenthesizedExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ParenthesizedExpressionSyntax, /) -> None: ...

    @property
    def action(self) -> ActionBlockSyntax: ...

    @action.setter
    def action(self, arg: ActionBlockSyntax, /) -> None: ...

class DisableIffSyntax(SyntaxNode):
    @property
    def disable(self) -> pyslang.parsing.Token: ...

    @disable.setter
    def disable(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def iff(self) -> pyslang.parsing.Token: ...

    @iff.setter
    def iff(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class PropertySpecSyntax(SyntaxNode):
    @property
    def clocking(self) -> TimingControlSyntax: ...

    @clocking.setter
    def clocking(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def disable(self) -> DisableIffSyntax: ...

    @disable.setter
    def disable(self, arg: DisableIffSyntax, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class ConcurrentAssertionStatementSyntax(StatementSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def propertyOrSequence(self) -> pyslang.parsing.Token: ...

    @propertyOrSequence.setter
    def propertyOrSequence(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def propertySpec(self) -> PropertySpecSyntax: ...

    @propertySpec.setter
    def propertySpec(self, arg: PropertySpecSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def action(self) -> ActionBlockSyntax: ...

    @action.setter
    def action(self, arg: ActionBlockSyntax, /) -> None: ...

class ConcurrentAssertionMemberSyntax(MemberSyntax):
    @property
    def statement(self) -> ConcurrentAssertionStatementSyntax: ...

    @statement.setter
    def statement(self, arg: ConcurrentAssertionStatementSyntax, /) -> None: ...

class ImmediateAssertionMemberSyntax(MemberSyntax):
    @property
    def statement(self) -> ImmediateAssertionStatementSyntax: ...

    @statement.setter
    def statement(self, arg: ImmediateAssertionStatementSyntax, /) -> None: ...

class EmptyStatementSyntax(StatementSyntax):
    @property
    def semicolon(self) -> pyslang.parsing.Token: ...

    @semicolon.setter
    def semicolon(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConditionalStatementSyntax(StatementSyntax):
    @property
    def uniqueOrPriority(self) -> pyslang.parsing.Token: ...

    @uniqueOrPriority.setter
    def uniqueOrPriority(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ifKeyword(self) -> pyslang.parsing.Token: ...

    @ifKeyword.setter
    def ifKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def predicate(self) -> ConditionalPredicateSyntax: ...

    @predicate.setter
    def predicate(self, arg: ConditionalPredicateSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

    @property
    def elseClause(self) -> ElseClauseSyntax: ...

    @elseClause.setter
    def elseClause(self, arg: ElseClauseSyntax, /) -> None: ...

class CaseItemSyntax(SyntaxNode):
    pass

class DefaultCaseItemSyntax(CaseItemSyntax):
    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def clause(self) -> SyntaxNode: ...

    @clause.setter
    def clause(self, arg: SyntaxNode, /) -> None: ...

class PatternCaseItemSyntax(CaseItemSyntax):
    @property
    def pattern(self) -> PatternSyntax: ...

    @pattern.setter
    def pattern(self, arg: PatternSyntax, /) -> None: ...

    @property
    def tripleAnd(self) -> pyslang.parsing.Token: ...

    @tripleAnd.setter
    def tripleAnd(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class StandardCaseItemSyntax(CaseItemSyntax):
    @property
    def expressions(self) -> SeparatedSyntaxList: ...

    @expressions.setter
    def expressions(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def clause(self) -> SyntaxNode: ...

    @clause.setter
    def clause(self, arg: SyntaxNode, /) -> None: ...

class CaseStatementSyntax(StatementSyntax):
    @property
    def uniqueOrPriority(self) -> pyslang.parsing.Token: ...

    @uniqueOrPriority.setter
    def uniqueOrPriority(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def caseKeyword(self) -> pyslang.parsing.Token: ...

    @caseKeyword.setter
    def caseKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def matchesOrInside(self) -> pyslang.parsing.Token: ...

    @matchesOrInside.setter
    def matchesOrInside(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def endcase(self) -> pyslang.parsing.Token: ...

    @endcase.setter
    def endcase(self, arg: pyslang.parsing.Token, /) -> None: ...

class ForeverStatementSyntax(StatementSyntax):
    @property
    def foreverKeyword(self) -> pyslang.parsing.Token: ...

    @foreverKeyword.setter
    def foreverKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class LoopStatementSyntax(StatementSyntax):
    @property
    def repeatOrWhile(self) -> pyslang.parsing.Token: ...

    @repeatOrWhile.setter
    def repeatOrWhile(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class DoWhileStatementSyntax(StatementSyntax):
    @property
    def doKeyword(self) -> pyslang.parsing.Token: ...

    @doKeyword.setter
    def doKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

    @property
    def whileKeyword(self) -> pyslang.parsing.Token: ...

    @whileKeyword.setter
    def whileKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ForVariableDeclarationSyntax(SyntaxNode):
    @property
    def varKeyword(self) -> pyslang.parsing.Token: ...

    @varKeyword.setter
    def varKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def declarator(self) -> DeclaratorSyntax: ...

    @declarator.setter
    def declarator(self, arg: DeclaratorSyntax, /) -> None: ...

class ForLoopStatementSyntax(StatementSyntax):
    @property
    def forKeyword(self) -> pyslang.parsing.Token: ...

    @forKeyword.setter
    def forKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def initializers(self) -> SeparatedSyntaxList: ...

    @initializers.setter
    def initializers(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi1(self) -> pyslang.parsing.Token: ...

    @semi1.setter
    def semi1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def stopExpr(self) -> ExpressionSyntax: ...

    @stopExpr.setter
    def stopExpr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi2(self) -> pyslang.parsing.Token: ...

    @semi2.setter
    def semi2(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def steps(self) -> SeparatedSyntaxList: ...

    @steps.setter
    def steps(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class ForeachLoopListSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def arrayName(self) -> ExpressionSyntax: ...

    @arrayName.setter
    def arrayName(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def loopVariables(self) -> SeparatedSyntaxList: ...

    @loopVariables.setter
    def loopVariables(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ForeachLoopStatementSyntax(StatementSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def loopList(self) -> ForeachLoopListSyntax: ...

    @loopList.setter
    def loopList(self, arg: ForeachLoopListSyntax, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class ReturnStatementSyntax(StatementSyntax):
    @property
    def returnKeyword(self) -> pyslang.parsing.Token: ...

    @returnKeyword.setter
    def returnKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def returnValue(self) -> ExpressionSyntax: ...

    @returnValue.setter
    def returnValue(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class JumpStatementSyntax(StatementSyntax):
    @property
    def breakOrContinue(self) -> pyslang.parsing.Token: ...

    @breakOrContinue.setter
    def breakOrContinue(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class TimingControlStatementSyntax(StatementSyntax):
    @property
    def timingControl(self) -> TimingControlSyntax: ...

    @timingControl.setter
    def timingControl(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class ExpressionStatementSyntax(StatementSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class VoidCastedCallStatementSyntax(StatementSyntax):
    @property
    def voidKeyword(self) -> pyslang.parsing.Token: ...

    @voidKeyword.setter
    def voidKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def apostrophe(self) -> pyslang.parsing.Token: ...

    @apostrophe.setter
    def apostrophe(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ProceduralAssignStatementSyntax(StatementSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ProceduralDeassignStatementSyntax(StatementSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def variable(self) -> ExpressionSyntax: ...

    @variable.setter
    def variable(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class DisableStatementSyntax(StatementSyntax):
    @property
    def disable(self) -> pyslang.parsing.Token: ...

    @disable.setter
    def disable(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class DisableForkStatementSyntax(StatementSyntax):
    @property
    def disable(self) -> pyslang.parsing.Token: ...

    @disable.setter
    def disable(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def fork(self) -> pyslang.parsing.Token: ...

    @fork.setter
    def fork(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class NamedBlockClauseSyntax(SyntaxNode):
    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

class BlockStatementSyntax(StatementSyntax):
    @property
    def begin(self) -> pyslang.parsing.Token: ...

    @begin.setter
    def begin(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def blockName(self) -> NamedBlockClauseSyntax: ...

    @blockName.setter
    def blockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def end(self) -> pyslang.parsing.Token: ...

    @end.setter
    def end(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class WaitStatementSyntax(StatementSyntax):
    @property
    def wait(self) -> pyslang.parsing.Token: ...

    @wait.setter
    def wait(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class WaitForkStatementSyntax(StatementSyntax):
    @property
    def wait(self) -> pyslang.parsing.Token: ...

    @wait.setter
    def wait(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def fork(self) -> pyslang.parsing.Token: ...

    @fork.setter
    def fork(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class WaitOrderStatementSyntax(StatementSyntax):
    @property
    def wait_order(self) -> pyslang.parsing.Token: ...

    @wait_order.setter
    def wait_order(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def names(self) -> SeparatedSyntaxList: ...

    @names.setter
    def names(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def action(self) -> ActionBlockSyntax: ...

    @action.setter
    def action(self, arg: ActionBlockSyntax, /) -> None: ...

class RandCaseItemSyntax(SyntaxNode):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class RandCaseStatementSyntax(StatementSyntax):
    @property
    def randCase(self) -> pyslang.parsing.Token: ...

    @randCase.setter
    def randCase(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def endCase(self) -> pyslang.parsing.Token: ...

    @endCase.setter
    def endCase(self, arg: pyslang.parsing.Token, /) -> None: ...

class RsProdSyntax(SyntaxNode):
    pass

class RsProdItemSyntax(RsProdSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def argList(self) -> ArgumentListSyntax: ...

    @argList.setter
    def argList(self, arg: ArgumentListSyntax, /) -> None: ...

class RsCodeBlockSyntax(RsProdSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class RsElseClauseSyntax(SyntaxNode):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def item(self) -> RsProdItemSyntax: ...

    @item.setter
    def item(self, arg: RsProdItemSyntax, /) -> None: ...

class RsIfElseSyntax(RsProdSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def condition(self) -> ExpressionSyntax: ...

    @condition.setter
    def condition(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ifItem(self) -> RsProdItemSyntax: ...

    @ifItem.setter
    def ifItem(self, arg: RsProdItemSyntax, /) -> None: ...

    @property
    def elseClause(self) -> RsElseClauseSyntax: ...

    @elseClause.setter
    def elseClause(self, arg: RsElseClauseSyntax, /) -> None: ...

class RsRepeatSyntax(RsProdSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def item(self) -> RsProdItemSyntax: ...

    @item.setter
    def item(self, arg: RsProdItemSyntax, /) -> None: ...

class RsCaseItemSyntax(SyntaxNode):
    pass

class DefaultRsCaseItemSyntax(RsCaseItemSyntax):
    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def item(self) -> RsProdItemSyntax: ...

    @item.setter
    def item(self, arg: RsProdItemSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class StandardRsCaseItemSyntax(RsCaseItemSyntax):
    @property
    def expressions(self) -> SeparatedSyntaxList: ...

    @expressions.setter
    def expressions(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def item(self) -> RsProdItemSyntax: ...

    @item.setter
    def item(self, arg: RsProdItemSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class RsCaseSyntax(RsProdSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def endcase(self) -> pyslang.parsing.Token: ...

    @endcase.setter
    def endcase(self, arg: pyslang.parsing.Token, /) -> None: ...

class RandJoinClauseSyntax(SyntaxNode):
    @property
    def rand(self) -> pyslang.parsing.Token: ...

    @rand.setter
    def rand(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def join(self) -> pyslang.parsing.Token: ...

    @join.setter
    def join(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ParenthesizedExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ParenthesizedExpressionSyntax, /) -> None: ...

class RsWeightClauseSyntax(SyntaxNode):
    @property
    def colonEqual(self) -> pyslang.parsing.Token: ...

    @colonEqual.setter
    def colonEqual(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def weight(self) -> ExpressionSyntax: ...

    @weight.setter
    def weight(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def codeBlock(self) -> RsProdSyntax: ...

    @codeBlock.setter
    def codeBlock(self, arg: RsProdSyntax, /) -> None: ...

class RsRuleSyntax(SyntaxNode):
    @property
    def randJoin(self) -> RandJoinClauseSyntax: ...

    @randJoin.setter
    def randJoin(self, arg: RandJoinClauseSyntax, /) -> None: ...

    @property
    def prods(self) -> SyntaxList: ...

    @prods.setter
    def prods(self, arg: SyntaxList, /) -> None: ...

    @property
    def weightClause(self) -> RsWeightClauseSyntax: ...

    @weightClause.setter
    def weightClause(self, arg: RsWeightClauseSyntax, /) -> None: ...

class ProductionSyntax(SyntaxNode):
    @property
    def dataType(self) -> DataTypeSyntax: ...

    @dataType.setter
    def dataType(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> FunctionPortListSyntax: ...

    @portList.setter
    def portList(self, arg: FunctionPortListSyntax, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def rules(self) -> SeparatedSyntaxList: ...

    @rules.setter
    def rules(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class RandSequenceStatementSyntax(StatementSyntax):
    @property
    def randsequence(self) -> pyslang.parsing.Token: ...

    @randsequence.setter
    def randsequence(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def firstProduction(self) -> pyslang.parsing.Token: ...

    @firstProduction.setter
    def firstProduction(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def productions(self) -> SyntaxList: ...

    @productions.setter
    def productions(self, arg: SyntaxList, /) -> None: ...

    @property
    def endsequence(self) -> pyslang.parsing.Token: ...

    @endsequence.setter
    def endsequence(self, arg: pyslang.parsing.Token, /) -> None: ...

class EventTriggerStatementSyntax(StatementSyntax):
    @property
    def trigger(self) -> pyslang.parsing.Token: ...

    @trigger.setter
    def trigger(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def timing(self) -> TimingControlSyntax: ...

    @timing.setter
    def timing(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PortListSyntax(SyntaxNode):
    pass

class NonAnsiPortSyntax(SyntaxNode):
    pass

class PortExpressionSyntax(SyntaxNode):
    pass

class PortReferenceSyntax(PortExpressionSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def select(self) -> ElementSelectSyntax: ...

    @select.setter
    def select(self, arg: ElementSelectSyntax, /) -> None: ...

class PortConcatenationSyntax(PortExpressionSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def references(self) -> SeparatedSyntaxList: ...

    @references.setter
    def references(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class EmptyNonAnsiPortSyntax(NonAnsiPortSyntax):
    @property
    def placeholder(self) -> pyslang.parsing.Token: ...

    @placeholder.setter
    def placeholder(self, arg: pyslang.parsing.Token, /) -> None: ...

class ImplicitNonAnsiPortSyntax(NonAnsiPortSyntax):
    @property
    def expr(self) -> PortExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: PortExpressionSyntax, /) -> None: ...

class ExplicitNonAnsiPortSyntax(NonAnsiPortSyntax):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PortExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: PortExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class NonAnsiPortListSyntax(PortListSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> SeparatedSyntaxList: ...

    @ports.setter
    def ports(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class InterfacePortHeaderSyntax(PortHeaderSyntax):
    @property
    def nameOrKeyword(self) -> pyslang.parsing.Token: ...

    @nameOrKeyword.setter
    def nameOrKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def modport(self) -> DotMemberClauseSyntax: ...

    @modport.setter
    def modport(self, arg: DotMemberClauseSyntax, /) -> None: ...

class VariablePortHeaderSyntax(PortHeaderSyntax):
    @property
    def constKeyword(self) -> pyslang.parsing.Token: ...

    @constKeyword.setter
    def constKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def direction(self) -> pyslang.parsing.Token: ...

    @direction.setter
    def direction(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def varKeyword(self) -> pyslang.parsing.Token: ...

    @varKeyword.setter
    def varKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dataType(self) -> DataTypeSyntax: ...

    @dataType.setter
    def dataType(self, arg: DataTypeSyntax, /) -> None: ...

class NetPortHeaderSyntax(PortHeaderSyntax):
    @property
    def direction(self) -> pyslang.parsing.Token: ...

    @direction.setter
    def direction(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def netType(self) -> pyslang.parsing.Token: ...

    @netType.setter
    def netType(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dataType(self) -> DataTypeSyntax: ...

    @dataType.setter
    def dataType(self, arg: DataTypeSyntax, /) -> None: ...

class ImplicitAnsiPortSyntax(MemberSyntax):
    @property
    def header(self) -> PortHeaderSyntax: ...

    @header.setter
    def header(self, arg: PortHeaderSyntax, /) -> None: ...

    @property
    def declarator(self) -> DeclaratorSyntax: ...

    @declarator.setter
    def declarator(self, arg: DeclaratorSyntax, /) -> None: ...

class ExplicitAnsiPortSyntax(MemberSyntax):
    @property
    def direction(self) -> pyslang.parsing.Token: ...

    @direction.setter
    def direction(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class AnsiPortListSyntax(PortListSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> SeparatedSyntaxList: ...

    @ports.setter
    def ports(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class WildcardPortListSyntax(PortListSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def star(self) -> pyslang.parsing.Token: ...

    @star.setter
    def star(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ParameterPortListSyntax(SyntaxNode):
    @property
    def hash(self) -> pyslang.parsing.Token: ...

    @hash.setter
    def hash(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def declarations(self) -> SeparatedSyntaxList: ...

    @declarations.setter
    def declarations(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ModuleHeaderSyntax(SyntaxNode):
    @property
    def moduleKeyword(self) -> pyslang.parsing.Token: ...

    @moduleKeyword.setter
    def moduleKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def lifetime(self) -> pyslang.parsing.Token: ...

    @lifetime.setter
    def lifetime(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def imports(self) -> SyntaxList: ...

    @imports.setter
    def imports(self, arg: SyntaxList, /) -> None: ...

    @property
    def parameters(self) -> ParameterPortListSyntax: ...

    @parameters.setter
    def parameters(self, arg: ParameterPortListSyntax, /) -> None: ...

    @property
    def ports(self) -> PortListSyntax: ...

    @ports.setter
    def ports(self, arg: PortListSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ModuleDeclarationSyntax(MemberSyntax):
    @property
    def header(self) -> ModuleHeaderSyntax: ...

    @header.setter
    def header(self, arg: ModuleHeaderSyntax, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def endmodule(self) -> pyslang.parsing.Token: ...

    @endmodule.setter
    def endmodule(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def blockName(self) -> NamedBlockClauseSyntax: ...

    @blockName.setter
    def blockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class AnonymousProgramSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def endkeyword(self) -> pyslang.parsing.Token: ...

    @endkeyword.setter
    def endkeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

class EmptyMemberSyntax(MemberSyntax):
    @property
    def qualifiers(self) -> TokenList: ...

    @qualifiers.setter
    def qualifiers(self, arg: TokenList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ProceduralBlockSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def statement(self) -> StatementSyntax: ...

    @statement.setter
    def statement(self, arg: StatementSyntax, /) -> None: ...

class GenerateRegionSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def endgenerate(self) -> pyslang.parsing.Token: ...

    @endgenerate.setter
    def endgenerate(self, arg: pyslang.parsing.Token, /) -> None: ...

class LoopGenerateSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def genvar(self) -> pyslang.parsing.Token: ...

    @genvar.setter
    def genvar(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def identifier(self) -> pyslang.parsing.Token: ...

    @identifier.setter
    def identifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def initialExpr(self) -> ExpressionSyntax: ...

    @initialExpr.setter
    def initialExpr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi1(self) -> pyslang.parsing.Token: ...

    @semi1.setter
    def semi1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def stopExpr(self) -> ExpressionSyntax: ...

    @stopExpr.setter
    def stopExpr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi2(self) -> pyslang.parsing.Token: ...

    @semi2.setter
    def semi2(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def iterationExpr(self) -> ExpressionSyntax: ...

    @iterationExpr.setter
    def iterationExpr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def block(self) -> MemberSyntax: ...

    @block.setter
    def block(self, arg: MemberSyntax, /) -> None: ...

class IfGenerateSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def condition(self) -> ExpressionSyntax: ...

    @condition.setter
    def condition(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def block(self) -> MemberSyntax: ...

    @block.setter
    def block(self, arg: MemberSyntax, /) -> None: ...

    @property
    def elseClause(self) -> ElseClauseSyntax: ...

    @elseClause.setter
    def elseClause(self, arg: ElseClauseSyntax, /) -> None: ...

class CaseGenerateSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def condition(self) -> ExpressionSyntax: ...

    @condition.setter
    def condition(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def endCase(self) -> pyslang.parsing.Token: ...

    @endCase.setter
    def endCase(self, arg: pyslang.parsing.Token, /) -> None: ...

class GenerateBlockSyntax(MemberSyntax):
    @property
    def label(self) -> NamedLabelSyntax: ...

    @label.setter
    def label(self, arg: NamedLabelSyntax, /) -> None: ...

    @property
    def begin(self) -> pyslang.parsing.Token: ...

    @begin.setter
    def begin(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def beginName(self) -> NamedBlockClauseSyntax: ...

    @beginName.setter
    def beginName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def end(self) -> pyslang.parsing.Token: ...

    @end.setter
    def end(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endName(self) -> NamedBlockClauseSyntax: ...

    @endName.setter
    def endName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class DividerClauseSyntax(SyntaxNode):
    @property
    def divide(self) -> pyslang.parsing.Token: ...

    @divide.setter
    def divide(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def value(self) -> pyslang.parsing.Token: ...

    @value.setter
    def value(self, arg: pyslang.parsing.Token, /) -> None: ...

class TimeUnitsDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def time(self) -> pyslang.parsing.Token: ...

    @time.setter
    def time(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def divider(self) -> DividerClauseSyntax: ...

    @divider.setter
    def divider(self, arg: DividerClauseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PortConnectionSyntax(SyntaxNode):
    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

class EmptyPortConnectionSyntax(PortConnectionSyntax):
    @property
    def placeholder(self) -> pyslang.parsing.Token: ...

    @placeholder.setter
    def placeholder(self, arg: pyslang.parsing.Token, /) -> None: ...

class OrderedPortConnectionSyntax(PortConnectionSyntax):
    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class NamedPortConnectionSyntax(PortConnectionSyntax):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class WildcardPortConnectionSyntax(PortConnectionSyntax):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def star(self) -> pyslang.parsing.Token: ...

    @star.setter
    def star(self, arg: pyslang.parsing.Token, /) -> None: ...

class InstanceNameSyntax(SyntaxNode):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dimensions(self) -> SyntaxList: ...

    @dimensions.setter
    def dimensions(self, arg: SyntaxList, /) -> None: ...

class HierarchicalInstanceSyntax(SyntaxNode):
    @property
    def decl(self) -> InstanceNameSyntax: ...

    @decl.setter
    def decl(self, arg: InstanceNameSyntax, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def connections(self) -> SeparatedSyntaxList: ...

    @connections.setter
    def connections(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class HierarchyInstantiationSyntax(MemberSyntax):
    @property
    def type(self) -> pyslang.parsing.Token: ...

    @type.setter
    def type(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def parameters(self) -> ParameterValueAssignmentSyntax: ...

    @parameters.setter
    def parameters(self, arg: ParameterValueAssignmentSyntax, /) -> None: ...

    @property
    def instances(self) -> SeparatedSyntaxList: ...

    @instances.setter
    def instances(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PrimitiveInstantiationSyntax(MemberSyntax):
    @property
    def type(self) -> pyslang.parsing.Token: ...

    @type.setter
    def type(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def strength(self) -> NetStrengthSyntax: ...

    @strength.setter
    def strength(self, arg: NetStrengthSyntax, /) -> None: ...

    @property
    def delay(self) -> TimingControlSyntax: ...

    @delay.setter
    def delay(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def instances(self) -> SeparatedSyntaxList: ...

    @instances.setter
    def instances(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class CheckerInstantiationSyntax(MemberSyntax):
    @property
    def type(self) -> NameSyntax: ...

    @type.setter
    def type(self, arg: NameSyntax, /) -> None: ...

    @property
    def parameters(self) -> ParameterValueAssignmentSyntax: ...

    @parameters.setter
    def parameters(self, arg: ParameterValueAssignmentSyntax, /) -> None: ...

    @property
    def instances(self) -> SeparatedSyntaxList: ...

    @instances.setter
    def instances(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class CheckerInstanceStatementSyntax(StatementSyntax):
    @property
    def instance(self) -> CheckerInstantiationSyntax: ...

    @instance.setter
    def instance(self, arg: CheckerInstantiationSyntax, /) -> None: ...

class BindTargetListSyntax(SyntaxNode):
    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def targets(self) -> SeparatedSyntaxList: ...

    @targets.setter
    def targets(self, arg: SeparatedSyntaxList, /) -> None: ...

class BindDirectiveSyntax(MemberSyntax):
    @property
    def bind(self) -> pyslang.parsing.Token: ...

    @bind.setter
    def bind(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def target(self) -> NameSyntax: ...

    @target.setter
    def target(self, arg: NameSyntax, /) -> None: ...

    @property
    def targetInstances(self) -> BindTargetListSyntax: ...

    @targetInstances.setter
    def targetInstances(self, arg: BindTargetListSyntax, /) -> None: ...

    @property
    def instantiation(self) -> MemberSyntax: ...

    @instantiation.setter
    def instantiation(self, arg: MemberSyntax, /) -> None: ...

class ClassSpecifierSyntax(SyntaxNode):
    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

class FunctionPrototypeSyntax(SyntaxNode):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def specifiers(self) -> SyntaxList: ...

    @specifiers.setter
    def specifiers(self, arg: SyntaxList, /) -> None: ...

    @property
    def lifetime(self) -> pyslang.parsing.Token: ...

    @lifetime.setter
    def lifetime(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def returnType(self) -> DataTypeSyntax: ...

    @returnType.setter
    def returnType(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

    @property
    def portList(self) -> FunctionPortListSyntax: ...

    @portList.setter
    def portList(self, arg: FunctionPortListSyntax, /) -> None: ...

class FunctionDeclarationSyntax(MemberSyntax):
    @property
    def prototype(self) -> FunctionPrototypeSyntax: ...

    @prototype.setter
    def prototype(self, arg: FunctionPrototypeSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def end(self) -> pyslang.parsing.Token: ...

    @end.setter
    def end(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class EqualsAssertionArgClauseSyntax(SyntaxNode):
    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class AssertionItemPortSyntax(SyntaxNode):
    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def local(self) -> pyslang.parsing.Token: ...

    @local.setter
    def local(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def direction(self) -> pyslang.parsing.Token: ...

    @direction.setter
    def direction(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dimensions(self) -> SyntaxList: ...

    @dimensions.setter
    def dimensions(self, arg: SyntaxList, /) -> None: ...

    @property
    def defaultValue(self) -> EqualsAssertionArgClauseSyntax: ...

    @defaultValue.setter
    def defaultValue(self, arg: EqualsAssertionArgClauseSyntax, /) -> None: ...

class AssertionItemPortListSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> SeparatedSyntaxList: ...

    @ports.setter
    def ports(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class LetDeclarationSyntax(MemberSyntax):
    @property
    def let(self) -> pyslang.parsing.Token: ...

    @let.setter
    def let(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def identifier(self) -> pyslang.parsing.Token: ...

    @identifier.setter
    def identifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> AssertionItemPortListSyntax: ...

    @portList.setter
    def portList(self, arg: AssertionItemPortListSyntax, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class DefaultExtendsClauseArgSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ExtendsClauseSyntax(SyntaxNode):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def baseName(self) -> NameSyntax: ...

    @baseName.setter
    def baseName(self, arg: NameSyntax, /) -> None: ...

    @property
    def arguments(self) -> ArgumentListSyntax: ...

    @arguments.setter
    def arguments(self, arg: ArgumentListSyntax, /) -> None: ...

    @property
    def defaultedArg(self) -> DefaultExtendsClauseArgSyntax: ...

    @defaultedArg.setter
    def defaultedArg(self, arg: DefaultExtendsClauseArgSyntax, /) -> None: ...

class ImplementsClauseSyntax(SyntaxNode):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def interfaces(self) -> SeparatedSyntaxList: ...

    @interfaces.setter
    def interfaces(self, arg: SeparatedSyntaxList, /) -> None: ...

class ClassDeclarationSyntax(MemberSyntax):
    @property
    def virtualOrInterface(self) -> pyslang.parsing.Token: ...

    @virtualOrInterface.setter
    def virtualOrInterface(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def classKeyword(self) -> pyslang.parsing.Token: ...

    @classKeyword.setter
    def classKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def finalSpecifier(self) -> ClassSpecifierSyntax: ...

    @finalSpecifier.setter
    def finalSpecifier(self, arg: ClassSpecifierSyntax, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def parameters(self) -> ParameterPortListSyntax: ...

    @parameters.setter
    def parameters(self, arg: ParameterPortListSyntax, /) -> None: ...

    @property
    def extendsClause(self) -> ExtendsClauseSyntax: ...

    @extendsClause.setter
    def extendsClause(self, arg: ExtendsClauseSyntax, /) -> None: ...

    @property
    def implementsClause(self) -> ImplementsClauseSyntax: ...

    @implementsClause.setter
    def implementsClause(self, arg: ImplementsClauseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def endClass(self) -> pyslang.parsing.Token: ...

    @endClass.setter
    def endClass(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class ClassPropertyDeclarationSyntax(MemberSyntax):
    @property
    def qualifiers(self) -> TokenList: ...

    @qualifiers.setter
    def qualifiers(self, arg: TokenList, /) -> None: ...

    @property
    def declaration(self) -> MemberSyntax: ...

    @declaration.setter
    def declaration(self, arg: MemberSyntax, /) -> None: ...

class ClassMethodDeclarationSyntax(MemberSyntax):
    @property
    def qualifiers(self) -> TokenList: ...

    @qualifiers.setter
    def qualifiers(self, arg: TokenList, /) -> None: ...

    @property
    def declaration(self) -> FunctionDeclarationSyntax: ...

    @declaration.setter
    def declaration(self, arg: FunctionDeclarationSyntax, /) -> None: ...

class ClassMethodPrototypeSyntax(MemberSyntax):
    @property
    def qualifiers(self) -> TokenList: ...

    @qualifiers.setter
    def qualifiers(self, arg: TokenList, /) -> None: ...

    @property
    def prototype(self) -> FunctionPrototypeSyntax: ...

    @prototype.setter
    def prototype(self, arg: FunctionPrototypeSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ContinuousAssignSyntax(MemberSyntax):
    @property
    def assign(self) -> pyslang.parsing.Token: ...

    @assign.setter
    def assign(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def strength(self) -> DriveStrengthSyntax: ...

    @strength.setter
    def strength(self, arg: DriveStrengthSyntax, /) -> None: ...

    @property
    def delay(self) -> TimingControlSyntax: ...

    @delay.setter
    def delay(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def assignments(self) -> SeparatedSyntaxList: ...

    @assignments.setter
    def assignments(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class DefParamAssignmentSyntax(SyntaxNode):
    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

    @property
    def setter(self) -> EqualsValueClauseSyntax: ...

    @setter.setter
    def setter(self, arg: EqualsValueClauseSyntax, /) -> None: ...

class DefParamSyntax(MemberSyntax):
    @property
    def defparam(self) -> pyslang.parsing.Token: ...

    @defparam.setter
    def defparam(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def assignments(self) -> SeparatedSyntaxList: ...

    @assignments.setter
    def assignments(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ModportClockingPortSyntax(MemberSyntax):
    @property
    def clocking(self) -> pyslang.parsing.Token: ...

    @clocking.setter
    def clocking(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

class ModportPortSyntax(SyntaxNode):
    pass

class ModportNamedPortSyntax(ModportPortSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

class ModportExplicitPortSyntax(ModportPortSyntax):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ModportSimplePortListSyntax(MemberSyntax):
    @property
    def direction(self) -> pyslang.parsing.Token: ...

    @direction.setter
    def direction(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> SeparatedSyntaxList: ...

    @ports.setter
    def ports(self, arg: SeparatedSyntaxList, /) -> None: ...

class ModportSubroutinePortSyntax(ModportPortSyntax):
    @property
    def prototype(self) -> FunctionPrototypeSyntax: ...

    @prototype.setter
    def prototype(self, arg: FunctionPrototypeSyntax, /) -> None: ...

class ModportSubroutinePortListSyntax(MemberSyntax):
    @property
    def importExport(self) -> pyslang.parsing.Token: ...

    @importExport.setter
    def importExport(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> SeparatedSyntaxList: ...

    @ports.setter
    def ports(self, arg: SeparatedSyntaxList, /) -> None: ...

class ModportItemSyntax(SyntaxNode):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> AnsiPortListSyntax: ...

    @ports.setter
    def ports(self, arg: AnsiPortListSyntax, /) -> None: ...

class ModportDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ClockingSkewSyntax(SyntaxNode):
    @property
    def edge(self) -> pyslang.parsing.Token: ...

    @edge.setter
    def edge(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delay(self) -> TimingControlSyntax: ...

    @delay.setter
    def delay(self, arg: TimingControlSyntax, /) -> None: ...

class ClockingDirectionSyntax(SyntaxNode):
    @property
    def input(self) -> pyslang.parsing.Token: ...

    @input.setter
    def input(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def inputSkew(self) -> ClockingSkewSyntax: ...

    @inputSkew.setter
    def inputSkew(self, arg: ClockingSkewSyntax, /) -> None: ...

    @property
    def output(self) -> pyslang.parsing.Token: ...

    @output.setter
    def output(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def outputSkew(self) -> ClockingSkewSyntax: ...

    @outputSkew.setter
    def outputSkew(self, arg: ClockingSkewSyntax, /) -> None: ...

class DefaultSkewItemSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def direction(self) -> ClockingDirectionSyntax: ...

    @direction.setter
    def direction(self, arg: ClockingDirectionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ClockingItemSyntax(MemberSyntax):
    @property
    def direction(self) -> ClockingDirectionSyntax: ...

    @direction.setter
    def direction(self, arg: ClockingDirectionSyntax, /) -> None: ...

    @property
    def decls(self) -> SeparatedSyntaxList: ...

    @decls.setter
    def decls(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ClockingDeclarationSyntax(MemberSyntax):
    @property
    def globalOrDefault(self) -> pyslang.parsing.Token: ...

    @globalOrDefault.setter
    def globalOrDefault(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def clocking(self) -> pyslang.parsing.Token: ...

    @clocking.setter
    def clocking(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def blockName(self) -> pyslang.parsing.Token: ...

    @blockName.setter
    def blockName(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def at(self) -> pyslang.parsing.Token: ...

    @at.setter
    def at(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def event(self) -> EventExpressionSyntax: ...

    @event.setter
    def event(self, arg: EventExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def endClocking(self) -> pyslang.parsing.Token: ...

    @endClocking.setter
    def endClocking(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class DefaultClockingReferenceSyntax(MemberSyntax):
    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def clocking(self) -> pyslang.parsing.Token: ...

    @clocking.setter
    def clocking(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class DefaultDisableDeclarationSyntax(MemberSyntax):
    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def disableKeyword(self) -> pyslang.parsing.Token: ...

    @disableKeyword.setter
    def disableKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def iffKeyword(self) -> pyslang.parsing.Token: ...

    @iffKeyword.setter
    def iffKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class DPIImportSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def specString(self) -> pyslang.parsing.Token: ...

    @specString.setter
    def specString(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def property(self) -> pyslang.parsing.Token: ...

    @property.setter
    def property(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def c_identifier(self) -> pyslang.parsing.Token: ...

    @c_identifier.setter
    def c_identifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def method(self) -> FunctionPrototypeSyntax: ...

    @method.setter
    def method(self, arg: FunctionPrototypeSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class DPIExportSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def specString(self) -> pyslang.parsing.Token: ...

    @specString.setter
    def specString(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def c_identifier(self) -> pyslang.parsing.Token: ...

    @c_identifier.setter
    def c_identifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def functionOrTask(self) -> pyslang.parsing.Token: ...

    @functionOrTask.setter
    def functionOrTask(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ElabSystemTaskSyntax(MemberSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def arguments(self) -> ArgumentListSyntax: ...

    @arguments.setter
    def arguments(self, arg: ArgumentListSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class UdpPortDeclSyntax(SyntaxNode):
    @property
    def attributes(self) -> SyntaxList: ...

    @attributes.setter
    def attributes(self, arg: SyntaxList, /) -> None: ...

class UdpOutputPortDeclSyntax(UdpPortDeclSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def reg(self) -> pyslang.parsing.Token: ...

    @reg.setter
    def reg(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def initializer(self) -> EqualsValueClauseSyntax: ...

    @initializer.setter
    def initializer(self, arg: EqualsValueClauseSyntax, /) -> None: ...

class UdpInputPortDeclSyntax(UdpPortDeclSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def names(self) -> SeparatedSyntaxList: ...

    @names.setter
    def names(self, arg: SeparatedSyntaxList, /) -> None: ...

class UdpPortListSyntax(SyntaxNode):
    pass

class AnsiUdpPortListSyntax(UdpPortListSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> SeparatedSyntaxList: ...

    @ports.setter
    def ports(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class NonAnsiUdpPortListSyntax(UdpPortListSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ports(self) -> SeparatedSyntaxList: ...

    @ports.setter
    def ports(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class WildcardUdpPortListSyntax(UdpPortListSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def star(self) -> pyslang.parsing.Token: ...

    @star.setter
    def star(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class UdpInitialStmtSyntax(SyntaxNode):
    @property
    def initial(self) -> pyslang.parsing.Token: ...

    @initial.setter
    def initial(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def value(self) -> ExpressionSyntax: ...

    @value.setter
    def value(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class UdpFieldBaseSyntax(SyntaxNode):
    pass

class UdpEdgeFieldSyntax(UdpFieldBaseSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def first(self) -> pyslang.parsing.Token: ...

    @first.setter
    def first(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def second(self) -> pyslang.parsing.Token: ...

    @second.setter
    def second(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class UdpSimpleFieldSyntax(UdpFieldBaseSyntax):
    @property
    def field(self) -> pyslang.parsing.Token: ...

    @field.setter
    def field(self, arg: pyslang.parsing.Token, /) -> None: ...

class UdpEntrySyntax(SyntaxNode):
    @property
    def inputs(self) -> SyntaxList: ...

    @inputs.setter
    def inputs(self, arg: SyntaxList, /) -> None: ...

    @property
    def colon1(self) -> pyslang.parsing.Token: ...

    @colon1.setter
    def colon1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def current(self) -> UdpFieldBaseSyntax: ...

    @current.setter
    def current(self, arg: UdpFieldBaseSyntax, /) -> None: ...

    @property
    def colon2(self) -> pyslang.parsing.Token: ...

    @colon2.setter
    def colon2(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def next(self) -> UdpFieldBaseSyntax: ...

    @next.setter
    def next(self, arg: UdpFieldBaseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class UdpBodySyntax(SyntaxNode):
    @property
    def portDecls(self) -> SeparatedSyntaxList: ...

    @portDecls.setter
    def portDecls(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def initialStmt(self) -> UdpInitialStmtSyntax: ...

    @initialStmt.setter
    def initialStmt(self, arg: UdpInitialStmtSyntax, /) -> None: ...

    @property
    def table(self) -> pyslang.parsing.Token: ...

    @table.setter
    def table(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def entries(self) -> SyntaxList: ...

    @entries.setter
    def entries(self, arg: SyntaxList, /) -> None: ...

    @property
    def endtable(self) -> pyslang.parsing.Token: ...

    @endtable.setter
    def endtable(self, arg: pyslang.parsing.Token, /) -> None: ...

class UdpDeclarationSyntax(MemberSyntax):
    @property
    def primitive(self) -> pyslang.parsing.Token: ...

    @primitive.setter
    def primitive(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> UdpPortListSyntax: ...

    @portList.setter
    def portList(self, arg: UdpPortListSyntax, /) -> None: ...

    @property
    def body(self) -> UdpBodySyntax: ...

    @body.setter
    def body(self, arg: UdpBodySyntax, /) -> None: ...

    @property
    def endprimitive(self) -> pyslang.parsing.Token: ...

    @endprimitive.setter
    def endprimitive(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class SpecparamDeclaratorSyntax(SyntaxNode):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def value1(self) -> ExpressionSyntax: ...

    @value1.setter
    def value1(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def comma(self) -> pyslang.parsing.Token: ...

    @comma.setter
    def comma(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def value2(self) -> ExpressionSyntax: ...

    @value2.setter
    def value2(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class SpecparamDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> ImplicitTypeSyntax: ...

    @type.setter
    def type(self, arg: ImplicitTypeSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PathSuffixSyntax(SyntaxNode):
    pass

class SimplePathSuffixSyntax(PathSuffixSyntax):
    @property
    def outputs(self) -> SeparatedSyntaxList: ...

    @outputs.setter
    def outputs(self, arg: SeparatedSyntaxList, /) -> None: ...

class EdgeSensitivePathSuffixSyntax(PathSuffixSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def outputs(self) -> SeparatedSyntaxList: ...

    @outputs.setter
    def outputs(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def polarityOperator(self) -> pyslang.parsing.Token: ...

    @polarityOperator.setter
    def polarityOperator(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class PathDescriptionSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def edgeIdentifier(self) -> pyslang.parsing.Token: ...

    @edgeIdentifier.setter
    def edgeIdentifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def inputs(self) -> SeparatedSyntaxList: ...

    @inputs.setter
    def inputs(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def polarityOperator(self) -> pyslang.parsing.Token: ...

    @polarityOperator.setter
    def polarityOperator(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def pathOperator(self) -> pyslang.parsing.Token: ...

    @pathOperator.setter
    def pathOperator(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def suffix(self) -> PathSuffixSyntax: ...

    @suffix.setter
    def suffix(self, arg: PathSuffixSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class PathDeclarationSyntax(MemberSyntax):
    @property
    def desc(self) -> PathDescriptionSyntax: ...

    @desc.setter
    def desc(self, arg: PathDescriptionSyntax, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delays(self) -> SeparatedSyntaxList: ...

    @delays.setter
    def delays(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConditionalPathDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def predicate(self) -> ExpressionSyntax: ...

    @predicate.setter
    def predicate(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def path(self) -> PathDeclarationSyntax: ...

    @path.setter
    def path(self, arg: PathDeclarationSyntax, /) -> None: ...

class IfNonePathDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def path(self) -> PathDeclarationSyntax: ...

    @path.setter
    def path(self, arg: PathDeclarationSyntax, /) -> None: ...

class PulseStyleDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def inputs(self) -> SeparatedSyntaxList: ...

    @inputs.setter
    def inputs(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class TimingCheckArgSyntax(SyntaxNode):
    pass

class EmptyTimingCheckArgSyntax(TimingCheckArgSyntax):
    @property
    def placeholder(self) -> pyslang.parsing.Token: ...

    @placeholder.setter
    def placeholder(self, arg: pyslang.parsing.Token, /) -> None: ...

class EdgeDescriptorSyntax(SyntaxNode):
    @property
    def t1(self) -> pyslang.parsing.Token: ...

    @t1.setter
    def t1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def t2(self) -> pyslang.parsing.Token: ...

    @t2.setter
    def t2(self, arg: pyslang.parsing.Token, /) -> None: ...

class EdgeControlSpecifierSyntax(SyntaxNode):
    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def descriptors(self) -> SeparatedSyntaxList: ...

    @descriptors.setter
    def descriptors(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

class TimingCheckEventConditionSyntax(SyntaxNode):
    @property
    def tripleAnd(self) -> pyslang.parsing.Token: ...

    @tripleAnd.setter
    def tripleAnd(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class TimingCheckEventArgSyntax(TimingCheckArgSyntax):
    @property
    def edge(self) -> pyslang.parsing.Token: ...

    @edge.setter
    def edge(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def controlSpecifier(self) -> EdgeControlSpecifierSyntax: ...

    @controlSpecifier.setter
    def controlSpecifier(self, arg: EdgeControlSpecifierSyntax, /) -> None: ...

    @property
    def terminal(self) -> ExpressionSyntax: ...

    @terminal.setter
    def terminal(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def condition(self) -> TimingCheckEventConditionSyntax: ...

    @condition.setter
    def condition(self, arg: TimingCheckEventConditionSyntax, /) -> None: ...

class ExpressionTimingCheckArgSyntax(TimingCheckArgSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class SystemTimingCheckSyntax(MemberSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def args(self) -> SeparatedSyntaxList: ...

    @args.setter
    def args(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class SpecifyBlockSyntax(MemberSyntax):
    @property
    def specify(self) -> pyslang.parsing.Token: ...

    @specify.setter
    def specify(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def endspecify(self) -> pyslang.parsing.Token: ...

    @endspecify.setter
    def endspecify(self, arg: pyslang.parsing.Token, /) -> None: ...

class NetAliasSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def nets(self) -> SeparatedSyntaxList: ...

    @nets.setter
    def nets(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ExternModuleDeclSyntax(MemberSyntax):
    @property
    def externKeyword(self) -> pyslang.parsing.Token: ...

    @externKeyword.setter
    def externKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def actualAttributes(self) -> SyntaxList: ...

    @actualAttributes.setter
    def actualAttributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def header(self) -> ModuleHeaderSyntax: ...

    @header.setter
    def header(self, arg: ModuleHeaderSyntax, /) -> None: ...

class ExternUdpDeclSyntax(MemberSyntax):
    @property
    def externKeyword(self) -> pyslang.parsing.Token: ...

    @externKeyword.setter
    def externKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def actualAttributes(self) -> SyntaxList: ...

    @actualAttributes.setter
    def actualAttributes(self, arg: SyntaxList, /) -> None: ...

    @property
    def primitive(self) -> pyslang.parsing.Token: ...

    @primitive.setter
    def primitive(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> UdpPortListSyntax: ...

    @portList.setter
    def portList(self, arg: UdpPortListSyntax, /) -> None: ...

class ExternInterfaceMethodSyntax(MemberSyntax):
    @property
    def externKeyword(self) -> pyslang.parsing.Token: ...

    @externKeyword.setter
    def externKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def forkJoin(self) -> pyslang.parsing.Token: ...

    @forkJoin.setter
    def forkJoin(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def prototype(self) -> FunctionPrototypeSyntax: ...

    @prototype.setter
    def prototype(self, arg: FunctionPrototypeSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConstraintItemSyntax(SyntaxNode):
    pass

class DistWeightSyntax(SyntaxNode):
    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def extraOp(self) -> pyslang.parsing.Token: ...

    @extraOp.setter
    def extraOp(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class DistItemBaseSyntax(SyntaxNode):
    pass

class DistItemSyntax(DistItemBaseSyntax):
    @property
    def range(self) -> ExpressionSyntax: ...

    @range.setter
    def range(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def weight(self) -> DistWeightSyntax: ...

    @weight.setter
    def weight(self, arg: DistWeightSyntax, /) -> None: ...

class DefaultDistItemSyntax(DistItemBaseSyntax):
    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def weight(self) -> DistWeightSyntax: ...

    @weight.setter
    def weight(self, arg: DistWeightSyntax, /) -> None: ...

class DistConstraintListSyntax(SyntaxNode):
    @property
    def dist(self) -> pyslang.parsing.Token: ...

    @dist.setter
    def dist(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class ExpressionOrDistSyntax(ExpressionSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def distribution(self) -> DistConstraintListSyntax: ...

    @distribution.setter
    def distribution(self, arg: DistConstraintListSyntax, /) -> None: ...

class ExpressionConstraintSyntax(ConstraintItemSyntax):
    @property
    def soft(self) -> pyslang.parsing.Token: ...

    @soft.setter
    def soft(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class UniquenessConstraintSyntax(ConstraintItemSyntax):
    @property
    def unique(self) -> pyslang.parsing.Token: ...

    @unique.setter
    def unique(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ranges(self) -> RangeListSyntax: ...

    @ranges.setter
    def ranges(self, arg: RangeListSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ImplicationConstraintSyntax(ConstraintItemSyntax):
    @property
    def left(self) -> ExpressionSyntax: ...

    @left.setter
    def left(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def arrow(self) -> pyslang.parsing.Token: ...

    @arrow.setter
    def arrow(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def constraints(self) -> ConstraintItemSyntax: ...

    @constraints.setter
    def constraints(self, arg: ConstraintItemSyntax, /) -> None: ...

class ElseConstraintClauseSyntax(SyntaxNode):
    @property
    def elseKeyword(self) -> pyslang.parsing.Token: ...

    @elseKeyword.setter
    def elseKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def constraints(self) -> ConstraintItemSyntax: ...

    @constraints.setter
    def constraints(self, arg: ConstraintItemSyntax, /) -> None: ...

class ConditionalConstraintSyntax(ConstraintItemSyntax):
    @property
    def ifKeyword(self) -> pyslang.parsing.Token: ...

    @ifKeyword.setter
    def ifKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def condition(self) -> ExpressionSyntax: ...

    @condition.setter
    def condition(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def constraints(self) -> ConstraintItemSyntax: ...

    @constraints.setter
    def constraints(self, arg: ConstraintItemSyntax, /) -> None: ...

    @property
    def elseClause(self) -> ElseConstraintClauseSyntax: ...

    @elseClause.setter
    def elseClause(self, arg: ElseConstraintClauseSyntax, /) -> None: ...

class LoopConstraintSyntax(ConstraintItemSyntax):
    @property
    def foreachKeyword(self) -> pyslang.parsing.Token: ...

    @foreachKeyword.setter
    def foreachKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def loopList(self) -> ForeachLoopListSyntax: ...

    @loopList.setter
    def loopList(self, arg: ForeachLoopListSyntax, /) -> None: ...

    @property
    def constraints(self) -> ConstraintItemSyntax: ...

    @constraints.setter
    def constraints(self, arg: ConstraintItemSyntax, /) -> None: ...

class DisableConstraintSyntax(ConstraintItemSyntax):
    @property
    def disable(self) -> pyslang.parsing.Token: ...

    @disable.setter
    def disable(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def soft(self) -> pyslang.parsing.Token: ...

    @soft.setter
    def soft(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> ExpressionSyntax: ...

    @name.setter
    def name(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class SolveBeforeConstraintSyntax(ConstraintItemSyntax):
    @property
    def solve(self) -> pyslang.parsing.Token: ...

    @solve.setter
    def solve(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def beforeExpr(self) -> SeparatedSyntaxList: ...

    @beforeExpr.setter
    def beforeExpr(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def before(self) -> pyslang.parsing.Token: ...

    @before.setter
    def before(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def afterExpr(self) -> SeparatedSyntaxList: ...

    @afterExpr.setter
    def afterExpr(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConstraintBlockSyntax(ConstraintItemSyntax):
    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConstraintPrototypeSyntax(MemberSyntax):
    @property
    def qualifiers(self) -> TokenList: ...

    @qualifiers.setter
    def qualifiers(self, arg: TokenList, /) -> None: ...

    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def specifiers(self) -> SyntaxList: ...

    @specifiers.setter
    def specifiers(self, arg: SyntaxList, /) -> None: ...

    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConstraintDeclarationSyntax(MemberSyntax):
    @property
    def qualifiers(self) -> TokenList: ...

    @qualifiers.setter
    def qualifiers(self, arg: TokenList, /) -> None: ...

    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def specifiers(self) -> SyntaxList: ...

    @specifiers.setter
    def specifiers(self, arg: SyntaxList, /) -> None: ...

    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

    @property
    def block(self) -> ConstraintBlockSyntax: ...

    @block.setter
    def block(self, arg: ConstraintBlockSyntax, /) -> None: ...

class ParenExpressionListSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expressions(self) -> SeparatedSyntaxList: ...

    @expressions.setter
    def expressions(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ArrayOrRandomizeMethodExpressionSyntax(ExpressionSyntax):
    @property
    def method(self) -> ExpressionSyntax: ...

    @method.setter
    def method(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def args(self) -> ParenExpressionListSyntax: ...

    @args.setter
    def args(self, arg: ParenExpressionListSyntax, /) -> None: ...

    @property
    def constraints(self) -> ConstraintBlockSyntax: ...

    @constraints.setter
    def constraints(self, arg: ConstraintBlockSyntax, /) -> None: ...

class WithFunctionSampleSyntax(SyntaxNode):
    @property
    def function(self) -> pyslang.parsing.Token: ...

    @function.setter
    def function(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def sample(self) -> pyslang.parsing.Token: ...

    @sample.setter
    def sample(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> FunctionPortListSyntax: ...

    @portList.setter
    def portList(self, arg: FunctionPortListSyntax, /) -> None: ...

class BlockEventExpressionSyntax(SyntaxNode):
    pass

class BinaryBlockEventExpressionSyntax(BlockEventExpressionSyntax):
    @property
    def left(self) -> BlockEventExpressionSyntax: ...

    @left.setter
    def left(self, arg: BlockEventExpressionSyntax, /) -> None: ...

    @property
    def orKeyword(self) -> pyslang.parsing.Token: ...

    @orKeyword.setter
    def orKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> BlockEventExpressionSyntax: ...

    @right.setter
    def right(self, arg: BlockEventExpressionSyntax, /) -> None: ...

class PrimaryBlockEventExpressionSyntax(BlockEventExpressionSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

class BlockCoverageEventSyntax(SyntaxNode):
    @property
    def atat(self) -> pyslang.parsing.Token: ...

    @atat.setter
    def atat(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> BlockEventExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: BlockEventExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class CovergroupDeclarationSyntax(MemberSyntax):
    @property
    def covergroup(self) -> pyslang.parsing.Token: ...

    @covergroup.setter
    def covergroup(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def extends(self) -> pyslang.parsing.Token: ...

    @extends.setter
    def extends(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> FunctionPortListSyntax: ...

    @portList.setter
    def portList(self, arg: FunctionPortListSyntax, /) -> None: ...

    @property
    def event(self) -> SyntaxNode: ...

    @event.setter
    def event(self, arg: SyntaxNode, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def endgroup(self) -> pyslang.parsing.Token: ...

    @endgroup.setter
    def endgroup(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class CoverageOptionSyntax(MemberSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class CoverageIffClauseSyntax(SyntaxNode):
    @property
    def iff(self) -> pyslang.parsing.Token: ...

    @iff.setter
    def iff(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class CoverpointSyntax(MemberSyntax):
    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def label(self) -> NamedLabelSyntax: ...

    @label.setter
    def label(self, arg: NamedLabelSyntax, /) -> None: ...

    @property
    def coverpoint(self) -> pyslang.parsing.Token: ...

    @coverpoint.setter
    def coverpoint(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def iff(self) -> CoverageIffClauseSyntax: ...

    @iff.setter
    def iff(self, arg: CoverageIffClauseSyntax, /) -> None: ...

    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def emptySemi(self) -> pyslang.parsing.Token: ...

    @emptySemi.setter
    def emptySemi(self, arg: pyslang.parsing.Token, /) -> None: ...

class CoverageBinInitializerSyntax(SyntaxNode):
    pass

class DefaultCoverageBinInitializerSyntax(CoverageBinInitializerSyntax):
    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def sequenceKeyword(self) -> pyslang.parsing.Token: ...

    @sequenceKeyword.setter
    def sequenceKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

class WithClauseSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ExpressionCoverageBinInitializerSyntax(CoverageBinInitializerSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

class RangeCoverageBinInitializerSyntax(CoverageBinInitializerSyntax):
    @property
    def ranges(self) -> RangeListSyntax: ...

    @ranges.setter
    def ranges(self, arg: RangeListSyntax, /) -> None: ...

    @property
    def withClause(self) -> WithClauseSyntax: ...

    @withClause.setter
    def withClause(self, arg: WithClauseSyntax, /) -> None: ...

class IdWithExprCoverageBinInitializerSyntax(CoverageBinInitializerSyntax):
    @property
    def id(self) -> pyslang.parsing.Token: ...

    @id.setter
    def id(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def withClause(self) -> WithClauseSyntax: ...

    @withClause.setter
    def withClause(self, arg: WithClauseSyntax, /) -> None: ...

class TransRepeatRangeSyntax(SyntaxNode):
    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def specifier(self) -> pyslang.parsing.Token: ...

    @specifier.setter
    def specifier(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def selector(self) -> SelectorSyntax: ...

    @selector.setter
    def selector(self, arg: SelectorSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

class TransRangeSyntax(SyntaxNode):
    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def repeat(self) -> TransRepeatRangeSyntax: ...

    @repeat.setter
    def repeat(self, arg: TransRepeatRangeSyntax, /) -> None: ...

class TransSetSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ranges(self) -> SeparatedSyntaxList: ...

    @ranges.setter
    def ranges(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class TransListCoverageBinInitializerSyntax(CoverageBinInitializerSyntax):
    @property
    def sets(self) -> SeparatedSyntaxList: ...

    @sets.setter
    def sets(self, arg: SeparatedSyntaxList, /) -> None: ...

class CoverageBinsArraySizeSyntax(SyntaxNode):
    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

class CoverageBinsSyntax(MemberSyntax):
    @property
    def wildcard(self) -> pyslang.parsing.Token: ...

    @wildcard.setter
    def wildcard(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def size(self) -> CoverageBinsArraySizeSyntax: ...

    @size.setter
    def size(self, arg: CoverageBinsArraySizeSyntax, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def initializer(self) -> CoverageBinInitializerSyntax: ...

    @initializer.setter
    def initializer(self, arg: CoverageBinInitializerSyntax, /) -> None: ...

    @property
    def iff(self) -> CoverageIffClauseSyntax: ...

    @iff.setter
    def iff(self, arg: CoverageIffClauseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class CoverCrossSyntax(MemberSyntax):
    @property
    def label(self) -> NamedLabelSyntax: ...

    @label.setter
    def label(self, arg: NamedLabelSyntax, /) -> None: ...

    @property
    def cross(self) -> pyslang.parsing.Token: ...

    @cross.setter
    def cross(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def iff(self) -> CoverageIffClauseSyntax: ...

    @iff.setter
    def iff(self, arg: CoverageIffClauseSyntax, /) -> None: ...

    @property
    def openBrace(self) -> pyslang.parsing.Token: ...

    @openBrace.setter
    def openBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def closeBrace(self) -> pyslang.parsing.Token: ...

    @closeBrace.setter
    def closeBrace(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def emptySemi(self) -> pyslang.parsing.Token: ...

    @emptySemi.setter
    def emptySemi(self, arg: pyslang.parsing.Token, /) -> None: ...

class BinsSelectExpressionSyntax(SyntaxNode):
    pass

class IntersectClauseSyntax(SyntaxNode):
    @property
    def intersect(self) -> pyslang.parsing.Token: ...

    @intersect.setter
    def intersect(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def ranges(self) -> RangeListSyntax: ...

    @ranges.setter
    def ranges(self, arg: RangeListSyntax, /) -> None: ...

class BinsSelectConditionExprSyntax(BinsSelectExpressionSyntax):
    @property
    def binsof(self) -> pyslang.parsing.Token: ...

    @binsof.setter
    def binsof(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> NameSyntax: ...

    @name.setter
    def name(self, arg: NameSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def intersects(self) -> IntersectClauseSyntax: ...

    @intersects.setter
    def intersects(self, arg: IntersectClauseSyntax, /) -> None: ...

class UnaryBinsSelectExprSyntax(BinsSelectExpressionSyntax):
    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> BinsSelectConditionExprSyntax: ...

    @expr.setter
    def expr(self, arg: BinsSelectConditionExprSyntax, /) -> None: ...

class BinaryBinsSelectExprSyntax(BinsSelectExpressionSyntax):
    @property
    def left(self) -> BinsSelectExpressionSyntax: ...

    @left.setter
    def left(self, arg: BinsSelectExpressionSyntax, /) -> None: ...

    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> BinsSelectExpressionSyntax: ...

    @right.setter
    def right(self, arg: BinsSelectExpressionSyntax, /) -> None: ...

class ParenthesizedBinsSelectExprSyntax(BinsSelectExpressionSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> BinsSelectExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: BinsSelectExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class SimpleBinsSelectExprSyntax(BinsSelectExpressionSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def matchesClause(self) -> MatchesClauseSyntax: ...

    @matchesClause.setter
    def matchesClause(self, arg: MatchesClauseSyntax, /) -> None: ...

class BinSelectWithFilterExprSyntax(BinsSelectExpressionSyntax):
    @property
    def expr(self) -> BinsSelectExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: BinsSelectExpressionSyntax, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def filter(self) -> ExpressionSyntax: ...

    @filter.setter
    def filter(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def matchesClause(self) -> MatchesClauseSyntax: ...

    @matchesClause.setter
    def matchesClause(self, arg: MatchesClauseSyntax, /) -> None: ...

class BinsSelectionSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> BinsSelectExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: BinsSelectExpressionSyntax, /) -> None: ...

    @property
    def iff(self) -> CoverageIffClauseSyntax: ...

    @iff.setter
    def iff(self, arg: CoverageIffClauseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class SequenceRepetitionSyntax(SyntaxNode):
    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def selector(self) -> SelectorSyntax: ...

    @selector.setter
    def selector(self, arg: SelectorSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

class SimpleSequenceExprSyntax(SequenceExprSyntax):
    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def repetition(self) -> SequenceRepetitionSyntax: ...

    @repetition.setter
    def repetition(self, arg: SequenceRepetitionSyntax, /) -> None: ...

class SequenceMatchListSyntax(SyntaxNode):
    @property
    def comma(self) -> pyslang.parsing.Token: ...

    @comma.setter
    def comma(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SeparatedSyntaxList: ...

    @items.setter
    def items(self, arg: SeparatedSyntaxList, /) -> None: ...

class ParenthesizedSequenceExprSyntax(SequenceExprSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> SequenceExprSyntax: ...

    @expr.setter
    def expr(self, arg: SequenceExprSyntax, /) -> None: ...

    @property
    def matchList(self) -> SequenceMatchListSyntax: ...

    @matchList.setter
    def matchList(self, arg: SequenceMatchListSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def repetition(self) -> SequenceRepetitionSyntax: ...

    @repetition.setter
    def repetition(self, arg: SequenceRepetitionSyntax, /) -> None: ...

class BinarySequenceExprSyntax(SequenceExprSyntax):
    @property
    def left(self) -> SequenceExprSyntax: ...

    @left.setter
    def left(self, arg: SequenceExprSyntax, /) -> None: ...

    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> SequenceExprSyntax: ...

    @right.setter
    def right(self, arg: SequenceExprSyntax, /) -> None: ...

class FirstMatchSequenceExprSyntax(SequenceExprSyntax):
    @property
    def first_match(self) -> pyslang.parsing.Token: ...

    @first_match.setter
    def first_match(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> SequenceExprSyntax: ...

    @expr.setter
    def expr(self, arg: SequenceExprSyntax, /) -> None: ...

    @property
    def matchList(self) -> SequenceMatchListSyntax: ...

    @matchList.setter
    def matchList(self, arg: SequenceMatchListSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ClockingSequenceExprSyntax(SequenceExprSyntax):
    @property
    def event(self) -> TimingControlSyntax: ...

    @event.setter
    def event(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def expr(self) -> SequenceExprSyntax: ...

    @expr.setter
    def expr(self, arg: SequenceExprSyntax, /) -> None: ...

class DelayedSequenceElementSyntax(SyntaxNode):
    @property
    def doubleHash(self) -> pyslang.parsing.Token: ...

    @doubleHash.setter
    def doubleHash(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def delayVal(self) -> ExpressionSyntax: ...

    @delayVal.setter
    def delayVal(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def range(self) -> SelectorSyntax: ...

    @range.setter
    def range(self, arg: SelectorSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> SequenceExprSyntax: ...

    @expr.setter
    def expr(self, arg: SequenceExprSyntax, /) -> None: ...

class DelayedSequenceExprSyntax(SequenceExprSyntax):
    @property
    def first(self) -> SequenceExprSyntax: ...

    @first.setter
    def first(self, arg: SequenceExprSyntax, /) -> None: ...

    @property
    def elements(self) -> SyntaxList: ...

    @elements.setter
    def elements(self, arg: SyntaxList, /) -> None: ...

class SimplePropertyExprSyntax(PropertyExprSyntax):
    @property
    def expr(self) -> SequenceExprSyntax: ...

    @expr.setter
    def expr(self, arg: SequenceExprSyntax, /) -> None: ...

class ParenthesizedPropertyExprSyntax(PropertyExprSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

    @property
    def matchList(self) -> SequenceMatchListSyntax: ...

    @matchList.setter
    def matchList(self, arg: SequenceMatchListSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class StrongWeakPropertyExprSyntax(PropertyExprSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> SequenceExprSyntax: ...

    @expr.setter
    def expr(self, arg: SequenceExprSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class UnaryPropertyExprSyntax(PropertyExprSyntax):
    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class UnarySelectPropertyExprSyntax(PropertyExprSyntax):
    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openBracket(self) -> pyslang.parsing.Token: ...

    @openBracket.setter
    def openBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def selector(self) -> SelectorSyntax: ...

    @selector.setter
    def selector(self, arg: SelectorSyntax, /) -> None: ...

    @property
    def closeBracket(self) -> pyslang.parsing.Token: ...

    @closeBracket.setter
    def closeBracket(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class BinaryPropertyExprSyntax(PropertyExprSyntax):
    @property
    def left(self) -> PropertyExprSyntax: ...

    @left.setter
    def left(self, arg: PropertyExprSyntax, /) -> None: ...

    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> PropertyExprSyntax: ...

    @right.setter
    def right(self, arg: PropertyExprSyntax, /) -> None: ...

class ClockingPropertyExprSyntax(PropertyExprSyntax):
    @property
    def event(self) -> TimingControlSyntax: ...

    @event.setter
    def event(self, arg: TimingControlSyntax, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class AcceptOnPropertyExprSyntax(PropertyExprSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def condition(self) -> ExpressionSyntax: ...

    @condition.setter
    def condition(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class ElsePropertyClauseSyntax(SyntaxNode):
    @property
    def elseKeyword(self) -> pyslang.parsing.Token: ...

    @elseKeyword.setter
    def elseKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

class ConditionalPropertyExprSyntax(PropertyExprSyntax):
    @property
    def ifKeyword(self) -> pyslang.parsing.Token: ...

    @ifKeyword.setter
    def ifKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def condition(self) -> ExpressionSyntax: ...

    @condition.setter
    def condition(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

    @property
    def elseClause(self) -> ElsePropertyClauseSyntax: ...

    @elseClause.setter
    def elseClause(self, arg: ElsePropertyClauseSyntax, /) -> None: ...

class PropertyCaseItemSyntax(SyntaxNode):
    pass

class DefaultPropertyCaseItemSyntax(PropertyCaseItemSyntax):
    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class StandardPropertyCaseItemSyntax(PropertyCaseItemSyntax):
    @property
    def expressions(self) -> SeparatedSyntaxList: ...

    @expressions.setter
    def expressions(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> PropertyExprSyntax: ...

    @expr.setter
    def expr(self, arg: PropertyExprSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class CasePropertyExprSyntax(PropertyExprSyntax):
    @property
    def caseKeyword(self) -> pyslang.parsing.Token: ...

    @caseKeyword.setter
    def caseKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def expr(self) -> ExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def items(self) -> SyntaxList: ...

    @items.setter
    def items(self, arg: SyntaxList, /) -> None: ...

    @property
    def endcase(self) -> pyslang.parsing.Token: ...

    @endcase.setter
    def endcase(self, arg: pyslang.parsing.Token, /) -> None: ...

class LocalVariableDeclarationSyntax(MemberSyntax):
    @property
    def var(self) -> pyslang.parsing.Token: ...

    @var.setter
    def var(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def type(self) -> DataTypeSyntax: ...

    @type.setter
    def type(self, arg: DataTypeSyntax, /) -> None: ...

    @property
    def declarators(self) -> SeparatedSyntaxList: ...

    @declarators.setter
    def declarators(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class PropertyDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> AssertionItemPortListSyntax: ...

    @portList.setter
    def portList(self, arg: AssertionItemPortListSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def variables(self) -> SyntaxList: ...

    @variables.setter
    def variables(self, arg: SyntaxList, /) -> None: ...

    @property
    def propertySpec(self) -> PropertySpecSyntax: ...

    @propertySpec.setter
    def propertySpec(self, arg: PropertySpecSyntax, /) -> None: ...

    @property
    def optionalSemi(self) -> pyslang.parsing.Token: ...

    @optionalSemi.setter
    def optionalSemi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def end(self) -> pyslang.parsing.Token: ...

    @end.setter
    def end(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class SequenceDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> AssertionItemPortListSyntax: ...

    @portList.setter
    def portList(self, arg: AssertionItemPortListSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def variables(self) -> SyntaxList: ...

    @variables.setter
    def variables(self, arg: SyntaxList, /) -> None: ...

    @property
    def seqExpr(self) -> SequenceExprSyntax: ...

    @seqExpr.setter
    def seqExpr(self, arg: SequenceExprSyntax, /) -> None: ...

    @property
    def optionalSemi(self) -> pyslang.parsing.Token: ...

    @optionalSemi.setter
    def optionalSemi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def end(self) -> pyslang.parsing.Token: ...

    @end.setter
    def end(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class CheckerDeclarationSyntax(MemberSyntax):
    @property
    def keyword(self) -> pyslang.parsing.Token: ...

    @keyword.setter
    def keyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def portList(self) -> AssertionItemPortListSyntax: ...

    @portList.setter
    def portList(self, arg: AssertionItemPortListSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def end(self) -> pyslang.parsing.Token: ...

    @end.setter
    def end(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def endBlockName(self) -> NamedBlockClauseSyntax: ...

    @endBlockName.setter
    def endBlockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class CheckerDataDeclarationSyntax(MemberSyntax):
    @property
    def rand(self) -> pyslang.parsing.Token: ...

    @rand.setter
    def rand(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def data(self) -> DataDeclarationSyntax: ...

    @data.setter
    def data(self, arg: DataDeclarationSyntax, /) -> None: ...

class CompilationUnitSyntax(SyntaxNode):
    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def endOfFile(self) -> pyslang.parsing.Token: ...

    @endOfFile.setter
    def endOfFile(self, arg: pyslang.parsing.Token, /) -> None: ...

class LibraryMapSyntax(SyntaxNode):
    @property
    def members(self) -> SyntaxList: ...

    @members.setter
    def members(self, arg: SyntaxList, /) -> None: ...

    @property
    def endOfFile(self) -> pyslang.parsing.Token: ...

    @endOfFile.setter
    def endOfFile(self, arg: pyslang.parsing.Token, /) -> None: ...

class DirectiveSyntax(SyntaxNode):
    @property
    def directive(self) -> pyslang.parsing.Token: ...

    @directive.setter
    def directive(self, arg: pyslang.parsing.Token, /) -> None: ...

class SimpleDirectiveSyntax(DirectiveSyntax):
    pass

class IncludeDirectiveSyntax(DirectiveSyntax):
    @property
    def fileName(self) -> pyslang.parsing.Token: ...

    @fileName.setter
    def fileName(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConditionalDirectiveExpressionSyntax(SyntaxNode):
    pass

class NamedConditionalDirectiveExpressionSyntax(ConditionalDirectiveExpressionSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

class UnaryConditionalDirectiveExpressionSyntax(ConditionalDirectiveExpressionSyntax):
    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def operand(self) -> ConditionalDirectiveExpressionSyntax: ...

    @operand.setter
    def operand(self, arg: ConditionalDirectiveExpressionSyntax, /) -> None: ...

class BinaryConditionalDirectiveExpressionSyntax(ConditionalDirectiveExpressionSyntax):
    @property
    def left(self) -> ConditionalDirectiveExpressionSyntax: ...

    @left.setter
    def left(self, arg: ConditionalDirectiveExpressionSyntax, /) -> None: ...

    @property
    def op(self) -> pyslang.parsing.Token: ...

    @op.setter
    def op(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def right(self) -> ConditionalDirectiveExpressionSyntax: ...

    @right.setter
    def right(self, arg: ConditionalDirectiveExpressionSyntax, /) -> None: ...

class ParenthesizedConditionalDirectiveExpressionSyntax(ConditionalDirectiveExpressionSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def operand(self) -> ConditionalDirectiveExpressionSyntax: ...

    @operand.setter
    def operand(self, arg: ConditionalDirectiveExpressionSyntax, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConditionalBranchDirectiveSyntax(DirectiveSyntax):
    @property
    def expr(self) -> ConditionalDirectiveExpressionSyntax: ...

    @expr.setter
    def expr(self, arg: ConditionalDirectiveExpressionSyntax, /) -> None: ...

    @property
    def disabledTokens(self) -> TokenList: ...

    @disabledTokens.setter
    def disabledTokens(self, arg: TokenList, /) -> None: ...

class UnconditionalBranchDirectiveSyntax(DirectiveSyntax):
    @property
    def disabledTokens(self) -> TokenList: ...

    @disabledTokens.setter
    def disabledTokens(self, arg: TokenList, /) -> None: ...

class MacroArgumentDefaultSyntax(SyntaxNode):
    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def tokens(self) -> TokenList: ...

    @tokens.setter
    def tokens(self, arg: TokenList, /) -> None: ...

class MacroFormalArgumentSyntax(SyntaxNode):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def defaultValue(self) -> MacroArgumentDefaultSyntax: ...

    @defaultValue.setter
    def defaultValue(self, arg: MacroArgumentDefaultSyntax, /) -> None: ...

class MacroFormalArgumentListSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def args(self) -> SeparatedSyntaxList: ...

    @args.setter
    def args(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class DefineDirectiveSyntax(DirectiveSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def formalArguments(self) -> MacroFormalArgumentListSyntax: ...

    @formalArguments.setter
    def formalArguments(self, arg: MacroFormalArgumentListSyntax, /) -> None: ...

    @property
    def body(self) -> TokenList: ...

    @body.setter
    def body(self, arg: TokenList, /) -> None: ...

class MacroActualArgumentSyntax(SyntaxNode):
    @property
    def tokens(self) -> TokenList: ...

    @tokens.setter
    def tokens(self, arg: TokenList, /) -> None: ...

class MacroActualArgumentListSyntax(SyntaxNode):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def args(self) -> SeparatedSyntaxList: ...

    @args.setter
    def args(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class MacroUsageSyntax(DirectiveSyntax):
    @property
    def args(self) -> MacroActualArgumentListSyntax: ...

    @args.setter
    def args(self, arg: MacroActualArgumentListSyntax, /) -> None: ...

class TimeScaleDirectiveSyntax(DirectiveSyntax):
    @property
    def timeUnit(self) -> pyslang.parsing.Token: ...

    @timeUnit.setter
    def timeUnit(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def slash(self) -> pyslang.parsing.Token: ...

    @slash.setter
    def slash(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def timePrecision(self) -> pyslang.parsing.Token: ...

    @timePrecision.setter
    def timePrecision(self, arg: pyslang.parsing.Token, /) -> None: ...

class DefaultNetTypeDirectiveSyntax(DirectiveSyntax):
    @property
    def netType(self) -> pyslang.parsing.Token: ...

    @netType.setter
    def netType(self, arg: pyslang.parsing.Token, /) -> None: ...

class UnconnectedDriveDirectiveSyntax(DirectiveSyntax):
    @property
    def strength(self) -> pyslang.parsing.Token: ...

    @strength.setter
    def strength(self, arg: pyslang.parsing.Token, /) -> None: ...

class DefaultDecayTimeDirectiveSyntax(DirectiveSyntax):
    @property
    def time(self) -> pyslang.parsing.Token: ...

    @time.setter
    def time(self, arg: pyslang.parsing.Token, /) -> None: ...

class DefaultTriregStrengthDirectiveSyntax(DirectiveSyntax):
    @property
    def strength(self) -> pyslang.parsing.Token: ...

    @strength.setter
    def strength(self, arg: pyslang.parsing.Token, /) -> None: ...

class LineDirectiveSyntax(DirectiveSyntax):
    @property
    def lineNumber(self) -> pyslang.parsing.Token: ...

    @lineNumber.setter
    def lineNumber(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def fileName(self) -> pyslang.parsing.Token: ...

    @fileName.setter
    def fileName(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def level(self) -> pyslang.parsing.Token: ...

    @level.setter
    def level(self, arg: pyslang.parsing.Token, /) -> None: ...

class UndefDirectiveSyntax(DirectiveSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

class BeginKeywordsDirectiveSyntax(DirectiveSyntax):
    @property
    def versionSpecifier(self) -> pyslang.parsing.Token: ...

    @versionSpecifier.setter
    def versionSpecifier(self, arg: pyslang.parsing.Token, /) -> None: ...

class PragmaExpressionSyntax(SyntaxNode):
    pass

class SimplePragmaExpressionSyntax(PragmaExpressionSyntax):
    @property
    def value(self) -> pyslang.parsing.Token: ...

    @value.setter
    def value(self, arg: pyslang.parsing.Token, /) -> None: ...

class NameValuePragmaExpressionSyntax(PragmaExpressionSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def equals(self) -> pyslang.parsing.Token: ...

    @equals.setter
    def equals(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def value(self) -> PragmaExpressionSyntax: ...

    @value.setter
    def value(self, arg: PragmaExpressionSyntax, /) -> None: ...

class NumberPragmaExpressionSyntax(PragmaExpressionSyntax):
    @property
    def size(self) -> pyslang.parsing.Token: ...

    @size.setter
    def size(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def base(self) -> pyslang.parsing.Token: ...

    @base.setter
    def base(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def value(self) -> pyslang.parsing.Token: ...

    @value.setter
    def value(self, arg: pyslang.parsing.Token, /) -> None: ...

class ParenPragmaExpressionSyntax(PragmaExpressionSyntax):
    @property
    def openParen(self) -> pyslang.parsing.Token: ...

    @openParen.setter
    def openParen(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def values(self) -> SeparatedSyntaxList: ...

    @values.setter
    def values(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def closeParen(self) -> pyslang.parsing.Token: ...

    @closeParen.setter
    def closeParen(self, arg: pyslang.parsing.Token, /) -> None: ...

class PragmaDirectiveSyntax(DirectiveSyntax):
    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def args(self) -> SeparatedSyntaxList: ...

    @args.setter
    def args(self, arg: SeparatedSyntaxList, /) -> None: ...

class ConfigCellIdentifierSyntax(SyntaxNode):
    @property
    def library(self) -> pyslang.parsing.Token: ...

    @library.setter
    def library(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def cell(self) -> pyslang.parsing.Token: ...

    @cell.setter
    def cell(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConfigRuleClauseSyntax(SyntaxNode):
    pass

class ConfigLiblistSyntax(ConfigRuleClauseSyntax):
    @property
    def liblist(self) -> pyslang.parsing.Token: ...

    @liblist.setter
    def liblist(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def libraries(self) -> TokenList: ...

    @libraries.setter
    def libraries(self, arg: TokenList, /) -> None: ...

class ConfigUseClauseSyntax(ConfigRuleClauseSyntax):
    @property
    def use(self) -> pyslang.parsing.Token: ...

    @use.setter
    def use(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> ConfigCellIdentifierSyntax: ...

    @name.setter
    def name(self, arg: ConfigCellIdentifierSyntax, /) -> None: ...

    @property
    def paramAssignments(self) -> ParameterValueAssignmentSyntax: ...

    @paramAssignments.setter
    def paramAssignments(self, arg: ParameterValueAssignmentSyntax, /) -> None: ...

    @property
    def colon(self) -> pyslang.parsing.Token: ...

    @colon.setter
    def colon(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def config(self) -> pyslang.parsing.Token: ...

    @config.setter
    def config(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConfigRuleSyntax(SyntaxNode):
    pass

class DefaultConfigRuleSyntax(ConfigRuleSyntax):
    @property
    def defaultKeyword(self) -> pyslang.parsing.Token: ...

    @defaultKeyword.setter
    def defaultKeyword(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def liblist(self) -> ConfigLiblistSyntax: ...

    @liblist.setter
    def liblist(self, arg: ConfigLiblistSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConfigInstanceIdentifierSyntax(SyntaxNode):
    @property
    def dot(self) -> pyslang.parsing.Token: ...

    @dot.setter
    def dot(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

class InstanceConfigRuleSyntax(ConfigRuleSyntax):
    @property
    def instance(self) -> pyslang.parsing.Token: ...

    @instance.setter
    def instance(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def topModule(self) -> pyslang.parsing.Token: ...

    @topModule.setter
    def topModule(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def instanceNames(self) -> SyntaxList: ...

    @instanceNames.setter
    def instanceNames(self, arg: SyntaxList, /) -> None: ...

    @property
    def ruleClause(self) -> ConfigRuleClauseSyntax: ...

    @ruleClause.setter
    def ruleClause(self, arg: ConfigRuleClauseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class CellConfigRuleSyntax(ConfigRuleSyntax):
    @property
    def cell(self) -> pyslang.parsing.Token: ...

    @cell.setter
    def cell(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> ConfigCellIdentifierSyntax: ...

    @name.setter
    def name(self, arg: ConfigCellIdentifierSyntax, /) -> None: ...

    @property
    def ruleClause(self) -> ConfigRuleClauseSyntax: ...

    @ruleClause.setter
    def ruleClause(self, arg: ConfigRuleClauseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class ConfigDeclarationSyntax(MemberSyntax):
    @property
    def config(self) -> pyslang.parsing.Token: ...

    @config.setter
    def config(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def semi1(self) -> pyslang.parsing.Token: ...

    @semi1.setter
    def semi1(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def localparams(self) -> SyntaxList: ...

    @localparams.setter
    def localparams(self, arg: SyntaxList, /) -> None: ...

    @property
    def design(self) -> pyslang.parsing.Token: ...

    @design.setter
    def design(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def topCells(self) -> SyntaxList: ...

    @topCells.setter
    def topCells(self, arg: SyntaxList, /) -> None: ...

    @property
    def semi2(self) -> pyslang.parsing.Token: ...

    @semi2.setter
    def semi2(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def rules(self) -> SyntaxList: ...

    @rules.setter
    def rules(self, arg: SyntaxList, /) -> None: ...

    @property
    def endconfig(self) -> pyslang.parsing.Token: ...

    @endconfig.setter
    def endconfig(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def blockName(self) -> NamedBlockClauseSyntax: ...

    @blockName.setter
    def blockName(self, arg: NamedBlockClauseSyntax, /) -> None: ...

class FilePathSpecSyntax(SyntaxNode):
    @property
    def path(self) -> pyslang.parsing.Token: ...

    @path.setter
    def path(self, arg: pyslang.parsing.Token, /) -> None: ...

class LibraryIncDirClauseSyntax(SyntaxNode):
    @property
    def minus(self) -> pyslang.parsing.Token: ...

    @minus.setter
    def minus(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def incdir(self) -> pyslang.parsing.Token: ...

    @incdir.setter
    def incdir(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def filePaths(self) -> SeparatedSyntaxList: ...

    @filePaths.setter
    def filePaths(self, arg: SeparatedSyntaxList, /) -> None: ...

class LibraryDeclarationSyntax(MemberSyntax):
    @property
    def library(self) -> pyslang.parsing.Token: ...

    @library.setter
    def library(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def name(self) -> pyslang.parsing.Token: ...

    @name.setter
    def name(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def filePaths(self) -> SeparatedSyntaxList: ...

    @filePaths.setter
    def filePaths(self, arg: SeparatedSyntaxList, /) -> None: ...

    @property
    def incDirClause(self) -> LibraryIncDirClauseSyntax: ...

    @incDirClause.setter
    def incDirClause(self, arg: LibraryIncDirClauseSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class LibraryIncludeStatementSyntax(MemberSyntax):
    @property
    def include(self) -> pyslang.parsing.Token: ...

    @include.setter
    def include(self, arg: pyslang.parsing.Token, /) -> None: ...

    @property
    def filePath(self) -> FilePathSpecSyntax: ...

    @filePath.setter
    def filePath(self, arg: FilePathSpecSyntax, /) -> None: ...

    @property
    def semi(self) -> pyslang.parsing.Token: ...

    @semi.setter
    def semi(self, arg: pyslang.parsing.Token, /) -> None: ...

class SyntaxFactory:
    """Factory for creating syntax nodes. Access via SyntaxRewriter.factory."""

    def acceptOnPropertyExpr(self, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, condition: ExpressionSyntax, closeParen: pyslang.parsing.Token, expr: PropertyExprSyntax) -> AcceptOnPropertyExprSyntax: ...

    def actionBlock(self, statement: StatementSyntax | None = None, elseClause: ElseClauseSyntax | None = None) -> ActionBlockSyntax: ...

    def anonymousProgram(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, semi: pyslang.parsing.Token, members: SyntaxList, endkeyword: pyslang.parsing.Token) -> AnonymousProgramSyntax: ...

    def ansiPortList(self, openParen: pyslang.parsing.Token, ports: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> AnsiPortListSyntax: ...

    def ansiUdpPortList(self, openParen: pyslang.parsing.Token, ports: SeparatedSyntaxList, closeParen: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> AnsiUdpPortListSyntax: ...

    def argumentList(self, openParen: pyslang.parsing.Token, parameters: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> ArgumentListSyntax: ...

    def arrayOrRandomizeMethodExpression(self, method: ExpressionSyntax, with_: pyslang.parsing.Token, args: ParenExpressionListSyntax | None = None, constraints: ConstraintBlockSyntax | None = None) -> ArrayOrRandomizeMethodExpressionSyntax: ...

    def assertionItemPortList(self, openParen: pyslang.parsing.Token, ports: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> AssertionItemPortListSyntax: ...

    def assertionItemPort(self, attributes: SyntaxList, local: pyslang.parsing.Token, direction: pyslang.parsing.Token, type: DataTypeSyntax, name: pyslang.parsing.Token, dimensions: SyntaxList, defaultValue: EqualsAssertionArgClauseSyntax | None = None) -> AssertionItemPortSyntax: ...

    def assignmentPatternExpression(self, type: DataTypeSyntax | None, pattern: AssignmentPatternSyntax) -> AssignmentPatternExpressionSyntax: ...

    def assignmentPatternItem(self, key: ExpressionSyntax, colon: pyslang.parsing.Token, expr: ExpressionSyntax) -> AssignmentPatternItemSyntax: ...

    def attributeInstance(self, openParen: pyslang.parsing.Token, openStar: pyslang.parsing.Token, specs: SeparatedSyntaxList, closeStar: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> AttributeInstanceSyntax: ...

    def attributeSpec(self, name: pyslang.parsing.Token, value: EqualsValueClauseSyntax | None = None) -> AttributeSpecSyntax: ...

    def badExpression(self, expr: ExpressionSyntax) -> BadExpressionSyntax: ...

    def beginKeywordsDirective(self, directive: pyslang.parsing.Token, versionSpecifier: pyslang.parsing.Token) -> BeginKeywordsDirectiveSyntax: ...

    def binSelectWithFilterExpr(self, expr: BinsSelectExpressionSyntax, with_: pyslang.parsing.Token, openParen: pyslang.parsing.Token, filter: ExpressionSyntax, closeParen: pyslang.parsing.Token, matchesClause: MatchesClauseSyntax | None = None) -> BinSelectWithFilterExprSyntax: ...

    def binaryBinsSelectExpr(self, left: BinsSelectExpressionSyntax, op: pyslang.parsing.Token, right: BinsSelectExpressionSyntax) -> BinaryBinsSelectExprSyntax: ...

    def binaryBlockEventExpression(self, left: BlockEventExpressionSyntax, orKeyword: pyslang.parsing.Token, right: BlockEventExpressionSyntax) -> BinaryBlockEventExpressionSyntax: ...

    def binaryConditionalDirectiveExpression(self, left: ConditionalDirectiveExpressionSyntax, op: pyslang.parsing.Token, right: ConditionalDirectiveExpressionSyntax) -> BinaryConditionalDirectiveExpressionSyntax: ...

    def binaryEventExpression(self, left: EventExpressionSyntax, operatorToken: pyslang.parsing.Token, right: EventExpressionSyntax) -> BinaryEventExpressionSyntax: ...

    def binaryExpression(self, kind: SyntaxKind, left: ExpressionSyntax, operatorToken: pyslang.parsing.Token, attributes: SyntaxList, right: ExpressionSyntax) -> BinaryExpressionSyntax: ...

    def binaryPropertyExpr(self, kind: SyntaxKind, left: PropertyExprSyntax, op: pyslang.parsing.Token, right: PropertyExprSyntax) -> BinaryPropertyExprSyntax: ...

    def binarySequenceExpr(self, kind: SyntaxKind, left: SequenceExprSyntax, op: pyslang.parsing.Token, right: SequenceExprSyntax) -> BinarySequenceExprSyntax: ...

    def bindDirective(self, attributes: SyntaxList, bind: pyslang.parsing.Token, target: NameSyntax, targetInstances: BindTargetListSyntax | None, instantiation: MemberSyntax) -> BindDirectiveSyntax: ...

    def bindTargetList(self, colon: pyslang.parsing.Token, targets: SeparatedSyntaxList) -> BindTargetListSyntax: ...

    def binsSelectConditionExpr(self, binsof: pyslang.parsing.Token, openParen: pyslang.parsing.Token, name: NameSyntax, closeParen: pyslang.parsing.Token, intersects: IntersectClauseSyntax | None = None) -> BinsSelectConditionExprSyntax: ...

    def binsSelection(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, name: pyslang.parsing.Token, equals: pyslang.parsing.Token, expr: BinsSelectExpressionSyntax, iff: CoverageIffClauseSyntax | None, semi: pyslang.parsing.Token) -> BinsSelectionSyntax: ...

    def bitSelect(self, expr: ExpressionSyntax) -> BitSelectSyntax: ...

    def blockCoverageEvent(self, atat: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: BlockEventExpressionSyntax, closeParen: pyslang.parsing.Token) -> BlockCoverageEventSyntax: ...

    def blockStatement(self, kind: SyntaxKind, label: NamedLabelSyntax | None, attributes: SyntaxList, begin: pyslang.parsing.Token, blockName: NamedBlockClauseSyntax | None, items: SyntaxList, end: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> BlockStatementSyntax: ...

    def caseGenerate(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, condition: ExpressionSyntax, closeParen: pyslang.parsing.Token, items: SyntaxList, endCase: pyslang.parsing.Token) -> CaseGenerateSyntax: ...

    def casePropertyExpr(self, caseKeyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, items: SyntaxList, endcase: pyslang.parsing.Token) -> CasePropertyExprSyntax: ...

    def caseStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, uniqueOrPriority: pyslang.parsing.Token, caseKeyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, matchesOrInside: pyslang.parsing.Token, items: SyntaxList, endcase: pyslang.parsing.Token) -> CaseStatementSyntax: ...

    def castExpression(self, left: ExpressionSyntax, apostrophe: pyslang.parsing.Token, right: ParenthesizedExpressionSyntax) -> CastExpressionSyntax: ...

    def cellConfigRule(self, cell: pyslang.parsing.Token, name: ConfigCellIdentifierSyntax, ruleClause: ConfigRuleClauseSyntax, semi: pyslang.parsing.Token) -> CellConfigRuleSyntax: ...

    def chargeStrength(self, openParen: pyslang.parsing.Token, strength: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> ChargeStrengthSyntax: ...

    def checkerDataDeclaration(self, attributes: SyntaxList, rand: pyslang.parsing.Token, data: DataDeclarationSyntax) -> CheckerDataDeclarationSyntax: ...

    def checkerDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, name: pyslang.parsing.Token, portList: AssertionItemPortListSyntax | None, semi: pyslang.parsing.Token, members: SyntaxList, end: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> CheckerDeclarationSyntax: ...

    def checkerInstanceStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, instance: CheckerInstantiationSyntax) -> CheckerInstanceStatementSyntax: ...

    def checkerInstantiation(self, attributes: SyntaxList, type: NameSyntax, parameters: ParameterValueAssignmentSyntax | None, instances: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> CheckerInstantiationSyntax: ...

    def classDeclaration(self, attributes: SyntaxList, virtualOrInterface: pyslang.parsing.Token, classKeyword: pyslang.parsing.Token, finalSpecifier: ClassSpecifierSyntax | None, name: pyslang.parsing.Token, parameters: ParameterPortListSyntax | None, extendsClause: ExtendsClauseSyntax | None, implementsClause: ImplementsClauseSyntax | None, semi: pyslang.parsing.Token, items: SyntaxList, endClass: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> ClassDeclarationSyntax: ...

    def classMethodDeclaration(self, attributes: SyntaxList, qualifiers: TokenList, declaration: FunctionDeclarationSyntax) -> ClassMethodDeclarationSyntax: ...

    def classMethodPrototype(self, attributes: SyntaxList, qualifiers: TokenList, prototype: FunctionPrototypeSyntax, semi: pyslang.parsing.Token) -> ClassMethodPrototypeSyntax: ...

    def className(self, identifier: pyslang.parsing.Token, parameters: ParameterValueAssignmentSyntax) -> ClassNameSyntax: ...

    def classPropertyDeclaration(self, attributes: SyntaxList, qualifiers: TokenList, declaration: MemberSyntax) -> ClassPropertyDeclarationSyntax: ...

    def classSpecifier(self, colon: pyslang.parsing.Token, keyword: pyslang.parsing.Token) -> ClassSpecifierSyntax: ...

    def clockingDeclaration(self, attributes: SyntaxList, globalOrDefault: pyslang.parsing.Token, clocking: pyslang.parsing.Token, blockName: pyslang.parsing.Token, at: pyslang.parsing.Token, event: EventExpressionSyntax, semi: pyslang.parsing.Token, items: SyntaxList, endClocking: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> ClockingDeclarationSyntax: ...

    def clockingDirection(self, input: pyslang.parsing.Token, inputSkew: ClockingSkewSyntax | None, output: pyslang.parsing.Token, outputSkew: ClockingSkewSyntax | None = None) -> ClockingDirectionSyntax: ...

    def clockingItem(self, attributes: SyntaxList, direction: ClockingDirectionSyntax, decls: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> ClockingItemSyntax: ...

    def clockingPropertyExpr(self, event: TimingControlSyntax, expr: PropertyExprSyntax | None = None) -> ClockingPropertyExprSyntax: ...

    def clockingSequenceExpr(self, event: TimingControlSyntax, expr: SequenceExprSyntax) -> ClockingSequenceExprSyntax: ...

    def clockingSkew(self, edge: pyslang.parsing.Token, delay: TimingControlSyntax | None = None) -> ClockingSkewSyntax: ...

    def colonExpressionClause(self, colon: pyslang.parsing.Token, expr: ExpressionSyntax) -> ColonExpressionClauseSyntax: ...

    def compilationUnit(self, members: SyntaxList, endOfFile: pyslang.parsing.Token) -> CompilationUnitSyntax: ...

    def concatenationExpression(self, openBrace: pyslang.parsing.Token, expressions: SeparatedSyntaxList, closeBrace: pyslang.parsing.Token) -> ConcatenationExpressionSyntax: ...

    def concurrentAssertionMember(self, attributes: SyntaxList, statement: ConcurrentAssertionStatementSyntax) -> ConcurrentAssertionMemberSyntax: ...

    def concurrentAssertionStatement(self, kind: SyntaxKind, label: NamedLabelSyntax | None, attributes: SyntaxList, keyword: pyslang.parsing.Token, propertyOrSequence: pyslang.parsing.Token, openParen: pyslang.parsing.Token, propertySpec: PropertySpecSyntax, closeParen: pyslang.parsing.Token, action: ActionBlockSyntax) -> ConcurrentAssertionStatementSyntax: ...

    def conditionalBranchDirective(self, kind: SyntaxKind, directive: pyslang.parsing.Token, expr: ConditionalDirectiveExpressionSyntax, disabledTokens: TokenList) -> ConditionalBranchDirectiveSyntax: ...

    def conditionalConstraint(self, ifKeyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, condition: ExpressionSyntax, closeParen: pyslang.parsing.Token, constraints: ConstraintItemSyntax, elseClause: ElseConstraintClauseSyntax | None = None) -> ConditionalConstraintSyntax: ...

    def conditionalExpression(self, predicate: ConditionalPredicateSyntax, question: pyslang.parsing.Token, attributes: SyntaxList, left: ExpressionSyntax, colon: pyslang.parsing.Token, right: ExpressionSyntax) -> ConditionalExpressionSyntax: ...

    def conditionalPathDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, predicate: ExpressionSyntax, closeParen: pyslang.parsing.Token, path: PathDeclarationSyntax) -> ConditionalPathDeclarationSyntax: ...

    def conditionalPattern(self, expr: ExpressionSyntax, matchesClause: MatchesClauseSyntax | None = None) -> ConditionalPatternSyntax: ...

    def conditionalPredicate(self, conditions: SeparatedSyntaxList) -> ConditionalPredicateSyntax: ...

    def conditionalPropertyExpr(self, ifKeyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, condition: ExpressionSyntax, closeParen: pyslang.parsing.Token, expr: PropertyExprSyntax, elseClause: ElsePropertyClauseSyntax | None = None) -> ConditionalPropertyExprSyntax: ...

    def conditionalStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, uniqueOrPriority: pyslang.parsing.Token, ifKeyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, predicate: ConditionalPredicateSyntax, closeParen: pyslang.parsing.Token, statement: StatementSyntax, elseClause: ElseClauseSyntax | None = None) -> ConditionalStatementSyntax: ...

    def configCellIdentifier(self, library: pyslang.parsing.Token, dot: pyslang.parsing.Token, cell: pyslang.parsing.Token) -> ConfigCellIdentifierSyntax: ...

    def configDeclaration(self, attributes: SyntaxList, config: pyslang.parsing.Token, name: pyslang.parsing.Token, semi1: pyslang.parsing.Token, localparams: SyntaxList, design: pyslang.parsing.Token, topCells: SyntaxList, semi2: pyslang.parsing.Token, rules: SyntaxList, endconfig: pyslang.parsing.Token, blockName: NamedBlockClauseSyntax | None = None) -> ConfigDeclarationSyntax: ...

    def configInstanceIdentifier(self, dot: pyslang.parsing.Token, name: pyslang.parsing.Token) -> ConfigInstanceIdentifierSyntax: ...

    def configLiblist(self, liblist: pyslang.parsing.Token, libraries: TokenList) -> ConfigLiblistSyntax: ...

    def configUseClause(self, use: pyslang.parsing.Token, name: ConfigCellIdentifierSyntax | None, paramAssignments: ParameterValueAssignmentSyntax | None, colon: pyslang.parsing.Token, config: pyslang.parsing.Token) -> ConfigUseClauseSyntax: ...

    def constraintBlock(self, openBrace: pyslang.parsing.Token, items: SyntaxList, closeBrace: pyslang.parsing.Token) -> ConstraintBlockSyntax: ...

    def constraintDeclaration(self, attributes: SyntaxList, qualifiers: TokenList, keyword: pyslang.parsing.Token, specifiers: SyntaxList, name: NameSyntax, block: ConstraintBlockSyntax) -> ConstraintDeclarationSyntax: ...

    def constraintPrototype(self, attributes: SyntaxList, qualifiers: TokenList, keyword: pyslang.parsing.Token, specifiers: SyntaxList, name: NameSyntax, semi: pyslang.parsing.Token) -> ConstraintPrototypeSyntax: ...

    def continuousAssign(self, attributes: SyntaxList, assign: pyslang.parsing.Token, strength: DriveStrengthSyntax | None, delay: TimingControlSyntax | None, assignments: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> ContinuousAssignSyntax: ...

    def copyClassExpression(self, scopedNew: NameSyntax, expr: ExpressionSyntax) -> CopyClassExpressionSyntax: ...

    def coverCross(self, attributes: SyntaxList, label: NamedLabelSyntax | None, cross: pyslang.parsing.Token, items: SeparatedSyntaxList, iff: CoverageIffClauseSyntax | None, openBrace: pyslang.parsing.Token, members: SyntaxList, closeBrace: pyslang.parsing.Token, emptySemi: pyslang.parsing.Token) -> CoverCrossSyntax: ...

    def coverageBinsArraySize(self, openBracket: pyslang.parsing.Token, expr: ExpressionSyntax | None, closeBracket: pyslang.parsing.Token) -> CoverageBinsArraySizeSyntax: ...

    def coverageBins(self, attributes: SyntaxList, wildcard: pyslang.parsing.Token, keyword: pyslang.parsing.Token, name: pyslang.parsing.Token, size: CoverageBinsArraySizeSyntax | None, equals: pyslang.parsing.Token, initializer: CoverageBinInitializerSyntax, iff: CoverageIffClauseSyntax | None, semi: pyslang.parsing.Token) -> CoverageBinsSyntax: ...

    def coverageIffClause(self, iff: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token) -> CoverageIffClauseSyntax: ...

    def coverageOption(self, attributes: SyntaxList, expr: ExpressionSyntax, semi: pyslang.parsing.Token) -> CoverageOptionSyntax: ...

    def covergroupDeclaration(self, attributes: SyntaxList, covergroup: pyslang.parsing.Token, extends: pyslang.parsing.Token, name: pyslang.parsing.Token, portList: FunctionPortListSyntax | None, event: SyntaxNode | None, semi: pyslang.parsing.Token, members: SyntaxList, endgroup: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> CovergroupDeclarationSyntax: ...

    def coverpoint(self, attributes: SyntaxList, type: DataTypeSyntax, label: NamedLabelSyntax | None, coverpoint: pyslang.parsing.Token, expr: ExpressionSyntax, iff: CoverageIffClauseSyntax | None, openBrace: pyslang.parsing.Token, members: SyntaxList, closeBrace: pyslang.parsing.Token, emptySemi: pyslang.parsing.Token) -> CoverpointSyntax: ...

    def dPIExport(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, specString: pyslang.parsing.Token, c_identifier: pyslang.parsing.Token, equals: pyslang.parsing.Token, functionOrTask: pyslang.parsing.Token, name: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> DPIExportSyntax: ...

    def dPIImport(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, specString: pyslang.parsing.Token, property: pyslang.parsing.Token, c_identifier: pyslang.parsing.Token, equals: pyslang.parsing.Token, method: FunctionPrototypeSyntax, semi: pyslang.parsing.Token) -> DPIImportSyntax: ...

    def dataDeclaration(self, attributes: SyntaxList, modifiers: TokenList, type: DataTypeSyntax, declarators: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> DataDeclarationSyntax: ...

    def declarator(self, name: pyslang.parsing.Token, dimensions: SyntaxList, initializer: EqualsValueClauseSyntax | None = None) -> DeclaratorSyntax: ...

    def defParamAssignment(self, name: NameSyntax, setter: EqualsValueClauseSyntax) -> DefParamAssignmentSyntax: ...

    def defParam(self, attributes: SyntaxList, defparam: pyslang.parsing.Token, assignments: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> DefParamSyntax: ...

    def defaultCaseItem(self, defaultKeyword: pyslang.parsing.Token, colon: pyslang.parsing.Token, clause: SyntaxNode) -> DefaultCaseItemSyntax: ...

    def defaultClockingReference(self, attributes: SyntaxList, defaultKeyword: pyslang.parsing.Token, clocking: pyslang.parsing.Token, name: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> DefaultClockingReferenceSyntax: ...

    def defaultConfigRule(self, defaultKeyword: pyslang.parsing.Token, liblist: ConfigLiblistSyntax, semi: pyslang.parsing.Token) -> DefaultConfigRuleSyntax: ...

    def defaultCoverageBinInitializer(self, defaultKeyword: pyslang.parsing.Token, sequenceKeyword: pyslang.parsing.Token) -> DefaultCoverageBinInitializerSyntax: ...

    def defaultDecayTimeDirective(self, directive: pyslang.parsing.Token, time: pyslang.parsing.Token) -> DefaultDecayTimeDirectiveSyntax: ...

    def defaultDisableDeclaration(self, attributes: SyntaxList, defaultKeyword: pyslang.parsing.Token, disableKeyword: pyslang.parsing.Token, iffKeyword: pyslang.parsing.Token, expr: ExpressionSyntax, semi: pyslang.parsing.Token) -> DefaultDisableDeclarationSyntax: ...

    def defaultDistItem(self, defaultKeyword: pyslang.parsing.Token, weight: DistWeightSyntax | None = None) -> DefaultDistItemSyntax: ...

    def defaultExtendsClauseArg(self, openParen: pyslang.parsing.Token, defaultKeyword: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> DefaultExtendsClauseArgSyntax: ...

    def defaultFunctionPort(self, keyword: pyslang.parsing.Token) -> DefaultFunctionPortSyntax: ...

    def defaultNetTypeDirective(self, directive: pyslang.parsing.Token, netType: pyslang.parsing.Token) -> DefaultNetTypeDirectiveSyntax: ...

    def defaultPropertyCaseItem(self, defaultKeyword: pyslang.parsing.Token, colon: pyslang.parsing.Token, expr: PropertyExprSyntax, semi: pyslang.parsing.Token) -> DefaultPropertyCaseItemSyntax: ...

    def defaultRsCaseItem(self, defaultKeyword: pyslang.parsing.Token, colon: pyslang.parsing.Token, item: RsProdItemSyntax, semi: pyslang.parsing.Token) -> DefaultRsCaseItemSyntax: ...

    def defaultSkewItem(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, direction: ClockingDirectionSyntax, semi: pyslang.parsing.Token) -> DefaultSkewItemSyntax: ...

    def defaultTriregStrengthDirective(self, directive: pyslang.parsing.Token, strength: pyslang.parsing.Token) -> DefaultTriregStrengthDirectiveSyntax: ...

    def deferredAssertion(self, hash: pyslang.parsing.Token, zero: pyslang.parsing.Token, finalKeyword: pyslang.parsing.Token) -> DeferredAssertionSyntax: ...

    def defineDirective(self, directive: pyslang.parsing.Token, name: pyslang.parsing.Token, formalArguments: MacroFormalArgumentListSyntax | None, body: TokenList) -> DefineDirectiveSyntax: ...

    def delay3(self, hash: pyslang.parsing.Token, openParen: pyslang.parsing.Token, delay1: ExpressionSyntax, comma1: pyslang.parsing.Token, delay2: ExpressionSyntax | None, comma2: pyslang.parsing.Token, delay3: ExpressionSyntax | None, closeParen: pyslang.parsing.Token) -> Delay3Syntax: ...

    def delay(self, kind: SyntaxKind, hash: pyslang.parsing.Token, delayValue: ExpressionSyntax) -> DelaySyntax: ...

    def delayedSequenceElement(self, doubleHash: pyslang.parsing.Token, delayVal: ExpressionSyntax | None, openBracket: pyslang.parsing.Token, op: pyslang.parsing.Token, range: SelectorSyntax | None, closeBracket: pyslang.parsing.Token, expr: SequenceExprSyntax) -> DelayedSequenceElementSyntax: ...

    def delayedSequenceExpr(self, first: SequenceExprSyntax | None, elements: SyntaxList) -> DelayedSequenceExprSyntax: ...

    def disableConstraint(self, disable: pyslang.parsing.Token, soft: pyslang.parsing.Token, name: ExpressionSyntax, semi: pyslang.parsing.Token) -> DisableConstraintSyntax: ...

    def disableForkStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, disable: pyslang.parsing.Token, fork: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> DisableForkStatementSyntax: ...

    def disableIff(self, disable: pyslang.parsing.Token, iff: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token) -> DisableIffSyntax: ...

    def disableStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, disable: pyslang.parsing.Token, name: NameSyntax, semi: pyslang.parsing.Token) -> DisableStatementSyntax: ...

    def distConstraintList(self, dist: pyslang.parsing.Token, openBrace: pyslang.parsing.Token, items: SeparatedSyntaxList, closeBrace: pyslang.parsing.Token) -> DistConstraintListSyntax: ...

    def distItem(self, range: ExpressionSyntax, weight: DistWeightSyntax | None = None) -> DistItemSyntax: ...

    def distWeight(self, op: pyslang.parsing.Token, extraOp: pyslang.parsing.Token, expr: ExpressionSyntax) -> DistWeightSyntax: ...

    def dividerClause(self, divide: pyslang.parsing.Token, value: pyslang.parsing.Token) -> DividerClauseSyntax: ...

    def doWhileStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, doKeyword: pyslang.parsing.Token, statement: StatementSyntax, whileKeyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> DoWhileStatementSyntax: ...

    def dotMemberClause(self, dot: pyslang.parsing.Token, member: pyslang.parsing.Token) -> DotMemberClauseSyntax: ...

    def driveStrength(self, openParen: pyslang.parsing.Token, strength0: pyslang.parsing.Token, comma: pyslang.parsing.Token, strength1: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> DriveStrengthSyntax: ...

    def edgeControlSpecifier(self, openBracket: pyslang.parsing.Token, descriptors: SeparatedSyntaxList, closeBracket: pyslang.parsing.Token) -> EdgeControlSpecifierSyntax: ...

    def edgeDescriptor(self, t1: pyslang.parsing.Token, t2: pyslang.parsing.Token) -> EdgeDescriptorSyntax: ...

    def edgeSensitivePathSuffix(self, openParen: pyslang.parsing.Token, outputs: SeparatedSyntaxList, polarityOperator: pyslang.parsing.Token, colon: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token) -> EdgeSensitivePathSuffixSyntax: ...

    def elabSystemTask(self, attributes: SyntaxList, name: pyslang.parsing.Token, arguments: ArgumentListSyntax | None, semi: pyslang.parsing.Token) -> ElabSystemTaskSyntax: ...

    def elementSelectExpression(self, left: ExpressionSyntax, select: ElementSelectSyntax) -> ElementSelectExpressionSyntax: ...

    def elementSelect(self, openBracket: pyslang.parsing.Token, selector: SelectorSyntax | None, closeBracket: pyslang.parsing.Token) -> ElementSelectSyntax: ...

    def elseClause(self, elseKeyword: pyslang.parsing.Token, clause: SyntaxNode) -> ElseClauseSyntax: ...

    def elseConstraintClause(self, elseKeyword: pyslang.parsing.Token, constraints: ConstraintItemSyntax) -> ElseConstraintClauseSyntax: ...

    def elsePropertyClause(self, elseKeyword: pyslang.parsing.Token, expr: PropertyExprSyntax) -> ElsePropertyClauseSyntax: ...

    def emptyArgument(self, placeholder: pyslang.parsing.Token) -> EmptyArgumentSyntax: ...

    def emptyIdentifierName(self, placeholder: pyslang.parsing.Token) -> EmptyIdentifierNameSyntax: ...

    def emptyMember(self, attributes: SyntaxList, qualifiers: TokenList, semi: pyslang.parsing.Token) -> EmptyMemberSyntax: ...

    def emptyNonAnsiPort(self, placeholder: pyslang.parsing.Token) -> EmptyNonAnsiPortSyntax: ...

    def emptyPortConnection(self, attributes: SyntaxList, placeholder: pyslang.parsing.Token) -> EmptyPortConnectionSyntax: ...

    def emptyQueueExpression(self, openBrace: pyslang.parsing.Token, closeBrace: pyslang.parsing.Token) -> EmptyQueueExpressionSyntax: ...

    def emptyStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, semicolon: pyslang.parsing.Token) -> EmptyStatementSyntax: ...

    def emptyTimingCheckArg(self, placeholder: pyslang.parsing.Token) -> EmptyTimingCheckArgSyntax: ...

    def enumType(self, keyword: pyslang.parsing.Token, baseType: DataTypeSyntax | None, openBrace: pyslang.parsing.Token, members: SeparatedSyntaxList, closeBrace: pyslang.parsing.Token, dimensions: SyntaxList) -> EnumTypeSyntax: ...

    def equalsAssertionArgClause(self, equals: pyslang.parsing.Token, expr: PropertyExprSyntax) -> EqualsAssertionArgClauseSyntax: ...

    def equalsTypeClause(self, equals: pyslang.parsing.Token, type: DataTypeSyntax) -> EqualsTypeClauseSyntax: ...

    def equalsValueClause(self, equals: pyslang.parsing.Token, expr: ExpressionSyntax) -> EqualsValueClauseSyntax: ...

    def eventControl(self, at: pyslang.parsing.Token, eventName: ExpressionSyntax) -> EventControlSyntax: ...

    def eventControlWithExpression(self, at: pyslang.parsing.Token, expr: EventExpressionSyntax) -> EventControlWithExpressionSyntax: ...

    def eventTriggerStatement(self, kind: SyntaxKind, label: NamedLabelSyntax | None, attributes: SyntaxList, trigger: pyslang.parsing.Token, timing: TimingControlSyntax | None, name: NameSyntax, semi: pyslang.parsing.Token) -> EventTriggerStatementSyntax: ...

    def explicitAnsiPort(self, attributes: SyntaxList, direction: pyslang.parsing.Token, dot: pyslang.parsing.Token, name: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax | None, closeParen: pyslang.parsing.Token) -> ExplicitAnsiPortSyntax: ...

    def explicitNonAnsiPort(self, dot: pyslang.parsing.Token, name: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: PortExpressionSyntax | None, closeParen: pyslang.parsing.Token) -> ExplicitNonAnsiPortSyntax: ...

    def expressionConstraint(self, soft: pyslang.parsing.Token, expr: ExpressionSyntax, semi: pyslang.parsing.Token) -> ExpressionConstraintSyntax: ...

    def expressionCoverageBinInitializer(self, expr: ExpressionSyntax) -> ExpressionCoverageBinInitializerSyntax: ...

    def expressionOrDist(self, expr: ExpressionSyntax, distribution: DistConstraintListSyntax) -> ExpressionOrDistSyntax: ...

    def expressionPattern(self, expr: ExpressionSyntax) -> ExpressionPatternSyntax: ...

    def expressionStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, expr: ExpressionSyntax, semi: pyslang.parsing.Token) -> ExpressionStatementSyntax: ...

    def expressionTimingCheckArg(self, expr: ExpressionSyntax) -> ExpressionTimingCheckArgSyntax: ...

    def extendsClause(self, keyword: pyslang.parsing.Token, baseName: NameSyntax, arguments: ArgumentListSyntax | None = None, defaultedArg: DefaultExtendsClauseArgSyntax | None = None) -> ExtendsClauseSyntax: ...

    def externInterfaceMethod(self, attributes: SyntaxList, externKeyword: pyslang.parsing.Token, forkJoin: pyslang.parsing.Token, prototype: FunctionPrototypeSyntax, semi: pyslang.parsing.Token) -> ExternInterfaceMethodSyntax: ...

    def externModuleDecl(self, attributes: SyntaxList, externKeyword: pyslang.parsing.Token, actualAttributes: SyntaxList, header: ModuleHeaderSyntax) -> ExternModuleDeclSyntax: ...

    def externUdpDecl(self, attributes: SyntaxList, externKeyword: pyslang.parsing.Token, actualAttributes: SyntaxList, primitive: pyslang.parsing.Token, name: pyslang.parsing.Token, portList: UdpPortListSyntax) -> ExternUdpDeclSyntax: ...

    def filePathSpec(self, path: pyslang.parsing.Token) -> FilePathSpecSyntax: ...

    def firstMatchSequenceExpr(self, first_match: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: SequenceExprSyntax, matchList: SequenceMatchListSyntax | None, closeParen: pyslang.parsing.Token) -> FirstMatchSequenceExprSyntax: ...

    def forLoopStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, forKeyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, initializers: SeparatedSyntaxList, semi1: pyslang.parsing.Token, stopExpr: ExpressionSyntax | None, semi2: pyslang.parsing.Token, steps: SeparatedSyntaxList, closeParen: pyslang.parsing.Token, statement: StatementSyntax) -> ForLoopStatementSyntax: ...

    def forVariableDeclaration(self, varKeyword: pyslang.parsing.Token, type: DataTypeSyntax | None, declarator: DeclaratorSyntax) -> ForVariableDeclarationSyntax: ...

    def foreachLoopList(self, openParen: pyslang.parsing.Token, arrayName: ExpressionSyntax, openBracket: pyslang.parsing.Token, loopVariables: SeparatedSyntaxList, closeBracket: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> ForeachLoopListSyntax: ...

    def foreachLoopStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, keyword: pyslang.parsing.Token, loopList: ForeachLoopListSyntax, statement: StatementSyntax) -> ForeachLoopStatementSyntax: ...

    def foreverStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, foreverKeyword: pyslang.parsing.Token, statement: StatementSyntax) -> ForeverStatementSyntax: ...

    def forwardTypeRestriction(self, keyword1: pyslang.parsing.Token, keyword2: pyslang.parsing.Token) -> ForwardTypeRestrictionSyntax: ...

    def forwardTypedefDeclaration(self, attributes: SyntaxList, typedefKeyword: pyslang.parsing.Token, typeRestriction: ForwardTypeRestrictionSyntax | None, name: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> ForwardTypedefDeclarationSyntax: ...

    def functionDeclaration(self, kind: SyntaxKind, attributes: SyntaxList, prototype: FunctionPrototypeSyntax, semi: pyslang.parsing.Token, items: SyntaxList, end: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> FunctionDeclarationSyntax: ...

    def functionPortList(self, openParen: pyslang.parsing.Token, ports: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> FunctionPortListSyntax: ...

    def functionPort(self, attributes: SyntaxList, constKeyword: pyslang.parsing.Token, direction: pyslang.parsing.Token, staticKeyword: pyslang.parsing.Token, varKeyword: pyslang.parsing.Token, dataType: DataTypeSyntax | None, declarator: DeclaratorSyntax) -> FunctionPortSyntax: ...

    def functionPrototype(self, keyword: pyslang.parsing.Token, specifiers: SyntaxList, lifetime: pyslang.parsing.Token, returnType: DataTypeSyntax, name: NameSyntax, portList: FunctionPortListSyntax | None = None) -> FunctionPrototypeSyntax: ...

    def generateBlock(self, attributes: SyntaxList, label: NamedLabelSyntax | None, begin: pyslang.parsing.Token, beginName: NamedBlockClauseSyntax | None, members: SyntaxList, end: pyslang.parsing.Token, endName: NamedBlockClauseSyntax | None = None) -> GenerateBlockSyntax: ...

    def generateRegion(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, members: SyntaxList, endgenerate: pyslang.parsing.Token) -> GenerateRegionSyntax: ...

    def genvarDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, identifiers: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> GenvarDeclarationSyntax: ...

    def hierarchicalInstance(self, decl: InstanceNameSyntax | None, openParen: pyslang.parsing.Token, connections: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> HierarchicalInstanceSyntax: ...

    def hierarchyInstantiation(self, attributes: SyntaxList, type: pyslang.parsing.Token, parameters: ParameterValueAssignmentSyntax | None, instances: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> HierarchyInstantiationSyntax: ...

    def idWithExprCoverageBinInitializer(self, id: pyslang.parsing.Token, withClause: WithClauseSyntax) -> IdWithExprCoverageBinInitializerSyntax: ...

    def identifierName(self, identifier: pyslang.parsing.Token) -> IdentifierNameSyntax: ...

    def identifierSelectName(self, identifier: pyslang.parsing.Token, selectors: SyntaxList) -> IdentifierSelectNameSyntax: ...

    def ifGenerate(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, condition: ExpressionSyntax, closeParen: pyslang.parsing.Token, block: MemberSyntax, elseClause: ElseClauseSyntax | None = None) -> IfGenerateSyntax: ...

    def ifNonePathDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, path: PathDeclarationSyntax) -> IfNonePathDeclarationSyntax: ...

    def iffEventClause(self, iff: pyslang.parsing.Token, expr: ExpressionSyntax) -> IffEventClauseSyntax: ...

    def immediateAssertionMember(self, attributes: SyntaxList, statement: ImmediateAssertionStatementSyntax) -> ImmediateAssertionMemberSyntax: ...

    def immediateAssertionStatement(self, kind: SyntaxKind, label: NamedLabelSyntax | None, attributes: SyntaxList, keyword: pyslang.parsing.Token, delay: DeferredAssertionSyntax | None, expr: ParenthesizedExpressionSyntax, action: ActionBlockSyntax) -> ImmediateAssertionStatementSyntax: ...

    def implementsClause(self, keyword: pyslang.parsing.Token, interfaces: SeparatedSyntaxList) -> ImplementsClauseSyntax: ...

    def implicationConstraint(self, left: ExpressionSyntax, arrow: pyslang.parsing.Token, constraints: ConstraintItemSyntax) -> ImplicationConstraintSyntax: ...

    def implicitAnsiPort(self, attributes: SyntaxList, header: PortHeaderSyntax, declarator: DeclaratorSyntax) -> ImplicitAnsiPortSyntax: ...

    def implicitEventControl(self, at: pyslang.parsing.Token, openParen: pyslang.parsing.Token, star: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> ImplicitEventControlSyntax: ...

    def implicitNonAnsiPort(self, expr: PortExpressionSyntax) -> ImplicitNonAnsiPortSyntax: ...

    def implicitType(self, signing: pyslang.parsing.Token, dimensions: SyntaxList, placeholder: pyslang.parsing.Token) -> ImplicitTypeSyntax: ...

    def includeDirective(self, directive: pyslang.parsing.Token, fileName: pyslang.parsing.Token) -> IncludeDirectiveSyntax: ...

    def insideExpression(self, expr: ExpressionSyntax, inside: pyslang.parsing.Token, ranges: RangeListSyntax) -> InsideExpressionSyntax: ...

    def instanceConfigRule(self, instance: pyslang.parsing.Token, topModule: pyslang.parsing.Token, instanceNames: SyntaxList, ruleClause: ConfigRuleClauseSyntax, semi: pyslang.parsing.Token) -> InstanceConfigRuleSyntax: ...

    def instanceName(self, name: pyslang.parsing.Token, dimensions: SyntaxList) -> InstanceNameSyntax: ...

    def integerType(self, kind: SyntaxKind, keyword: pyslang.parsing.Token, signing: pyslang.parsing.Token, dimensions: SyntaxList) -> IntegerTypeSyntax: ...

    def integerVectorExpression(self, size: pyslang.parsing.Token, base: pyslang.parsing.Token, value: pyslang.parsing.Token) -> IntegerVectorExpressionSyntax: ...

    def interfacePortHeader(self, nameOrKeyword: pyslang.parsing.Token, modport: DotMemberClauseSyntax | None = None) -> InterfacePortHeaderSyntax: ...

    def intersectClause(self, intersect: pyslang.parsing.Token, ranges: RangeListSyntax) -> IntersectClauseSyntax: ...

    def invocationExpression(self, left: ExpressionSyntax, attributes: SyntaxList, arguments: ArgumentListSyntax | None = None) -> InvocationExpressionSyntax: ...

    def jumpStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, breakOrContinue: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> JumpStatementSyntax: ...

    def keywordName(self, kind: SyntaxKind, keyword: pyslang.parsing.Token) -> KeywordNameSyntax: ...

    def keywordType(self, kind: SyntaxKind, keyword: pyslang.parsing.Token) -> KeywordTypeSyntax: ...

    def letDeclaration(self, attributes: SyntaxList, let: pyslang.parsing.Token, identifier: pyslang.parsing.Token, portList: AssertionItemPortListSyntax | None, equals: pyslang.parsing.Token, expr: ExpressionSyntax, semi: pyslang.parsing.Token) -> LetDeclarationSyntax: ...

    def libraryDeclaration(self, attributes: SyntaxList, library: pyslang.parsing.Token, name: pyslang.parsing.Token, filePaths: SeparatedSyntaxList, incDirClause: LibraryIncDirClauseSyntax | None, semi: pyslang.parsing.Token) -> LibraryDeclarationSyntax: ...

    def libraryIncDirClause(self, minus: pyslang.parsing.Token, incdir: pyslang.parsing.Token, filePaths: SeparatedSyntaxList) -> LibraryIncDirClauseSyntax: ...

    def libraryIncludeStatement(self, attributes: SyntaxList, include: pyslang.parsing.Token, filePath: FilePathSpecSyntax, semi: pyslang.parsing.Token) -> LibraryIncludeStatementSyntax: ...

    def libraryMap(self, members: SyntaxList, endOfFile: pyslang.parsing.Token) -> LibraryMapSyntax: ...

    def lineDirective(self, directive: pyslang.parsing.Token, lineNumber: pyslang.parsing.Token, fileName: pyslang.parsing.Token, level: pyslang.parsing.Token) -> LineDirectiveSyntax: ...

    def literalExpression(self, kind: SyntaxKind, literal: pyslang.parsing.Token) -> LiteralExpressionSyntax: ...

    def localVariableDeclaration(self, attributes: SyntaxList, var: pyslang.parsing.Token, type: DataTypeSyntax, declarators: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> LocalVariableDeclarationSyntax: ...

    def loopConstraint(self, foreachKeyword: pyslang.parsing.Token, loopList: ForeachLoopListSyntax, constraints: ConstraintItemSyntax) -> LoopConstraintSyntax: ...

    def loopGenerate(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, genvar: pyslang.parsing.Token, identifier: pyslang.parsing.Token, equals: pyslang.parsing.Token, initialExpr: ExpressionSyntax, semi1: pyslang.parsing.Token, stopExpr: ExpressionSyntax, semi2: pyslang.parsing.Token, iterationExpr: ExpressionSyntax, closeParen: pyslang.parsing.Token, block: MemberSyntax) -> LoopGenerateSyntax: ...

    def loopStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, repeatOrWhile: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, statement: StatementSyntax) -> LoopStatementSyntax: ...

    def macroActualArgumentList(self, openParen: pyslang.parsing.Token, args: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> MacroActualArgumentListSyntax: ...

    def macroActualArgument(self, tokens: TokenList) -> MacroActualArgumentSyntax: ...

    def macroArgumentDefault(self, equals: pyslang.parsing.Token, tokens: TokenList) -> MacroArgumentDefaultSyntax: ...

    def macroFormalArgumentList(self, openParen: pyslang.parsing.Token, args: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> MacroFormalArgumentListSyntax: ...

    def macroFormalArgument(self, name: pyslang.parsing.Token, defaultValue: MacroArgumentDefaultSyntax | None = None) -> MacroFormalArgumentSyntax: ...

    def macroUsage(self, directive: pyslang.parsing.Token, args: MacroActualArgumentListSyntax | None = None) -> MacroUsageSyntax: ...

    def matchesClause(self, matchesKeyword: pyslang.parsing.Token, pattern: PatternSyntax) -> MatchesClauseSyntax: ...

    def memberAccessExpression(self, left: ExpressionSyntax, dot: pyslang.parsing.Token, name: pyslang.parsing.Token) -> MemberAccessExpressionSyntax: ...

    def minTypMaxExpression(self, min: ExpressionSyntax, colon1: pyslang.parsing.Token, typ: ExpressionSyntax, colon2: pyslang.parsing.Token, max: ExpressionSyntax) -> MinTypMaxExpressionSyntax: ...

    def modportClockingPort(self, attributes: SyntaxList, clocking: pyslang.parsing.Token, name: pyslang.parsing.Token) -> ModportClockingPortSyntax: ...

    def modportDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, items: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> ModportDeclarationSyntax: ...

    def modportExplicitPort(self, dot: pyslang.parsing.Token, name: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax | None, closeParen: pyslang.parsing.Token) -> ModportExplicitPortSyntax: ...

    def modportItem(self, name: pyslang.parsing.Token, ports: AnsiPortListSyntax) -> ModportItemSyntax: ...

    def modportNamedPort(self, name: pyslang.parsing.Token) -> ModportNamedPortSyntax: ...

    def modportSimplePortList(self, attributes: SyntaxList, direction: pyslang.parsing.Token, ports: SeparatedSyntaxList) -> ModportSimplePortListSyntax: ...

    def modportSubroutinePortList(self, attributes: SyntaxList, importExport: pyslang.parsing.Token, ports: SeparatedSyntaxList) -> ModportSubroutinePortListSyntax: ...

    def modportSubroutinePort(self, prototype: FunctionPrototypeSyntax) -> ModportSubroutinePortSyntax: ...

    def moduleDeclaration(self, kind: SyntaxKind, attributes: SyntaxList, header: ModuleHeaderSyntax, members: SyntaxList, endmodule: pyslang.parsing.Token, blockName: NamedBlockClauseSyntax | None = None) -> ModuleDeclarationSyntax: ...

    def moduleHeader(self, kind: SyntaxKind, moduleKeyword: pyslang.parsing.Token, lifetime: pyslang.parsing.Token, name: pyslang.parsing.Token, imports: SyntaxList, parameters: ParameterPortListSyntax | None, ports: PortListSyntax | None, semi: pyslang.parsing.Token) -> ModuleHeaderSyntax: ...

    def multipleConcatenationExpression(self, openBrace: pyslang.parsing.Token, expression: ExpressionSyntax, concatenation: ConcatenationExpressionSyntax, closeBrace: pyslang.parsing.Token) -> MultipleConcatenationExpressionSyntax: ...

    def nameValuePragmaExpression(self, name: pyslang.parsing.Token, equals: pyslang.parsing.Token, value: PragmaExpressionSyntax) -> NameValuePragmaExpressionSyntax: ...

    def namedArgument(self, dot: pyslang.parsing.Token, name: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: PropertyExprSyntax | None, closeParen: pyslang.parsing.Token) -> NamedArgumentSyntax: ...

    def namedBlockClause(self, colon: pyslang.parsing.Token, name: pyslang.parsing.Token) -> NamedBlockClauseSyntax: ...

    def namedConditionalDirectiveExpression(self, name: pyslang.parsing.Token) -> NamedConditionalDirectiveExpressionSyntax: ...

    def namedLabel(self, name: pyslang.parsing.Token, colon: pyslang.parsing.Token) -> NamedLabelSyntax: ...

    def namedParamAssignment(self, dot: pyslang.parsing.Token, name: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax | None, closeParen: pyslang.parsing.Token) -> NamedParamAssignmentSyntax: ...

    def namedPortConnection(self, attributes: SyntaxList, dot: pyslang.parsing.Token, name: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: PropertyExprSyntax | None, closeParen: pyslang.parsing.Token) -> NamedPortConnectionSyntax: ...

    def namedStructurePatternMember(self, name: pyslang.parsing.Token, colon: pyslang.parsing.Token, pattern: PatternSyntax) -> NamedStructurePatternMemberSyntax: ...

    def namedType(self, name: NameSyntax) -> NamedTypeSyntax: ...

    def netAlias(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, nets: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> NetAliasSyntax: ...

    def netDeclaration(self, attributes: SyntaxList, netType: pyslang.parsing.Token, strength: NetStrengthSyntax | None, expansionHint: pyslang.parsing.Token, type: DataTypeSyntax, delay: TimingControlSyntax | None, declarators: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> NetDeclarationSyntax: ...

    def netPortHeader(self, direction: pyslang.parsing.Token, netType: pyslang.parsing.Token, dataType: DataTypeSyntax) -> NetPortHeaderSyntax: ...

    def netTypeDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, type: DataTypeSyntax, name: pyslang.parsing.Token, withFunction: WithFunctionClauseSyntax | None, semi: pyslang.parsing.Token) -> NetTypeDeclarationSyntax: ...

    def newArrayExpression(self, newKeyword: NameSyntax, openBracket: pyslang.parsing.Token, sizeExpr: ExpressionSyntax, closeBracket: pyslang.parsing.Token, initializer: ParenthesizedExpressionSyntax | None = None) -> NewArrayExpressionSyntax: ...

    def newClassExpression(self, scopedNew: NameSyntax, argList: ArgumentListSyntax | None = None) -> NewClassExpressionSyntax: ...

    def nonAnsiPortList(self, openParen: pyslang.parsing.Token, ports: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> NonAnsiPortListSyntax: ...

    def nonAnsiUdpPortList(self, openParen: pyslang.parsing.Token, ports: SeparatedSyntaxList, closeParen: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> NonAnsiUdpPortListSyntax: ...

    def numberPragmaExpression(self, size: pyslang.parsing.Token, base: pyslang.parsing.Token, value: pyslang.parsing.Token) -> NumberPragmaExpressionSyntax: ...

    def oneStepDelay(self, hash: pyslang.parsing.Token, oneStep: pyslang.parsing.Token) -> OneStepDelaySyntax: ...

    def orderedArgument(self, expr: PropertyExprSyntax) -> OrderedArgumentSyntax: ...

    def orderedParamAssignment(self, expr: ExpressionSyntax) -> OrderedParamAssignmentSyntax: ...

    def orderedPortConnection(self, attributes: SyntaxList, expr: PropertyExprSyntax) -> OrderedPortConnectionSyntax: ...

    def orderedStructurePatternMember(self, pattern: PatternSyntax) -> OrderedStructurePatternMemberSyntax: ...

    def packageExportAllDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, star1: pyslang.parsing.Token, doubleColon: pyslang.parsing.Token, star2: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> PackageExportAllDeclarationSyntax: ...

    def packageExportDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, items: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> PackageExportDeclarationSyntax: ...

    def packageImportDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, items: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> PackageImportDeclarationSyntax: ...

    def packageImportItem(self, package: pyslang.parsing.Token, doubleColon: pyslang.parsing.Token, item: pyslang.parsing.Token) -> PackageImportItemSyntax: ...

    def parameterDeclarationStatement(self, attributes: SyntaxList, parameter: ParameterDeclarationBaseSyntax, semi: pyslang.parsing.Token) -> ParameterDeclarationStatementSyntax: ...

    def parameterDeclaration(self, keyword: pyslang.parsing.Token, type: DataTypeSyntax, declarators: SeparatedSyntaxList) -> ParameterDeclarationSyntax: ...

    def parameterPortList(self, hash: pyslang.parsing.Token, openParen: pyslang.parsing.Token, declarations: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> ParameterPortListSyntax: ...

    def parameterValueAssignment(self, hash: pyslang.parsing.Token, openParen: pyslang.parsing.Token, parameters: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> ParameterValueAssignmentSyntax: ...

    def parenExpressionList(self, openParen: pyslang.parsing.Token, expressions: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> ParenExpressionListSyntax: ...

    def parenPragmaExpression(self, openParen: pyslang.parsing.Token, values: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> ParenPragmaExpressionSyntax: ...

    def parenthesizedBinsSelectExpr(self, openParen: pyslang.parsing.Token, expr: BinsSelectExpressionSyntax, closeParen: pyslang.parsing.Token) -> ParenthesizedBinsSelectExprSyntax: ...

    def parenthesizedConditionalDirectiveExpression(self, openParen: pyslang.parsing.Token, operand: ConditionalDirectiveExpressionSyntax, closeParen: pyslang.parsing.Token) -> ParenthesizedConditionalDirectiveExpressionSyntax: ...

    def parenthesizedEventExpression(self, openParen: pyslang.parsing.Token, expr: EventExpressionSyntax, closeParen: pyslang.parsing.Token) -> ParenthesizedEventExpressionSyntax: ...

    def parenthesizedExpression(self, openParen: pyslang.parsing.Token, expression: ExpressionSyntax, closeParen: pyslang.parsing.Token) -> ParenthesizedExpressionSyntax: ...

    def parenthesizedPattern(self, openParen: pyslang.parsing.Token, pattern: PatternSyntax, closeParen: pyslang.parsing.Token) -> ParenthesizedPatternSyntax: ...

    def parenthesizedPropertyExpr(self, openParen: pyslang.parsing.Token, expr: PropertyExprSyntax, matchList: SequenceMatchListSyntax | None, closeParen: pyslang.parsing.Token) -> ParenthesizedPropertyExprSyntax: ...

    def parenthesizedSequenceExpr(self, openParen: pyslang.parsing.Token, expr: SequenceExprSyntax, matchList: SequenceMatchListSyntax | None, closeParen: pyslang.parsing.Token, repetition: SequenceRepetitionSyntax | None = None) -> ParenthesizedSequenceExprSyntax: ...

    def pathDeclaration(self, attributes: SyntaxList, desc: PathDescriptionSyntax, equals: pyslang.parsing.Token, openParen: pyslang.parsing.Token, delays: SeparatedSyntaxList, closeParen: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> PathDeclarationSyntax: ...

    def pathDescription(self, openParen: pyslang.parsing.Token, edgeIdentifier: pyslang.parsing.Token, inputs: SeparatedSyntaxList, polarityOperator: pyslang.parsing.Token, pathOperator: pyslang.parsing.Token, suffix: PathSuffixSyntax, closeParen: pyslang.parsing.Token) -> PathDescriptionSyntax: ...

    def patternCaseItem(self, pattern: PatternSyntax, tripleAnd: pyslang.parsing.Token, expr: ExpressionSyntax | None, colon: pyslang.parsing.Token, statement: StatementSyntax) -> PatternCaseItemSyntax: ...

    def portConcatenation(self, openBrace: pyslang.parsing.Token, references: SeparatedSyntaxList, closeBrace: pyslang.parsing.Token) -> PortConcatenationSyntax: ...

    def portDeclaration(self, attributes: SyntaxList, header: PortHeaderSyntax, declarators: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> PortDeclarationSyntax: ...

    def portReference(self, name: pyslang.parsing.Token, select: ElementSelectSyntax | None = None) -> PortReferenceSyntax: ...

    def postfixUnaryExpression(self, kind: SyntaxKind, operand: ExpressionSyntax, attributes: SyntaxList, operatorToken: pyslang.parsing.Token) -> PostfixUnaryExpressionSyntax: ...

    def pragmaDirective(self, directive: pyslang.parsing.Token, name: pyslang.parsing.Token, args: SeparatedSyntaxList) -> PragmaDirectiveSyntax: ...

    def prefixUnaryExpression(self, kind: SyntaxKind, operatorToken: pyslang.parsing.Token, attributes: SyntaxList, operand: ExpressionSyntax) -> PrefixUnaryExpressionSyntax: ...

    def primaryBlockEventExpression(self, keyword: pyslang.parsing.Token, name: NameSyntax) -> PrimaryBlockEventExpressionSyntax: ...

    def primitiveInstantiation(self, attributes: SyntaxList, type: pyslang.parsing.Token, strength: NetStrengthSyntax | None, delay: TimingControlSyntax | None, instances: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> PrimitiveInstantiationSyntax: ...

    def proceduralAssignStatement(self, kind: SyntaxKind, label: NamedLabelSyntax | None, attributes: SyntaxList, keyword: pyslang.parsing.Token, expr: ExpressionSyntax, semi: pyslang.parsing.Token) -> ProceduralAssignStatementSyntax: ...

    def proceduralBlock(self, kind: SyntaxKind, attributes: SyntaxList, keyword: pyslang.parsing.Token, statement: StatementSyntax) -> ProceduralBlockSyntax: ...

    def proceduralDeassignStatement(self, kind: SyntaxKind, label: NamedLabelSyntax | None, attributes: SyntaxList, keyword: pyslang.parsing.Token, variable: ExpressionSyntax, semi: pyslang.parsing.Token) -> ProceduralDeassignStatementSyntax: ...

    def production(self, dataType: DataTypeSyntax | None, name: pyslang.parsing.Token, portList: FunctionPortListSyntax | None, colon: pyslang.parsing.Token, rules: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> ProductionSyntax: ...

    def propertyDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, name: pyslang.parsing.Token, portList: AssertionItemPortListSyntax | None, semi: pyslang.parsing.Token, variables: SyntaxList, propertySpec: PropertySpecSyntax, optionalSemi: pyslang.parsing.Token, end: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> PropertyDeclarationSyntax: ...

    def propertySpec(self, clocking: TimingControlSyntax | None, disable: DisableIffSyntax | None, expr: PropertyExprSyntax) -> PropertySpecSyntax: ...

    def pullStrength(self, openParen: pyslang.parsing.Token, strength: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> PullStrengthSyntax: ...

    def pulseStyleDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, inputs: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> PulseStyleDeclarationSyntax: ...

    def queueDimensionSpecifier(self, dollar: pyslang.parsing.Token, maxSizeClause: ColonExpressionClauseSyntax | None = None) -> QueueDimensionSpecifierSyntax: ...

    def randCaseItem(self, expr: ExpressionSyntax, colon: pyslang.parsing.Token, statement: StatementSyntax) -> RandCaseItemSyntax: ...

    def randCaseStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, randCase: pyslang.parsing.Token, items: SyntaxList, endCase: pyslang.parsing.Token) -> RandCaseStatementSyntax: ...

    def randJoinClause(self, rand: pyslang.parsing.Token, join: pyslang.parsing.Token, expr: ParenthesizedExpressionSyntax | None = None) -> RandJoinClauseSyntax: ...

    def randSequenceStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, randsequence: pyslang.parsing.Token, openParen: pyslang.parsing.Token, firstProduction: pyslang.parsing.Token, closeParen: pyslang.parsing.Token, productions: SyntaxList, endsequence: pyslang.parsing.Token) -> RandSequenceStatementSyntax: ...

    def rangeCoverageBinInitializer(self, ranges: RangeListSyntax, withClause: WithClauseSyntax | None = None) -> RangeCoverageBinInitializerSyntax: ...

    def rangeDimensionSpecifier(self, selector: SelectorSyntax) -> RangeDimensionSpecifierSyntax: ...

    def rangeList(self, openBrace: pyslang.parsing.Token, valueRanges: SeparatedSyntaxList, closeBrace: pyslang.parsing.Token) -> RangeListSyntax: ...

    def rangeSelect(self, kind: SyntaxKind, left: ExpressionSyntax, range: pyslang.parsing.Token, right: ExpressionSyntax) -> RangeSelectSyntax: ...

    def repeatedEventControl(self, repeat: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, eventControl: TimingControlSyntax | None = None) -> RepeatedEventControlSyntax: ...

    def replicatedAssignmentPattern(self, openBrace: pyslang.parsing.Token, countExpr: ExpressionSyntax, innerOpenBrace: pyslang.parsing.Token, items: SeparatedSyntaxList, innerCloseBrace: pyslang.parsing.Token, closeBrace: pyslang.parsing.Token) -> ReplicatedAssignmentPatternSyntax: ...

    def returnStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, returnKeyword: pyslang.parsing.Token, returnValue: ExpressionSyntax | None, semi: pyslang.parsing.Token) -> ReturnStatementSyntax: ...

    def rsCase(self, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, items: SyntaxList, endcase: pyslang.parsing.Token) -> RsCaseSyntax: ...

    def rsCodeBlock(self, openBrace: pyslang.parsing.Token, items: SyntaxList, closeBrace: pyslang.parsing.Token) -> RsCodeBlockSyntax: ...

    def rsElseClause(self, keyword: pyslang.parsing.Token, item: RsProdItemSyntax) -> RsElseClauseSyntax: ...

    def rsIfElse(self, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, condition: ExpressionSyntax, closeParen: pyslang.parsing.Token, ifItem: RsProdItemSyntax, elseClause: RsElseClauseSyntax | None = None) -> RsIfElseSyntax: ...

    def rsProdItem(self, name: pyslang.parsing.Token, argList: ArgumentListSyntax | None = None) -> RsProdItemSyntax: ...

    def rsRepeat(self, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, item: RsProdItemSyntax) -> RsRepeatSyntax: ...

    def rsRule(self, randJoin: RandJoinClauseSyntax | None, prods: SyntaxList, weightClause: RsWeightClauseSyntax | None = None) -> RsRuleSyntax: ...

    def rsWeightClause(self, colonEqual: pyslang.parsing.Token, weight: ExpressionSyntax, codeBlock: RsProdSyntax | None = None) -> RsWeightClauseSyntax: ...

    def scopedName(self, left: NameSyntax, separator: pyslang.parsing.Token, right: NameSyntax) -> ScopedNameSyntax: ...

    def sequenceDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, name: pyslang.parsing.Token, portList: AssertionItemPortListSyntax | None, semi: pyslang.parsing.Token, variables: SyntaxList, seqExpr: SequenceExprSyntax, optionalSemi: pyslang.parsing.Token, end: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> SequenceDeclarationSyntax: ...

    def sequenceMatchList(self, comma: pyslang.parsing.Token, items: SeparatedSyntaxList) -> SequenceMatchListSyntax: ...

    def sequenceRepetition(self, openBracket: pyslang.parsing.Token, op: pyslang.parsing.Token, selector: SelectorSyntax | None, closeBracket: pyslang.parsing.Token) -> SequenceRepetitionSyntax: ...

    def signalEventExpression(self, edge: pyslang.parsing.Token, expr: ExpressionSyntax, iffClause: IffEventClauseSyntax | None = None) -> SignalEventExpressionSyntax: ...

    def signedCastExpression(self, signing: pyslang.parsing.Token, apostrophe: pyslang.parsing.Token, inner: ParenthesizedExpressionSyntax) -> SignedCastExpressionSyntax: ...

    def simpleAssignmentPattern(self, openBrace: pyslang.parsing.Token, items: SeparatedSyntaxList, closeBrace: pyslang.parsing.Token) -> SimpleAssignmentPatternSyntax: ...

    def simpleBinsSelectExpr(self, expr: ExpressionSyntax, matchesClause: MatchesClauseSyntax | None = None) -> SimpleBinsSelectExprSyntax: ...

    def simpleDirective(self, kind: SyntaxKind, directive: pyslang.parsing.Token) -> SimpleDirectiveSyntax: ...

    def simplePathSuffix(self, outputs: SeparatedSyntaxList) -> SimplePathSuffixSyntax: ...

    def simplePragmaExpression(self, value: pyslang.parsing.Token) -> SimplePragmaExpressionSyntax: ...

    def simplePropertyExpr(self, expr: SequenceExprSyntax) -> SimplePropertyExprSyntax: ...

    def simpleSequenceExpr(self, expr: ExpressionSyntax, repetition: SequenceRepetitionSyntax | None = None) -> SimpleSequenceExprSyntax: ...

    def solveBeforeConstraint(self, solve: pyslang.parsing.Token, beforeExpr: SeparatedSyntaxList, before: pyslang.parsing.Token, afterExpr: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> SolveBeforeConstraintSyntax: ...

    def specifyBlock(self, attributes: SyntaxList, specify: pyslang.parsing.Token, items: SyntaxList, endspecify: pyslang.parsing.Token) -> SpecifyBlockSyntax: ...

    def specparamDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, type: ImplicitTypeSyntax, declarators: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> SpecparamDeclarationSyntax: ...

    def specparamDeclarator(self, name: pyslang.parsing.Token, equals: pyslang.parsing.Token, openParen: pyslang.parsing.Token, value1: ExpressionSyntax, comma: pyslang.parsing.Token, value2: ExpressionSyntax | None, closeParen: pyslang.parsing.Token) -> SpecparamDeclaratorSyntax: ...

    def standardCaseItem(self, expressions: SeparatedSyntaxList, colon: pyslang.parsing.Token, clause: SyntaxNode) -> StandardCaseItemSyntax: ...

    def standardPropertyCaseItem(self, expressions: SeparatedSyntaxList, colon: pyslang.parsing.Token, expr: PropertyExprSyntax, semi: pyslang.parsing.Token) -> StandardPropertyCaseItemSyntax: ...

    def standardRsCaseItem(self, expressions: SeparatedSyntaxList, colon: pyslang.parsing.Token, item: RsProdItemSyntax, semi: pyslang.parsing.Token) -> StandardRsCaseItemSyntax: ...

    def streamExpression(self, expression: ExpressionSyntax, withRange: StreamExpressionWithRangeSyntax | None = None) -> StreamExpressionSyntax: ...

    def streamExpressionWithRange(self, withKeyword: pyslang.parsing.Token, range: ElementSelectSyntax) -> StreamExpressionWithRangeSyntax: ...

    def streamingConcatenationExpression(self, openBrace: pyslang.parsing.Token, operatorToken: pyslang.parsing.Token, sliceSize: ExpressionSyntax | None, innerOpenBrace: pyslang.parsing.Token, expressions: SeparatedSyntaxList, innerCloseBrace: pyslang.parsing.Token, closeBrace: pyslang.parsing.Token) -> StreamingConcatenationExpressionSyntax: ...

    def strongWeakPropertyExpr(self, keyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: SequenceExprSyntax, closeParen: pyslang.parsing.Token) -> StrongWeakPropertyExprSyntax: ...

    def structUnionMember(self, attributes: SyntaxList, randomQualifier: pyslang.parsing.Token, type: DataTypeSyntax, declarators: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> StructUnionMemberSyntax: ...

    def structUnionType(self, kind: SyntaxKind, keyword: pyslang.parsing.Token, taggedOrSoft: pyslang.parsing.Token, packed: pyslang.parsing.Token, signing: pyslang.parsing.Token, openBrace: pyslang.parsing.Token, members: SyntaxList, closeBrace: pyslang.parsing.Token, dimensions: SyntaxList) -> StructUnionTypeSyntax: ...

    def structurePattern(self, openBrace: pyslang.parsing.Token, members: SeparatedSyntaxList, closeBrace: pyslang.parsing.Token) -> StructurePatternSyntax: ...

    def structuredAssignmentPattern(self, openBrace: pyslang.parsing.Token, items: SeparatedSyntaxList, closeBrace: pyslang.parsing.Token) -> StructuredAssignmentPatternSyntax: ...

    def superNewDefaultedArgsExpression(self, scopedNew: NameSyntax, openParen: pyslang.parsing.Token, defaultKeyword: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> SuperNewDefaultedArgsExpressionSyntax: ...

    def systemName(self, systemIdentifier: pyslang.parsing.Token) -> SystemNameSyntax: ...

    def systemTimingCheck(self, attributes: SyntaxList, name: pyslang.parsing.Token, openParen: pyslang.parsing.Token, args: SeparatedSyntaxList, closeParen: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> SystemTimingCheckSyntax: ...

    def taggedPattern(self, tagged: pyslang.parsing.Token, memberName: pyslang.parsing.Token, pattern: PatternSyntax | None = None) -> TaggedPatternSyntax: ...

    def taggedUnionExpression(self, tagged: pyslang.parsing.Token, member: pyslang.parsing.Token, expr: ExpressionSyntax | None = None) -> TaggedUnionExpressionSyntax: ...

    def timeScaleDirective(self, directive: pyslang.parsing.Token, timeUnit: pyslang.parsing.Token, slash: pyslang.parsing.Token, timePrecision: pyslang.parsing.Token) -> TimeScaleDirectiveSyntax: ...

    def timeUnitsDeclaration(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, time: pyslang.parsing.Token, divider: DividerClauseSyntax | None, semi: pyslang.parsing.Token) -> TimeUnitsDeclarationSyntax: ...

    def timingCheckEventArg(self, edge: pyslang.parsing.Token, controlSpecifier: EdgeControlSpecifierSyntax | None, terminal: ExpressionSyntax, condition: TimingCheckEventConditionSyntax | None = None) -> TimingCheckEventArgSyntax: ...

    def timingCheckEventCondition(self, tripleAnd: pyslang.parsing.Token, expr: ExpressionSyntax) -> TimingCheckEventConditionSyntax: ...

    def timingControlExpression(self, timing: TimingControlSyntax, expr: ExpressionSyntax) -> TimingControlExpressionSyntax: ...

    def timingControlStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, timingControl: TimingControlSyntax, statement: StatementSyntax) -> TimingControlStatementSyntax: ...

    def transListCoverageBinInitializer(self, sets: SeparatedSyntaxList) -> TransListCoverageBinInitializerSyntax: ...

    def transRange(self, items: SeparatedSyntaxList, repeat: TransRepeatRangeSyntax | None = None) -> TransRangeSyntax: ...

    def transRepeatRange(self, openBracket: pyslang.parsing.Token, specifier: pyslang.parsing.Token, selector: SelectorSyntax | None, closeBracket: pyslang.parsing.Token) -> TransRepeatRangeSyntax: ...

    def transSet(self, openParen: pyslang.parsing.Token, ranges: SeparatedSyntaxList, closeParen: pyslang.parsing.Token) -> TransSetSyntax: ...

    def typeAssignment(self, name: pyslang.parsing.Token, assignment: EqualsTypeClauseSyntax | None = None) -> TypeAssignmentSyntax: ...

    def typeParameterDeclaration(self, keyword: pyslang.parsing.Token, typeKeyword: pyslang.parsing.Token, typeRestriction: ForwardTypeRestrictionSyntax | None, declarators: SeparatedSyntaxList) -> TypeParameterDeclarationSyntax: ...

    def typeReference(self, typeKeyword: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token) -> TypeReferenceSyntax: ...

    def typedefDeclaration(self, attributes: SyntaxList, typedefKeyword: pyslang.parsing.Token, type: DataTypeSyntax, name: pyslang.parsing.Token, dimensions: SyntaxList, semi: pyslang.parsing.Token) -> TypedefDeclarationSyntax: ...

    def udpBody(self, portDecls: SeparatedSyntaxList, initialStmt: UdpInitialStmtSyntax | None, table: pyslang.parsing.Token, entries: SyntaxList, endtable: pyslang.parsing.Token) -> UdpBodySyntax: ...

    def udpDeclaration(self, attributes: SyntaxList, primitive: pyslang.parsing.Token, name: pyslang.parsing.Token, portList: UdpPortListSyntax, body: UdpBodySyntax, endprimitive: pyslang.parsing.Token, endBlockName: NamedBlockClauseSyntax | None = None) -> UdpDeclarationSyntax: ...

    def udpEdgeField(self, openParen: pyslang.parsing.Token, first: pyslang.parsing.Token, second: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> UdpEdgeFieldSyntax: ...

    def udpEntry(self, inputs: SyntaxList, colon1: pyslang.parsing.Token, current: UdpFieldBaseSyntax | None, colon2: pyslang.parsing.Token, next: UdpFieldBaseSyntax | None, semi: pyslang.parsing.Token) -> UdpEntrySyntax: ...

    def udpInitialStmt(self, initial: pyslang.parsing.Token, name: pyslang.parsing.Token, equals: pyslang.parsing.Token, value: ExpressionSyntax, semi: pyslang.parsing.Token) -> UdpInitialStmtSyntax: ...

    def udpInputPortDecl(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, names: SeparatedSyntaxList) -> UdpInputPortDeclSyntax: ...

    def udpOutputPortDecl(self, attributes: SyntaxList, keyword: pyslang.parsing.Token, reg: pyslang.parsing.Token, name: pyslang.parsing.Token, initializer: EqualsValueClauseSyntax | None = None) -> UdpOutputPortDeclSyntax: ...

    def udpSimpleField(self, field: pyslang.parsing.Token) -> UdpSimpleFieldSyntax: ...

    def unaryBinsSelectExpr(self, op: pyslang.parsing.Token, expr: BinsSelectConditionExprSyntax) -> UnaryBinsSelectExprSyntax: ...

    def unaryConditionalDirectiveExpression(self, op: pyslang.parsing.Token, operand: ConditionalDirectiveExpressionSyntax) -> UnaryConditionalDirectiveExpressionSyntax: ...

    def unaryPropertyExpr(self, op: pyslang.parsing.Token, expr: PropertyExprSyntax) -> UnaryPropertyExprSyntax: ...

    def unarySelectPropertyExpr(self, op: pyslang.parsing.Token, openBracket: pyslang.parsing.Token, selector: SelectorSyntax | None, closeBracket: pyslang.parsing.Token, expr: PropertyExprSyntax) -> UnarySelectPropertyExprSyntax: ...

    def unconditionalBranchDirective(self, kind: SyntaxKind, directive: pyslang.parsing.Token, disabledTokens: TokenList) -> UnconditionalBranchDirectiveSyntax: ...

    def unconnectedDriveDirective(self, directive: pyslang.parsing.Token, strength: pyslang.parsing.Token) -> UnconnectedDriveDirectiveSyntax: ...

    def undefDirective(self, directive: pyslang.parsing.Token, name: pyslang.parsing.Token) -> UndefDirectiveSyntax: ...

    def uniquenessConstraint(self, unique: pyslang.parsing.Token, ranges: RangeListSyntax, semi: pyslang.parsing.Token) -> UniquenessConstraintSyntax: ...

    def userDefinedNetDeclaration(self, attributes: SyntaxList, netType: pyslang.parsing.Token, delay: TimingControlSyntax, declarators: SeparatedSyntaxList, semi: pyslang.parsing.Token) -> UserDefinedNetDeclarationSyntax: ...

    def valueRangeExpression(self, openBracket: pyslang.parsing.Token, left: ExpressionSyntax, op: pyslang.parsing.Token, right: ExpressionSyntax, closeBracket: pyslang.parsing.Token) -> ValueRangeExpressionSyntax: ...

    def variableDimension(self, openBracket: pyslang.parsing.Token, specifier: DimensionSpecifierSyntax | None, closeBracket: pyslang.parsing.Token) -> VariableDimensionSyntax: ...

    def variablePattern(self, dot: pyslang.parsing.Token, variableName: pyslang.parsing.Token) -> VariablePatternSyntax: ...

    def variablePortHeader(self, constKeyword: pyslang.parsing.Token, direction: pyslang.parsing.Token, varKeyword: pyslang.parsing.Token, dataType: DataTypeSyntax) -> VariablePortHeaderSyntax: ...

    def virtualInterfaceType(self, virtualKeyword: pyslang.parsing.Token, interfaceKeyword: pyslang.parsing.Token, name: pyslang.parsing.Token, parameters: ParameterValueAssignmentSyntax | None = None, modport: DotMemberClauseSyntax | None = None) -> VirtualInterfaceTypeSyntax: ...

    def voidCastedCallStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, voidKeyword: pyslang.parsing.Token, apostrophe: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> VoidCastedCallStatementSyntax: ...

    def waitForkStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, wait: pyslang.parsing.Token, fork: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> WaitForkStatementSyntax: ...

    def waitOrderStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, wait_order: pyslang.parsing.Token, openParen: pyslang.parsing.Token, names: SeparatedSyntaxList, closeParen: pyslang.parsing.Token, action: ActionBlockSyntax) -> WaitOrderStatementSyntax: ...

    def waitStatement(self, label: NamedLabelSyntax | None, attributes: SyntaxList, wait: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token, statement: StatementSyntax) -> WaitStatementSyntax: ...

    def wildcardDimensionSpecifier(self, star: pyslang.parsing.Token) -> WildcardDimensionSpecifierSyntax: ...

    def wildcardPattern(self, dot: pyslang.parsing.Token, star: pyslang.parsing.Token) -> WildcardPatternSyntax: ...

    def wildcardPortConnection(self, attributes: SyntaxList, dot: pyslang.parsing.Token, star: pyslang.parsing.Token) -> WildcardPortConnectionSyntax: ...

    def wildcardPortList(self, openParen: pyslang.parsing.Token, dot: pyslang.parsing.Token, star: pyslang.parsing.Token, closeParen: pyslang.parsing.Token) -> WildcardPortListSyntax: ...

    def wildcardUdpPortList(self, openParen: pyslang.parsing.Token, dot: pyslang.parsing.Token, star: pyslang.parsing.Token, closeParen: pyslang.parsing.Token, semi: pyslang.parsing.Token) -> WildcardUdpPortListSyntax: ...

    def withClause(self, with_: pyslang.parsing.Token, openParen: pyslang.parsing.Token, expr: ExpressionSyntax, closeParen: pyslang.parsing.Token) -> WithClauseSyntax: ...

    def withFunctionClause(self, with_: pyslang.parsing.Token, name: NameSyntax) -> WithFunctionClauseSyntax: ...

    def withFunctionSample(self, with_: pyslang.parsing.Token, function: pyslang.parsing.Token, sample: pyslang.parsing.Token, portList: FunctionPortListSyntax | None = None) -> WithFunctionSampleSyntax: ...
