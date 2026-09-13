# Modules 7, 8, 9 - Exactly 6 bullets per question, strictly 5-7 words per bullet

m7 = {
    "id": "module-7",
    "title": "Module 7: Mobile Security, Cryptography & Hardening",
    "badge": "Teal",
    "color": "teal",
    "summary": "Android KeyStore TEE/StrongBox, EncryptedPrefs, Certificate Pinning, R8 Obfuscation, Play Integrity API, Root/Frida Detection.",
    "questions": [
        {
            "id": "q73",
            "title": "1. How do you generate and manage hardware-backed cryptographic keys with KeyStore?",
            "problem": "Software keys can be dumped from device RAM by root memory tools.",
            "solution": [
                ("HARDWARE TEE", "KeyGenParameterSpec generates keys inside StrongBox."),
                ("ENCRYPT PURPOSE", "Keys are restricted to AES-GCM encryption."),
                ("BIOMETRIC LOCK", "setUserAuthenticationRequired mandates fingerprint for decryption."),
                ("ZERO KEY EXPORT", "Hardware keys cannot leave the device."),
                ("AUTH TAGS", "AES-GCM verifies payload authentication tags automatically."),
                ("HIGH SECURITY", "Protects sensitive payment credentials on mobile.")
            ],
            "code": """val spec = KeyGenParameterSpec.Builder("MasterKey", KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)
    .setIsStrongBoxBacked(true)
    .build()""",
            "metric": "Protected payment credentials across 10M+ devices with zero key extraction breaches."
        },
        {
            "id": "q74",
            "title": "2. How do you implement OkHttp Certificate Pinning with backup SPKI hashes?",
            "problem": "Rogue Certificate Authorities or enterprise proxies can execute Man-in-the-Middle attacks.",
            "solution": [
                ("CERTIFICATE PINNER", "CertificatePinner pins SHA-256 Public Key hashes."),
                ("BACKUP PINS", "Includes intermediate CA and backup pins."),
                ("FAIL CLOSED", "OkHttp throws SSLPeerUnverifiedException on mismatch."),
                ("NETWORK CONFIG", "Mirrors pins in network security config."),
                ("PREVENT OUTAGES", "Rotating backup pins prevents sudden outages."),
                ("BLOCK PROXIES", "Blocks man-in-the-middle network proxy attacks.")
            ],
            "code": """val pinner = CertificatePinner.Builder()
    .add("api.lenskart.com", "sha256/k2oTTrsvErP43b1m4e97J8FDCm8gW59G=")
    .add("api.lenskart.com", "sha256/WoiWRyIOVNa9ihaBciRSC7XHjliYS9V=")
    .build()
val client = OkHttpClient.Builder().certificatePinner(pinner).build()""",
            "metric": "Thwarted 100% of proxy-based network eavesdropping during penetration testing."
        },
        {
            "id": "q75",
            "title": "3. How do you detect Rooted Devices, Magisk, and Frida dynamic instrumentation?",
            "problem": "Attackers use Magisk root and Frida scripts to hook sensitive methods and bypass checks.",
            "solution": [
                ("NATIVE C CHECKS", "Native C++ scans memory maps for frida."),
                ("PORT SCANS", "Scans for default Frida port 27042."),
                ("SU BINARY CHECK", "Checks for su binary paths on system."),
                ("BUILD TAGS", "Build.TAGS checks for unofficial test keys."),
                ("SILENT DEGRADE", "Disables payment tokens silently when tampering detected."),
                ("PLAY INTEGRITY", "Attests device trust via Play Integrity.")
            ],
            "code": """bool isFridaDetected() {
    FILE* fp = fopen("/proc/self/maps", "r");
    char line[512];
    while (fgets(line, sizeof(line), fp)) {
        if (strstr(line, "frida")) { fclose(fp); return true; }
    }
    fclose(fp);
    return false;
}""",
            "metric": "Blocked 45,000+ unauthorized tampering and Frida hook attempts against checkout logic."
        },
        {
            "id": "q76",
            "title": "4. How do you implement Google Play Integrity API with server-side nonce verification?",
            "problem": "Client-side checks can be patched in modified APKs by reverse engineers.",
            "solution": [
                ("SERVER NONCE", "Backend creates a unique request nonce."),
                ("INTEGRITY TOKEN", "PlayIntegrityManager requests signed attestation on device."),
                ("SERVER DECRYPT", "Server verifies MEETS_STRONG_INTEGRITY with Google."),
                ("BINARY DIGEST", "Server validates app signing certificate SHA digest."),
                ("NO REPLAY ATTACKS", "Reusing nonces triggers immediate server rejection."),
                ("BLOCK CLONES", "Eliminates pirated clone APKs and bots.")
            ],
            "code": """val response = integrityManager.requestIntegrityToken(
    IntegrityTokenRequest.builder().setNonce(serverNonce).build()
).await()
backendApi.verifyToken(response.token())""",
            "metric": "Eliminated 99.8% of automated bot attacks and pirated clone APKs."
        },
        {
            "id": "q77",
            "title": "5. How do you configure R8 ProGuard with custom dictionary obfuscation?",
            "problem": "Default ProGuard mappings (a, b, c) are easy to read and reverse-engineer.",
            "solution": [
                ("CUSTOM DICTIONARY", "obfuscationdictionary uses invisible Unicode for mapping."),
                ("CLASS DICTIONARY", "classobfuscationdictionary scrambles class and package hierarchies."),
                ("FLATTEN PACKAGES", "repackageclasses flattens internal classes into root."),
                ("MINIMAL KEEPS", "Specific Keep rules protect serialization models."),
                ("R8 FULL MODE", "Full mode eliminates dead code and inlines."),
                ("HARD DECOMPILE", "Makes decompiled bytecodes difficult to read.")
            ],
            "code": """# proguard-rules.pro
-obfuscationdictionary dict.txt
-classobfuscationdictionary dict.txt
-repackageclasses ''
-allowaccessmodification""",
            "metric": "Increased reverse-engineering decompilation difficulty by 10x while shrinking APK by 28%."
        },
        {
            "id": "q78",
            "title": "6. How do you secure IPC with PendingIntent, FLAG_IMMUTABLE, and Exported components?",
            "problem": "Mutable PendingIntents allow external malicious apps to hijack elevated privileges.",
            "solution": [
                ("FLAG IMMUTABLE", "FLAG_IMMUTABLE prevents external intent extra overwriting."),
                ("EXPORTED FALSE", "Unneeded manifest components set android:exported false."),
                ("SIGNATURE PERMISSION", "Shared components require signature level permissions."),
                ("AUDIT MUTABLE", "FLAG_MUTABLE is restricted strictly to notification replies."),
                ("EXPLICIT INTENTS", "Bans implicit intents for background service bindings."),
                ("SECURE IPC", "Blocks unauthorized inter-app IPC attacks.")
            ],
            "code": """val pi = PendingIntent.getActivity(
    context, 0, explicitIntent,
    PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
)""",
            "metric": "Zero IPC vulnerability warnings in Google Play Pre-launch Reports across all releases."
        },
        {
            "id": "q79",
            "title": "7. How do you implement Biometric Prompt with CryptoObject authentication?",
            "problem": "Checking biometric success without a cryptographic signature allows method hooking.",
            "solution": [
                ("CRYPTOOBJECT", "BiometricPrompt wraps an initialized cipher object."),
                ("HARDWARE AUTH", "Cipher unlocks only on biometric scan."),
                ("STRONG BIOMETRICS", "BIOMETRIC_STRONG enforces hardware-backed biometric security."),
                ("DEVICE CREDENTIALS", "PIN and pattern fallbacks handle degraded hardware."),
                ("ATTEST CIPHER", "cipher.doFinal executes securely inside authentication callback."),
                ("SECURE CHECKOUT", "Guarantees cryptographic proof for payments.")
            ],
            "code": """val prompt = BiometricPrompt.PromptInfo.Builder()
    .setTitle("Authenticate")
    .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_STRONG)
    .setNegativeButtonText("Cancel")
    .build()
biometricPrompt.authenticate(prompt, BiometricPrompt.CryptoObject(cipher))""",
            "metric": "Guaranteed cryptographic authenticity for 100% of biometric enterprise transactions."
        },
        {
            "id": "q80",
            "title": "8. How do you prevent Tapjacking and Screen Recording overlays in sensitive screens?",
            "problem": "Malicious overlay apps steal user taps or record banking screen inputs.",
            "solution": [
                ("FLAG SECURE", "FLAG_SECURE blocks screenshots and screen recording."),
                ("FILTER OBSCURED", "filterTouchesWhenObscured rejects touches from overlays."),
                ("OBSCURED EVENTS", "MotionEvent.FLAG_WINDOW_IS_OBSCURED discards compromised touch taps."),
                ("RECENTS BLUR", "FLAG_SECURE blacks out recent app previews."),
                ("FINANCIAL AUDIT", "Enforces strict financial banking compliance rules."),
                ("PROTECT DATA", "Prevents credential theft from invisible windows.")
            ],
            "code": """override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    window.setFlags(WindowManager.LayoutParams.FLAG_SECURE, WindowManager.LayoutParams.FLAG_SECURE)
}""",
            "metric": "Eliminated 100% of overlay tapjacking attacks and screenshot credential leaks."
        },
        {
            "id": "q81",
            "title": "9. How do you securely store API keys and secrets using C++ NDK and Obfuscation?",
            "problem": "Storing keys in strings.xml exposes plaintext secrets in decompiled DEX files.",
            "solution": [
                ("NDK C++ SECRETS", "Keys are compiled inside native binaries."),
                ("XOR ENCODING", "XOR encoded byte arrays decrypt in-memory."),
                ("SIGNATURE CHECK", "Native code verifies app signature first."),
                ("STRIP SYMBOLS", "llvm-strip removes debugging symbols in release builds."),
                ("BACKEND PROXY", "Payment secrets route through backend API proxies."),
                ("HIDE API KEYS", "Stops automated static decompilation tools.")
            ],
            "code": """extern "C" JNIEXPORT jstring JNICALL
Java_com_app_Keys_getApiKey(JNIEnv* env, jobject thiz) {
    if (!verifyAppSignature(env, thiz)) return env->NewStringUTF("");
    const char obs[] = { 0x5A, 0x1F, 0x3C };
    return env->NewStringUTF(decode(obs));
}""",
            "metric": "Protected critical infrastructure API keys from static decompilation."
        },
        {
            "id": "q82",
            "title": "10. How do you audit Third-Party SDKs for Privacy Sandbox and Data Safety compliance?",
            "problem": "Unvetted SDKs collecting device IDs trigger immediate Google Play policy bans.",
            "solution": [
                ("DATA SAFETY AUDIT", "I audit SDKs for collected data."),
                ("PRIVACY SANDBOX", "Privacy Sandbox isolates third-party SDK runtimes."),
                ("VULNERABILITY SCAN", "OWASP and Snyk audit dependencies in CI."),
                ("REMOVE PERMISSIONS", "tools:node remove strips dangerous merged permissions."),
                ("LEAST PRIVILEGE", "Rejects SDKs requesting broad unwarranted system permissions."),
                ("PLAY COMPLIANCE", "Keeps Google Play Data Safety clean.")
            ],
            "code": """<manifest xmlns:tools="http://schemas.android.com/tools">
    <uses-permission android:name="android.permission.READ_PHONE_STATE" tools:node="remove" />
</manifest>""",
            "metric": "Maintained 100% clean Google Play Data Safety compliance across 20+ SDKs."
        },
        {
            "id": "q83",
            "title": "11. How do you implement Cryptographic Secure Shredding of memory and files?",
            "problem": "Garbage-collected JVM Strings linger in memory, allowing RAM dump exploits.",
            "solution": [
                ("CHAR ARRAYS", "Passwords store in CharArray instead String."),
                ("ARRAYS FILL ZERO", "Arrays.fill zeroes sensitive bytes after use."),
                ("SHRED FILES", "Temporary files overwrite with random bytes."),
                ("DIRECT BUFFERS", "Direct ByteBuffers are cleared and zeroed out."),
                ("DELETE ON EXIT", "Deletes temporary cached files after execution finishes."),
                ("ZERO RAM ARTIFACTS", "Leaves zero plaintext secrets in memory.")
            ],
            "code": """fun wipe(chars: CharArray) {
    Arrays.fill(chars, '\u0000')
}
fun shred(file: File) {
    val randomBytes = ByteArray(file.length().toInt()).also { SecureRandom().nextBytes(it) }
    file.writeBytes(randomBytes)
    file.delete()
}""",
            "metric": "Passed Tier-1 banking memory forensic audits with zero residual artifacts."
        },
        {
            "id": "q84",
            "title": "12. How do you implement Network Security Config with Cleartext Traffic bans?",
            "problem": "Accidental cleartext HTTP traffic allows sniffing of user session tokens.",
            "solution": [
                ("BAN CLEARTEXT", "cleartextTrafficPermitted false blocks plain HTTP."),
                ("SYSTEM CA ONLY", "Trusts only system certificates, ignoring users."),
                ("DOMAIN PINNING", "Enforces strict TLS 1.3 on production domains."),
                ("DEBUG OVERRIDES", "debug-overrides config allows Charles Proxy safely."),
                ("SOCKET VERIFY", "OkHttp rejects non-HTTPS socket connections before sending."),
                ("ENFORCE HTTPS", "Forces 100% encrypted HTTPS network traffic.")
            ],
            "code": """<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors><certificates src="system" /></trust-anchors>
    </base-config>
    <debug-overrides>
        <trust-anchors><certificates src="user" /></trust-anchors>
    </debug-overrides>
</network-security-config>""",
            "metric": "Blocked 100% of accidental plaintext HTTP transmissions across all modules."
        }
    ]
}

m8 = {
    "id": "module-8",
    "title": "Module 8: Staff Engineering, Code Reviews & STAR Scenarios",
    "badge": "Blue",
    "color": "blue",
    "summary": "ADRs, CI/CD Review Rigor, Mentorship, Tech Debt Alignment, 6 Concrete STAR Scenarios across Production Crises.",
    "questions": [
        {
            "id": "q85",
            "title": "1. What is your architectural philosophy and code review rigor as a Staff Engineer?",
            "problem": "Lax code reviews create tech debt, performance regressions, and architectural drift.",
            "solution": [
                ("ADR DOCUMENTS", "I author Architectural Decision Records first."),
                ("AUTOMATED GATES", "CI automates lint and test checks."),
                ("FOCUS ON BOUNDARIES", "Code reviews focus on system architecture."),
                ("THREAD SAFETY", "Reviews evaluate thread safety and lifecycle scoping."),
                ("MEASURE IMPACT", "Evaluates proposals through customer impact and reliability."),
                ("LEAD BY EXAMPLE", "Mentors engineers through pairing and feedback.")
            ],
            "code": """# Architectural Decision Record (ADR-042)
## Decision: Adopt MediaPipe LLM on mobile.
## Context: Cloud API latency is 1.4s.
## Consequences: 180ms time-to-first-token, zero cloud API cost.""",
            "metric": "Mentored 14 engineers to promotions and increased team velocity by 35%."
        },
        {
            "id": "q86",
            "title": "2. How do you balance Tech Debt vs Feature Delivery when negotiating with Product?",
            "problem": "Product roadmaps prioritize short-term features until development velocity collapses.",
            "solution": [
                ("QUANTIFY COSTS", "I translate tech debt to revenue."),
                ("TWENTY PERCENT RULE", "I allocate 20% bandwidth to refactoring."),
                ("SCOUT RULE", "Engineers leave touched code cleaner daily."),
                ("BUNDLE REFACTORS", "Bundles architectural refactors into strategic product milestones."),
                ("HEALTH DASHBOARD", "Presents engineering health dashboards to product leadership."),
                ("FASTER DELIVERY", "Doubles feature delivery speed after refactors.")
            ],
            "code": """// Business Impact Formula
Business_Gain = (Crash_Reduction * Active_Users * LTV) - Refactor_Cost""",
            "metric": "Negotiated a 4-month modularization that doubled quarterly feature velocity."
        },
        {
            "id": "q87",
            "title": "3. STAR 1: Resolving a Critical Production CameraX Memory Leak Crisis",
            "problem": "STAR Scenario: CameraX memory leaks crashed 4.2% of sessions during Black Friday launch.",
            "solution": [
                ("SITUATION PRODUCTION OUTAGE", "Situation: 4.2% OOM crashes in CameraX."),
                ("TASK ROOT CAUSE", "Task: Deploy a zero-crash emergency hotfix."),
                ("ACTION PROFILER FORENSICS", "Action: Captured heap dumps using Android Studio."),
                ("ACTION FIX IMAGEPROXY", "Action: Profiler identified unclosed ImageProxy buffers."),
                ("ACTION SERIAL QUEUE", "Action: Added try-finally close inside serial queue."),
                ("RESULT 99.9 CRASH FREE", "Result: Crash rate dropped to 0.02%.")
            ],
            "code": """imageAnalysis.setAnalyzer(executor) { proxy ->
    try {
        processFrame(proxy)
    } finally {
        proxy.close() // Hardware buffer release
    }
}""",
            "metric": "Recovered 99.91% crash-free session rate, saving $1.2M in Black Friday sales."
        },
        {
            "id": "q88",
            "title": "4. STAR 2: Leading Multi-Module Jetpack Compose Migration for 50 Engineers",
            "problem": "STAR Scenario: Monolithic XML codebase caused 22-minute build times and blocked 50 devs.",
            "solution": [
                ("SITUATION MONOLITH BOTTLENECK", "Situation: 22-minute builds blocked 50 engineers."),
                ("TASK MODULAR ROADMAP", "Task: Architect 35-module Clean Jetpack Compose."),
                ("ACTION DESIGN TOKENS", "Action: Created shared Material 3 tokens."),
                ("ACTION COMPILER METRICS", "Action: Added compiler metrics in CI pipelines."),
                ("ACTION INTEROP GUIDELINES", "Action: Created Compose-in-XML interoperability patterns for teams."),
                ("RESULT 3 MINUTE BUILDS", "Result: Build times dropped to 3.5m.")
            ],
            "code": """// Multi-Module Architecture
// :core:designsystem (Material 3 tokens)
// :feature:catalog:ui (Jetpack Compose)
// :feature:legacy:cart (Compose in XML)""",
            "metric": "Reduced clean build times by 84% and onboarded 50 engineers in 90 days."
        },
        {
            "id": "q89",
            "title": "5. STAR 3: Eradicating a 0.85% Google Play Bad Behavior ANR Rate",
            "problem": "STAR Scenario: App exceeded Google Play ANR threshold (0.47%), risking search demotion.",
            "solution": [
                ("SITUATION ANR WARNING", "Situation: 0.85% ANRs from disk SharedPreferences."),
                ("TASK LOWER ANR RATE", "Task: Reduce ANR rate below 0.10%."),
                ("ACTION STRICTMODE PROFILING", "Action: StrictMode isolated synchronous main-thread disk writes."),
                ("ACTION DATASTORE COROUTINES", "Action: Migrated SharedPreferences to background DataStore."),
                ("ACTION DISPATCHERS IO", "Action: Offloaded database writes to Dispatchers.IO threads."),
                ("RESULT 0.03 ANR RECORD", "Result: ANR rate dropped to 0.03%.")
            ],
            "code": """StrictMode.setThreadPolicy(
    StrictMode.ThreadPolicy.Builder().detectDiskReads().detectDiskWrites().penaltyLog().build()
)""",
            "metric": "Cut ANRs by 96%, removing all Google Play bad behavior warnings."
        },
        {
            "id": "q90",
            "title": "6. STAR 4: Stabilizing Flaky CI Test Suite from 32% Failure Rate to 0.5%",
            "problem": "STAR Scenario: Flaky tests failed 32% of CI builds, wasting 60 engineering hours weekly.",
            "solution": [
                ("SITUATION FLAKY BUILDS", "Situation: 32% CI builds failed randomly."),
                ("TASK ZERO FLAKINESS", "Task: Achieve under 1% CI flakiness."),
                ("ACTION REMOVE SLEEPS", "Action: Removed all Thread.sleep calls from tests."),
                ("ACTION TURBINE TESTING", "Action: Replaced Thread.sleep with Turbine flows."),
                ("ACTION VIRTUAL CLOCK", "Action: StandardTestDispatcher controls virtual coroutine execution time."),
                ("RESULT SUB 1 PERCENT", "Result: CI flakiness dropped to 0.4%.")
            ],
            "code": """@Test
fun testSearch() = runTest {
    vm.results.test {
        assertEquals(UiState.Idle, awaitItem())
        vm.onQuery("glasses")
        advanceTimeBy(300L)
        assertTrue(awaitItem() is UiState.Success)
    }
}""",
            "metric": "Saved 60+ engineering hours weekly and cut CI test run time to 3.8m."
        },
        {
            "id": "q91",
            "title": "7. STAR 5: Rapid Response and Mitigation of a Zero-Day Security Vulnerability",
            "problem": "STAR Scenario: External audit discovered an exported ContentProvider exposing customer orders.",
            "solution": [
                ("SITUATION EXPOSED DATA", "Situation: Vulnerability found in legacy ContentProvider."),
                ("TASK 12 HOUR FIX", "Task: Secure the attack surface immediately."),
                ("ACTION EXPORTED FALSE", "Action: Set android:exported false and signature."),
                ("ACTION IPC LINT", "Action: Added static lint check in CI."),
                ("ACTION AUDIT ALL", "Action: Audited all AndroidManifest components across modules."),
                ("RESULT ZERO LEAKS", "Result: Released hotfix with zero leaks.")
            ],
            "code": """<provider
    android:name=".OrderProvider"
    android:authorities="com.app.orders"
    android:exported="false"
    android:permission="com.app.INTERNAL_DATA" />""",
            "metric": "Patched 100% of IPC attack surfaces and passed SOC2 audit."
        },
        {
            "id": "q92",
            "title": "8. STAR 6: Designing High-Volume Flash Sale Resiliency for 100k Concurrent Users",
            "problem": "STAR Scenario: Flash sale 10x traffic spike caused 504 gateway timeouts across checkout.",
            "solution": [
                ("SITUATION TRAFFIC SPIKE", "Situation: 10x spike overwhelmed checkout servers."),
                ("TASK CLIENT RESILIENCY", "Task: Implement circuit breaking and queues."),
                ("ACTION RETRY JITTER", "Action: Built Circuit Breaker with jitter."),
                ("ACTION WAITING ROOM", "Action: Polled waiting room UI using WebSockets."),
                ("ACTION LOCAL RESERVATION", "Action: Cached cart reservations locally in Room."),
                ("RESULT ZERO CRASHES", "Result: Handled 120,000 sessions with 0 crashes.")
            ],
            "code": """val backoffMs = minOf(10000L, baseMs * 2.0.pow(retries).toLong()) + Random.nextLong(0, 500)""",
            "metric": "Handled 120,000 concurrent checkouts with 99.95% transactional success rate."
        },
        {
            "id": "q93",
            "title": "9. How do you cultivate an Engineering Culture of High Standards and Learning?",
            "problem": "Siloed feature teams create duplicate code, technical drift, and declining rigor.",
            "solution": [
                ("TECH TALKS", "I organize bi-weekly Android guild talks."),
                ("ARCHITECTURE GUILD", "Architecture guild reviews major ADR proposals."),
                ("OPEN SOURCE", "Encourages open source contributions to Android libraries."),
                ("BLAMELESS REVIEWS", "Blameless postmortems focus on root causes."),
                ("INTERNAL LABS", "Authors interactive internal Codelabs for fast onboarding."),
                ("HIGH HAPPINESS", "Increases team engineering satisfaction and velocity.")
            ],
            "code": """detekt {
    buildUponDefaultConfig = true
    config = files("$rootDir/config/detekt/detekt.yml")
}""",
            "metric": "Boosted team engineering happiness to 92% and cut onboarding time in half."
        },
        {
            "id": "q94",
            "title": "10. How do you architect Feature Flagging and Dynamic Configuration at Scale?",
            "problem": "Hardcoded logic requires full APK releases to toggle experiments, increasing blast radius.",
            "solution": [
                ("COMPILED DEFAULTS", "Feature flags have safe default values."),
                ("REMOTE CONFIG", "Firebase Remote Config updates flags dynamically."),
                ("RETIRE DEAD FLAGS", "Removes dead flags within 30 days."),
                ("USER TARGETING", "Runs A/B experiments segmented by country cohort."),
                ("KILL SWITCHES", "Remote kill switches disable bad features."),
                ("SAFE LAUNCHES", "Reduces blast radius during major feature rollouts.")
            ],
            "code": """class FlagManager(private val config: FirebaseRemoteConfig) {
    fun isAiEnabled(): Boolean = config.getBoolean("feature_ai_enabled")
}""",
            "metric": "Safely launched 80+ experiments annually with zero production rollbacks."
        },
        {
            "id": "q95",
            "title": "11. How do you design an Enterprise Mobile Observability and Logging Pipeline?",
            "problem": "Unstructured logs get lost; excessive telemetry spams backend and drains user data.",
            "solution": [
                ("STRUCTURED SCHEMA", "Protobuf schemas define structured event payloads."),
                ("IN-MEMORY BUFFER", "Ring-buffer stores 50 diagnostic crash breadcrumbs."),
                ("SAMPLING CONTROLS", "Dynamic sampling rates control high frequency telemetry."),
                ("PII SCRUBBING", "Regex sanitizes emails and auth tokens."),
                ("BATCH UPLOADS", "WorkManager uploads compressed telemetry on Wi-Fi."),
                ("LOW DATA IMPACT", "Transmits under 1.5MB analytics data daily.")
            ],
            "code": """class SecureLogTree : Timber.Tree() {
    override fun log(p: Int, tag: String?, msg: String, t: Throwable?) {
        val clean = PiiScrubber.mask(msg)
        BreadcrumbBuffer.add(p, tag, clean)
    }
}""",
            "metric": "Processed 100M+ daily analytical events with zero PII leaks."
        },
        {
            "id": "q96",
            "title": "12. How do you handle Cross-Functional Technical Conflict with Backend and Product?",
            "problem": "Disagreements over API payloads, pagination, and release timelines stall projects.",
            "solution": [
                ("CONTRACT FIRST", "OpenAPI specifications agree on contracts first."),
                ("SHARED PROTOBUF", "Protocol Buffers generate client and server models."),
                ("DATA DRIVEN", "Benchmarks and metrics resolve debates objectively."),
                ("EMPATHETIC LISTENING", "Listens to backend database indexing constraints."),
                ("ESCALATION MATRICES", "Clear risk-benefit matrices resolve deadlocked product trade-offs."),
                ("ON TIME DELIVERY", "Keeps cross-functional projects on agreed schedule.")
            ],
            "code": """// OpenAPI Contract Spec agreed prior to coding
openapi: 3.0.0
paths:
  /v1/products:
    get:
      parameters: [{ name: cursor, in: query, schema: { type: string } }]""",
            "metric": "Reduced cross-functional API integration blockers by 70%."
        }
    ]
}

m9 = {
    "id": "module-9",
    "title": "Module 9: AI Strategy, On-Device LLM & CLI Tooling",
    "badge": "Violet",
    "color": "violet",
    "summary": "Hybrid Edge vs Cloud Routing, Gemini Nano AICore, MediaPipe Gemma INT4, Streaming Tokens, Vector DBs, LiteRT CLI Model Choice.",
    "questions": [
        {
            "id": "q97",
            "title": "1. How do you architect a Hybrid Edge vs Cloud AI routing strategy?",
            "problem": "Cloud-only AI incurs high 1.5s latency and cost; edge-only lacks big parameter reasoning.",
            "solution": [
                ("SMART ROUTER", "Routes private tasks to on-device models."),
                ("CLOUD FOR DEEP", "Gemini 1.5 Pro handles complex analysis."),
                ("SUB-200MS SPEED", "Edge delivers instant 180ms responses locally."),
                ("OFFLINE PRIVACY", "Processes user data with zero transmission."),
                ("AUTO FALLBACK", "Falls back to cloud if NPU unavailable."),
                ("ZERO API COST", "Cuts cloud API spend by thousands monthly.")
            ],
            "code": """class AiRouter(private val local: OnDeviceLlm, private val cloud: GeminiApi) {
    suspend fun query(prompt: String, isComplex: Boolean): Flow<String> {
        return if (!isComplex && local.isAvailable()) local.stream(prompt)
        else cloud.stream(prompt)
    }
}""",
            "metric": "Saved $140,000 annually in cloud API costs while reducing p50 latency to 180ms."
        },
        {
            "id": "q98",
            "title": "2. How do you integrate Android AICore and Gemini Nano for system on-device intelligence?",
            "problem": "Bundling large LLM weights inside APKs adds 1.5GB+, causing user uninstalls.",
            "solution": [
                ("SYSTEM AICORE", "Android AICore system service provides Nano."),
                ("ZERO APK OVERHEAD", "OS manages weights, adding zero megabytes."),
                ("NPU ACCELERATED", "Inference runs directly on device NPUs."),
                ("FAST SUMMARIES", "Generates high-speed text summaries and replies."),
                ("OS UPDATES", "Google Play System updates maintain foundation models."),
                ("ON-DEVICE AI", "Runs foundation intelligence directly on modern Android.")
            ],
            "code": """val model = GenerativeModel(
    modelName = "gemini-nano",
    apiKey = "" // System AICore needs no API key
)
val res = model.generateContent("Summarize notes: $notes")""",
            "metric": "Enabled zero-size on-device generative AI across millions of Android phones."
        },
        {
            "id": "q99",
            "title": "3. How do you implement MediaPipe LLM Inference Engine with Gemma-2B INT4?",
            "problem": "Running raw open-weight LLMs on mobile CPUs causes throttling and 3s delays.",
            "solution": [
                ("MEDIAPIPE LLM", "MediaPipe LlmInference runs models on GPU."),
                ("GEMMA 2B INT4", "Gemma-2B INT4 weights optimize for mobile."),
                ("DYNAMIC FEATURE", "Downloads the 1.2GB model binary dynamically."),
                ("HYPERPARAMETERS", "Configures temperature 0.7 and topK 40 safely."),
                ("GPU DELEGATE", "Binds inference execution to mobile GPU backends."),
                ("14 TOKENS PER SEC", "Generates 14 tokens per second.")
            ],
            "code": """val options = LlmInference.LlmInferenceOptions.builder()
    .setModelPath("/data/local/tmp/gemma-2b-int4.bin")
    .setMaxTokens(512)
    .setTemperature(0.7f)
    .build()
val llm = LlmInference.createFromOptions(context, options)
val text = llm.generateResponse("Suggest frames for round face:")""",
            "metric": "Achieved 14 tokens per second streaming speed on Snapdragon hardware."
        },
        {
            "id": "q100",
            "title": "4. How do you architect Streaming Token Generation directly into Compose UI?",
            "problem": "Waiting for complete LLM responses causes a 5-second blank screen freeze.",
            "solution": [
                ("FLOW STREAMING", "Repository emits incremental Coroutine Flow tokens."),
                ("STATEFLOW REDUCTION", "ViewModel accumulates streaming text into StateFlow."),
                ("AUTO SCROLL LIST", "LazyColumn automatically scrolls on new tokens."),
                ("COROUTINE CANCEL", "Cancelling collection coroutine interrupts native NPU inference."),
                ("SMOOTH CHAT", "Delivers responsive ChatGPT-like mobile UI experience."),
                ("100MS FIRST TOKEN", "Renders initial words in 100ms.")
            ],
            "code": """fun streamPrompt(prompt: String): Flow<String> = callbackFlow {
    llm.generateResponseAsync(prompt) { chunk, isDone ->
        trySend(chunk)
        if (isDone) close()
    }
    awaitClose { /* Cancel native handle */ }
}""",
            "metric": "Cut perceived latency from 4.8s down to 95ms Time-To-First-Token."
        },
        {
            "id": "q101",
            "title": "5. How do you implement Structured JSON Output and Function Calling on Mobile?",
            "problem": "Hallucinated free-text output breaks mobile app parsing and SQL queries.",
            "solution": [
                ("TOOL DEFINITIONS", "Defines tool specs with JSON schemas."),
                ("GRAMMAR DECODING", "Grammar decoding forces valid JSON format."),
                ("DISPATCH TOOL", "App executes local Kotlin function calls."),
                ("CONTEXT FEEDBACK", "Feeds function results back into conversation context."),
                ("KOTLINX SAFETY", "Kotlinx.serialization parses structured tool response objects."),
                ("ZERO HALLUCINATIONS", "Guarantees valid JSON responses for logic.")
            ],
            "code": """val tool = Tool(listOf(FunctionDeclaration("bookVisit", "Book frame fitting", schema)))
if (response.hasFunctionCall()) {
    val args = response.getFunctionCall().args
    appointmentManager.book(args["storeId"], args["date"])
}""",
            "metric": "Achieved 100% syntactically valid JSON extraction with zero hallucinations."
        },
        {
            "id": "q102",
            "title": "6. How do you build an On-Device Mobile RAG (Retrieval-Augmented Generation) Pipeline?",
            "problem": "On-device models have small context windows and lack private enterprise data.",
            "solution": [
                ("MOBILEBERT EMBED", "TFLite MobileBERT generates vector embeddings locally."),
                ("VECTOR DATABASE", "ObjectBox Vector indexes document chunks locally."),
                ("COSINE SEARCH", "Retrieves top-3 relevant chunks via cosine."),
                ("AUGMENT PROMPT", "Injects retrieved chunks into system prompt context."),
                ("OFFLINE PRIVACY", "Entire semantic search executes without internet access."),
                ("GROUNDED ANSWERS", "Augments prompt context for accurate answers.")
            ],
            "code": """val queryVec = embeddingModel.embed(userQuery)
val chunks = vectorDb.findNearest(queryVec, limit = 3)
val prompt = "Context: ${chunks.joinToString()}\nQuestion: $userQuery"
val answer = localLlm.generate(prompt)""",
            "metric": "Reduced LLM hallucination rate to 0.2% with instant offline search."
        },
        {
            "id": "q103",
            "title": "7. How do you select mobile AI models using LiteRT Benchmark CLI tool?",
            "problem": "Choosing models without physical device profiling causes RAM overflows and overheating.",
            "solution": [
                ("LITERT BENCHMARK", "benchmark_model CLI runs via ADB shell."),
                ("MEASURE LATENCY", "Measures warmup time and memory footprint."),
                ("TEST DELEGATES", "Benchmarks GPU, NNAPI, and XNNPACK backends."),
                ("SELECTION MATRIX", "Evaluates latency versus accuracy trade-offs across models."),
                ("CI BENCHMARK GATES", "Automated device farm benchmarks gate model PRs."),
                ("OPTIMAL MODEL", "Selects optimal quantized model fitting memory.")
            ],
            "code": """adb push model_int8.tflite /data/local/tmp/
adb shell /data/local/tmp/benchmark_model \
  --graph=/data/local/tmp/model_int8.tflite \
  --use_gpu=true \
  --num_threads=4 \
  --num_runs=50""",
            "metric": "Selected optimal 1.8-bit quantized model running in 18ms within 120MB RAM."
        },
        {
            "id": "q104",
            "title": "8. What are the trade-offs between INT4, INT8, and FP16 Quantization on Mobile?",
            "problem": "Wrong quantization precision breaks conversational fluency or overflows phone RAM.",
            "solution": [
                ("FP16 ACCURACY", "FP16 gives accuracy but needs 4GB."),
                ("INT8 FOR VISION", "INT8 gives 4x size reduction."),
                ("INT4 FOR SLMS", "INT4 shrinks 2B LLMs to 1.1GB."),
                ("NPU ACCELERATION", "Mobile NPUs accelerate INT4 and INT8."),
                ("AWQ ALGORITHMS", "Activation-aware quantization preserves complex language reasoning."),
                ("FIT MOBILE RAM", "Fits 2B models into standard 6GB phones.")
            ],
            "code": """// Model Matrix
// FP16: 4.2 GB RAM | 100% Accuracy | 4 tokens/s
// INT8: 2.1 GB RAM | 99.2% Accuracy | 9 tokens/s
// INT4: 1.1 GB RAM | 97.5% Accuracy | 16 tokens/s (Selected Standard)""",
            "metric": "Fit 2-billion parameter model into standard 6GB RAM phone at 16 tokens/sec."
        },
        {
            "id": "q105",
            "title": "9. How do you manage Context Window Token Budgets and KV Cache on mobile?",
            "problem": "Long chat histories exceed 2048-token context windows, crashing mobile memory.",
            "solution": [
                ("TOKEN BUDGETS", "Allocates 300 system and 1200 history."),
                ("REUSE KV CACHE", "Retains Key-Value cache across conversation turns."),
                ("SLIDING SUMMARY", "Oldest conversation turns summarize into bullets."),
                ("BPE TOKENIZER", "Local Byte-Pair Encoding counts prompt tokens accurately."),
                ("OUTPUT BUFFER", "Reserves 548 tokens for model output buffer."),
                ("PREVENT CRASHES", "Stops out-of-memory native allocation faults.")
            ],
            "code": """class ContextManager(private val maxTokens: Int = 1200) {
    fun prune(msgs: List<Message>): List<Message> {
        var count = 0
        return msgs.reversed().takeWhile { 
            count += tokenizer.count(it.text)
            count <= maxTokens 
        }.reversed()
    }
}""",
            "metric": "Maintained multi-turn chat sessions spanning 50+ messages with 90MB KV cache."
        },
        {
            "id": "q106",
            "title": "10. How do you implement AI Guardrails, Content Safety, and PII Sanitization?",
            "problem": "Unfiltered generative AI outputs risk exposing toxic text or user PII.",
            "solution": [
                ("INPUT SANITIZER", "Regex strips potential prompt injection patterns."),
                ("PII MASKING", "Parsers mask credit cards and emails."),
                ("SAFETY MODEL", "On-device 5MB classifier checks safety scores."),
                ("CONFIDENCE CHECKS", "Safety threshold checks trigger safe response replacements."),
                ("AUDIT LOGGING", "Safety events log anonymously to monitor attacks."),
                ("SAFE FALLBACKS", "Replaces toxic responses with safe fallbacks.")
            ],
            "code": """fun applyGuardrails(input: String): String {
    val clean = PiiMasker.mask(input)
    if (InjectionDetector.isSuspicious(clean)) {
        throw SecurityException("Invalid prompt pattern")
    }
    return clean
}""",
            "metric": "Blocked 100% of prompt injection attacks and prevented PII leakage."
        },
        {
            "id": "q107",
            "title": "11. How do you govern Battery, Thermal, and Cost metrics for Mobile AI Features?",
            "problem": "Continuous background AI tasks drain battery, causing negative app reviews.",
            "solution": [
                ("BATTERY CHECKS", "Disables generation when battery drops below 20%."),
                ("THERMAL THROTTLING", "Throttles token generation when phone heats."),
                ("COST CEILINGS", "User token usage caps prevent cloud overuse."),
                ("WORKMANAGER RULES", "Background embedding runs only while charging."),
                ("POWER HISTORIAN", "Profiles energy impact with Android Battery Historian."),
                ("SAVE BATTERY", "Keeps 24-hour AI battery under 2.2%.")
            ],
            "code": """val constraints = Constraints.Builder()
    .setRequiresCharging(true)
    .setRequiresBatteryNotLow(true)
    .setRequiredNetworkType(NetworkType.UNMETERED)
    .build()""",
            "metric": "Kept 24-hour mobile AI assistant battery consumption below 2.2% of total battery."
        },
        {
            "id": "q108",
            "title": "12. How do you build Autonomous Mobile Agent Workflows with WorkManager & Local AI?",
            "problem": "Multi-step background tasks (fetch data, summarize, notify) fail if process dies.",
            "solution": [
                ("WORKMANAGER CHAIN", "Chained OneTimeWorkRequests orchestrate sequential autonomous steps."),
                ("COROUTINE INFERENCE", "Workers execute fetch, embedding, and summarization."),
                ("ROOM PERSISTENCE", "Intermediate step outputs save into Room."),
                ("LOCAL NOTIFICATIONS", "Interactive Android notification posts completed agent output."),
                ("EXPEDITED JOBS", "Urgent tasks use Expedited WorkManager execution quotas."),
                ("AUTOMATE TASKS", "Delivers daily briefings with zero intervention.")
            ],
            "code": """WorkManager.getInstance(context)
    .beginWith(OneTimeWorkRequestBuilder<FetchWorker>().build())
    .then(OneTimeWorkRequestBuilder<EmbeddingWorker>().build())
    .then(OneTimeWorkRequestBuilder<SummarizeWorker>().build())
    .then(OneTimeWorkRequestBuilder<NotifyWorker>().build())
    .enqueue()""",
            "metric": "Automated 100% of daily field worker briefing generation with zero manual input."
        }
    ]
}

print("Part 3 (6 points): Modules 7, 8, 9 compiled.")
