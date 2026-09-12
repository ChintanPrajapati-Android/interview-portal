import json

modules_data = [
    {
        "id": "module-1",
        "title": "Module 1: Architecture, Flow & Scalable Search",
        "badge": "Emerald",
        "color": "emerald",
        "summary": "StateFlow, Debounce, flatMapLatest, MVI, Dispatchers, Channels, and 99.85% Crash-Free SLA.",
        "questions": [
            {
                "id": "q1",
                "title": "1. How do you architect a high-scale real-time search with Coroutines and StateFlow?",
                "problem": "Uncontrolled keystroke emissions cause race conditions, UI jank, and backend search service saturation.",
                "solution": [
                    ("DEBOUNCE 300MS", "I debounce text inputs by three hundred milliseconds to throttle redundant query emissions effectively."),
                    ("DISTINCT FILTER", "I apply distinctUntilChanged to eliminate identical consecutive search string emissions completely."),
                    ("FLATMAPLATEST CANCELLATION", "I execute flatMapLatest to cancel in-flight network searches whenever newer queries arrive."),
                    ("FLOWON IO DISPATCHER", "I switch upstream flow execution to Dispatchers.IO using flowOn operator safely."),
                    ("CATCH FALLBACK", "I intercept all upstream pipeline exceptions using the catch operator gracefully."),
                    ("STATEIN SHARING", "I convert cold flows into StateFlow using stateIn with SharingStarted.WhileSubscribed.")
                ],
                "code": """// Production Debounced Search Flow in Android ViewModel
class SearchViewModel(private val repository: SearchRepository) : ViewModel() {
    private val _query = MutableStateFlow("")
    val searchResults: StateFlow<UiState<List<Item>>> = _query
        .debounce(300L)
        .distinctUntilChanged()
        .filter { it.trim().length >= 2 }
        .flatMapLatest { query ->
            repository.searchStream(query)
                .flowOn(Dispatchers.IO)
                .catch { emit(UiState.Error(it)) }
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000L),
            initialValue = UiState.Idle
        )
}""",
                "metric": "Maintained 99.85% crash-free sessions across 10M+ active users during peak flash sales."
            },
            {
                "id": "q2",
                "title": "2. Why choose MVI over standard MVVM for complex mission-critical screens?",
                "problem": "Scattered mutable UI state variables cause race conditions, conflicting UI states, and unpredictable state reproduction.",
                "solution": [
                    ("SINGLE SOURCE TRUTH", "I consolidate multiple mutable state variables into a single immutable UI data class."),
                    ("UNIDIRECTIONAL DATA FLOW", "I enforce strict unidirectional data flow where user intents drive state mutations."),
                    ("REDUCER DETERMINISM", "I process user intents through pure reducer functions to generate predictable states."),
                    ("SIDE EFFECT CHANNELS", "I dispatch one-off transient events like navigation and snackbars via Channel buffers."),
                    ("TIME TRAVEL DEBUG", "I log immutable sequential states enabling instant bug replication and automated testing.")
                ],
                "code": """// MVI Single Immutable State and Reducer Architecture
data class CartUiState(
    val items: List<CartItem> = emptyList(),
    val totalAmount: Double = 0.0,
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)

sealed interface CartIntent {
    data class AddItem(val productId: String) : CartIntent
    data class RemoveItem(val productId: String) : CartIntent
    object Checkout : CartIntent
}""",
                "metric": "Reduced UI state synchronization defects by 78% across complex multi-step checkout flows."
            },
            {
                "id": "q3",
                "title": "3. StateFlow vs SharedFlow: How do you choose between them in production?",
                "problem": "Misusing StateFlow for events causes duplicated toast/navigation events on screen rotation, while SharedFlow leaks memory if misused.",
                "solution": [
                    ("STATEFLOW FOR STATE", "I utilize StateFlow exclusively for holding and conflating observable UI state models."),
                    ("INITIAL VALUE REQUIREMENT", "StateFlow mandates an initial state and replays latest value to new collectors."),
                    ("SHAREDFLOW FOR EVENTS", "I configure SharedFlow without replay buffers to emit one-off transient broadcast events."),
                    ("EXTRA BUFFER CAPACITY", "I configure extraBufferCapacity to prevent coroutine suspension during high-frequency emissions."),
                    ("BUFFER OVERFLOW STRATEGY", "I set BufferOverflow.DROP_OLDEST to drop stale unconsumed UI notifications gracefully.")
                ],
                "code": """// StateFlow for State vs SharedFlow for One-off Events
class ProfileViewModel : ViewModel() {
    // UI State: Always holds latest value, conflated
    private val _uiState = MutableStateFlow(ProfileState.Loading)
    val uiState: StateFlow<ProfileState> = _uiState.asStateFlow()

    // Transient Events: No replay, dropped if no active collector
    private val _eventFlow = MutableSharedFlow<ProfileEvent>(
        replay = 0,
        extraBufferCapacity = 1,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    val eventFlow: SharedFlow<ProfileEvent> = _eventFlow.asSharedFlow()
}""",
                "metric": "Eliminated 100% of duplicate navigation and snackbar triggers during configuration changes."
            },
            {
                "id": "q4",
                "title": "4. How do you govern Coroutine Dispatchers and avoid thread starvation at scale?",
                "problem": "Hardcoding Dispatchers.IO or Dispatchers.Default makes unit tests untestable and causes thread pool starvation under heavy loads.",
                "solution": [
                    ("DEPENDENCY INJECTION", "I inject CoroutineDispatcher interfaces using Hilt to enable deterministic unit test mocking."),
                    ("LIMITED PARALLELISM", "I restrict background database writes using Dispatchers.IO.limitedParallelism(4) concurrency ceilings."),
                    ("DEFAULT FOR CPU", "I route JSON parsing and bitmap transformations strictly to Dispatchers.Default threads."),
                    ("MAIN IMMEDIATE", "I leverage Dispatchers.Main.immediate to execute UI updates without posting message delays."),
                    ("ZERO HARDCODING", "I ban direct Dispatcher references across domain and data layer class implementations.")
                ],
                "code": """// Injected Coroutine Dispatchers with Concurrency Ceilings
@Module
@InstallIn(SingletonComponent::class)
object DispatcherModule {
    @Provides
    @IoDispatcher
    fun provideIoDispatcher(): CoroutineDispatcher = Dispatchers.IO

    @Provides
    @DbDispatcher
    fun provideDbDispatcher(): CoroutineDispatcher = Dispatchers.IO.limitedParallelism(4)
}""",
                "metric": "Prevented thread starvation, keeping background thread pool utilization under 35% during heavy sync."
            },
            {
                "id": "q5",
                "title": "5. Channels vs SharedFlow: When is Channel strictly required?",
                "problem": "SharedFlow broadcasts to all collectors; if multiple collectors listen, events duplicate. Channels ensure single-subscriber delivery.",
                "solution": [
                    ("SINGLE SUBSCRIBER", "I choose Channels when each emitted event must be handled by exactly one receiver."),
                    ("QUEUE WORK PATTERN", "Channels implement classic queue semantics where multiple workers compete for sequential tasks."),
                    ("UNLIMITED VS BUFFERED", "I employ Channel.BUFFERED with capacity 64 to buffer rapid background event bursts."),
                    ("RECEIVE AS FLOW", "I expose Channel streams using channel.receiveAsFlow() for structured coroutine collection."),
                    ("CONSUME ONLY ONCE", "Channel guarantees each message is consumed once, preventing duplicated analytical dispatch.")
                ],
                "code": """// Channel for Single-Consumer Event Pipeline
class CheckoutViewModel : ViewModel() {
    private val _eventChannel = Channel<CheckoutEvent>(Channel.BUFFERED)
    val events = _eventChannel.receiveAsFlow()

    fun processPayment() {
        viewModelScope.launch {
            _eventChannel.send(CheckoutEvent.NavigateToReceipt)
        }
    }
}""",
                "metric": "Ensured 100% zero-loss, single-execution guarantee for critical payment analytics and navigation."
            },
            {
                "id": "q6",
                "title": "6. How do you implement Structured Concurrency with SupervisorJob?",
                "problem": "Uncaught exceptions in child coroutines cancel the entire parent Job, unintentionally breaking unrelated UI tasks.",
                "solution": [
                    ("SUPERVISOR ISOLATION", "I wrap child coroutine scopes with SupervisorJob to isolate individual child failures."),
                    ("COROUTINE EXCEPTION HANDLER", "I attach CoroutineExceptionHandler at root scope to intercept uncaught exceptions reliably."),
                    ("INDEPENDENT EXECUTION", "Child coroutine crashes do not cancel sibling tasks under SupervisorJob hierarchy."),
                    ("STRUCTURED TEARDOWN", "Cancelling the parent SupervisorJob automatically cancels all active descendant child jobs."),
                    ("ASYNC AWAIT HANDLING", "I wrap async await calls in runCatching to handle individual deferred exceptions.")
                ],
                "code": """// SupervisorJob Hierarchy with Structured Exception Handling
val exceptionHandler = CoroutineExceptionHandler { _, throwable ->
    Timber.e(throwable, "Background task failed safely")
}
val customScope = CoroutineScope(SupervisorJob() + Dispatchers.Default + exceptionHandler)

fun fetchDashboardData() = customScope.launch {
    // Failure in userDetails does NOT cancel analytics tracking
    val userDetails = async { api.fetchUser() }
    val analytics = launch { api.trackLaunch() }
}""",
                "metric": "Decreased screen-level crash propagation by 92% by isolating independent widget failures."
            },
            {
                "id": "q7",
                "title": "7. How do you design a Multi-Module Clean Architecture for 20+ feature teams?",
                "problem": "Monolithic app modules create 20+ minute build times, circular dependency deadlocks, and merge contention across large teams.",
                "solution": [
                    ("API IMPL SEPARATION", "I split features into lightweight interface api modules and concrete implementation modules."),
                    ("FEATURE INDEPENDENCE", "Feature modules never depend on peer features directly, eliminating circular dependency chains."),
                    ("CORE FOUNDATION MODULES", "I centralize shared network, design system, and database abstractions in core modules."),
                    ("GRADLE BUILD CACHE", "Granular modularization enables parallel Gradle task execution and remote build caching."),
                    ("DYNAMIC FEATURE DELIVERY", "I isolate large standalone features into on-demand dynamic feature modules cleanly.")
                ],
                "code": """// Multi-Module Architecture Dependency Graph
// :feature:checkout:impl -> :feature:checkout:api
// :feature:checkout:impl -> :core:designsystem
// :feature:checkout:impl -> :core:network
// :app -> :feature:checkout:impl""",
                "metric": "Cut clean build times from 18 minutes to 3.5 minutes and saved 45 engineering hours weekly."
            },
            {
                "id": "q8",
                "title": "8. How do you guarantee 99.85% Crash-Free Users in high-volume enterprise apps?",
                "problem": "Unhandled runtime exceptions, memory spikes, and null safety mismatches erode app store ratings and user trust.",
                "solution": [
                    ("GLOBAL CRASH INTERCEPTOR", "I establish UncaughtExceptionHandler wrappers to capture and persist diagnostic crash forensics."),
                    ("R8 PROGUARD VERIFICATION", "I enforce strict ProGuard validation rules in CI to prevent runtime reflection crashes."),
                    ("STRICT COROUTINE SCOPING", "I bind all asynchronous tasks to lifecycle-aware scopes, preventing leaks completely."),
                    ("STAGE ROLLOUT PHASING", "I deploy releases via Google Play 1%-5%-20%-100% phased rollout ladders."),
                    ("REALTIME SENTRY ALERTS", "I integrate automated Sentry alerts to halt rollouts if crash rates exceed 0.15%.")
                ],
                "code": """// Production Crash Guard and Strict Scoping
class GlobalCrashHandler(private val defaultHandler: Thread.UncaughtExceptionHandler?) : Thread.UncaughtExceptionHandler {
    override fun uncaughtException(thread: Thread, throwable: Throwable) {
        CrashReporter.logForensics(thread, throwable)
        defaultHandler?.uncaughtException(thread, throwable)
    }
}""",
                "metric": "Consistently delivered 99.91% crash-free session rates across 12 consecutive production releases."
            },
            {
                "id": "q9",
                "title": "9. How do you transition a native Android codebase to Kotlin Multiplatform (KMP)?",
                "problem": "Code duplication between iOS and Android doubles development costs and introduces business logic discrepancies.",
                "solution": [
                    ("DOMAIN LAYER FIRST", "I isolate pure Kotlin data models and validation logic into shared commonMain source sets."),
                    ("EXPECT ACTUAL PATTERN", "I use expect actual declarations for platform-specific capabilities like KeyStore and Bluetooth."),
                    ("KTOR AND SQLDELIGHT", "I standardize networking on Ktor client and persistence on cross-platform SQLDelight engine."),
                    ("SHARED VIEWMODELS", "I share ViewModel business logic while keeping native Jetpack Compose and SwiftUI UI layers."),
                    ("COCOAPODS XCFRAMEWORK", "I package shared multiplatform code into binary XCFrameworks for frictionless iOS integration.")
                ],
                "code": """// Shared Domain Logic in KMP commonMain
expect class PlatformCrypto() {
    fun encrypt(data: ByteArray): ByteArray
}

// commonMain Shared Repository
class SharedCatalogRepository(private val api: KtorClient, private val db: AppDatabase) {
    fun getProductsStream(): Flow<List<Product>> = db.productQueries.selectAll().asFlow()
}""",
                "metric": "Reduced cross-platform business logic redundancy by 65% with zero performance penalty on native UI."
            },
            {
                "id": "q10",
                "title": "10. How do you manage Memory Leaks and ANRs in background coroutine pipelines?",
                "problem": "Long-running coroutines holding Activity references or blocking Main thread cause severe ANRs and OutOfMemoryErrors.",
                "solution": [
                    ("LIFECYCLE AWARE COLLECTION", "I collect UI flows using repeatOnLifecycle(Lifecycle.State.STARTED) inside Views."),
                    ("LEAKCANARY AUTOMATION", "I integrate LeakCanary in debug builds to flag retaining memory graph leaks instantly."),
                    ("NON CANCELLABLE CLEANUP", "I wrap critical file closing operations inside withContext(NonCancellable) blocks safely."),
                    ("MAIN THREAD PROFILING", "I ban heavy computation and synchronous disk I/O from Main thread completely."),
                    ("WEAK REFERENCE ISOLATION", "I decouple long-lived background workers from UI listeners using WeakReferences.")
                ],
                "code": """// Safe Lifecycle-Aware Flow Collection in Jetpack Compose & Fragment
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { state ->
            renderUi(state)
        }
    }
}""",
                "metric": "Reduced Google Play Vitals ANR rate from 0.42% down to 0.04%, well below the bad threshold."
            },
            {
                "id": "q11",
                "title": "11. How do you implement a resilient Circuit Breaker pattern for mobile network calls?",
                "problem": "Repetitive failing network requests during server outages drain mobile battery, consume user data, and freeze UI.",
                "solution": [
                    ("THREE CIRCUIT STATES", "I implement Closed, Open, and Half-Open states to control network request flow."),
                    ("FAILURE THRESHOLD", "I trip circuit into Open state after five consecutive network connection timeouts."),
                    ("EXPONENTIAL BACKOFF SLEEP", "Open state blocks outgoing calls for thirty seconds, returning cached fallback data."),
                    ("PROBE TRIAL REQUEST", "Half-Open state sends a single trial request to verify backend service recovery."),
                    ("AUTOMATIC RECOVERY", "Successful trial resets circuit to Closed state, restoring normal network traffic seamlessly.")
                ],
                "code": """// Thread-Safe Mobile Circuit Breaker
class CircuitBreaker(private val failureThreshold: Int = 5, private val resetTimeoutMs: Long = 30_000L) {
    private var failureCount = AtomicInteger(0)
    private var lastFailureTime = AtomicLong(0L)
    private var state = AtomicReference(State.CLOSED)

    enum class State { CLOSED, OPEN, HALF_OPEN }

    suspend fun <T> execute(fallback: suspend () -> T, block: suspend () -> T): T {
        val now = System.currentTimeMillis()
        if (state.get() == State.OPEN && now - lastFailureTime.get() > resetTimeoutMs) {
            state.set(State.HALF_OPEN)
        }
        if (state.get() == State.OPEN) return fallback()
        return try {
            val result = block()
            if (state.get() == State.HALF_OPEN) state.set(State.CLOSED)
            result
        } catch (e: Exception) {
            lastFailureTime.set(now)
            if (failureCount.incrementAndGet() >= failureThreshold) state.set(State.OPEN)
            fallback()
        }
    }
}""",
                "metric": "Protected 5M+ mobile clients from cascading network timeouts during major cloud outage."
            },
            {
                "id": "q12",
                "title": "12. How do you implement Dependency Inversion with Hilt for dynamic testability?",
                "problem": "Direct class instantiations couple business logic to platform frameworks, making fast unit tests impossible.",
                "solution": [
                    ("INTERFACE BINDINGS", "I bind concrete implementations to domain interfaces using Hilt @Binds annotations."),
                    ("SCOPED SINGLETONS", "I annotate expensive shared dependencies with @Singleton to control memory footprint."),
                    ("CUSTOM ENTRY POINTS", "I utilize @EntryPoint accessors for non-Android classes and dynamic feature modules."),
                    ("TEST REPLACEMENT MODULES", "I replace production network modules with FakeNetworkModule in instrumentation suites."),
                    ("COMPILE TIME SAFETY", "Hilt validates full dependency graph correctness during Gradle compilation phase automatically.")
                ],
                "code": """// Clean Hilt Interface Binding Architecture
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    @Singleton
    abstract fun bindOrderRepository(impl: OrderRepositoryImpl): OrderRepository
}""",
                "metric": "Achieved 88% unit test code coverage across domain models with sub-millisecond test execution."
            }
        ]
    }
]

with open('/Users/prajapatichintankumar/.gemini/antigravity/scratch/android-interview-portal/modules_1.json', 'w') as f:
    json.dump(modules_data, f, indent=2)
print("Module 1 written successfully.")
