# Module 10 Part 2: Topics 26 to 50 (Android Framework & Architecture Deep Dive)

topics_26_to_50 = [
    {
        "id": "t26",
        "number": 26,
        "category": "Android Lifecycle",
        "title": "Android Activity & Fragment Lifecycle Transitions & SavedStateHandle",
        "why": "System configuration changes (screen rotations) and background process death destroy Activities, causing crashes and lost user input if state isn't preserved.",
        "how": "Configuration changes destroy and recreate the Activity, but preserve the ViewModel instance via `NonConfigurationInstances`. Process death kills the entire Linux process; when recreated, the OS restores data saved in `onSaveInstanceState(Bundle)` or `SavedStateHandle`. `SavedStateHandle` integrates directly with ViewModel constructors and uses `Parcelable` / `Bundle` key-value pairs.",
        "code": """@HiltViewModel
class SearchViewModel @Inject constructor(
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {
    // Survives both configuration changes AND process death!
    val queryState: StateFlow<String> = savedStateHandle.getStateFlow("SEARCH_QUERY", "")

    fun onQueryChange(newQuery: String) {
        savedStateHandle["SEARCH_QUERY"] = newQuery
    }
}""",
        "takeaway": "Store transient user input in `SavedStateHandle` so users don't lose search queries or form progress after OS process termination."
    },
    {
        "id": "t27",
        "number": 27,
        "category": "Android Architecture",
        "title": "ViewBinding vs DataBinding vs Jetpack Compose",
        "why": "Modern Android UI development has evolved from error-prone `findViewById` to type-safe ViewBinding and declarative Jetpack Compose.",
        "how": "`ViewBinding` generates binding classes for XML layouts at compile time, guaranteeing null safety and type safety with zero reflection or annotation processing overhead. `DataBinding` adds two-way binding and expression logic inside XML via kapt, which increases build times. `Jetpack Compose` completely eliminates XML, constructing UI trees as declarative Kotlin composable functions powered by a compiler plugin.",
        "code": """// ViewBinding in Fragment (Null-safe & Zero annotation overhead)
class ProfileFragment : Fragment(R.layout.fragment_profile) {
    private var _binding: FragmentProfileBinding? = null
    private val binding get() = _binding!!

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentProfileBinding.bind(view)
        binding.userNameText.text = "Staff Architect"
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null // Prevent memory leak when view hierarchy is destroyed
    }
}""",
        "takeaway": "Always null out ViewBinding references in Fragment `onDestroyView()` to prevent leaking the entire View hierarchy in memory."
    },
    {
        "id": "t28",
        "number": 28,
        "category": "Android OS Internals",
        "title": "Android Process Lifecycle, Low Memory Killer (LMK) & oom_adj Scores",
        "why": "The Android kernel terminates background processes to reclaim RAM for foreground apps; understanding LMK prevents sudden app termination surprises.",
        "how": "The Android Low Memory Killer daemon (`lmkd`) monitors available RAM. Every process is assigned an `oom_score_adj` (out-of-memory score from -1000 to 1000). Foreground apps (visible Activity / Foreground Service) have score 0 (highest priority). Visible activities have score 100. Cached background processes have scores 900-1000 and are the first to be killed when RAM drops below kernel watermarks.",
        "code": """// Inspecting process death behavior via ADB:
// 1. Send app to background (Home button)
// 2. Simulate OS killing the background process:
// adb shell am kill com.lenskart.app

// 3. Re-open app to test SavedStateHandle restoration:
// adb shell am start -n com.lenskart.app/.MainActivity""",
        "takeaway": "Never rely on in-memory singleton variables for long-term state; background processes can be killed at any moment by LMK."
    },
    {
        "id": "t29",
        "number": 29,
        "category": "Android Architecture",
        "title": "ViewModel Architecture & ViewModelStoreOwner Internals",
        "why": "Decouples screen UI controllers from business logic and retains state across configuration changes without leaking Activity references.",
        "how": "Activities implement `ViewModelStoreOwner`. During configuration change, `ComponentActivity.retainNonConfigurationInstances()` saves the `ViewModelStore` (a `HashMap<String, ViewModel>`). The new Activity instance retrieves the preserved `ViewModelStore` and re-attaches existing ViewModel instances. When the Activity finishes permanently (`isFinishing == true`), `ViewModelStore.clear()` is called, which triggers `ViewModel.onCleared()` for cleanup.",
        "code": """class CartViewModel : ViewModel() {
    init {
        Timber.d("ViewModel initialized")
    }

    override fun onCleared() {
        super.onCleared()
        // Called only when Activity finishes permanently, NOT on screen rotation
        Timber.d("Clean up open sockets and resources")
    }
}""",
        "takeaway": "Never pass Activity Context, View, or Fragment references into ViewModels to prevent massive memory leaks."
    },
    {
        "id": "t30",
        "number": 30,
        "category": "Android Lifecycle",
        "title": "Lifecycle-Aware Flow Collection (repeatOnLifecycle vs flowWithLifecycle)",
        "why": "Collecting Flows in standard `lifecycleScope.launch` keeps coroutines active in the background, consuming CPU, battery, and location/camera resources when the app is invisible.",
        "how": "`repeatOnLifecycle(Lifecycle.State.STARTED)` suspends the caller and launches a block when the lifecycle enters `STARTED`. If the Activity/Fragment goes to `STOPPED` (background), `repeatOnLifecycle` automatically cancels the inner coroutine, stopping flow collection. When the app returns to `STARTED`, it restarts collection automatically.",
        "code": """// Best practice flow collection in Fragment or Activity
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        // Coroutine cancels when screen is in background, restarts on resume!
        viewModel.locationFlow.collect { location ->
            updateMapPin(location)
        }
    }
}""",
        "takeaway": "Always collect UI flows inside `repeatOnLifecycle(Lifecycle.State.STARTED)` to stop background battery drain when the app is minimized."
    },
    {
        "id": "t31",
        "number": 31,
        "category": "Android OS Internals",
        "title": "Android Main Thread Looper, MessageQueue & Handler Architecture",
        "why": "Android's single-threaded UI model relies entirely on message passing; understanding this prevents thread synchronization bugs and UI freezes.",
        "how": "The Main thread runs an infinite loop via `Looper.loop()`. The `MessageQueue` holds work messages and `Runnable` tasks ordered by dispatch timestamp. `Handler` enqueues messages into the queue (`sendMessage()`, `post()`) and processes them when dispatched by the Looper. Android Choreographer schedules UI layout and draw frames as VSYNC messages every 16.6ms (60Hz) or 8.3ms (120Hz).",
        "code": """// Background thread posting UI update back to Main Looper
val mainHandler = Handler(Looper.getMainLooper())

Thread {
    val result = heavyComputation()
    mainHandler.post {
        // Executes on Main thread MessageQueue
        textView.text = result
    }
}.start()""",
        "takeaway": "Blocking the Main Looper with tasks exceeding 16ms drops frames; blocking it for 5 seconds triggers an Android ANR dialog."
    },
    {
        "id": "t32",
        "number": 32,
        "category": "Android Performance",
        "title": "ANRs (Application Not Responding): Thread Dump Analysis & Prevention",
        "why": "ANRs severely impact Google Play store rankings and occur when the Main thread is blocked for more than 5 seconds (Input/Broadcast) or 20 seconds (Service).",
        "how": "When an ANR occurs, the OS writes a thread dump trace to `/data/anr/traces.txt`. Common causes include: synchronous disk I/O (SharedPreferences `commit()`), Lock contention (Main thread waiting for a lock held by a background worker), and synchronous IPC binder calls. StrictMode helps identify accidental disk and network operations on the Main thread during development.",
        "code": """// Configure StrictMode in Application debug class to detect Main thread disk I/O
if (BuildConfig.DEBUG) {
    StrictMode.setThreadPolicy(
        StrictMode.ThreadPolicy.Builder()
            .detectDiskReads()
            .detectDiskWrites()
            .detectNetwork()
            .penaltyLog()
            .penaltyDeath() // Crash early in debug to fix before production
            .build()
    )
}""",
        "takeaway": "Replace synchronous SharedPreferences `apply()` / `commit()` with Jetpack DataStore and move all disk and IPC calls to `Dispatchers.IO`."
    },
    {
        "id": "t33",
        "number": 33,
        "category": "Android Performance",
        "title": "Android Memory Leaks: References (Strong, Weak, Soft) & LeakCanary",
        "why": "Retaining destroyed Activity/Fragment instances in memory causes OutOfMemoryErrors (OOM) and sluggish performance.",
        "how": "`StrongReference` prevents garbage collection. `WeakReference` allows GC to collect the referenced object immediately during the next GC cycle if no strong references exist. `SoftReference` is collected only when memory is low. `LeakCanary` hooks into `ActivityLifecycleCallbacks` and `FragmentLifecycleCallbacks`, watching destroyed instances via weak references and triggering a heap dump analysis if they aren't collected within 5 seconds.",
        "code": """class LocationHelper(context: Context) {
    // Use WeakReference to prevent leaking Activity context if listener outlives Activity
    private val contextRef: WeakReference<Context> = WeakReference(context)

    fun performAction() {
        val ctx = contextRef.get() ?: return // Already garbage collected safely
        Toast.makeText(ctx, "Action performed", Toast.LENGTH_SHORT).show()
    }
}""",
        "takeaway": "Integrate LeakCanary in debug builds and pass `ApplicationContext` (not Activity context) to long-lived singleton helper classes."
    },
    {
        "id": "t34",
        "number": 34,
        "category": "Android OS Internals",
        "title": "ART Garbage Collection: Generational GC, Concurrent Marking & Compaction",
        "why": "Excessive memory allocation in rendering loops triggers frequent GC pauses, causing visible frame drops and UI stutter (jank).",
        "how": "Android Runtime (ART) uses Generational Garbage Collection: Young Generation (Ephemeral objects collected quickly) and Old Generation (Long-lived objects). ART uses Concurrent Mark-Sweep (CMS) and Compacting GC to defragment heap space. While modern ART reduces stop-the-world pauses to under 3ms, allocating thousands of temporary objects per frame (e.g. inside `onDraw` or Camera frame analyzers) still exhausts GC throughput.",
        "code": """// BAD: Allocating new objects inside frequent frame callback
fun onFrame(canvas: Canvas) {
    val paint = Paint() // Allocates on every frame -> High GC churn!
    canvas.drawRect(0f, 0f, 100f, 100f, paint)
}

// GOOD: Reuse pre-allocated object instances
private val reusablePaint = Paint()
fun onFrameOptimized(canvas: Canvas) {
    canvas.drawRect(0f, 0f, 100f, 100f, reusablePaint)
}""",
        "takeaway": "Never allocate objects inside `onDraw()`, Camera frame analyzers, or high-frequency touch gesture listeners."
    },
    {
        "id": "t35",
        "number": 35,
        "category": "Jetpack Compose",
        "title": "Compose: Recomposition Lifecycle, Slots API & Composer Runtime",
        "why": "Understanding how Compose updates UI without regenerating full view hierarchies is critical for building 120 FPS high-performance interfaces.",
        "how": "Compose represents the UI tree as a gap-buffer array managed by the `Composer`. When observable `State<T>` read within a composable changes, Compose schedules recomposition. The runtime skips any composable whose input parameters are stable and have not changed (`equals() == true`), executing only the specific lambdas and sub-composables affected by the state mutation.",
        "code": """@Composable
fun OrderCard(orderId: String, total: Double, onPayClick: (String) -> Unit) {
    // Recomposes ONLY when total or orderId values change
    Card(modifier = Modifier.fillMaxWidth().padding(8.dp)) {
        Row(horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Order #$orderId")
            Text("$$total")
            Button(onClick = { onPayClick(orderId) }) {
                Text("Pay")
            }
        }
    }
}""",
        "takeaway": "Keep composable functions pure and pass immutable, stable parameters so the Compose runtime can skip recompositions."
    },
    {
        "id": "t36",
        "number": 36,
        "category": "Jetpack Compose",
        "title": "Compose State Snapshot System & Snapshot Mutation Tracking",
        "why": "Compose's reactivity is powered by its Snapshot state system, enabling isolated state changes and atomic multi-threaded updates.",
        "how": "`mutableStateOf()` creates a `SnapshotMutableState`. When read inside a composable, the Snapshot system automatically records the current `RecomposeScope` as a subscriber. When written to, `Snapshot.sendApplyNotifications()` notifies all subscribed scopes that a state change occurred, triggering scheduled recomposition on the Choreographer frame pulse.",
        "code": """// Creating snapshot state
var count by remember { mutableStateOf(0) }

// Atomic snapshot transactions
Snapshot.withMutableSnapshot {
    // All state changes inside this block apply atomically to UI
    user.name = "Alice"
    user.age = 29
}""",
        "takeaway": "State reads should happen as low in the composable tree as possible to minimize the scope of recompositions."
    },
    {
        "id": "t37",
        "number": 37,
        "category": "Jetpack Compose",
        "title": "@Stable and @Immutable Contracts in Compose Compiler",
        "why": "Unstable types (like standard Kotlin `List<T>` or multi-module classes) force composables to always recompose even when inputs are unchanged.",
        "how": "The Compose Compiler categorizes types into Stable and Unstable. `@Immutable` promises that all public properties are `val` and will never change after creation. `@Stable` promises that if public properties change, Compose will be notified (e.g. via `MutableState`), and `equals()` is reliable. Unstable types break the skippable contract, causing parent recompositions to cascade through all children.",
        "code": """// Mark external or multi-module models as @Immutable
@Immutable
data class ProductUiModel(
    val id: String,
    val title: String,
    val price: Double,
    // Use PersistentList instead of standard List for full stability
    val tags: PersistentList<String> = persistentListOf()
)""",
        "takeaway": "Always annotate UI state data classes with `@Immutable` and use `PersistentList` to guarantee skippable composable performance."
    },
    {
        "id": "t38",
        "number": 38,
        "category": "Jetpack Compose",
        "title": "remember vs rememberSaveable with Custom Savers",
        "why": "`remember` only survives recompositions, but loses state on screen rotation or process death. `rememberSaveable` preserves state across both.",
        "how": "`rememberSaveable` writes state into the Android `SavedStateRegistry` bundle. Primitives and `@Parcelize` types are saved automatically. For custom non-parcelable domain models, a custom `Saver` (`mapSaver` or `listSaver`) defines how to serialize the object into a Bundle map and restore it upon activity recreation.",
        "code": """data class PriceFilter(val min: Double, val max: Double)

val PriceFilterSaver = mapSaver(
    save = { mapOf("min" to it.min, "max" to it.max) },
    restore = { PriceFilter(it["min"] as Double, it["max"] as Double) }
)

@Composable
fun FilterScreen() {
    // Survives screen rotation and background process termination!
    var filter by rememberSaveable(stateSaver = PriceFilterSaver) {
        mutableStateOf(PriceFilter(0.0, 500.0))
    }
}""",
        "takeaway": "Use `rememberSaveable` for critical user form fields, expanded card states, and scroll positions that must survive process death."
    },
    {
        "id": "t39",
        "number": 39,
        "category": "Jetpack Compose",
        "title": "SideEffect, LaunchedEffect, and DisposableEffect Execution Phases",
        "why": "Triggering non-UI operations (analytics, network calls, hardware listeners) inside a composable body causes repeat bugs on every recomposition.",
        "how": "`LaunchedEffect(key)` launches a coroutine tied to the composable lifecycle; if `key` changes, the old coroutine is cancelled and a new one launches. `DisposableEffect(key)` is for listeners that require cleanup via `onDispose { }`. `SideEffect` runs on EVERY successful recomposition commit to synchronize Compose state with non-Compose external objects.",
        "code": """// 1. One-time or key-driven async side-effect
LaunchedEffect(userId) {
    viewModel.fetchUserData(userId)
}

// 2. Lifecycle listener with mandatory cleanup
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, event -> /* handle */ }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose {
        lifecycleOwner.lifecycle.removeObserver(observer)
    }
}""",
        "takeaway": "Never launch naked coroutines or register listeners directly in the composable body; always use the appropriate Effect handler."
    },
    {
        "id": "t40",
        "number": 40,
        "category": "Jetpack Compose",
        "title": "Custom Compose Modifiers (Modifier.Node API)",
        "why": "Creating custom layout, drawing, and pointer interaction modifiers using the new `Modifier.Node` API provides 2-3x better performance than legacy `composed { }`.",
        "how": "Legacy `Modifier.composed { }` re-executes composition logic on every recomposition, generating significant heap allocations. The modern `Modifier.Node` API allocates a lightweight node object once and reuses it across layout, draw, and pointer input passes via interfaces like `DrawModifierNode`, `LayoutModifierNode`, and `PointerInputModifierNode`.",
        "code": """// Custom Modifier using modern Modifier.Node API
class PulsingCircleNode(var color: Color) : Modifier.Node(), DrawModifierNode {
    override fun ContentDrawScope.draw() {
        drawCircle(color = color, radius = size.minDimension / 2)
        drawContent() // Draws underlying composable content
    }
}

data class PulsingCircleElement(val color: Color) : ModifierNodeElement<PulsingCircleNode>() {
    override fun create() = PulsingCircleNode(color)
    override fun update(node: PulsingCircleNode) { node.color = color }
}

fun Modifier.pulsingCircle(color: Color) = this.then(PulsingCircleElement(color))""",
        "takeaway": "Always build custom Compose modifiers with the `Modifier.Node` API to eliminate composition overhead and memory churn."
    },
    {
        "id": "t41",
        "number": 41,
        "category": "Android Architecture",
        "title": "Dependency Injection: Hilt Scopes, Components & @EntryPoint",
        "why": "Provides compile-time validated dependency injection, avoiding memory leaks and making large multi-module codebases easily testable.",
        "how": "Hilt defines standard hierarchical components tied to Android lifecycles: `SingletonComponent` (Application), `ActivityRetainedComponent` (ViewModel), `ActivityComponent`, and `FragmentComponent`. Scoped dependencies are retained as long as their matching component is alive. `@EntryPoint` provides an access point to inject dependencies into classes Hilt doesn't natively support (like ContentProviders, BroadcastReceivers, or dynamic feature modules).",
        "code": """@EntryPoint
@InstallIn(SingletonComponent::class)
interface AnalyticsEntryPoint {
    fun getAnalyticsTracker(): AnalyticsTracker
}

// Accessing Hilt dependencies inside a non-standard Android class:
class CustomBroadcastReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val entryPoint = EntryPointAccessors.fromApplication(
            context.applicationContext, AnalyticsEntryPoint::class.java
        )
        entryPoint.getAnalyticsTracker().trackEvent("RECEIVER_TRIGGERED")
    }
}""",
        "takeaway": "Use `@EntryPoint` to access Hilt-managed dependencies in custom Views, BroadcastReceivers, and dynamic feature modules."
    },
    {
        "id": "t42",
        "number": 42,
        "category": "Data Persistence",
        "title": "Room ORM Architecture: SQLite WAL, DAOs & InvalidationTracker",
        "why": "Provides type-safe SQLite abstraction with compile-time query verification and automatic reactive flow emissions on table changes.",
        "how": "Room verifies SQL queries at compile time using annotation processing. When returning a `Flow<List<T>>` from a DAO query, Room registers an `InvalidationTracker.Observer` on the target tables. When any insert/update/delete query touches those tables, SQLite triggers notify the InvalidationTracker, which automatically triggers a re-query and emits the fresh list to active Flow collectors.",
        "code": """@Dao
interface OrderDao {
    // Automatically re-emits fresh list whenever 'orders' table is modified!
    @Query("SELECT * FROM orders ORDER BY timestamp DESC")
    fun getOrdersFlow(): Flow<List<OrderEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrder(order: OrderEntity)
}""",
        "takeaway": "Enable Write-Ahead Logging (`setJournalMode(JournalMode.WRITE_AHEAD_LOGGING)`) in Room to allow concurrent readers without blocking writers."
    },
    {
        "id": "t43",
        "number": 43,
        "category": "Background Work",
        "title": "WorkManager: Constraints, Battery Optimization & Backoff Policies",
        "why": "Guarantees execution of deferrable, persistent background jobs even if the app closes or the device reboots.",
        "how": "WorkManager chooses the optimal OS scheduler (JobScheduler on API 23+, AlarmManager/BroadcastReceiver on older devices). Work requests can specify hardware `Constraints` (Charging, Unmetered Wi-Fi, Storage Not Low). If a worker returns `Result.retry()`, WorkManager reschedules it using an Exponential or Linear backoff policy to prevent server flooding.",
        "code": """val syncConstraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.UNMETERED) // Wi-Fi only
    .setRequiresCharging(true)                    // Charging only
    .setRequiresBatteryNotLow(true)
    .build()

val syncWorkRequest = OneTimeWorkRequestBuilder<TelemetrySyncWorker>()
    .setConstraints(syncConstraints)
    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 10, TimeUnit.SECONDS)
    .build()

WorkManager.getInstance(context).enqueueUniqueWork(
    "TELEMETRY_SYNC", ExistingWorkPolicy.KEEP, syncWorkRequest
)""",
        "takeaway": "Use `OneTimeWorkRequestBuilder` with strict constraints for heavy uploads to guarantee zero battery drain when the device is in use."
    },
    {
        "id": "t44",
        "number": 44,
        "category": "Android Security",
        "title": "Android 14 Foreground Service Types & Permission Hardening",
        "why": "Google Play enforces strict Foreground Service policies on Android 14 (API 34), crashing apps that lack explicit types or valid permissions.",
        "how": "Android 14 requires declaring `android:foregroundServiceType` in the manifest (e.g. `location`, `connectedDevice`, `mediaPlayback`, `dataSync`). Apps must request the matching permission (e.g. `FOREGROUND_SERVICE_LOCATION`). Calling `startForeground()` requires passing the matching type flag bitmask; passing an undeclared type throws a `SecurityException`.",
        "code": """<!-- AndroidManifest.xml -->
<service
    android:name=".TrackingService"
    android:foregroundServiceType="location"
    android:exported="false" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" />

// In Service onStartCommand:
ServiceCompat.startForeground(
    this, NOTIFICATION_ID, notification,
    ServiceInfo.FOREGROUND_SERVICE_TYPE_LOCATION
)""",
        "takeaway": "Always declare exact Foreground Service types in your Manifest and pass the matching type bitmask in `startForeground()` for Android 14."
    },
    {
        "id": "t45",
        "number": 45,
        "category": "Android Security",
        "title": "BroadcastReceivers: Static vs Dynamic & Security (RECEIVER_NOT_EXPORTED)",
        "why": "Android 14 requires all dynamic BroadcastReceivers to declare export flags to prevent malicious external apps from injecting fake broadcast intents.",
        "how": "Static receivers are declared in `AndroidManifest.xml` (most implicit broadcasts are restricted since Android 8). Dynamic receivers are registered in code via `registerReceiver()`. On Android 14+, you MUST specify `Context.RECEIVER_NOT_EXPORTED` (internal to your app) or `Context.RECEIVER_EXPORTED` (can receive broadcasts from other apps). Failing to pass this flag throws a runtime `SecurityException`.",
        "code": """val receiver = object : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        // Handle internal broadcast event safely
    }
}

// Android 14 mandatory export security flag:
val flag = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
    ContextCompat.RECEIVER_NOT_EXPORTED
} else 0

ContextCompat.registerReceiver(context, receiver, IntentFilter("CUSTOM_ACTION"), flag)""",
        "takeaway": "Always register dynamic receivers with `RECEIVER_NOT_EXPORTED` unless they are explicitly designed to receive intents from external apps."
    },
    {
        "id": "t46",
        "number": 46,
        "category": "Android Security",
        "title": "Android KeyStore TEE, StrongBox & MasterKey AES-GCM Cryptography",
        "why": "Hardware-backed cryptography prevents extraction of encryption keys even if the Android device is rooted or memory-dumped.",
        "how": "Android KeyStore generates and stores cryptographic keys inside the device's Trusted Execution Environment (TEE) or Dedicated Hardware Security Module (StrongBox). Keys never enter the Linux kernel or JVM memory. The CPU sends data to the hardware crypto chip, which encrypts/decrypts the payload using AES-GCM (256-bit) and returns the authenticated ciphertext.",
        "code": """val keyGenSpec = KeyGenParameterSpec.Builder(
    "MasterPaymentKey",
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setKeySize(256)
    .setIsStrongBoxBacked(true) // StrongBox Hardware Chip
    .build()

val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
keyGenerator.init(keyGenSpec)
keyGenerator.generateKey()""",
        "takeaway": "Use `MasterKey.Builder(context).setKeyScheme(AES256_GCM)` from Jetpack Security to store sensitive auth tokens and database passphrases."
    },
    {
        "id": "t47",
        "number": 47,
        "category": "Android Security",
        "title": "Network Security Config, Cleartext Traffic & SSL Certificate Pinning",
        "why": "Protects API communications against Man-in-the-Middle (MITM) attacks and rogue enterprise proxies on untrusted Wi-Fi networks.",
        "how": "`network_security_config.xml` allows enforcing `cleartextTrafficPermitted=\"false\"` globally and pinning SHA-256 certificate public key hashes (SPKI). OkHttp's `CertificatePinner` verifies that the TLS handshake certificate chain contains at least one pinned public key hash. If the pin does not match, OkHttp terminates the socket connection before transmitting sensitive HTTP headers.",
        "code": """val certificatePinner = CertificatePinner.Builder()
    .add("api.lenskart.com", "sha256/k2oTTrsvErP43b1m4e97J8FDCm8gW59G=")
    .add("api.lenskart.com", "sha256/WoiWRyIOVNa9ihaBciRSC7XHjliYS9V=") // Backup pin
    .build()

val okHttpClient = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()""",
        "takeaway": "Always include at least one backup certificate pin in your `CertificatePinner` to prevent mobile outages during server certificate rotation."
    },
    {
        "id": "t48",
        "number": 48,
        "category": "Build & Optimization",
        "title": "R8 Compiler: Tree Shaking, Inlining, Class Merging & ProGuard Keep Rules",
        "why": "Shrinks app download size by 30-50%, eliminates dead code, inlines small functions, and obfuscates class names to deter reverse-engineering.",
        "how": "R8 combines desugaring, shrinking, optimization, and dexing into a single compiler pass. Tree shaking traces roots from entrypoints (`AndroidManifest.xml` classes, `@Keep` annotations) and deletes unreferenced methods/classes. ProGuard rules (`-keep`, `-keepclassmembers`) instruct R8 not to rename or strip classes referenced via runtime reflection (e.g. Gson/Moshi models).",
        "code": """# proguard-rules.pro
# Preserve data models used in reflection-based JSON deserialization
-keepclassmembers class com.app.models.** {
    <fields>;
}

# Remove all logging calls in release builds for speed and security
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
}""",
        "takeaway": "Enable `android.enableR8.fullMode=true` in `gradle.properties` for aggressive method inlining and maximum APK shrinkage."
    },
    {
        "id": "t49",
        "number": 49,
        "category": "Architecture & Delivery",
        "title": "Dynamic Feature Modules (Play Feature Delivery & SplitCompat)",
        "why": "Reduces initial app download size by packaging large standalone features (like AR Try-On or On-Device AI models) as on-demand downloadable modules.",
        "how": "Dynamic feature modules depend on the `:app` base module (inverted dependency). The base module installs the core app; when the user taps an on-demand feature, `SplitInstallManager` requests the module from Google Play. `SplitCompat.installActivity()` injects the downloaded feature's DEX files and resources into the active ClassLoader at runtime without restarting the app.",
        "code": """val splitInstallManager = SplitInstallManagerFactory.create(context)
val request = SplitInstallRequest.newBuilder()
    .addModule("feature_virtual_tryon")
    .build()

splitInstallManager.startInstall(request).addOnSuccessListener { sessionId ->
    Timber.d("Downloading module on demand: $sessionId")
}""",
        "takeaway": "Use Dynamic Feature Modules for heavy ML models and specialized AR features to keep your baseline initial APK download under 15MB."
    },
    {
        "id": "t50",
        "number": 50,
        "category": "Performance & Startup",
        "title": "Android App Startup Optimization & Baseline Profiles (ART AOT Compilation)",
        "why": "Slow cold app startup increases user churn; Baseline Profiles pre-compile critical user journeys into native machine code at installation.",
        "how": "By default, Android Runtime (ART) interprets DEX bytecode and uses Just-In-Time (JIT) compilation, creating startup jank during initial launches. `Baseline Profiles` are binary files bundled in the APK containing class and method indices from critical user journeys. During installation, ART uses Ahead-Of-Time (AOT) compilation to pre-compile those exact methods into native machine code, speeding up cold startup by 30-40%.",
        "code": """// Baseline Profile Generator Test in Android Studio
@RunWith(AndroidJUnit4::class)
class BaselineProfileGenerator {
    @get:Rule
    val rule = BaselineProfileRule()

    @Test
    fun generateBaselineProfile() = rule.collect(
        packageName = "com.lenskart.app"
    ) {
        pressHome()
        startActivityAndWait()
        // Scroll through feed to capture hot bytecode paths for AOT pre-compilation
        device.findObject(By.res("feed_list")).scroll(Direction.DOWN, 2f)
    }
}""",
        "takeaway": "Generate Baseline Profiles for your startup and primary checkout screens to achieve sub-500ms cold startup on mid-tier Android hardware."
    }
]

print(f"Loaded {len(topics_26_to_50)} topics for Part 2.")
