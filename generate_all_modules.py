import json

def get_all_modules():
    # Return full array of 9 modules, each with 12 questions
    from build_complete_app import modules as m1
    
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
                "problem": "Heavy frame processing in ImageAnalysis blocks CameraX capture pipeline, causing frame drops and OutOfMemoryErrors.",
                "solution": [
                    ("KEEP ONLY LATEST", "I set backpressure strategy to STRATEGY_KEEP_ONLY_LATEST to discard stale camera frames automatically."),
                    ("DEDICATED EXECUTOR", "I dispatch frame analysis to dedicated single-thread Executors.newSingleThreadExecutor() background pipeline."),
                    ("ZERO COPY BUFFERS", "I extract ByteBuffer planes directly without allocating intermediate JVM byte array copies."),
                    ("TRY FINALLY CLOSE", "I invoke imageProxy.close() inside mandatory finally blocks to release hardware buffers."),
                    ("ROTATION TRANSFORMS", "I calculate sensor rotation degrees to orient input bitmaps before model inference.")
                ],
                "code": """val imageAnalysis = ImageAnalysis.Builder()
    .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
    .setOutputImageFormat(ImageAnalysis.OUTPUT_IMAGE_FORMAT_YUV_420_888)
    .build()

imageAnalysis.setAnalyzer(analysisExecutor) { imageProxy ->
    try {
        processFrameWithTFLite(imageProxy)
    } finally {
        imageProxy.close()
    }
}""",
                "metric": "Maintained rock-solid 60 FPS preview with zero buffer drops across 500+ Android device models."
            },
            {
                "id": "q14",
                "title": "2. How do you optimize On-Device ML Models with INT8 Post-Training Quantization?",
                "problem": "Float32 neural network models are too large (100MB+), consume excessive battery, and run too slowly on mobile CPUs.",
                "solution": [
                    ("INT8 QUANTIZATION", "I quantize Float32 weights into signed INT8 values, shrinking model size by 75%."),
                    ("NNAPI AND GPU DELEGATE", "I bind TFLite interpreter to NNAPI and GPU hardware acceleration delegates directly."),
                    ("CALIBRATION DATASET", "I feed representative representative_dataset inputs during quantization to retain 99% accuracy."),
                    ("DYNAMIC MEMORY BUFFER", "I pre-allocate direct ByteBuffers matching model tensor dimensions to avoid GC churn."),
                    ("FALLBACK CPU RUNTIME", "I configure graceful XNNPACK CPU fallback if hardware delegate initialization fails.")
                ],
                "code": """val options = Interpreter.Options().apply {
    setNumThreads(4)
    addDelegate(GpuDelegate())
    setUseXNNPACK(true)
}
val tflite = Interpreter(loadModelFile(context, "model_int8.tflite"), options)""",
                "metric": "Reduced model size from 84MB to 21MB and sped up inference latency from 140ms to 18ms."
            },
            {
                "id": "q15",
                "title": "3. How do you integrate ML Kit Face Mesh with Filament 3D Engine for Virtual Try-On?",
                "problem": "High rendering latency, coordinate mismatch, and jitter during 3D eyewear/accessory augmented reality try-on.",
                "solution": [
                    ("FACE MESH 468 POINTS", "I track 468 high-density 3D facial landmarks using ML Kit Face Mesh detection."),
                    ("KALMAN SMOOTHING", "I apply 1D Kalman filters over facial coordinates to suppress camera sensor jitter."),
                    ("FILAMENT PBR ENGINE", "I render photorealistic physical materials using Google's Filament lightweight 3D engine."),
                    ("TRANSFORMATION MATRIX", "I map facial landmarks to 3D model translation, scale, and rotation quaternions."),
                    ("SURFACEVIEW SYNCHRONIZATION", "I synchronize camera preview frames with Filament surface rendering on Choreographer pulses.")
                ],
                "code": """val detector = FaceMeshDetection.getClient(FaceMeshDetectorOptions.Builder().build())
detector.process(inputImage).addOnSuccessListener { meshes ->
    val face = meshes.firstOrNull() ?: return@addOnSuccessListener
    val noseBridge = face.allPoints[6].position
    val smoothedPose = kalmanFilter.update(noseBridge)
    filamentRenderer.updateModelPose(smoothedPose)
}""",
                "metric": "Delivered fluid 60 FPS AR Try-On experience with sub-16ms end-to-end rendering latency."
            },
            {
                "id": "q16",
                "title": "4. How do you convert YUV_420_888 frames to RGB ByteBuffers with zero allocation?",
                "problem": "Standard Java YUV-to-Bitmap conversion creates massive garbage collection allocations, dropping UI frame rates.",
                "solution": [
                    ("NATIVE LIBYUV", "I leverage libyuv C++ native libraries to perform YUV-to-RGB color space conversions."),
                    ("DIRECT BYTEBUFFER", "I reuse pre-allocated direct ByteBuffer pools across successive frame analysis passes."),
                    ("RENDER SCRIPT REPLACEMENT", "I utilize Vulkan Compute or NDK SIMD instructions replacing deprecated RenderScript APIs."),
                    ("STRIDE PADDING HANDLING", "I account for row stride and pixel stride offsets when indexing plane buffers."),
                    ("ZERO GC PRESSURE", "Zero JVM heap allocations during frame transformation completely eliminates GC pauses.")
                ],
                "code": """// Native NDK binding for zero-copy frame conversion
external fun nativeYuvToRgb(
    yBuffer: ByteBuffer, uBuffer: ByteBuffer, vBuffer: ByteBuffer,
    yRowStride: Int, uvRowStride: Int, uvPixelStride: Int,
    width: Int, height: Int, outRgbBuffer: ByteBuffer
)""",
                "metric": "Eliminated 100% of frame-time GC pauses, recovering 4.2ms per frame on low-tier hardware."
            },
            {
                "id": "q17",
                "title": "5. How do you architect dynamic Model Hot-Swapping without restarting the app?",
                "problem": "Shipping new ML models via full APK releases delays rapid iterations and bloats baseline app download sizes.",
                "solution": [
                    ("PLAY FEATURE DELIVERY", "I deliver updated ML models dynamically using Google Play Feature Delivery on-demand."),
                    ("THREAD SAFE SWAP", "I wrap TFLite Interpreter inside AtomicReference to swap model instances without locking."),
                    ("CHECKSUM VERIFICATION", "I verify SHA-256 cryptographic hashes before loading newly downloaded model binaries."),
                    ("WARMUP INFERENCE", "I execute dummy inference on background thread to warm up model caches prior to swapping."),
                    ("ROLLBACK ON FAILURE", "I automatically revert to bundled baseline model if downloaded model execution throws errors.")
                ],
                "code": """class DynamicModelManager(private val context: Context) {
    private val interpreterRef = AtomicReference<Interpreter>()

    fun swapModel(newModelBytes: ByteArray, expectedSha: String) {
        if (!verifyChecksum(newModelBytes, expectedSha)) return
        val newInterpreter = Interpreter(ByteBuffer.wrap(newModelBytes))
        newInterpreter.run(dummyInput, dummyOutput) // Warmup
        val old = interpreterRef.getAndSet(newInterpreter)
        old?.close()
    }
}""",
                "metric": "Reduced initial APK download size by 42MB and enabled remote zero-downtime model deployments."
            },
            {
                "id": "q18",
                "title": "6. How do you manage Dual Camera concurrency (ConcurrentCamera) in CameraX?",
                "problem": "Simultaneously accessing front and back cameras causes hardware resource conflicts on unsupported Android devices.",
                "solution": [
                    ("FEATURE QUERYING", "I query CameraManager.getConcurrentCameraIds() to check hardware dual-camera support safely."),
                    ("DUAL USE CASE BINDINGS", "I bind front and back preview use cases simultaneously using ConcurrentCameraConfig."),
                    ("COMPOSITIONAL RENDERING", "I composite front and back streams onto a single hardware Surface using OpenGL shaders."),
                    ("FALLBACK TO PIPELINING", "I gracefully downgrade to fast alternating snapshot mode if dual hardware is unavailable."),
                    ("LIFECYCLE UNBINDING", "I unbind both camera providers cleanly in onPause to release ISP hardware blocks.")
                ],
                "code": """val cameraProvider = ProcessCameraProvider.getInstance(context).get()
val availableCombinations = cameraProvider.availableConcurrentCameraInfos
if (availableCombinations.isNotEmpty()) {
    val singleCameraConfigFront = SingleCameraConfig(frontCameraSelector, frontUseCaseGroup, lifecycleOwner)
    val singleCameraConfigBack = SingleCameraConfig(backCameraSelector, backUseCaseGroup, lifecycleOwner)
    cameraProvider.bindToLifecycle(listOf(singleCameraConfigFront, singleCameraConfigBack))
}""",
                "metric": "Delivered Picture-in-Picture dual-stream capture with seamless 30 FPS synchronization."
            },
            {
                "id": "q19",
                "title": "7. How do you prevent Thermal Throttling during intensive on-device vision workloads?",
                "problem": "Continuous GPU/NPU utilization heats up device, triggering OS thermal throttling and severe frame drops.",
                "solution": [
                    ("THERMAL STATUS LISTENER", "I register PowerManager.OnThermalStatusChangedListener to monitor device thermal headroom dynamically."),
                    ("DYNAMIC FPS THROTTLING", "I scale analysis frequency from 30 FPS down to 10 FPS when thermal warning triggers."),
                    ("DELEGATE DOWNSHIFTING", "I switch model execution from GPU delegate to low-power DSP/NPU cores during heat spikes."),
                    ("RESOLUTION DOWNSCALING", "I downscale analysis input resolution from 1080p to 480p to reduce MAC computation loads."),
                    ("PROACTIVE COOLING REST", "I pause background ML feature detection during prolonged user idle states.")
                ],
                "code": """val powerManager = context.getSystemService(Context.POWER_SERVICE) as PowerManager
powerManager.addThermalStatusListener { status ->
    when (status) {
        PowerManager.THERMAL_STATUS_SEVERE, PowerManager.THERMAL_STATUS_CRITICAL -> {
            analysisExecutor.throttleDownSampling(factor = 3)
        }
        PowerManager.THERMAL_STATUS_NONE -> {
            analysisExecutor.restoreDefaultSampling()
        }
    }
}""",
                "metric": "Eliminated thermal-induced crash shutdowns, extending continuous AR sessions by 35 minutes."
            },
            {
                "id": "q20",
                "title": "8. How do you implement Real-Time Document Edge Detection and Perspective Warping?",
                "problem": "Poor document lighting and angled perspectives produce distorted scans and failed OCR extraction.",
                "solution": [
                    ("CANNY EDGE DETECTION", "I run Canny edge filtering and Hough line transforms to identify document boundaries."),
                    ("CONVEX HULL CORNERS", "I locate the 4 outermost corner vertices by finding the largest closed contour."),
                    ("OPENCV PERSPECTIVE TRANSFORM", "I calculate 3x3 homography matrix to warp perspective into flat rectangular bitmap."),
                    ("ADAPTIVE THRESHOLDING", "I apply adaptive binarization to clean up shadows and enhance text contrast."),
                    ("COROUTINE ACCELERATION", "I execute geometric warping on Dispatchers.Default with pre-allocated native matrices.")
                ],
                "code": """fun getTransformedBitmap(srcBitmap: Bitmap, corners: List<PointF>): Bitmap {
    val srcMat = Mat()
    Utils.bitmapToMat(srcBitmap, srcMat)
    val destMat = Mat(outputHeight, outputWidth, CvType.CV_8UC4)
    val perspectiveMatrix = Imgproc.getPerspectiveTransform(srcCornersMat, destCornersMat)
    Imgproc.warpPerspective(srcMat, destMat, perspectiveMatrix, Size(outputWidth.toDouble(), outputHeight.toDouble()))
    return Bitmap.createBitmap(outputWidth, outputHeight, Bitmap.Config.ARGB_8888).also {
        Utils.matToBitmap(destMat, it)
    }
}""",
                "metric": "Boosted downstream OCR recognition accuracy from 71% to 98.4% on angled receipts."
            },
            {
                "id": "q21",
                "title": "9. How do you handle Camera Permission denial and 'Don't Ask Again' gracefully?",
                "problem": "Premature permission prompts cause permanent user denial, breaking core camera features permanently.",
                "solution": [
                    ("RATIONALE EXPLANATION", "I explain feature benefits via educational bottom sheet before requesting system permissions."),
                    ("ACTIVITY RESULT CONTRACT", "I use ActivityResultContracts.RequestPermission() modern type-safe contract bindings."),
                    ("SHOULD SHOW RATIONALE", "I check shouldShowRequestPermissionRationale to distinguish first denial from permanent denial."),
                    ("APP SETTINGS REDIRECT", "I guide permanently denied users directly to Android Settings screen with clear instructions."),
                    ("DEGRADED UI MODE", "I maintain degraded gallery picker fallback when camera access is refused.")
                ],
                "code": """val requestCamera = registerForActivityResult(ActivityResultContracts.RequestPermission()) { isGranted ->
    if (isGranted) {
        startCamera()
    } else if (!shouldShowRequestPermissionRationale(Manifest.permission.CAMERA)) {
        showSettingsRedirectDialog()
    } else {
        showPermissionRationaleBottomSheet()
    }
}""",
                "metric": "Increased first-time camera permission acceptance rate from 62% to 89% via pre-prompts."
            },
            {
                "id": "q22",
                "title": "10. How do you optimize Custom TFLite Operators using NDK and CMake?",
                "problem": "Unsupported custom mathematical operations in specialized ML models cause TFLite interpreter initialization crashes.",
                "solution": [
                    ("CUSTOM OP REGISTRATION", "I write custom C++ kernel implementations extending tflite::OpKernel interface."),
                    ("CMAKE NDK BUILD", "I compile native kernel libraries using CMake toolchain targeting ARM64-v8a architectures."),
                    ("OP RESOLVER REGISTRATION", "I register custom kernels into MutableOpResolver before loading model files."),
                    ("NEON SIMD VECTORIZATION", "I vectorize inner mathematical loops with ARM NEON intrinsics for 4x speedup."),
                    ("STABILITY PROFILING", "I benchmark custom op latency using TFLite Benchmark Tool on physical hardware.")
                ],
                "code": """// Custom C++ TFLite Operator Registration
TfLiteRegistration* Register_CUSTOM_TRANSFORM() {
    static TfLiteRegistration r = {nullptr, nullptr, CustomOpPrepare, CustomOpEval};
    return &r;
}
// Resolver in Kotlin
val resolver = MutableOpResolver().apply {
    addCustom("CustomTransform", Register_CUSTOM_TRANSFORM())
}""",
                "metric": "Enabled proprietary signal processing model execution with 3.8x faster throughput over standard ops."
            },
            {
                "id": "q23",
                "title": "11. How do you architect an offline-first Object Detection and Bounding Box Tracker?",
                "problem": "Running heavy object detection on every frame causes stutter; tracking without detection drifts over time.",
                "solution": [
                    ("DETECTOR TRACKER PIPELINE", "I run heavy YOLO/SSDMobileNet detection every 5th frame and lightweight tracker every frame."),
                    ("IOU TRACKING OVERLAP", "I associate bounding boxes across frames using Intersection-Over-Union spatial metrics."),
                    ("EXPONENTIAL SMOOTHING", "I smooth bounding box coordinates across frames to prevent visual flickering."),
                    ("THREAD DECOUPLING", "I decouple detector thread from tracker thread using double-buffered state queues."),
                    ("OFFLINE ZERO BANDWIDTH", "All vision models run 100% on-device with zero cloud API dependencies.")
                ],
                "code": """class RealTimeTracker {
    private var lastDetections: List<TrackedBox> = emptyList()
    
    fun onNewFrame(bitmap: Bitmap, isKeyFrame: Boolean): List<TrackedBox> {
        return if (isKeyFrame) {
            val freshBoxes = detector.detect(bitmap)
            lastDetections = matchAndSmooth(lastDetections, freshBoxes)
            lastDetections
        } else {
            lastDetections = opticalFlowTracker.updatePositions(bitmap, lastDetections)
            lastDetections
        }
    }
}""",
                "metric": "Maintained real-time 30 FPS bounding box tracking while cutting CPU power consumption by 52%."
            },
            {
                "id": "q24",
                "title": "12. How do you implement Camera Zoom, Tap-to-Focus, and Exposure Compensation?",
                "problem": "Poor manual focus and exposure controls cause blurry captures and frustrating camera UX.",
                "solution": [
                    ("METERING POINT FACTORY", "I convert touch screen coordinates into normalized sensor MeteringPoints using SurfaceOrientedMeteringPointFactory."),
                    ("FOCUS AND METERING ACTION", "I build FocusMeteringAction targeting both AF (auto-focus) and AE (auto-exposure) regions."),
                    ("AUTO CANCEL TIMEOUT", "I configure auto-cancel after 3 seconds to restore continuous auto-focus mode."),
                    ("LINEAR ZOOM RATIO", "I clamp user pinch gestures to cameraControl.setZoomRatio() within supported hardware limits."),
                    ("EXPOSURE BIAS INDEX", "I adjust exposure compensation index dynamically to brighten high-contrast scenes.")
                ],
                "code": """val factory = SurfaceOrientedMeteringPointFactory(previewView.width.toFloat(), previewView.height.toFloat())
val point = factory.createPoint(tapX, tapY)
val action = FocusMeteringAction.Builder(point, FocusMeteringAction.FLAG_AF or FocusMeteringAction.FLAG_AE)
    .setAutoCancelDuration(3, TimeUnit.SECONDS)
    .build()
cameraControl.startFocusAndMetering(action)""",
                "metric": "Reduced blurry capture rates by 68% and improved barcode scanning time-to-first-read to 210ms."
            }
        ]
    }
    
    return [m1[0], m2]

print("Modules 1 and 2 ready.")
