# Module 10 Part 1: Topics 1 to 25 (Kotlin Core & Advanced Deep Dive)

topics_1_to_25 = [
    {
        "id": "t1",
        "number": 1,
        "category": "Kotlin Core",
        "title": "val vs var vs const val (Bytecode, Immutability & Inlining)",
        "why": "Understanding immutability prevents unexpected mutation bugs, enables safe multi-threading, and lets the compiler optimize runtime constants.",
        "how": "In Kotlin bytecode, `val` generates a private final field with a getter (read-only reference, but internal object state can still mutate). `var` generates a non-final field with both getter and setter. `const val` is evaluated at compile time; the compiler directly inlines the primitive or String literal everywhere it is referenced, completely eliminating function call overhead and bytecode field lookups.",
        "code": """// Compile-time constant (inlined directly into bytecode at call sites)
const val TIMEOUT_MS = 5000L

class UserSession {
    // Read-only reference: cannot be reassigned, but list contents can change
    val activeTokens: MutableList<String> = mutableListOf("tok_1")

    // Mutable variable: can be reassigned freely
    var retryCount: Int = 0

    fun test() {
        // TIMEOUT_MS is replaced with 5000L in compiled bytecode
        val delay = TIMEOUT_MS
        activeTokens.add("tok_2") // Valid: modifying internal state
        // activeTokens = mutableListOf() // Error: Val cannot be reassigned
    }
}""",
        "takeaway": "Default to `val` for thread-safe immutability. Use `const val` only for top-level or companion primitive/String constants known at compile time."
    },
    {
        "id": "t2",
        "number": 2,
        "category": "Kotlin Core",
        "title": "Extension Functions & Member Resolution (Static Dispatch)",
        "why": "Extension functions let you add capabilities to third-party or platform classes (like Android Context or String) without inheritance or utility class clutter.",
        "how": "Extension functions do NOT modify the target class or insert methods into it. The Kotlin compiler generates a standard static Java method where the receiver instance (`this`) becomes the first parameter. Because they are resolved statically at compile time, if a class has a member function and an extension function with the exact same name and signature, the member function ALWAYS wins.",
        "code": """// Extension function on Android Context
fun Context.showToast(message: String, duration: Int = Toast.LENGTH_SHORT) {
    Toast.makeText(this, message, duration).show()
}

// Under the hood in decompiled Java bytecode:
// public static final void showToast(@NotNull Context $this, @NotNull String message, int duration) {
//     Toast.makeText($this, message, duration).show();
// }

// Usage in an Activity:
showToast("Order submitted!")""",
        "takeaway": "Extension functions are purely static sugar resolved at compile time based on the declared reference type, not the runtime instance type."
    },
    {
        "id": "t3",
        "number": 3,
        "category": "Kotlin Core",
        "title": "Higher-Order Functions & Lambda Inlining (inline, noinline, crossinline)",
        "why": "Passing lambdas in standard functions creates hidden Function objects in heap memory on every invocation, causing garbage collection pauses in hot loops.",
        "how": "`inline` instructs the compiler to copy the entire function body and lambda code directly into the calling site, eliminating object allocation and virtual method dispatch. `noinline` prevents specific lambdas in an inlined function from being inlined (e.g., if you need to store or pass the lambda). `crossinline` allows inlining while forbidding non-local returns (e.g., calling `return` inside a lambda executed in a different execution context like a Runnable).",
        "code": """// Inlined higher-order function with crossinline guard
inline fun <T> measureExecutionTime(
    tag: String,
    crossinline onAsyncFinish: () -> Unit,
    noinline errorLogger: ((Exception) -> Unit)?,
    block: () -> T
): T {
    val start = System.currentTimeMillis()
    val result = block() // Inlined directly into caller bytecode
    println("$tag took ${System.currentTimeMillis() - start} ms")
    
    // crossinline prevents non-local return inside this lambda
    Thread { onAsyncFinish() }.start()
    return result
}""",
        "takeaway": "Use `inline` for functions taking lambdas called frequently (e.g. locks, measurements, collections). Avoid inlining huge functions to prevent bytecode bloat."
    },
    {
        "id": "t4",
        "number": 4,
        "category": "Kotlin Core",
        "title": "Data Classes (copy(), equals(), hashCode(), ComponentN & Destructuring)",
        "why": "Eliminates hundreds of lines of boilerplate for immutable value-holding models used across network, database, and UI layers.",
        "how": "For properties declared in the primary constructor, the compiler automatically generates `equals()`, `hashCode()`, `toString()`, `copy()`, and positional `component1()`, `component2()` functions. Destructuring declarations (`val (id, name) = user`) rely entirely on these generated `componentN()` functions, which match constructor argument order, NOT property names.",
        "code": """data class UserProfile(
    val id: String,
    val name: String,
    val email: String,
    val isActive: Boolean = true
)

fun handleUser(user: UserProfile) {
    // copy() creates a new immutable instance with specific modifications
    val updated = user.copy(isActive = false)

    // Destructuring: translates to user.component1() and user.component2()
    val (userId, userName) = updated
    println("User: $userName (ID: $userId)")
}""",
    "takeaway": "Only declare immutable properties (`val`) in data class primary constructors to guarantee hash code consistency in Maps and Sets."
    },
    {
        "id": "t5",
        "number": 5,
        "category": "Kotlin Core",
        "title": "Sealed Classes & Sealed Interfaces (Algebraic Data Types & Exhaustive When)",
        "why": "Models restricted class hierarchies where a type can only be one of a predefined set of subtypes, enabling compiler-enforced exhaustive state handling.",
        "how": "All direct subclasses of a sealed class/interface must be known at compile time and located in the same module/package. When using a `when` expression on a sealed type, the Kotlin compiler checks that every possible subtype is handled. If all branches are covered, no `else` branch is required. Adding a new subtype immediately causes a compile-time error wherever the `when` is missing it.",
        "code": """sealed interface NetworkState<out T> {
    object Loading : NetworkState<Nothing>
    data class Success<T>(val data: T) : NetworkState<T>
    data class Error(val throwable: Throwable) : NetworkState<Nothing>
}

// Exhaustive when check (no else branch needed)
fun render(state: NetworkState<List<String>>) = when (state) {
    is NetworkState.Loading -> showProgressBar()
    is NetworkState.Success -> showList(state.data)
    is NetworkState.Error -> showError(state.throwable.message)
}""",
        "takeaway": "Use sealed interfaces for UI States and Domain Events so adding a new state forces every handler screen to explicitly handle it at compile time."
    },
    {
        "id": "t6",
        "number": 6,
        "category": "Kotlin Core",
        "title": "Kotlin Generics: Variance (out Covariance, in Contravariance, Star Projection)",
        "why": "Provides type safety when dealing with polymorphic collections and producer/consumer generic interfaces.",
        "how": "`out T` (Covariance / Producer): You can read `T` from the class, but cannot write `T` into it (`List<out Number>` allows assigning `List<Int>`). `in T` (Contravariance / Consumer): You can pass `T` into the class methods, but cannot read specific `T` out (`Comparable<in String>`). Star projection `*` represents an unknown type safely (`List<*>` allows reading `Any?`).",
        "code": """// Producer (Covariant): Produces T, never consumes T
interface Source<out T> {
    fun next(): T
}

// Consumer (Contravariant): Consumes T, never produces T
interface Sink<in T> {
    fun consume(item: T)
}

fun copy(from: Source<Int>, to: Sink<Number>) {
    val num: Number = from.next() // Valid: Int is a subtype of Number
    to.consume(num)               // Valid: Sink accepts Number and subtypes
}""",
        "takeaway": "Remember PECS: Producer Out, Consumer In. Use `out` when your class only returns/emits types, `in` when it only accepts parameters."
    },
    {
        "id": "t7",
        "number": 7,
        "category": "Kotlin Core",
        "title": "Reified Type Parameters (inline fun <reified T>)",
        "why": "Java type erasure deletes generic type information at runtime, making `T::class.java` impossible in standard generic functions.",
        "how": "By combining `inline` with `reified`, the compiler inlines the function directly into the call site where the actual type argument is known. It replaces generic type references with the concrete class literal (e.g. `String::class.java`) in the compiled bytecode, enabling runtime type checks (`is T`), class reflection, and JSON deserialization.",
        "code": """// Reified type helper for Gson / Moshi deserialization
inline fun <reified T> String.fromJson(): T {
    return Gson().fromJson(this, T::class.java)
}

// Reified type helper for Android Intent navigation
inline fun <reified T : Activity> Context.startActivity() {
    startActivity(Intent(this, T::class.java))
}

// Clean usage without passing Class<T> parameter manually:
val user = jsonString.fromJson<UserProfile>()
context.startActivity<DetailActivity>()""",
        "takeaway": "Use `reified` whenever you need reflection, `instanceof` checks (`is T`), or class tokens without forcing callers to pass `Class<T>`."
    },
    {
        "id": "t8",
        "number": 8,
        "category": "Kotlin Coroutines",
        "title": "Coroutines: Continuation-Passing Style (CPS) & State Machine Internals",
        "why": "Allows writing asynchronous, non-blocking code sequentially without callback hell or blocking expensive OS threads.",
        "how": "The Kotlin compiler transforms every `suspend` function into a state machine implementing the `Continuation<T>` interface. Every suspension point becomes a label in a `switch/when` table. When a coroutine suspends, it returns `COROUTINE_SUSPENDED` and saves its local variables into the Continuation object. When the async operation finishes, `continuation.resumeWith()` is invoked to restore state and resume at the next label.",
        "code": """// Suspend function written sequentially
suspend fun fetchAndProcess(): String {
    val token = fetchAuthToken() // Suspension point 1 (State 0 -> State 1)
    val data = fetchUserData(token) // Suspension point 2 (State 1 -> State 2)
    return formatData(data) // State 2 -> Return
}

// Under the hood, compiler compiles to:
// Object fetchAndProcess(Continuation<String> $completion) {
//     switch(continuation.label) {
//         case 0: ... fetchAuthToken(this); return COROUTINE_SUSPENDED;
//         case 1: ... fetchUserData(token, this); return COROUTINE_SUSPENDED;
//         case 2: ... return formatData(data);
//     }
// }""",
        "takeaway": "Coroutines are non-blocking state machines that pause execution and free their underlying thread until resumed via their Continuation callback."
    },
    {
        "id": "t9",
        "number": 9,
        "category": "Kotlin Coroutines",
        "title": "Coroutine Builders: launch vs async vs runBlocking",
        "why": "Different asynchronous tasks require different execution semantics (fire-and-forget vs returning computed values vs blocking unit test runners).",
        "how": "`launch` starts a fire-and-forget coroutine returning a `Job` (does not return a result value directly). `async` starts a deferred coroutine returning `Deferred<T>` which computes a value retrieved via `await()`. `runBlocking` blocks the current thread until the coroutine finishes (used exclusively in `main()` entrypoints and unit tests, never in production UI code).",
        "code": """// Parallel async fetching with CoroutineScope
fun loadDashboardData(scope: CoroutineScope) = scope.launch {
    // Both network calls execute concurrently in parallel
    val profileDeferred = async(Dispatchers.IO) { api.fetchProfile() }
    val ordersDeferred = async(Dispatchers.IO) { api.fetchOrders() }

    // Await results concurrently
    val profile = profileDeferred.await()
    val orders = ordersDeferred.await()
    
    renderUi(profile, orders)
}""",
        "takeaway": "Use `launch` for fire-and-forget actions and UI events. Use `async` when you need parallel decomposition and must combine return values."
    },
    {
        "id": "t10",
        "number": 10,
        "category": "Kotlin Coroutines",
        "title": "Coroutine Cancellation & Cooperative Checking (ensureActive, yield, NonCancellable)",
        "why": "Coroutines must be cancelled when screens close to prevent memory leaks, background CPU waste, and obsolete network processing.",
        "how": "Cancellation in Kotlin coroutines is cooperative. When a Job is cancelled, it enters the `Cancelling` state. Standard suspending functions (`delay`, `withContext`) check for cancellation automatically and throw `CancellationException`. Long-running CPU loops do NOT suspend, so they must explicitly invoke `ensureActive()` or `yield()` to check for cancellation. Cleanup code that must finish during cancellation must use `withContext(NonCancellable)`.",
        "code": """suspend fun processLargeBitmap(pixels: IntArray) = withContext(Dispatchers.Default) {
    for (i in pixels.indices) {
        ensureActive() // Throws CancellationException if job was cancelled
        pixels[i] = applyFilter(pixels[i])
    }
}

suspend fun safeFileWrite(file: File, bytes: ByteArray) {
    try {
        writeFile(file, bytes)
    } finally {
        // Critical cleanup runs even if parent coroutine was cancelled
        withContext(NonCancellable) {
            closeFileHandles()
        }
    }
}""",
        "takeaway": "Always call `ensureActive()` in tight CPU computation loops so they cancel immediately when the user exits the screen."
    },
    {
        "id": "t11",
        "number": 11,
        "category": "Kotlin Coroutines",
        "title": "Coroutine Context & Dispatchers (Main, IO, Default, limitedParallelism)",
        "why": "Offloads blocking disk I/O and heavy CPU computation away from Android's 60/120 FPS Main UI thread to prevent UI freezing and ANRs.",
        "how": "`Dispatchers.Main` runs on Android's main Looper for UI mutations. `Dispatchers.IO` uses an elastic thread pool (default up to 64 threads) optimized for blocking disk/network I/O. `Dispatchers.Default` uses a fixed thread pool bounded by CPU core count (minimum 2) for heavy computations (JSON parsing, diffing, crypto). `limitedParallelism(N)` creates a sub-dispatcher with a strict concurrency limit without spinning up new threads.",
        "code": """class ProductRepository @Inject constructor() {
    // Restricts heavy SQLite writes to a single thread to avoid database locks
    private val dbDispatcher = Dispatchers.IO.limitedParallelism(1)

    suspend fun parseAndSave(jsonString: String) {
        // Heavy JSON parsing on CPU threads
        val products = withContext(Dispatchers.Default) {
            Json.decodeFromString<List<Product>>(jsonString)
        }
        
        // Serialized DB write on dedicated single-thread dispatcher
        withContext(dbDispatcher) {
            database.insertAll(products)
        }
    }
}""",
        "takeaway": "Use `Dispatchers.Default` for CPU computations, `Dispatchers.IO` for network/disk, and `limitedParallelism` to throttle concurrent operations."
    },
    {
        "id": "t12",
        "number": 12,
        "category": "Kotlin Coroutines",
        "title": "Exception Handling: Job vs SupervisorJob & CoroutineExceptionHandler",
        "why": "Uncaught coroutine exceptions can silently crash unrelated background tasks or cancel entire UI screens if structured concurrency is improperly configured.",
        "how": "In a standard `Job`, an unhandled exception in any child coroutine immediately cancels its parent Job, which cascades cancellation to all sibling coroutines. In a `SupervisorJob`, failure of one child does NOT cancel the parent or other children. `CoroutineExceptionHandler` can be attached to root scopes to catch unhandled exceptions, but it only catches exceptions from `launch` (exceptions from `async` are encapsulated in `Deferred` and thrown upon calling `.await()`).",
        "code": """// Supervisor scope ensures independent widget execution
val customExceptionHandler = CoroutineExceptionHandler { _, throwable ->
    Timber.e(throwable, "Background task failed safely")
}

val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default + customExceptionHandler)

fun loadDashboard() = scope.launch {
    // If fetchBanner crashes, fetchUserList STILL continues running!
    launch { fetchBanner() }
    launch { fetchUserList() }
}""",
        "takeaway": "Always use `SupervisorJob` when orchestrating independent parallel child tasks so that one widget failure does not break the entire screen."
    },
    {
        "id": "t13",
        "number": 13,
        "category": "Kotlin Flow",
        "title": "Cold Flows vs Hot Flows (Flow, StateFlow, SharedFlow, Channel)",
        "why": "Choosing the right stream type ensures predictable UI state holding, avoids missing one-off events, and prevents memory leaks.",
        "how": "`Flow` is Cold: code inside the builder does not execute until a terminal operator (`collect`) is called; each collector gets a fresh stream. `StateFlow` is Hot: holds a single conflated value, always requires an initial state, and replays the latest state to new collectors. `SharedFlow` is Hot: broadcasts events to zero or more collectors with configurable replay and buffer capacities. `Channel` is a hot point-to-point communication pipeline where each message is consumed by exactly one receiver.",
        "code": """// Cold Flow (runs on demand per collector)
fun coldDataStream(): Flow<Int> = flow {
    emit(fetchFromNetwork())
}

// Hot StateFlow (holds state, conflated, UI state holder)
val uiState: StateFlow<UiState> = _uiState.asStateFlow()

// Hot SharedFlow (one-off event bus, no replay)
val eventFlow = MutableSharedFlow<UiEvent>(replay = 0, extraBufferCapacity = 1)""",
        "takeaway": "Use `StateFlow` for observable UI state. Use `SharedFlow` or `Channel` for transient one-off events like navigation and snackbars."
    },
    {
        "id": "t14",
        "number": 14,
        "category": "Kotlin Flow",
        "title": "Flow Operators: flatMapConcat vs flatMapMerge vs flatMapLatest",
        "why": "Transforming upstream emissions into downstream flows requires choosing the correct concurrency and cancellation behavior.",
        "how": "`flatMapConcat` transforms emissions sequentially, waiting for the inner flow to complete before processing the next upstream item. `flatMapMerge` processes multiple inner flows concurrently in parallel up to a concurrency limit. `flatMapLatest` cancels the currently executing inner flow as soon as a new emission arrives from the upstream flow.",
        "code": """// Real-time search query pipeline
searchQueryFlow
    .debounce(300L)
    .distinctUntilChanged()
    // Whenever a new query arrives, previous search API call is CANCELLED immediately
    .flatMapLatest { query ->
        searchApi.searchFlow(query)
    }
    .flowOn(Dispatchers.IO)
    .collect { results -> render(results) }""",
        "takeaway": "Use `flatMapLatest` for search and autocomplete queries to automatically cancel obsolete in-flight network requests."
    },
    {
        "id": "t15",
        "number": 15,
        "category": "Kotlin Flow",
        "title": "Flow Backpressure Strategies & Buffer Overflow Policies",
        "why": "Fast producers emitting data faster than slow collectors can process will cause unbounded memory buffering or coroutine suspension.",
        "how": "By default, Flow backpressures by suspending the emitter until the collector is ready. You can buffer emissions using `.buffer(capacity, onBufferOverflow)`. Overflow policies include `BufferOverflow.SUSPEND` (suspends emitter), `BufferOverflow.DROP_OLDEST` (drops oldest buffered value to insert newest), and `BufferOverflow.DROP_LATEST` (drops newest value if buffer is full). `.conflate()` is equivalent to `buffer(0, DROP_OLDEST)`.",
        "code": """// Handling high-frequency hardware sensor emissions (100 Hz)
sensorFlow
    .buffer(
        capacity = 16,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    .collect { slowUiRender(it) } // Collector runs at 30 Hz without blocking sensor thread""",
        "takeaway": "Apply `DROP_OLDEST` or `.conflate()` for UI state and telemetry feeds where rendering only the freshest value matters."
    },
    {
        "id": "t16",
        "number": 16,
        "category": "Kotlin Core",
        "title": "Kotlin Scope Functions (let, run, with, apply, also) - Decision Tree",
        "why": "Scope functions execute code blocks within an object's context, making object configuration, null checks, and transformations concise and readable.",
        "how": "They differ by how the context object is referenced (`this` vs `it`) and what they return (the context object vs the lambda result). `apply` (this, returns object): configuring properties. `also` (it, returns object): side-effects like logging. `let` (it, returns lambda result): null checks and mappings. `run` (this, returns lambda result): computing values on receiver. `with` (this, returns lambda result): non-extension grouping calls.",
        "code": """// 1. apply: Object configuration
val intent = Intent(this, DetailActivity::class.java).apply {
    putExtra("KEY_ID", 42)
    flags = Intent.FLAG_ACTIVITY_NEW_TASK
}

// 2. let: Safe call execution and mapping
userEmail?.let { email -> sendVerification(email) }

// 3. also: Logging side-effect without modifying flow
val validatedUser = user.validate().also { Timber.d("Validated: $it") }""",
        "takeaway": "Use `apply` for object initialization, `let` for safe null mapping, and `also` for external side-effects like logging."
    },
    {
        "id": "t17",
        "number": 17,
        "category": "Kotlin Core",
        "title": "Delegation & Built-in Property Delegates (by lazy, observable, vetoable)",
        "why": "Delegation pattern shifts property getter/setter logic to reusable delegate objects, eliminating redundant lazy-init boilerplate.",
        "how": "When a property is declared `by delegate`, the compiler generates an auxiliary delegate object. Calling the getter calls `delegate.getValue()`; calling setter calls `delegate.setValue()`. `by lazy` computes value only on first access and caches it with thread-safety (`LazyThreadSafetyMode.SYNCHRONIZED` by default). `Delegates.observable` triggers a callback on change. `Delegates.vetoable` allows intercepting and vetoing proposed changes.",
        "code": """// Thread-safe lazy initialization
val expensiveService: CryptoService by lazy {
    CryptoService.initializeHardwareKeys()
}

// Vetoable delegate (only allows positive balance updates)
var accountBalance: Double by Delegates.vetoable(0.0) { _, old, new ->
    new >= 0.0 // Reject update if new balance is negative
}""",
        "takeaway": "Use `by lazy` for expensive-to-create objects. Use `LazyThreadSafetyMode.NONE` in UI ViewModels if access is strictly Main-thread only."
    },
    {
        "id": "t18",
        "number": 18,
        "category": "Kotlin Core",
        "title": "Custom Property Delegates (ReadOnlyProperty, ReadWriteProperty)",
        "why": "Encapsulates repetitive state binding patterns like Android SharedPreferences, Bundle arguments, or ViewBinding references into clean syntax.",
        "how": "A custom delegate implements `ReadOnlyProperty<R, T>` (provides `getValue(thisRef, property)`) or `ReadWriteProperty<R, T>` (adds `setValue(thisRef, property, value)`). The `thisRef` parameter provides access to the enclosing class instance, while `KProperty<*>` provides property metadata (name, return type).",
        "code": """// Custom Fragment Argument delegate
class FragmentArgument<T : Any> : ReadOnlyProperty<Fragment, T> {
    override fun getValue(thisRef: Fragment, property: KProperty<*>): T {
        val key = property.name
        return thisRef.arguments?.get(key) as? T
            ?: throw IllegalStateException("Missing required argument: $key")
    }
}

fun <T : Any> fragmentArg() = FragmentArgument<T>()

// Usage in Fragment:
class DetailFragment : Fragment() {
    private val userId: String by fragmentArg() // Reads arguments.getString("userId")
}""",
        "takeaway": "Write custom delegates to eliminate repeated boilerplate for Bundle arguments, SharedPreferences, and database caches."
    },
    {
        "id": "t19",
        "number": 19,
        "category": "Kotlin Core",
        "title": "Object Declarations, Companion Objects & @JvmStatic / @JvmField",
        "why": "Kotlin replaces Java's static members with first-class singleton objects and companion objects, but interop with Java requires explicit bytecode annotations.",
        "how": "`object` compiles to a thread-safe singleton with a private constructor and a static `INSTANCE` field initialized in a static initializer block. `companion object` is a nested singleton inside a class. `@JvmStatic` instructs the compiler to generate true static methods in the enclosing Java class bytecode. `@JvmField` exposes a public field directly without generating getter/setter methods.",
        "code": """class NetworkConfig {
    companion object {
        @JvmField
        val BASE_URL = "https://api.lenskart.com"

        @JvmStatic
        fun createDefaultHeader(): Map<String, String> {
            return mapOf("Content-Type" to "application/json")
        }
    }
}

// In Java: NetworkConfig.BASE_URL (direct field) and NetworkConfig.createDefaultHeader() (direct static method)""",
        "takeaway": "Use `@JvmStatic` and `@JvmField` on companion object members when creating shared libraries called from legacy Java code."
    },
    {
        "id": "t20",
        "number": 20,
        "category": "Kotlin Core",
        "title": "Inline Value Classes (@JvmInline value class) & Zero-Allocation Wrappers",
        "why": "Provides domain-specific type safety (e.g. distinguishing `UserId` from `ProductId`) without the memory overhead of heap object instantiation.",
        "how": "Annotating a class with `@JvmInline value class` forces the compiler to unbox the value in bytecode wherever possible. At runtime, the underlying primitive or reference type is used directly without allocating a wrapper object on the heap. Boxing occurs only when the value class is passed to a generic type or boxed interface.",
        "code": """@JvmInline
value class UserId(val rawId: String)

@JvmInline
value class OrderId(val rawId: String)

// Compiler prevents accidental mixing of ID types:
fun processOrder(userId: UserId, orderId: OrderId) {
    // In bytecode, parameters are compiled as standard String primitives!
}

// processOrder(orderId, userId) -> Compile error: Type mismatch!""",
        "takeaway": "Use `@JvmInline value class` for strongly-typed IDs, currency amounts, and password wrappers to get type safety with zero heap overhead."
    },
    {
        "id": "t21",
        "number": 21,
        "category": "Kotlin Core",
        "title": "Operator Overloading & Custom DSL Builders (@DslMarker)",
        "why": "Enables creation of expressive, domain-specific declarative languages (like Jetpack Compose UI or HTML/Gradle builders) with compile-time scope safety.",
        "how": "Kotlin allows overloading a predefined set of operators (`+`, `-`, `*`, `[]`, `invoke`) by adding the `operator` modifier to member or extension functions. `@DslMarker` is a meta-annotation that prevents outer receiver scopes from being inadvertently accessed inside nested lambda builder blocks without explicit qualifiers.",
        "code": """@DslMarker
annotation class LayoutDsl

@LayoutDsl
class RowBuilder {
    fun text(value: String) { println("Text: $value") }
}

fun row(block: RowBuilder.() -> Unit) = RowBuilder().apply(block)

// Clean DSL usage:
row {
    text("Item 1")
    text("Item 2")
}""",
        "takeaway": "Annotate all nested lambda builders with `@DslMarker` to prevent scope leakage bugs in complex declarative DSLs."
    },
    {
        "id": "t22",
        "number": 22,
        "category": "Kotlin Core",
        "title": "Sequences vs Collections (Lazy Evaluation & Intermediate Allocations)",
        "why": "Chaining standard collection operators (`filter`, `map`) creates a brand-new intermediate ArrayList on every step, wasting memory on large datasets.",
        "how": "Standard Collections use eager evaluation: `list.map { }.filter { }` traverses the entire list and allocates a new collection at each step. `Sequence` uses lazy evaluation: operations are pipeline elements evaluated element-by-element only when a terminal operator (like `toList()` or `first()`) is reached. Elements that fail early filters never execute subsequent downstream maps.",
        "code": """val items = (1..100_000).toList()

// Collection (Eager): Creates 2 intermediate 100k lists in heap
val eagerResult = items
    .map { it * 2 }
    .filter { it % 3 == 0 }
    .first()

// Sequence (Lazy): Evaluates element-by-element; stops on first match!
val lazyResult = items.asSequence()
    .map { it * 2 }
    .filter { it % 3 == 0 }
    .first() // Only processes elements until the first match is found!""",
        "takeaway": "Use `asSequence()` when chaining multi-step transformations on large collections (1000+ items) or when using short-circuit terminal operations (`first`)."
    },
    {
        "id": "t23",
        "number": 23,
        "category": "Kotlin Core",
        "title": "Null Safety Internals (Safe Calls ?., Elvis ?:, Not-Null !!, Platform Types T!)",
        "why": "Eliminates Tony Hoare's 'Billion Dollar Mistake' (NullPointerException) at compile time while providing clear interop rules for Java APIs.",
        "how": "The Kotlin compiler enforces nullability in the type system. A nullable type `String?` compiles with runtime null assertion checks (`Intrinsics.checkNotNullParameter`). When calling Java code lacking `@Nullable`/`@NonNull` annotations, Kotlin treats types as Flexible/Platform Types (`T!`), which can be assigned as either nullable or non-null without compile warnings, shifting null checks to runtime.",
        "code": """fun getDisplayName(user: UserProfile?): String {
    // Safe call + Elvis operator fallback
    return user?.name ?: "Guest User"
}

// Java Interop handling:
fun parseJavaResult(javaApi: LegacyJavaApi) {
    // Treat platform type String! as explicitly nullable to avoid unexpected runtime NPEs
    val title: String? = javaApi.getTitle()
    println(title?.uppercase() ?: "NO TITLE")
}""",
        "takeaway": "Always assign Java platform types (`T!`) to explicitly nullable Kotlin types (`T?`) at boundary layers to avoid silent runtime NPEs."
    },
    {
        "id": "t24",
        "number": 24,
        "category": "Kotlin Core",
        "title": "Kotlin Collections: Mutable vs Read-Only vs Immutable (PersistentList)",
        "why": "Passing mutable collections into background threads or Jetpack Compose composables causes race conditions and breaks skippable recomposition optimization.",
        "how": "Kotlin's standard `List<T>` is a read-only interface, NOT an immutable collection. It merely lacks mutating methods, but the underlying instance could still be a `java.util.ArrayList` being mutated by another thread. `kotlinx.collections.immutable.PersistentList` uses structural sharing (trie nodes): mutations return a new persistent collection while sharing unchanged nodes in memory, guaranteeing true immutability and Compose stability.",
        "code": """// Standard read-only list (can still be mutated underneath)
val readOnlyList: List<String> = mutableListOf("A", "B")

// Truly immutable PersistentList for Compose stability
val immutableList: PersistentList<String> = persistentListOf("A", "B")
val updatedList = immutableList.add("C") // Returns new PersistentList in O(log N) time""",
        "takeaway": "Use `PersistentList` or `ImmutableList` for Compose UI state models to enable compiler skippability and prevent multi-threaded data tearing."
    },
    {
        "id": "t25",
        "number": 25,
        "category": "Kotlin Core",
        "title": "Contracts DSL (contract { returns() implies ... } for Smart Casting)",
        "why": "Custom validation functions (like `isNotNullOrEmpty()`) normally break Kotlin's smart-casting compiler mechanics unless explicit contracts are declared.",
        "how": "Kotlin Contracts allow functions to declare their behavioral guarantees to the compiler. Using `contract { returns(true) implies (value != null) }`, the compiler is instructed that if the function returns `true`, it is mathematically guaranteed that the inspected parameter is not null, enabling instant smart-casting in subsequent lines without manual `!!` casts.",
        "code": """@OptIn(ExperimentalContracts::class)
fun requireValidString(value: String?) {
    contract {
        returns() implies (value != null)
    }
    if (value.isNullOrBlank()) {
        throw IllegalArgumentException("String cannot be blank")
    }
}

fun process(input: String?) {
    requireValidString(input)
    // Smart-cast to non-null String automatically!
    println(input.length)
}""",
        "takeaway": "Use Kotlin Contracts in custom assertion, validation, and guard functions to unlock automatic smart-casting across your codebase."
    }
]

print(f"Loaded {len(topics_1_to_25)} topics for Part 1.")
