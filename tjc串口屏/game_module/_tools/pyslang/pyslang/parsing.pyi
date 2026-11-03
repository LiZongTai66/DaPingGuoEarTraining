"""Lexer, parser, preprocessor types"""

from collections.abc import Mapping, Sequence, Set
import enum
import os
import pathlib
from typing import overload

import pyslang
import pyslang.syntax


class TriviaKind(enum.Enum):
    Unknown = 0

    Whitespace = 1

    EndOfLine = 2

    LineComment = 3

    BlockComment = 4

    DisabledText = 5

    SkippedTokens = 6

    SkippedSyntax = 7

    Directive = 8

class TokenKind(enum.Enum):
    Unknown = 0

    EndOfFile = 1

    Identifier = 2

    SystemIdentifier = 3

    StringLiteral = 4

    IntegerLiteral = 5

    IntegerBase = 6

    UnbasedUnsizedLiteral = 7

    RealLiteral = 8

    TimeLiteral = 9

    Placeholder = 10

    Apostrophe = 11

    ApostropheOpenBrace = 12

    OpenBrace = 13

    CloseBrace = 14

    OpenBracket = 15

    CloseBracket = 16

    OpenParenthesis = 17

    CloseParenthesis = 18

    Semicolon = 19

    Colon = 20

    ColonEquals = 21

    ColonSlash = 22

    DoubleColon = 23

    Comma = 24

    Dot = 25

    Slash = 26

    Star = 27

    DoubleStar = 28

    StarArrow = 29

    Plus = 30

    DoublePlus = 31

    PlusColon = 32

    PlusDivMinus = 33

    PlusModMinus = 34

    Minus = 35

    DoubleMinus = 36

    MinusColon = 37

    MinusArrow = 38

    MinusDoubleArrow = 39

    Tilde = 40

    TildeAnd = 41

    TildeOr = 42

    TildeXor = 43

    Dollar = 44

    Question = 45

    Hash = 46

    DoubleHash = 47

    HashMinusHash = 48

    HashEqualsHash = 49

    Xor = 50

    XorTilde = 51

    Equals = 52

    DoubleEquals = 53

    DoubleEqualsQuestion = 54

    TripleEquals = 55

    EqualsArrow = 56

    PlusEqual = 57

    MinusEqual = 58

    SlashEqual = 59

    StarEqual = 60

    AndEqual = 61

    OrEqual = 62

    PercentEqual = 63

    XorEqual = 64

    LeftShiftEqual = 65

    TripleLeftShiftEqual = 66

    RightShiftEqual = 67

    TripleRightShiftEqual = 68

    LeftShift = 69

    RightShift = 70

    TripleLeftShift = 71

    TripleRightShift = 72

    Exclamation = 73

    ExclamationEquals = 74

    ExclamationEqualsQuestion = 75

    ExclamationDoubleEquals = 76

    Percent = 77

    LessThan = 78

    LessThanEquals = 79

    LessThanMinusArrow = 80

    GreaterThan = 81

    GreaterThanEquals = 82

    Or = 83

    DoubleOr = 84

    OrMinusArrow = 85

    OrEqualsArrow = 86

    At = 87

    DoubleAt = 88

    And = 89

    DoubleAnd = 90

    TripleAnd = 91

    OneStep = 92

    AcceptOnKeyword = 93

    AliasKeyword = 94

    AlwaysKeyword = 95

    AlwaysCombKeyword = 96

    AlwaysFFKeyword = 97

    AlwaysLatchKeyword = 98

    AndKeyword = 99

    AssertKeyword = 100

    AssignKeyword = 101

    AssumeKeyword = 102

    AutomaticKeyword = 103

    BeforeKeyword = 104

    BeginKeyword = 105

    BindKeyword = 106

    BinsKeyword = 107

    BinsOfKeyword = 108

    BitKeyword = 109

    BreakKeyword = 110

    BufKeyword = 111

    BufIf0Keyword = 112

    BufIf1Keyword = 113

    ByteKeyword = 114

    CaseKeyword = 115

    CaseXKeyword = 116

    CaseZKeyword = 117

    CellKeyword = 118

    CHandleKeyword = 119

    CheckerKeyword = 120

    ClassKeyword = 121

    ClockingKeyword = 122

    CmosKeyword = 123

    ConfigKeyword = 124

    ConstKeyword = 125

    ConstraintKeyword = 126

    ContextKeyword = 127

    ContinueKeyword = 128

    CoverKeyword = 129

    CoverGroupKeyword = 130

    CoverPointKeyword = 131

    CrossKeyword = 132

    DeassignKeyword = 133

    DefaultKeyword = 134

    DefParamKeyword = 135

    DesignKeyword = 136

    DisableKeyword = 137

    DistKeyword = 138

    DoKeyword = 139

    EdgeKeyword = 140

    ElseKeyword = 141

    EndKeyword = 142

    EndCaseKeyword = 143

    EndCheckerKeyword = 144

    EndClassKeyword = 145

    EndClockingKeyword = 146

    EndConfigKeyword = 147

    EndFunctionKeyword = 148

    EndGenerateKeyword = 149

    EndGroupKeyword = 150

    EndInterfaceKeyword = 151

    EndModuleKeyword = 152

    EndPackageKeyword = 153

    EndPrimitiveKeyword = 154

    EndProgramKeyword = 155

    EndPropertyKeyword = 156

    EndSpecifyKeyword = 157

    EndSequenceKeyword = 158

    EndTableKeyword = 159

    EndTaskKeyword = 160

    EnumKeyword = 161

    EventKeyword = 162

    EventuallyKeyword = 163

    ExpectKeyword = 164

    ExportKeyword = 165

    ExtendsKeyword = 166

    ExternKeyword = 167

    FinalKeyword = 168

    FirstMatchKeyword = 169

    ForKeyword = 170

    ForceKeyword = 171

    ForeachKeyword = 172

    ForeverKeyword = 173

    ForkKeyword = 174

    ForkJoinKeyword = 175

    FunctionKeyword = 176

    GenerateKeyword = 177

    GenVarKeyword = 178

    GlobalKeyword = 179

    HighZ0Keyword = 180

    HighZ1Keyword = 181

    IfKeyword = 182

    IffKeyword = 183

    IfNoneKeyword = 184

    IgnoreBinsKeyword = 185

    IllegalBinsKeyword = 186

    ImplementsKeyword = 187

    ImpliesKeyword = 188

    ImportKeyword = 189

    IncDirKeyword = 190

    IncludeKeyword = 191

    InitialKeyword = 192

    InOutKeyword = 193

    InputKeyword = 194

    InsideKeyword = 195

    InstanceKeyword = 196

    IntKeyword = 197

    IntegerKeyword = 198

    InterconnectKeyword = 199

    InterfaceKeyword = 200

    IntersectKeyword = 201

    JoinKeyword = 202

    JoinAnyKeyword = 203

    JoinNoneKeyword = 204

    LargeKeyword = 205

    LetKeyword = 206

    LibListKeyword = 207

    LibraryKeyword = 208

    LocalKeyword = 209

    LocalParamKeyword = 210

    LogicKeyword = 211

    LongIntKeyword = 212

    MacromoduleKeyword = 213

    MatchesKeyword = 214

    MediumKeyword = 215

    ModPortKeyword = 216

    ModuleKeyword = 217

    NandKeyword = 218

    NegEdgeKeyword = 219

    NetTypeKeyword = 220

    NewKeyword = 221

    NextTimeKeyword = 222

    NmosKeyword = 223

    NorKeyword = 224

    NoShowCancelledKeyword = 225

    NotKeyword = 226

    NotIf0Keyword = 227

    NotIf1Keyword = 228

    NullKeyword = 229

    OrKeyword = 230

    OutputKeyword = 231

    PackageKeyword = 232

    PackedKeyword = 233

    ParameterKeyword = 234

    PmosKeyword = 235

    PosEdgeKeyword = 236

    PrimitiveKeyword = 237

    PriorityKeyword = 238

    ProgramKeyword = 239

    PropertyKeyword = 240

    ProtectedKeyword = 241

    Pull0Keyword = 242

    Pull1Keyword = 243

    PullDownKeyword = 244

    PullUpKeyword = 245

    PulseStyleOnDetectKeyword = 246

    PulseStyleOnEventKeyword = 247

    PureKeyword = 248

    RandKeyword = 249

    RandCKeyword = 250

    RandCaseKeyword = 251

    RandSequenceKeyword = 252

    RcmosKeyword = 253

    RealKeyword = 254

    RealTimeKeyword = 255

    RefKeyword = 256

    RegKeyword = 257

    RejectOnKeyword = 258

    ReleaseKeyword = 259

    RepeatKeyword = 260

    RestrictKeyword = 261

    ReturnKeyword = 262

    RnmosKeyword = 263

    RpmosKeyword = 264

    RtranKeyword = 265

    RtranIf0Keyword = 266

    RtranIf1Keyword = 267

    SAlwaysKeyword = 268

    SEventuallyKeyword = 269

    SNextTimeKeyword = 270

    SUntilKeyword = 271

    SUntilWithKeyword = 272

    ScalaredKeyword = 273

    SequenceKeyword = 274

    ShortIntKeyword = 275

    ShortRealKeyword = 276

    ShowCancelledKeyword = 277

    SignedKeyword = 278

    SmallKeyword = 279

    SoftKeyword = 280

    SolveKeyword = 281

    SpecifyKeyword = 282

    SpecParamKeyword = 283

    StaticKeyword = 284

    StringKeyword = 285

    StrongKeyword = 286

    Strong0Keyword = 287

    Strong1Keyword = 288

    StructKeyword = 289

    SuperKeyword = 290

    Supply0Keyword = 291

    Supply1Keyword = 292

    SyncAcceptOnKeyword = 293

    SyncRejectOnKeyword = 294

    TableKeyword = 295

    TaggedKeyword = 296

    TaskKeyword = 297

    ThisKeyword = 298

    ThroughoutKeyword = 299

    TimeKeyword = 300

    TimePrecisionKeyword = 301

    TimeUnitKeyword = 302

    TranKeyword = 303

    TranIf0Keyword = 304

    TranIf1Keyword = 305

    TriKeyword = 306

    Tri0Keyword = 307

    Tri1Keyword = 308

    TriAndKeyword = 309

    TriOrKeyword = 310

    TriRegKeyword = 311

    TypeKeyword = 312

    TypedefKeyword = 313

    UnionKeyword = 314

    UniqueKeyword = 315

    Unique0Keyword = 316

    UnsignedKeyword = 317

    UntilKeyword = 318

    UntilWithKeyword = 319

    UntypedKeyword = 320

    UseKeyword = 321

    UWireKeyword = 322

    VarKeyword = 323

    VectoredKeyword = 324

    VirtualKeyword = 325

    VoidKeyword = 326

    WaitKeyword = 327

    WaitOrderKeyword = 328

    WAndKeyword = 329

    WeakKeyword = 330

    Weak0Keyword = 331

    Weak1Keyword = 332

    WhileKeyword = 333

    WildcardKeyword = 334

    WireKeyword = 335

    WithKeyword = 336

    WithinKeyword = 337

    WOrKeyword = 338

    XnorKeyword = 339

    XorKeyword = 340

    UnitSystemName = 341

    RootSystemName = 342

    Directive = 343

    IncludeFileName = 344

    MacroUsage = 345

    MacroQuote = 346

    MacroTripleQuote = 347

    MacroEscapedQuote = 348

    MacroPaste = 349

    EmptyMacroArgument = 350

    LineContinuation = 351

class KnownSystemName(enum.Enum):
    Unknown = 0

    s_bits = 1

    s_typename = 2

    s_isunbounded = 3

    s_low = 4

    s_high = 5

    s_left = 6

    s_right = 7

    s_size = 8

    s_increment = 9

    s_dimensions = 10

    s_unpacked_dimensions = 11

    s_rtoi = 12

    s_itor = 13

    s_realtobits = 14

    s_bitstoreal = 15

    s_shortrealtobits = 16

    s_bitstoshortreal = 17

    s_signed = 18

    s_unsigned = 19

    s_coverage_control = 20

    s_coverage_get_max = 21

    s_coverage_get = 22

    s_coverage_merge = 23

    s_coverage_save = 24

    s_get_coverage = 25

    s_set_coverage_db_name = 26

    s_load_coverage_db = 27

    s_clog2 = 28

    s_countbits = 29

    s_countones = 30

    s_onehot = 31

    s_onehot0 = 32

    s_isunknown = 33

    s_ln = 34

    s_log10 = 35

    s_exp = 36

    s_sqrt = 37

    s_floor = 38

    s_ceil = 39

    s_sin = 40

    s_cos = 41

    s_tan = 42

    s_asin = 43

    s_acos = 44

    s_atan = 45

    s_sinh = 46

    s_cosh = 47

    s_tanh = 48

    s_asinh = 49

    s_acosh = 50

    s_atanh = 51

    s_pow = 52

    s_atan2 = 53

    s_hypot = 54

    s_value_plusargs = 55

    s_global_clock = 56

    s_sformatf = 57

    s_psprintf = 58

    s_inferred_clock = 59

    s_inferred_disable = 60

    randomize = 61

    triggered = 62

    matched = 63

    s_ferror = 64

    s_fgets = 65

    s_fscanf = 66

    s_sscanf = 67

    s_fread = 68

    s_fopen = 69

    s_fclose = 70

    s_fgetc = 71

    s_ungetc = 72

    s_ftell = 73

    s_fseek = 74

    s_rewind = 75

    s_fflush = 76

    s_feof = 77

    s_rose = 78

    s_fell = 79

    s_stable = 80

    s_changed = 81

    s_past_gclk = 82

    s_rose_gclk = 83

    s_fell_gclk = 84

    s_stable_gclk = 85

    s_changed_gclk = 86

    s_future_gclk = 87

    s_rising_gclk = 88

    s_falling_gclk = 89

    s_steady_gclk = 90

    s_changing_gclk = 91

    s_sampled = 92

    s_past = 93

    s_stacktrace = 94

    s_countdrivers = 95

    s_getpattern = 96

    s_test_plusargs = 97

    s_time = 98

    s_stime = 99

    s_realtime = 100

    s_random = 101

    s_urandom = 102

    s_urandom_range = 103

    s_reset_count = 104

    s_reset_value = 105

    s_timeunit = 106

    s_timeprecision = 107

    s_scale = 108

    s_sdf_annotate = 109

    s_dist_uniform = 110

    s_dist_normal = 111

    s_dist_exponential = 112

    s_dist_poisson = 113

    s_dist_chi_square = 114

    s_dist_t = 115

    s_dist_erlang = 116

    s_fatal = 117

    s_static_assert = 118

    s_cast = 119

    s_info = 120

    s_warning = 121

    s_error = 122

    s_finish = 123

    s_stop = 124

    s_assertcontrol = 125

    s_asserton = 126

    s_assertoff = 127

    s_assertkill = 128

    s_assertpasson = 129

    s_assertpassoff = 130

    s_assertfailon = 131

    s_assertfailoff = 132

    s_assertnonvacuouson = 133

    s_assertvacuousoff = 134

    s_deposit = 135

    s_display = 136

    s_displayb = 137

    s_displayo = 138

    s_displayh = 139

    s_write = 140

    s_writeb = 141

    s_writeo = 142

    s_writeh = 143

    s_strobe = 144

    s_strobeb = 145

    s_strobeo = 146

    s_strobeh = 147

    s_monitor = 148

    s_monitorb = 149

    s_monitoro = 150

    s_monitorh = 151

    s_fdisplay = 152

    s_fdisplayb = 153

    s_fdisplayo = 154

    s_fdisplayh = 155

    s_fwrite = 156

    s_fwriteb = 157

    s_fwriteo = 158

    s_fwriteh = 159

    s_fstrobe = 160

    s_fstrobeb = 161

    s_fstrobeo = 162

    s_fstrobeh = 163

    s_fmonitor = 164

    s_fmonitorb = 165

    s_fmonitoro = 166

    s_fmonitorh = 167

    s_swrite = 168

    s_swriteb = 169

    s_swriteo = 170

    s_swriteh = 171

    s_sformat = 172

    s_printtimescale = 173

    s_dumpvars = 174

    s_dumpports = 175

    s_showvars = 176

    s_readmemb = 177

    s_readmemh = 178

    s_writememb = 179

    s_writememh = 180

    s_sreadmemb = 181

    s_sreadmemh = 182

    s_system = 183

    s_list = 184

    s_scope = 185

    s_exit = 186

    s_timeformat = 187

    s_monitoron = 188

    s_monitoroff = 189

    s_dumpfile = 190

    s_dumpon = 191

    s_dumpoff = 192

    s_dumpall = 193

    s_dumplimit = 194

    s_dumpflush = 195

    s_dumpportson = 196

    s_dumpportsoff = 197

    s_dumpportsall = 198

    s_dumpportslimit = 199

    s_dumpportsflush = 200

    s_input = 201

    s_key = 202

    s_nokey = 203

    s_log = 204

    s_nolog = 205

    s_reset = 206

    s_save = 207

    s_restart = 208

    s_incsave = 209

    s_showscopes = 210

    s_q_initialize = 211

    s_q_add = 212

    s_q_remove = 213

    s_q_exam = 214

    s_q_full = 215

    s_async_and_array = 216

    s_sync_and_array = 217

    s_async_and_plane = 218

    s_sync_and_plane = 219

    s_async_nand_array = 220

    s_sync_nand_array = 221

    s_async_nand_plane = 222

    s_sync_nand_plane = 223

    s_async_or_array = 224

    s_sync_or_array = 225

    s_async_or_plane = 226

    s_sync_or_plane = 227

    s_async_nor_array = 228

    s_sync_nor_array = 229

    s_async_nor_plane = 230

    s_sync_nor_plane = 231

    reverse = 232

    delete = 233

    exists = 234

    insert = 235

    index = 236

    map = 237

    size = 238

    xor = 241

    sum = 242

    product = 243

    find = 244

    find_index = 245

    find_first = 246

    find_first_index = 247

    find_last = 248

    find_last_index = 249

    min = 250

    max = 251

    unique = 252

    unique_index = 253

    sort = 254

    rsort = 255

    shuffle = 256

    num = 257

    first = 258

    last = 259

    next = 260

    prev = 261

    pop_front = 262

    pop_back = 263

    push_front = 264

    push_back = 265

    name = 266

    len = 267

    putc = 268

    getc = 269

    substr = 270

    toupper = 271

    tolower = 272

    compare = 273

    icompare = 274

    atoi = 275

    atohex = 276

    atooct = 277

    atobin = 278

    atoreal = 279

    itoa = 280

    hextoa = 281

    octtoa = 282

    bintoa = 283

    realtoa = 284

    rand_mode = 285

    constraint_mode = 286

class Trivia:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, kind: TriviaKind, rawText: str) -> None: ...

    @property
    def kind(self) -> TriviaKind: ...

    def getExplicitLocation(self) -> pyslang.SourceLocation | None: ...

    def syntax(self) -> pyslang.syntax.SyntaxNode: ...

    def getRawText(self) -> str: ...

    def getSkippedTokens(self) -> span[Token]: ...

    def __repr__(self) -> str: ...

class Token:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, alloc: pyslang.BumpAllocator, kind: TokenKind, trivia: span[Trivia], rawText: str, location: pyslang.SourceLocation) -> None: ...

    @overload
    def __init__(self, alloc: pyslang.BumpAllocator, kind: TokenKind, trivia: span[Trivia], rawText: str, location: pyslang.SourceLocation, strText: str) -> None: ...

    @overload
    def __init__(self, alloc: pyslang.BumpAllocator, kind: TokenKind, trivia: span[Trivia], rawText: str, location: pyslang.SourceLocation, directive: pyslang.syntax.SyntaxKind) -> None: ...

    @overload
    def __init__(self, alloc: pyslang.BumpAllocator, kind: TokenKind, trivia: span[Trivia], rawText: str, location: pyslang.SourceLocation, bit: pyslang.logic_t) -> None: ...

    @overload
    def __init__(self, alloc: pyslang.BumpAllocator, kind: TokenKind, trivia: span[Trivia], rawText: str, location: pyslang.SourceLocation, value: pyslang.SVInt) -> None: ...

    @overload
    def __init__(self, alloc: pyslang.BumpAllocator, kind: TokenKind, trivia: span[Trivia], rawText: str, location: pyslang.SourceLocation, value: float, outOfRange: bool, timeUnit: pyslang.TimeUnit | None) -> None: ...

    @overload
    def __init__(self, alloc: pyslang.BumpAllocator, kind: TokenKind, trivia: span[Trivia], rawText: str, location: pyslang.SourceLocation, base: pyslang.LiteralBase, isSigned: bool) -> None: ...

    @property
    def kind(self) -> TokenKind: ...

    @property
    def isMissing(self) -> bool: ...

    @property
    def range(self) -> pyslang.SourceRange: ...

    @property
    def location(self) -> pyslang.SourceLocation: ...

    @property
    def trivia(self) -> list[Trivia]: ...

    @property
    def valueText(self) -> str: ...

    @property
    def rawText(self) -> str: ...

    @property
    def isOnSameLine(self) -> bool: ...

    @property
    def value(self) -> object: ...

    def __eq__(self, arg: Token, /) -> bool: ...

    def __ne__(self, arg: Token, /) -> bool: ...

    def __bool__(self) -> bool: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

class LexerOptions:
    def __init__(self) -> None: ...

    @property
    def maxErrors(self) -> int: ...

    @maxErrors.setter
    def maxErrors(self, arg: int, /) -> None: ...

    @property
    def languageVersion(self) -> pyslang.LanguageVersion: ...

    @languageVersion.setter
    def languageVersion(self, arg: pyslang.LanguageVersion, /) -> None: ...

    @property
    def enableLegacyProtect(self) -> bool: ...

    @enableLegacyProtect.setter
    def enableLegacyProtect(self, arg: bool, /) -> None: ...

    @property
    def commentHandlers(self) -> dict[str, dict[str, pyslang.syntax.CommentHandler]]: ...

    @commentHandlers.setter
    def commentHandlers(self, arg: Mapping[str, Mapping[str, pyslang.syntax.CommentHandler]], /) -> None: ...

class Lexer:
    def __init__(self, buffer: pyslang.SourceBuffer, alloc: pyslang.BumpAllocator, diagnostics: pyslang.Diagnostics, sourceManager: pyslang.SourceManager, options: LexerOptions = ...) -> None: ...

    def lex(self) -> Token: ...

    def isNextTokenOnSameLine(self) -> bool: ...

    @property
    def library(self) -> pyslang.SourceLibrary: ...

    @property
    def bufferId(self) -> pyslang.BufferID: ...

class PreprocessorOptions:
    def __init__(self) -> None: ...

    @property
    def maxIncludeDepth(self) -> int: ...

    @maxIncludeDepth.setter
    def maxIncludeDepth(self, arg: int, /) -> None: ...

    @property
    def languageVersion(self) -> pyslang.LanguageVersion: ...

    @languageVersion.setter
    def languageVersion(self, arg: pyslang.LanguageVersion, /) -> None: ...

    @property
    def predefineSource(self) -> str: ...

    @predefineSource.setter
    def predefineSource(self, arg: str, /) -> None: ...

    @property
    def predefines(self) -> list[str]: ...

    @predefines.setter
    def predefines(self, arg: Sequence[str], /) -> None: ...

    @property
    def undefines(self) -> list[str]: ...

    @undefines.setter
    def undefines(self, arg: Sequence[str], /) -> None: ...

    @property
    def additionalIncludePaths(self) -> list[pathlib.Path]: ...

    @additionalIncludePaths.setter
    def additionalIncludePaths(self, arg: Sequence[str | os.PathLike], /) -> None: ...

    @property
    def ignoreDirectives(self) -> set[str]: ...

    @ignoreDirectives.setter
    def ignoreDirectives(self, arg: Set[str], /) -> None: ...

    @property
    def keywordMapping(self) -> list[tuple[str, "slang::parsing::KeywordVersion"]]: ...

    @keywordMapping.setter
    def keywordMapping(self, arg: Sequence[tuple[str, "slang::parsing::KeywordVersion"]], /) -> None: ...

class ParserOptions:
    def __init__(self) -> None: ...

    @property
    def maxRecursionDepth(self) -> int: ...

    @maxRecursionDepth.setter
    def maxRecursionDepth(self, arg: int, /) -> None: ...

    @property
    def languageVersion(self) -> pyslang.LanguageVersion: ...

    @languageVersion.setter
    def languageVersion(self, arg: pyslang.LanguageVersion, /) -> None: ...
