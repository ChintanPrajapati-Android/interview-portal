# Modules 1, 2, 3 - Exactly 6 bullets per question, strictly 5-7 words per bullet

m1 = {
    "id": "module-1",
    "title": "Module 1: Architecture, Flow & Scalable Search",
    "badge": "Emerald",
    "color": "emerald",
    "summary": "StateFlow, Debounce, flatMapLatest, MVI, Dispatchers, Channels, and 99.85% Crash-Free SLA.",
    "questions": [
        {
            "id": "q1",
            "title": "1. How do you architect a high-scale real-time search with Coroutines and StateFlow?",
            "problem": "Fast user typing triggers too many network calls, creating lag and race conditions.",
            "solution": [
                ("DEBOUNCE 300MS", "I apply debounce with 300 millisecond delay."),
                ("DISTINCT FILTER", "distinctUntilChanged drops identical consecutive text queries."),
                ("FLATMAPLATEST", "flatMapLatest cancels previous in-flight network searches."),
                ("DISPATCHERS.IO", "flowOn runs background queries on Dispatchers.IO."),
                ("CATCH OPERATOR", "catch operator intercepts all network exceptions safely."),
                ("STATEIN SHARING", "stateIn converts flow into observable StateFlow.")
            ],
            "code": """class SearchViewModel(private val repo: SearchRepo) : ViewModel() {
    private val _query = MutableStateFlow("")
    val searchResults = _query
        .debounce(300L)
        .distinctUntilChanged()
        .filter { it.trim().length >= 2 }
        .flatMapLatest { repo.searchStream(it) }
        .flowOn(Dispatchers.IO)
        .catch { emit(UiState.Error(it)) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), UiState.Idle)
}""",
            "metric": "Maintained 99.85% crash-free sessions across 10M+ users during flash sales."
        },
        {
            "id": "q2",
            "title": "2. Why choose MVI over standard MVVM for complex mission-critical screens?",
            "problem": "Multiple separate state variables cause screen sync bugs and race conditions.",
            "solution": [
                ("SINGLE STATE", "I bundle state into one immutable class."),
                ("INTENT STREAM", "User actions flow as explicit single intents."),
                ("REDUCER LOGIC", "Pure reducer functions calculate the next state."),
                ("SIDE EFFECTS", "Channels dispatch one-off navigation and snackbar events."),
                ("TIME TRAVEL", "Immutable states make unit tests deterministic."),
                ("PREDICTABLE UI", "This eliminates state bugs in complex checkouts.")
            ],
            "code": """data class CartUiState(
    val items: List<CartItem> = emptyList(),
    val total: Double = 0.0,
    val isLoading: Boolean = false
)

sealed interface CartIntent {
    data class AddItem(val id: String) : CartIntent
    object Checkout : CartIntent
}""",
            "metric": "Reduced cart and checkout state bugs by 78% in production."
        },
        {
            "id": "q3",
            "title": "3. StateFlow vs SharedFlow: How do you choose between them in production?",
            "problem": "Using StateFlow for toast messages causes repeated popups on screen rotation.",
            "solution": [
                ("STATEFLOW FOR STATE", "StateFlow stores current observable UI state values."),
                ("INITIAL VALUE", "StateFlow requires an initial default state value."),
                ("SHAREDFLOW EVENTS", "SharedFlow emits one-time transient UI events cleanly."),
                ("ZERO REPLAY", "SharedFlow with zero replay prevents repeated popups."),
                ("BUFFER OVERFLOW", "DROP_OLDEST drops unconsumed notifications during bursts."),
                ("LIFECYCLE SAFE", "Views collect events safely with repeatOnLifecycle.")
            ],
            "code": """class ProfileViewModel : ViewModel() {
    val uiState = MutableStateFlow(ProfileState.Loading).asStateFlow()

    private val _events = MutableSharedFlow<ProfileEvent>(
        replay = 0, extraBufferCapacity = 1, onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    val events = _events.asSharedFlow()
}""",
            "metric": "Eliminated duplicate navigation and snackbar triggers across all screens."
        },
        {
            "id": "q4",
            "title": "4. How do you govern Coroutine Dispatchers and avoid thread starvation at scale?",
            "problem": "Hardcoding Dispatchers locks unit testing and starves background thread pools.",
            "solution": [
                ("HILT INJECTION", "I inject all Dispatchers using Hilt modules."),
                ("LIMITED PARALLELISM", "I limit database writers to four threads."),
                ("DEFAULT FOR CPU", "Dispatchers.Default handles heavy JSON parsing tasks."),
                ("MAIN IMMEDIATE", "Dispatchers.Main.immediate updates UI without extra delay."),
                ("ZERO HARDCODING", "No class hardcodes direct Dispatcher references."),
                ("FAST UNIT TESTS", "StandardTestDispatcher makes all unit tests fast.")
            ],
            "code": """@Module
@InstallIn(SingletonComponent::class)
object DispatcherModule {
    @Provides @IoDispatcher
    fun provideIo(): CoroutineDispatcher = Dispatchers.IO

    @Provides @DbDispatcher
    fun provideDb(): CoroutineDispatcher = Dispatchers.IO.limitedParallelism(4)
}""",
            "metric": "Kept background thread pool utilization below 35% during heavy sync."
        },
        {
            "id": "q5",
            "title": "5. Channels vs SharedFlow: When is Channel strictly required?",
            "problem": "SharedFlow broadcasts to all collectors; if multiple workers listen, events duplicate.",
            "solution": [
                ("SINGLE RECEIVER", "Channel delivers every event to one consumer."),
                ("WORK QUEUE", "Multiple workers pull from one shared queue."),
                ("BUFFERED CAPACITY", "Channel buffers up to 64 rapid tasks."),
                ("RECEIVE AS FLOW", "receiveAsFlow exposes stream for structured coroutine collection."),
                ("CONSUME ONCE", "Guarantees payment actions process only once."),
                ("ZERO DUPLICATES", "Prevents duplicate analytical and payment dispatch.")
            ],
            "code": """class PaymentViewModel : ViewModel() {
    private val _eventChannel = Channel<PaymentEvent>(Channel.BUFFERED)
    val events = _eventChannel.receiveAsFlow()

    fun pay() = viewModelScope.launch {
        _eventChannel.send(PaymentEvent.OpenReceipt)
    }
}""",
            "metric": "Achieved zero duplicate orders and 100% reliable payment event delivery."
        },
        {
            "id": "q6",
            "title": "6. How do you implement Structured Concurrency with SupervisorJob?",
            "problem": "A crash in one child coroutine cancels the entire screen job.",
            "solution": [
                ("SUPERVISORJOB", "SupervisorJob isolates failures to each child coroutine."),
                ("ROOT SCOPE", "SupervisorJob attaches directly to custom CoroutineScope."),
                ("EXCEPTION HANDLER", "CoroutineExceptionHandler catches unhandled child errors safely."),
                ("INDEPENDENT JOBS", "Sibling tasks continue running without sudden cancellation."),
                ("STRUCTURED CANCEL", "Cancelling parent scope tears down all children."),
                ("ASYNC HANDLING", "runCatching wraps async await calls safely.")
            ],
            "code": """val handler = CoroutineExceptionHandler { _, ex ->
    Timber.e(ex, "Child task failed")
}
val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default + handler)

fun loadDashboard() = scope.launch {
    launch { fetchUserData() }
    launch { trackAppLaunch() }
}""",
            "metric": "Reduced screen-wide crash cascades by 92% across dashboard widgets."
        },
        {
            "id": "q7",
            "title": "7. How do you design a Multi-Module Clean Architecture for 20+ feature teams?",
            "problem": "Monolithic code causes 20-minute build times, circular dependencies, and merge conflicts.",
            "solution": [
                ("API SEPARATION", "I split features into api and implementation."),
                ("NO PEER COUPLING", "Feature modules never depend on each other."),
                ("CORE LIBRARIES", "Shared network and database live in core."),
                ("GRADLE CACHE", "Granular modules enable remote build caching."),
                ("PARALLEL BUILDS", "Gradle caches and builds modules in parallel."),
                ("DYNAMIC FEATURES", "Large standalone features isolate into dynamic modules.")
            ],
            "code": """// Multi-Module Architecture
// :feature:checkout:impl -> :feature:checkout:api
// :feature:checkout:impl -> :core:network
// :app -> :feature:checkout:impl""",
            "metric": "Cut clean build times from 18 minutes to 3.5 minutes."
        },
        {
            "id": "q8",
            "title": "8. How do you guarantee 99.85% Crash-Free Users in high-volume enterprise apps?",
            "problem": "Unhandled exceptions and memory spikes drop app ratings and hurt revenue.",
            "solution": [
                ("GLOBAL HANDLER", "UncaughtExceptionHandler catches and logs fatal crashes."),
                ("LIFECYCLE SCOPES", "Coroutines bind strictly to view lifecycle owners."),
                ("R8 PROGUARD", "Strict ProGuard rules prevent reflection runtime bugs."),
                ("STAGED ROLLOUT", "Google Play rolls out releases in stages."),
                ("REALTIME SENTRY", "Automated Sentry alerts monitor live crash rates."),
                ("QUICK ROLLBACK", "Halts rollouts if crash rates exceed threshold.")
            ],
            "code": """class CrashHandler(private val default: Thread.UncaughtExceptionHandler?) : Thread.UncaughtExceptionHandler {
    override fun uncaughtException(t: Thread, e: Throwable) {
        CrashReporter.log(e)
        default?.uncaughtException(t, e)
    }
}""",
            "metric": "Delivered 99.91% crash-free session rate across 12 consecutive app releases."
        },
        {
            "id": "q9",
            "title": "9. How do you transition a native Android codebase to Kotlin Multiplatform (KMP)?",
            "problem": "Writing separate business logic for iOS and Android doubles development costs.",
            "solution": [
                ("COMMON LOGIC", "I move data models into shared commonMain."),
                ("EXPECT ACTUAL", "expect actual bridges platform APIs like KeyStore."),
                ("KTOR CLIENT", "Ktor client handles cross-platform network calls."),
                ("SQLDELIGHT DB", "SQLDelight provides type-safe multiplatform database queries."),
                ("SHARED VIEWMODELS", "ViewModels share state while keeping native UI."),
                ("NATIVE UI", "Compose and SwiftUI render native UI layers.")
            ],
            "code": """// commonMain
expect class CryptoEngine() {
    fun encrypt(data: ByteArray): ByteArray
}

class ProductRepository(private val api: KtorClient) {
    fun getProducts(): Flow<List<Product>> = api.fetch()
}""",
            "metric": "Shared 65% of code between platforms with zero native UI performance loss."
        },
        {
            "id": "q10",
            "title": "10. How do you manage Memory Leaks and ANRs in background coroutine pipelines?",
            "problem": "Coroutines holding Activity context or blocking the main thread trigger ANRs.",
            "solution": [
                ("REPEATONLIFECYCLE", "Views collect flows using repeatOnLifecycle State.STARTED."),
                ("OFF MAIN THREAD", "All disk writes run on Dispatchers.IO."),
                ("LEAKCANARY", "LeakCanary detects retaining memory leaks in debug."),
                ("NONCANCELLABLE", "withContext NonCancellable finishes critical file closing."),
                ("WEAK REFERENCES", "WeakReferences decouple long background tasks from UI."),
                ("ZERO LEAKS", "Guarantees clean garbage collection on activity destruction.")
            ],
            "code": """viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}""",
            "metric": "Lowered Google Play ANR rate from 0.42% down to 0.04%."
        },
        {
            "id": "q11",
            "title": "11. How do you implement a resilient Circuit Breaker pattern for mobile network calls?",
            "problem": "Repeated network calls during server outages drain battery and freeze UI.",
            "solution": [
                ("THREE STATES", "Circuit uses Closed, Open, and Half-Open states."),
                ("TRIP ON ERRORS", "Five consecutive timeouts trip the circuit Open."),
                ("FAST CACHE", "Open state returns cached data for 30s."),
                ("PROBE REQUEST", "Half-Open state sends single test request."),
                ("AUTO RECOVERY", "One successful probe test closes the circuit."),
                ("SAVE BATTERY", "Stops wasting cellular radio power on errors.")
            ],
            "code": """class CircuitBreaker(private val maxFailures: Int = 5) {
    private var failures = 0
    private var state = State.CLOSED

    suspend fun <T> run(fallback: T, block: suspend () -> T): T {
        if (state == State.OPEN) return fallback
        return try {
            val res = block()
            state = State.CLOSED
            res
        } catch (e: Exception) {
            if (++failures >= maxFailures) state = State.OPEN
            fallback
        }
    }
}""",
            "metric": "Protected 5M+ mobile apps from timeouts during major cloud outage."
        },
        {
            "id": "q12",
            "title": "12. How do you implement Dependency Inversion with Hilt for dynamic testability?",
            "problem": "Direct class creation couples code to Android classes, blocking unit tests.",
            "solution": [
                ("HILT BINDS", "I bind concrete implementations to domain interfaces."),
                ("SINGLETON SCOPE", "Expensive dependencies are scoped with Singleton annotations."),
                ("CUSTOM ENTRYPOINTS", "EntryPoint accessors provide dependencies to dynamic modules."),
                ("TEST MODULES", "Test suites replace live APIs with fakes."),
                ("COMPILE SAFETY", "Hilt validates dependency graphs during project compilation."),
                ("FAST UNIT TESTS", "Achieves fast sub-millisecond unit test runs.")
            ],
            "code": """@Module
@InstallIn(SingletonComponent::class)
abstract class RepoModule {
    @Binds @Singleton
    abstract fun bindOrderRepo(impl: OrderRepoImpl): OrderRepo
}""",
            "metric": "Reached 88% unit test coverage with fast sub-millisecond execution times."
        }
    ]
}

m2 = {
    "id": "module-2",
    "title": "Module 2: CameraX, Real-Time Vision & On-Device ML",
    "badge": "Cyan",
    "color": "cyan",
    "summary": "STRATEGY_KEEP_ONLY_LATEST, TFLite INT8 Quantization, Face Mesh, 3D Filament, Zero-Copy Buffers, ImageProxy Leaks.",
    "questions": [
        {
            "id": "q13",
            "title": "1. How do you prevent ImageAnalysis backpressure drops and memory leaks in CameraX?",
            "problem": "Heavy frame processing in CameraX drops frames and causes OutOfMemory errors.",
            "solution": [
                ("KEEP LATEST", "I set backpressure to STRATEGY_KEEP_ONLY_LATEST."),
                ("SINGLE THREAD", "A dedicated background executor runs frame inference."),
                ("ZERO COPY PLANES", "Direct ByteBuffers extract planes without array copies."),
                ("CLOSE IMAGEPROXY", "I close imageProxy inside mandatory finally blocks."),
                ("ROTATION MATRIX", "Calculates sensor rotation degrees before model inference."),
                ("STEADY 60 FPS", "This keeps preview running at 60 FPS.")
            ],
            "code": """val analyzer = ImageAnalysis.Builder()
    .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
    .build()

analyzer.setAnalyzer(executor) { proxy ->
    try {
        processFrame(proxy)
    } finally {
        proxy.close() // Mandatory release
    }
}""",
            "metric": "Maintained steady 60 FPS camera preview with zero memory leaks."
        },
        {
            "id": "q14",
            "title": "2. How do you optimize On-Device ML Models with INT8 Post-Training Quantization?",
            "problem": "Float32 ML models take 100MB+, draining mobile battery and running slow.",
            "solution": [
                ("INT8 QUANTIZATION", "INT8 quantization shrinks model weights by 75%."),
                ("NNAPI DELEGATE", "I bind model inference to GPU delegates."),
                ("CALIBRATION DATA", "Representative datasets retain 99% baseline model accuracy."),
                ("DIRECT BUFFERS", "Reused direct ByteBuffers eliminate garbage collection churn."),
                ("XNNPACK FALLBACK", "XNNPACK CPU fallback runs if GPU fails."),
                ("HIGH SPEED", "Models run in 18ms on mobile.")
            ],
            "code": """val options = Interpreter.Options().apply {
    addDelegate(GpuDelegate())
    setNumThreads(4)
}
val tflite = Interpreter(loadModel("model_int8.tflite"), options)""",
            "metric": "Shrank model size from 84MB to 21MB and sped up latency to 18ms."
        },
        {
            "id": "q15",
            "title": "3. How do you integrate ML Kit Face Mesh with Filament 3D Engine for Virtual Try-On?",
            "problem": "Coordinate mismatch and jitter ruin 3D glasses try-on tracking.",
            "solution": [
                ("468 LANDMARKS", "ML Kit tracks 468 facial mesh landmarks."),
                ("KALMAN FILTER", "Kalman filters smooth out noisy sensor coordinates."),
                ("FILAMENT 3D", "Filament renders photorealistic 3D glasses models."),
                ("POSE MATRIX", "Maps facial landmarks to 3D rotation quaternions."),
                ("SURFACE SYNC", "Choreographer pulses synchronize preview with 3D rendering."),
                ("60 FPS AR", "Delivers smooth 60 FPS augmented reality.")
            ],
            "code": """detector.process(inputImage).addOnSuccessListener { meshes ->
    val face = meshes.firstOrNull() ?: return@addOnSuccessListener
    val rawNose = face.allPoints[6].position
    val smoothed = kalmanFilter.update(rawNose)
    filamentRenderer.updatePose(smoothed)
}""",
            "metric": "Delivered real-time 60 FPS virtual glasses try-on with sub-16ms latency."
        },
        {
            "id": "q16",
            "title": "4. How do you convert YUV_420_888 frames to RGB ByteBuffers with zero allocation?",
            "problem": "Converting camera frames in Java creates high GC pauses and drops frames.",
            "solution": [
                ("LIBYUV C++", "Native C++ libyuv converts color planes directly."),
                ("DIRECT POOLS", "I reuse pre-allocated direct ByteBuffers across frames."),
                ("HANDLE STRIDES", "NDK code accounts for row stride offsets."),
                ("NEON SIMD", "ARM NEON SIMD vectorizes color space math."),
                ("ZERO GC PAUSES", "Zero heap allocations eliminates garbage collection pauses."),
                ("SAVE FRAME TIME", "Recovers 4ms per frame on mobile devices.")
            ],
            "code": """external fun nativeYuvToRgb(
    y: ByteBuffer, u: ByteBuffer, v: ByteBuffer,
    yStride: Int, uvStride: Int, out: ByteBuffer
)""",
            "metric": "Recovered 4.2ms per frame, keeping camera feed completely smooth."
        },
        {
            "id": "q17",
            "title": "5. How do you architect dynamic Model Hot-Swapping without restarting the app?",
            "problem": "Shipping new ML models inside full APK updates slows down releases.",
            "solution": [
                ("FEATURE DELIVERY", "Play Feature Delivery downloads models on demand."),
                ("ATOMIC REFERENCE", "AtomicReference swaps Interpreter instances without locking threads."),
                ("SHA256 CHECKSUM", "Cryptographic hashes verify model integrity before swapping."),
                ("WARMUP RUN", "Dummy inference warms up model memory caches."),
                ("AUTO ROLLBACK", "Reverts to bundled model if errors happen."),
                ("ZERO DOWNTIME", "Users get updated models without app restarts.")
            ],
            "code": """class ModelManager {
    private val interpreterRef = AtomicReference<Interpreter>()

    fun swap(modelBytes: ByteArray) {
        val newInterpreter = Interpreter(ByteBuffer.wrap(modelBytes))
        val old = interpreterRef.getAndSet(newInterpreter)
        old?.close()
    }
}""",
            "metric": "Saved 42MB in initial app download size via dynamic model downloads."
        },
        {
            "id": "q18",
            "title": "6. How do you manage Dual Camera concurrency (ConcurrentCamera) in CameraX?",
            "problem": "Opening front and back cameras at once crashes unsupported Android hardware.",
            "solution": [
                ("QUERY HARDWARE", "I check CameraManager for dual camera support."),
                ("CONCURRENT BINDING", "ConcurrentCameraConfig binds front and back previews simultaneously."),
                ("OPENGL COMPOSITING", "OpenGL composites both streams into one surface."),
                ("SAFE FALLBACK", "Unsupported devices switch to fast alternating mode."),
                ("CLEAN UNBIND", "onPause unbinds camera providers to free hardware."),
                ("STEADY PREVIEW", "Delivers Picture-in-Picture camera feed at 30 FPS.")
            ],
            "code": """val provider = ProcessCameraProvider.getInstance(context).get()
if (provider.availableConcurrentCameraInfos.isNotEmpty()) {
    provider.bindToLifecycle(listOf(frontConfig, backConfig))
}""",
            "metric": "Delivered Picture-in-Picture dual camera capture at steady 30 FPS."
        },
        {
            "id": "q19",
            "title": "7. How do you prevent Thermal Throttling during intensive on-device vision workloads?",
            "problem": "Continuous GPU and NPU inference heats phone, causing OS throttling.",
            "solution": [
                ("THERMAL LISTENER", "OnThermalStatusChangedListener monitors device thermal headroom dynamically."),
                ("DOWNSCALE FPS", "I drop frame rate to 10 FPS."),
                ("DSP FALLBACK", "I switch model execution to low-power DSPs."),
                ("REDUCE RESOLUTION", "Downscales analysis input resolution from 1080p down."),
                ("PAUSE ON IDLE", "Pauses vision processing during prolonged user idle."),
                ("EXTEND SESSIONS", "Prevents device shutdowns during long AR sessions.")
            ],
            "code": """powerManager.addThermalStatusListener { status ->
    if (status >= PowerManager.THERMAL_STATUS_SEVERE) {
        analyzer.throttleRate(factor = 3)
    } else {
        analyzer.restoreNormalRate()
    }
}""",
            "metric": "Eliminated thermal shutdowns, extending continuous AR sessions by 35 minutes."
        },
        {
            "id": "q20",
            "title": "8. How do you implement Real-Time Document Edge Detection and Perspective Warping?",
            "problem": "Angled receipts and documents create distorted photos and broken OCR scans.",
            "solution": [
                ("CANNY EDGES", "Canny edge filters find document boundary contours."),
                ("CONVEX HULL", "Four corner points identify document perspective bounds."),
                ("OPENCV WARPING", "getPerspectiveTransform warps angled images into flat rectangles."),
                ("ADAPTIVE THRESHOLD", "Adaptive binarization cleans shadows and sharpens text."),
                ("COROUTINE DISPATCH", "Runs image warping on Dispatchers.Default threads."),
                ("HIGH ACCURACY", "Delivers crisp scans for text OCR extraction.")
            ],
            "code": """fun warp(src: Mat, corners: Mat): Mat {
    val dest = Mat(height, width, CvType.CV_8UC4)
    val matrix = Imgproc.getPerspectiveTransform(corners, targetCorners)
    Imgproc.warpPerspective(src, dest, matrix, Size(width, height))
    return dest
}""",
            "metric": "Boosted OCR text recognition accuracy from 71% to 98.4%."
        },
        {
            "id": "q21",
            "title": "9. How do you handle Camera Permission denial and 'Don't Ask Again' gracefully?",
            "problem": "Premature permission popups cause permanent denial, breaking camera features.",
            "solution": [
                ("EXPLAIN FIRST", "I show educational bottom sheet before requesting."),
                ("REQUEST CONTRACT", "ActivityResultContracts.RequestPermission handles modern permission callbacks."),
                ("CHECK RATIONALE", "shouldShowRequestPermissionRationale checks if user previously denied."),
                ("SETTINGS REDIRECT", "Permanently denied users are guided to Settings."),
                ("GALLERY FALLBACK", "App offers gallery upload fallback when denied."),
                ("HIGHER ADOPTION", "Increases camera permission grants significantly across users.")
            ],
            "code": """val launcher = registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
    if (granted) startCamera()
    else if (!shouldShowRequestPermissionRationale(Manifest.permission.CAMERA)) {
        showSettingsDialog()
    }
}""",
            "metric": "Increased first-time camera permission acceptance from 62% to 89%."
        },
        {
            "id": "q22",
            "title": "10. How do you optimize Custom TFLite Operators using NDK and CMake?",
            "problem": "Unsupported math operations in custom ML models crash TFLite.",
            "solution": [
                ("CUSTOM C++ OPS", "I implement custom kernels extending OpKernel interface."),
                ("CMAKE NDK", "CMake compiles kernels for ARM64-v8a architectures."),
                ("REGISTER OP", "MutableOpResolver registers the operator before model execution."),
                ("NEON INTRINSICS", "ARM NEON SIMD vectorizes inner loops."),
                ("BENCHMARK PROFILING", "TFLite Benchmark tool measures custom operator latency."),
                ("FAST EXECUTION", "Runs proprietary models at native processor speeds.")
            ],
            "code": """TfLiteRegistration* Register_CUSTOM_OP() {
    static TfLiteRegistration r = {nullptr, nullptr, CustomPrepare, CustomEval};
    return &r;
}
// In Kotlin
resolver.addCustom("CustomOp", Register_CUSTOM_OP())""",
            "metric": "Achieved 3.8x faster throughput on custom signal processing models."
        },
        {
            "id": "q23",
            "title": "11. How do you architect an offline-first Object Detection and Bounding Box Tracker?",
            "problem": "Running heavy object detection on every frame causes battery drain and stutter.",
            "solution": [
                ("KEYFRAME DETECT", "Heavy detection runs once every five frames."),
                ("LIGHT TRACKER", "Fast optical flow tracks boxes between keyframes."),
                ("IOU MATCHING", "Intersection-Over-Union associates matching object bounding boxes."),
                ("SMOOTH COORDS", "Exponential smoothing eliminates bounding box visual flickering."),
                ("THREAD DECOUPLING", "Double buffered queues decouple tracker from detector."),
                ("SAVE BATTERY", "Maintains 30 FPS while cutting CPU load.")
            ],
            "code": """class Tracker {
    fun onFrame(bitmap: Bitmap, isKey: Boolean): List<Box> {
        return if (isKey) detector.detect(bitmap)
        else opticalFlow.update(bitmap)
    }
}""",
            "metric": "Maintained smooth 30 FPS tracking while cutting power use by 52%."
        },
        {
            "id": "q24",
            "title": "12. How do you implement Camera Zoom, Tap-to-Focus, and Exposure Compensation?",
            "problem": "Blurry captures and dark images frustrate camera and scanner users.",
            "solution": [
                ("METERING POINT", "SurfaceOrientedMeteringPointFactory converts screen taps to coordinates."),
                ("FOCUS ACTION", "FocusMeteringAction sets auto-focus and auto-exposure points."),
                ("AUTO CANCEL", "Restores continuous autofocus after three seconds automatically."),
                ("PINCH ZOOM", "cameraControl.setZoomRatio handles smooth pinch gesture zooming."),
                ("EXPOSURE BIAS", "Dynamic exposure compensation brightens dark camera scenes."),
                ("CLEAR SCANS", "Produces sharp focus on barcodes and faces.")
            ],
            "code": """val factory = SurfaceOrientedMeteringPointFactory(width, height)
val action = FocusMeteringAction.Builder(factory.createPoint(x, y)).build()
cameraControl.startFocusAndMetering(action)""",
            "metric": "Sped up barcode scanner time-to-first-read to 210 milliseconds."
        }
    ]
}

m3 = {
    "id": "module-3",
    "title": "Module 3: BLE, GATT & Hardware Integration",
    "badge": "Indigo",
    "color": "indigo",
    "summary": "Mutex Serial Queue, Error 133 Elimination, MTU 517 Negotiation, CCCD 0x2902, autoConnect Modes, OTA Flashing.",
    "questions": [
        {
            "id": "q25",
            "title": "1. How do you resolve Android Bluetooth GATT Error 133 and connection drops?",
            "problem": "Android BLE stack crashes with Error 133 during rapid concurrent commands.",
            "solution": [
                ("MUTEX QUEUE", "A Coroutine Mutex serializes all GATT operations."),
                ("MAIN THREAD", "I invoke connectGatt strictly on Main thread."),
                ("AUTOCONNECT FALSE", "autoConnect false enables immediate direct connection attempts."),
                ("CLOSE GATTHANDLE", "gatt.close releases native client handles immediately."),
                ("RECONNECT BACKOFF", "Retries failed connections using exponential random backoff."),
                ("HIGH RELIABILITY", "Reaches 99.4% hardware Bluetooth connection success.")
            ],
            "code": """class BleQueue {
    private val mutex = Mutex()
    suspend fun <T> run(block: suspend () -> T): T = mutex.withLock {
        withTimeout(5000L) { block() }
    }
}""",
            "metric": "Eliminated Status 133 errors, reaching 99.4% BLE connection success."
        },
        {
            "id": "q26",
            "title": "2. How do you negotiate maximum BLE throughput with MTU 517 and PHY 2M?",
            "problem": "Default 23-byte MTU limits data speed to 3KB/s, lagging telemetry.",
            "solution": [
                ("REQUEST MTU 517", "I request MTU 517 on connection."),
                ("2M PHY SPEED", "setPreferredPhy PHY_LE_2M doubles raw RF speed."),
                ("NO RESPONSE WRITE", "WRITE_TYPE_NO_RESPONSE streams data without waiting ACKs."),
                ("PACKET PACKING", "Packs telemetry into 512-byte contiguous byte arrays."),
                ("WINDOW ACKS", "Sliding window ACKs guarantee zero packet loss."),
                ("HIGH SPEED STREAM", "Increases throughput from 3KB/s to 64KB/s.")
            ],
            "code": """override fun onConnectionStateChange(gatt: BluetoothGatt, status: Int, state: Int) {
    if (state == BluetoothProfile.STATE_CONNECTED) {
        gatt.requestMtu(517)
    }
}
override fun onMtuChanged(gatt: BluetoothGatt, mtu: Int, status: Int) {
    gatt.setPreferredPhy(BluetoothDevice.PHY_LE_2M_MASK, BluetoothDevice.PHY_LE_2M_MASK, 0)
}""",
            "metric": "Increased BLE payload data throughput from 2.8KB/s to 64.5KB/s (23x boost)."
        },
        {
            "id": "q27",
            "title": "3. How do you correctly enable CCCD (0x2902) Descriptor Notifications?",
            "problem": "Setting characteristic notification without writing CCCD fails to receive peripheral data.",
            "solution": [
                ("SET LOCAL NOTIFY", "setCharacteristicNotification registers local OS notification listener."),
                ("CCCD 0X2902", "I find Client Configuration descriptor 0x2902."),
                ("ENABLE VALUE", "Sets descriptor value to ENABLE_NOTIFICATION_VALUE bytes."),
                ("WRITE DESCRIPTOR", "I write descriptor through serial Mutex queue."),
                ("API 33 SUPPORT", "Adapts for Android 13 descriptor write signatures."),
                ("STREAM SENSORS", "Enables reliable real-time hardware sensor streaming.")
            ],
            "code": """val cccd = char.getDescriptor(UUID.fromString("00002902-0000-1000-8000-00805f9b34fb"))
cccd.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
bleQueue.run { gatt.writeDescriptor(cccd) }""",
            "metric": "Guaranteed 100% reliable telemetry reception across connected smart hardware."
        },
        {
            "id": "q28",
            "title": "4. When should you use autoConnect=true vs autoConnect=false in connectGatt?",
            "problem": "Wrong autoConnect flags cause 30-second timeouts or fail background reconnects.",
            "solution": [
                ("FALSE FOR DIRECT", "autoConnect false connects immediately with 30s timeout."),
                ("DIRECT CONTROLLER", "Instructs radio controller to attempt immediate connection."),
                ("TRUE FOR BACKGROUND", "autoConnect true passively waits for peripheral advertisements."),
                ("WHITELIST SCAN", "Registers device in native BLE hardware whitelist."),
                ("LOW POWER SCAN", "autoConnect true saves substantial background battery."),
                ("FAST CONNECTION", "Gives immediate connects in foreground user flows.")
            ],
            "code": """fun connect(device: BluetoothDevice, isBackground: Boolean) {
    val autoConnect = isBackground
    device.connectGatt(context, autoConnect, callback, BluetoothDevice.TRANSPORT_LE)
}""",
            "metric": "Reduced foreground connection wait times by 85%."
        },
        {
            "id": "q29",
            "title": "5. How do you implement robust Over-The-Air (OTA) Dual-Bank Firmware Flashing?",
            "problem": "Connection drops mid-flash brick connected hardware peripherals.",
            "solution": [
                ("DUAL BANK FLASH", "Firmware writes to inactive bank B safely."),
                ("PACKET CHUNKING", "Binary splits into MTU chunks with CRC16."),
                ("PROGRESS ACKS", "Verifies checksum ACK after every 32 packets."),
                ("RESUME ON DROP", "Reconnection resumes from last verified block offset."),
                ("ATOMIC SWAP", "Bootloader swaps partitions only after verification."),
                ("SAFE UPDATES", "Guarantees zero hardware bricking during OTA updates.")
            ],
            "code": """suspend fun flash(bytes: ByteArray) {
    bytes.asList().chunked(CHUNK_SIZE).forEachIndexed { i, chunk ->
        bleQueue.run { sendChunk(i, chunk.toByteArray()) }
        if (i % 32 == 0) bleQueue.run { verifyProgress(i) }
    }
}""",
            "metric": "Achieved 99.98% successful OTA completion rate across 250,000+ devices."
        },
        {
            "id": "q30",
            "title": "6. How do you handle Android 12+ Bluetooth Runtime Permissions?",
            "problem": "Requesting legacy location permissions for BLE scan confuses modern users.",
            "solution": [
                ("BLUETOOTH SCAN", "BLUETOOTH_SCAN declares neverForLocation in Manifest."),
                ("BLUETOOTH CONNECT", "BLUETOOTH_CONNECT allows reading and writing characteristics."),
                ("CONTRACT LAUNCHER", "RequestMultiplePermissions prompts runtime permissions cleanly together."),
                ("VERSION CHECKS", "Branches logic cleanly for Android 12 SDK."),
                ("ADVERTISE PERMISSION", "BLUETOOTH_ADVERTISE is requested for peripheral beacon modes."),
                ("ZERO LOCATION PROMPT", "Removes unnecessary location permission prompts on Android.")
            ],
            "code": """<uses-permission android:name="android.permission.BLUETOOTH_SCAN"
    android:usesPermissionFlags="neverForLocation" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />""",
            "metric": "Complied 100% with Android 12/13/14 runtime security requirements."
        },
        {
            "id": "q31",
            "title": "7. How do you filter noisy BLE RSSI telemetry using a 1D Kalman Filter?",
            "problem": "Fluctuating RSSI signals (+/-15 dBm) cause jumpy distance calculations.",
            "solution": [
                ("STATE ESTIMATE", "Kalman filter balances prediction and measured RSSI."),
                ("NOISE TUNING", "Measurement noise parameter R smooths RF spikes."),
                ("PROCESS NOISE", "Process noise Q controls filter tracking responsiveness."),
                ("KALMAN GAIN", "Dynamic gain weights each incoming RSSI packet."),
                ("PATH LOSS FORMULA", "Converts filtered RSSI into stable metric distances."),
                ("ACCURATE DISTANCE", "Produces stable indoor proximity and range estimation.")
            ],
            "code": """class RssiFilter(private val r: Double = 0.8, private val q: Double = 0.05) {
    private var x = -65.0
    private var p = 1.0
    fun update(rssi: Double): Double {
        p += q
        val k = p / (p + r)
        x += k * (rssi - x)
        p *= (1 - k)
        return x
    }
}""",
            "metric": "Smoothed RSSI noise fluctuations by 82%, reaching 0.5-meter indoor accuracy."
        },
        {
            "id": "q32",
            "title": "8. How do you manage BLE Peripheral GATT Server mode on Android?",
            "problem": "Acting as a BLE peripheral requires advertising services and handling client writes.",
            "solution": [
                ("LE ADVERTISER", "BluetoothLeAdvertiser broadcasts custom service UUIDs."),
                ("OPEN GATT SERVER", "openGattServer registers characteristics and read callbacks."),
                ("ADD SERVICES", "Adds custom GATT services with read characteristics."),
                ("SEND RESPONSES", "sendResponse sends explicit acknowledgments to central devices."),
                ("NOTIFY CENTRALS", "notifyCharacteristicChanged pushes real-time updates to connected centrals."),
                ("OFFLINE MESH", "Enables phone-to-phone data sync without internet.")
            ],
            "code": """val server = manager.openGattServer(context, object : BluetoothGattServerCallback() {
    override fun onCharacteristicReadRequest(dev: BluetoothDevice, id: Int, off: Int, c: BluetoothGattCharacteristic) {
        server.sendResponse(dev, id, BluetoothGatt.GATT_SUCCESS, off, c.value)
    }
})""",
            "metric": "Enabled phone-to-phone offline mesh sync with sub-50ms peer discovery."
        },
        {
            "id": "q33",
            "title": "9. How do you implement reliable background BLE Scanning without OS throttling?",
            "problem": "Android OS kills unconfigured background BLE scans to save battery.",
            "solution": [
                ("SCAN FILTERS", "ScanFilter with Service UUID allows screen-off scanning."),
                ("LOW POWER MODE", "SCAN_MODE_LOW_POWER reduces radio duty cycle."),
                ("PENDINGINTENT", "PendingIntent survives application process terminations cleanly."),
                ("BATCH RESULTS", "Batches BLE scan results at 5000ms intervals."),
                ("FOREGROUND SERVICE", "Binds sync to connectedDevice foreground service type."),
                ("LOW BATTERY USE", "Runs 24/7 background beacon discovery.")
            ],
            "code": """val filter = ScanFilter.Builder().setServiceUuid(ParcelUuid(SERVICE_UUID)).build()
val settings = ScanSettings.Builder()
    .setScanMode(ScanSettings.SCAN_MODE_LOW_POWER)
    .build()
scanner.startScan(listOf(filter), settings, pendingIntent)""",
            "metric": "Maintained 24/7 continuous beacon discovery with under 1.2% daily battery drain."
        },
        {
            "id": "q34",
            "title": "10. How do you handle Bluetooth Hardware Adapter toggles and unexpected resets?",
            "problem": "User toggling Bluetooth OFF leaves coroutines hanging and leaks handles.",
            "solution": [
                ("STATE RECEIVER", "BroadcastReceiver listens for ACTION_STATE_CHANGED intent events."),
                ("TEARDOWN ON OFF", "STATE_TURNING_OFF immediately closes all active GATTs."),
                ("CANCEL TIMEOUTS", "Cancels suspended coroutines and clears queues safely."),
                ("AUTO RECONNECT", "STATE_ON triggers exponential backoff reconnection loops."),
                ("UI STATE UPDATES", "Notifies UI layer via reactive StateFlow state."),
                ("ZERO DEADLOCKS", "Eliminates deadlocks from sudden hardware power changes.")
            ],
            "code": """class BleReceiver(private val onState: (Boolean) -> Unit) : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, -1)
        onState(state == BluetoothAdapter.STATE_ON)
    }
}""",
            "metric": "Eliminated 100% of deadlocks caused by sudden Bluetooth hardware toggles."
        },
        {
            "id": "q35",
            "title": "11. How do you implement End-to-End AES-GCM encryption over raw BLE characteristics?",
            "problem": "Standard BLE pairing is vulnerable to packet sniffing in public places.",
            "solution": [
                ("PAYLOAD ENCRYPTION", "I encrypt data bytes before BLE transmission."),
                ("AES GCM 128", "AES-GCM guarantees privacy and payload tampering detection."),
                ("ECDH KEYS", "Elliptic curve key exchange negotiates session keys."),
                ("DYNAMIC NONCE", "A 12-byte initialization vector increments per packet."),
                ("REPLAY PROTECTION", "Rejects packets with non-increasing IV nonce values."),
                ("BLOCK SNIFFING", "Blocks man-in-the-middle packet sniffing attacks.")
            ],
            "code": """fun encrypt(key: SecretKey, nonce: ByteArray, data: ByteArray): ByteArray {
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.ENCRYPT_MODE, key, GCMParameterSpec(128, nonce))
    return cipher.doFinal(data)
}""",
            "metric": "Passed third-party hardware security penetration test with zero vulnerabilities."
        },
        {
            "id": "q36",
            "title": "12. How do you benchmark BLE Packet Loss and Connection Interval latencies?",
            "problem": "Slow connection intervals cause high latency and sluggish sensor controls.",
            "solution": [
                ("HIGH PRIORITY", "requestConnectionPriority HIGH forces 11 to 15ms intervals."),
                ("PING TIMESTAMPS", "Timestamped ping packets measure round-trip times."),
                ("SEQUENCE NUMBERS", "Sequence IDs track packet loss percentage accurately."),
                ("DYNAMIC DOWNSHIFT", "Switches back to BALANCED when idle."),
                ("DEBUG OVERLAYS", "Shows real-time telemetry stats in developer overlay."),
                ("FAST CONTROLS", "Drops command latency from 180ms to 22ms.")
            ],
            "code": """fun setFastMode(gatt: BluetoothGatt) {
    gatt.requestConnectionPriority(BluetoothGatt.CONNECTION_PRIORITY_HIGH)
}
fun setIdleMode(gatt: BluetoothGatt) {
    gatt.requestConnectionPriority(BluetoothGatt.CONNECTION_PRIORITY_BALANCED)
}""",
            "metric": "Decreased end-to-end hardware sensor command latency from 180ms to 22ms."
        }
    ]
}

print("Part 1 (6 points): Modules 1, 2, 3 compiled.")
