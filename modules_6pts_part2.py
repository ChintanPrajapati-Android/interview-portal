# Modules 4, 5, 6 - Exactly 6 bullets per question, strictly 5-7 words per bullet

m4 = {
    "id": "module-4",
    "title": "Module 4: GPS Tracking, Battery & Background Architecture",
    "badge": "Amber",
    "color": "amber",
    "summary": "Activity Recognition Transition API, 40-60% Battery Cut, FusedLocation, Android 14 FGS, 100k Geofences.",
    "questions": [
        {
            "id": "q37",
            "title": "1. How do you reduce GPS battery consumption by 40-60% using Activity Recognition?",
            "problem": "Continuous high-accuracy GPS polling drains 15-20% battery per hour, killing the phone.",
            "solution": [
                ("ACTIVITY TRANSITION", "ActivityTransitionRequest detects when user is STILL."),
                ("PAUSE GPS", "I pause GPS polling while stationary."),
                ("HIGH ACCURACY", "Vehicle movement switches to fast GPS."),
                ("DISPLACEMENT FILTER", "setMinUpdateDistanceMeters ignores small micro jitter moves."),
                ("BATCH DELIVERIES", "setMaxUpdateDelayMillis batches location updates efficiently."),
                ("SAVE BATTERY", "Cuts battery drain by over 50%.")
            ],
            "code": """val request = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 5000L)
    .setMinUpdateDistanceMeters(25f)
    .setMaxUpdateDelayMillis(30000L)
    .build()""",
            "metric": "Cut continuous tracking battery consumption by 54% in Trakzee/MobiGPS."
        },
        {
            "id": "q38",
            "title": "2. How do you architect Foreground Services for Android 14 (API 34) compliance?",
            "problem": "Android 14 crashes services if foregroundServiceType or runtime permissions are missing.",
            "solution": [
                ("SERVICE TYPES", "AndroidManifest declares explicit foregroundServiceType for location."),
                ("RUNTIME PERMISSION", "FOREGROUND_SERVICE_LOCATION permission is requested in code."),
                ("START COMPAT", "ServiceCompat.startForeground passes matching service type."),
                ("USER NOTIFICATION", "Posts persistent notification with action buttons."),
                ("SHORT SERVICE", "shortService type handles quick background syncs."),
                ("PREVENT CRASHES", "Stops ForegroundServiceStartNotAllowedException on Android 14.")
            ],
            "code": """ServiceCompat.startForeground(
    this, NOTIFICATION_ID, notification,
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        ServiceInfo.FOREGROUND_SERVICE_TYPE_LOCATION
    } else 0
)""",
            "metric": "Achieved 100% Android 14 compliance with zero background crashes."
        },
        {
            "id": "q39",
            "title": "3. How do you scale to 100,000+ Geofences on mobile without hitting OS limits?",
            "problem": "Android hard-limits apps to 100 registered Geofences, blocking nation-wide geofencing.",
            "solution": [
                ("SQLITE R-TREE", "SQLite R-Tree stores 100,000 geofences locally."),
                ("SPATIAL QUERY", "Queries find the 50 closest geofences."),
                ("DYNAMIC SWAP", "GeofencingClient registers only active nearby fences."),
                ("BOUNDARY BUFFERS", "Calculates distance thresholds for next query."),
                ("WORKMANAGER RECEIVER", "BroadcastReceiver triggers background geofence processing workers."),
                ("NO LIMITS", "Bypasses the OS 100 geofence limit.")
            ],
            "code": """val nearest = geofenceDao.findNearest(userLat, userLng, limit = 50)
geofencingClient.addGeofences(buildRequest(nearest), pendingIntent)""",
            "metric": "Supported 150,000 enterprise merchant geofences with zero OS errors."
        },
        {
            "id": "q40",
            "title": "4. How do you survive Doze Mode and App Standby Buckets for time-critical alerts?",
            "problem": "Doze Mode blocks network and sleeps alarms when the device is idle.",
            "solution": [
                ("HIGH PRIORITY FCM", "High-Priority FCM push wakes the phone."),
                ("EXACT ALARM", "setExactAndAllowWhileIdle triggers critical wakeups on time."),
                ("EXPEDITED WORK", "WorkManager runs urgent tasks with setExpedited."),
                ("STANDBY BUCKETS", "Logic tolerates restricted and rare bucket modes."),
                ("BATTERY PROMPT", "Guides field workers to disable battery optimization."),
                ("TIMELY ALERTS", "Delivers 99.8% of critical emergency alerts.")
            ],
            "code": """val work = OneTimeWorkRequestBuilder<UrgentWorker>()
    .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
    .build()
WorkManager.getInstance(context).enqueue(work)""",
            "metric": "Delivered 99.8% on-time dispatch alerts during deep overnight Doze mode."
        },
        {
            "id": "q41",
            "title": "5. How do you filter GPS Multipath and Drift in urban canyon environments?",
            "problem": "Tall city buildings reflect GPS signals, causing 100-meter phantom jumps.",
            "solution": [
                ("ACCURACY FILTER", "I discard readings with accuracy above 25m."),
                ("SPEED SANITY", "Rejects delta jumps exceeding vehicle speed."),
                ("KALMAN FUSION", "Kalman filters fuse GPS with accelerometer."),
                ("ROAD SNAPPING", "Map matching snaps coordinates to road networks."),
                ("BEARING SMOOTHING", "Moving average bearing prevents erratic map rotations."),
                ("CLEAN ROUTES", "Eliminates phantom jumps on city maps.")
            ],
            "code": """fun isValid(last: Location?, cur: Location): Boolean {
    if (cur.accuracy > 25f) return false
    if (last == null) return true
    val speedKmh = (last.distanceTo(cur) / ((cur.time - last.time) / 1000f)) * 3.6
    return speedKmh < 180.0
}""",
            "metric": "Eliminated 94% of urban GPS jumps, improving driver ETA accuracy."
        },
        {
            "id": "q42",
            "title": "6. How do you manage Offline GPS Breadcrumb Caching and Batch Uploading?",
            "problem": "Transmitting every GPS ping immediately burns cellular radio power and battery.",
            "solution": [
                ("ROOM BUFFER", "Points save into Room with pending status."),
                ("BATCH TRANSMIT", "Fifty points buffer before turning on radio."),
                ("GZIP COMPRESSION", "GZIP compression cuts payload size by 80%."),
                ("EXPONENTIAL RETRY", "Failed uploads retry with exponential backoff intervals."),
                ("TRANSACTION PRUNING", "Room transactions prune successfully uploaded location records."),
                ("SAVE DATA", "Zero data loss during long tunnel outages.")
            ],
            "code": """@Dao
interface LocationDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBatch(points: List<LocationEntity>)
    
    @Query("SELECT * FROM locations WHERE synced = 0 LIMIT 50")
    suspend fun getPending(): List<LocationEntity>
}""",
            "metric": "Saved 45% mobile data bandwidth and achieved zero data loss in tunnels."
        },
        {
            "id": "q43",
            "title": "7. How do you implement Background Location permissions on Android 10 to 14?",
            "problem": "Requesting Foreground and Background location together triggers instant OS denial.",
            "solution": [
                ("TWO STEP PROMPT", "I request FINE_LOCATION first in UI."),
                ("BACKGROUND PROMPT", "ACCESS_BACKGROUND_LOCATION is requested only after approval."),
                ("EXPLAIN VALUE", "Custom dialog explains why background is needed."),
                ("SETTINGS DIRECT", "Directs users to settings for all-the-time access."),
                ("REVOCATION HANDLING", "Handles user permission revocations without sudden crashes."),
                ("PLAY APPROVAL", "Passes Google Play strict location reviews.")
            ],
            "code": """fun requestStep1() {
    launcher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
}
fun requestStep2() {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        launcher.launch(Manifest.permission.ACCESS_BACKGROUND_LOCATION)
    }
}""",
            "metric": "Achieved 100% Google Play policy approval for background location tracking."
        },
        {
            "id": "q44",
            "title": "8. How do you calculate high-precision Geodesic Distances (Vincenty vs Haversine)?",
            "problem": "Spherical Haversine introduces errors because Earth is an oblate spheroid.",
            "solution": [
                ("WGS84 ELLIPSOID", "Vincenty formula models true oblate Earth shape."),
                ("HIGH PRECISION", "Location.distanceBetween computes accurate WGS-84 distances internally."),
                ("HAVERSINE SPEED", "Haversine is used for fast micro checks."),
                ("TRIP ODOMETER", "Sums point-to-point geodesic deltas for trip totals."),
                ("RADIAL CORRECTION", "Accounts for polar flattening on long routes."),
                ("ACCURATE BILLING", "Guarantees accurate distance for commercial billing.")
            ],
            "code": """fun calculateOdometer(points: List<Location>): Double {
    var total = 0.0
    val res = FloatArray(1)
    for (i in 0 until points.size - 1) {
        Location.distanceBetween(points[i].latitude, points[i].longitude, points[i+1].latitude, points[i+1].longitude, res)
        total += res[0]
    }
    return total
}""",
            "metric": "Delivered 99.9% accurate commercial mileage calculations matching hardware odometers."
        },
        {
            "id": "q45",
            "title": "9. How do you implement Indoor Positioning using WiFi RTT (802.11mc) and Beacons?",
            "problem": "GPS signals are completely blocked indoors inside malls and warehouses.",
            "solution": [
                ("WIFI RTT", "RttManager measures time-of-flight to Access Points."),
                ("BLE TRILATERATION", "BLE beacons provide micro indoor proximity fixes."),
                ("PEDOMETER DEAD RECKONING", "Step counter tracks motion between fixes."),
                ("BAROMETER DELTAS", "Barometer pressure detects elevator and floor changes."),
                ("SMOOTH PATH", "Fuses sensor signals for smooth indoor paths."),
                ("ONE METER ACCURACY", "Delivers one-meter indoor warehouse positioning accuracy.")
            ],
            "code": """val rttRequest = RangingRequest.Builder().apply {
    aps.forEach { addAccessPoint(it) }
}.build()
rttManager.startRanging(rttRequest, executor, object : RangingResultCallback() {
    override fun onRangingResults(res: List<RangingResult>) {
        updateMap(trilaterate(res))
    }
})""",
            "metric": "Achieved 1.5-meter indoor warehouse forklift tracking accuracy."
        },
        {
            "id": "q46",
            "title": "10. How do you audit and prevent WakeLock Leaks that trigger Google Play warnings?",
            "problem": "Unreleased WakeLocks drain battery and trigger Google Play Vitals penalties.",
            "solution": [
                ("TIMEOUT WAKELOCKS", "I set explicit timeouts on acquire calls."),
                ("WORKMANAGER REPLACEMENT", "WorkManager replaces manual WakeLocks where possible."),
                ("TRY FINALLY RELEASE", "I release WakeLocks inside finally blocks."),
                ("CI STATIC AUDITS", "Static lint checks flag unreleased wakelock calls."),
                ("BATTERY HISTORIAN", "Battery Historian profiles bugreports for stuck locks."),
                ("ZERO PLAY WARNINGS", "Eliminates bad behavior battery warnings on Play.")
            ],
            "code": """val lock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "App:Sync")
try {
    lock.acquire(5000L) // 5s safety timeout
    doSync()
} finally {
    if (lock.isHeld) lock.release()
}""",
            "metric": "Maintained zero WakeLock leak alerts across 5M+ active daily installations."
        },
        {
            "id": "q47",
            "title": "11. How do you build an animated vehicle Smooth Marker on Google Maps / Mapbox?",
            "problem": "Raw GPS updates make vehicle marker jump abruptly on maps.",
            "solution": [
                ("VALUEANIMATOR", "ValueAnimator interpolates marker position over 2 seconds."),
                ("SPHERICAL MATH", "Spherical LatLngInterpolator computes smooth geographical arcs."),
                ("ROTATE BEARING", "Rotates car marker along heading smoothly."),
                ("SPLINE SMOOTHING", "Catmull-Rom splines smooth out road curve waypoints."),
                ("LATENCY BUFFER", "One-point latency buffer prevents jerky animation stops."),
                ("60 FPS CAR", "Givers smooth Uber-like 60 FPS car motion.")
            ],
            "code": """val animator = ValueAnimator.ofFloat(0f, 1f).apply {
    duration = 2000L
    addUpdateListener { va ->
        val v = va.animatedFraction
        marker.position = interpolator.interpolate(v, startPos, endPos)
        marker.rotation = computeRotation(v, startRot, endRot)
    }
}
animator.start()""",
            "metric": "Delivered Uber-grade 60 FPS smooth vehicle animation with zero jumping."
        },
        {
            "id": "q48",
            "title": "12. How do you manage Android 14 Exact Alarm scheduling policies?",
            "problem": "Android 14 revokes exact alarms for non-clock apps, throwing SecurityExceptions.",
            "solution": [
                ("CAN SCHEDULE CHECK", "canScheduleExactAlarms checks alarm permission before calling."),
                ("USE EXACT PERMISSION", "USE_EXACT_ALARM is declared for permitted alarm apps."),
                ("INEXACT FALLBACK", "Missing permissions fall back to WorkManager."),
                ("PERMISSION RECEIVER", "BroadcastReceiver detects when permission is granted later."),
                ("SETTINGS INTENT", "ACTION_REQUEST_SCHEDULE_EXACT_ALARM directs users to settings."),
                ("ZERO CRASHES", "Prevents SecurityException crashes on Android 14.")
            ],
            "code": """if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    if (alarmManager.canScheduleExactAlarms()) {
        alarmManager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, time, pi)
    } else {
        context.startActivity(Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM))
    }
}""",
            "metric": "Eliminated 100% of SecurityExceptions on Android 14 devices."
        }
    ]
}

m5 = {
    "id": "module-5",
    "title": "Module 5: Offline Sync, Room & Data Persistence",
    "badge": "Purple",
    "color": "purple",
    "summary": "Room SSOT, Outbox Pattern with pending_mutations, WorkManager Backoff, SQL Migrations, Paging 3 RemoteMediator, SQLCipher.",
    "questions": [
        {
            "id": "q49",
            "title": "1. How do you design an Offline-First Single Source of Truth (SSOT) with Room?",
            "problem": "Fetching directly from network causes blank screens offline and state tearing.",
            "solution": [
                ("ROOM AS SSOT", "UI observes Room database Flow streams exclusively."),
                ("NETWORK INGEST", "Repositories fetch APIs and insert into Room."),
                ("AUTO EMIT", "Room emits fresh lists on database writes."),
                ("TRANSACTIONS", "withTransaction wraps table writes to avoid tearing."),
                ("OFFLINE FIRST", "App works fully without active internet connection."),
                ("INSTANT UI", "Renders cached data instantly with zero lag.")
            ],
            "code": """class ProductRepo(private val api: Api, private val dao: ProductDao, private val db: AppDb) {
    val products = dao.getFlow()

    suspend fun refresh() = withContext(Dispatchers.IO) {
        val remote = api.fetch()
        db.withTransaction {
            dao.clear()
            dao.insert(remote)
        }
    }
}""",
            "metric": "Achieved sub-50ms instant cold-start screen rendering and full offline capability."
        },
        {
            "id": "q50",
            "title": "2. How do you implement the Outbox Pattern with pending_mutations table?",
            "problem": "Offline actions like cart additions are lost if the app process dies.",
            "solution": [
                ("MUTATIONS TABLE", "Room stores actions in pending_mutations table."),
                ("OPTIMISTIC UI", "Local state updates instantly in the UI."),
                ("WORKMANAGER SYNC", "WorkManager uploads pending mutations sequentially."),
                ("EXPONENTIAL BACKOFF", "Retries failed uploads using exponential backoff policies."),
                ("IDEMPOTENCY KEYS", "UUID idempotency keys prevent duplicate backend execution."),
                ("ZERO DATA LOSS", "Guarantees offline user actions never get lost.")
            ],
            "code": """@Entity(tableName = "pending_mutations")
data class Mutation(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val action: String,
    val payload: String,
    val status: String = "PENDING"
)""",
            "metric": "Guaranteed 100% zero data loss for offline actions across 2M+ operations."
        },
        {
            "id": "q51",
            "title": "3. How do you safely execute Room Database Migrations with MigrationTestHelper?",
            "problem": "Unhandled database schema changes crash apps on startup across millions of phones.",
            "solution": [
                ("EXPLICIT SQL", "Explicit Migration objects write table alter statements."),
                ("MIGRATION HELPER", "MigrationTestHelper tests schema parity in CI."),
                ("AUTOMIGRATION SPEC", "AutoMigration handles simple additive column additions safely."),
                ("EXPORT SCHEMAS", "exportSchema true versions database JSON schemas."),
                ("CI VALIDATION", "Automated tests validate all past migrations continuously."),
                ("ZERO MIGRATION BUGS", "Prevents database upgrade startup crashes in production.")
            ],
            "code": """val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE orders ADD COLUMN notes TEXT DEFAULT '' NOT NULL")
    }
}""",
            "metric": "Ran 14 major database migrations across 8M users with 0 crashes."
        },
        {
            "id": "q52",
            "title": "4. How do you implement Paging 3 RemoteMediator with Room and Retrofit?",
            "problem": "Combining local database caching with paginated network feeds causes jumpy scroll bugs.",
            "solution": [
                ("REMOTEMEDIATOR", "RemoteMediator manages network pagination boundary triggers."),
                ("REMOTE KEYS", "RemoteKeys table stores pagination token cursors."),
                ("PAGINGSOURCE", "Room DAO returns PagingSource to UI."),
                ("TRANSACTION CLEARS", "Clears and inserts items inside database transactions."),
                ("VIEWMODEL CACHED", "cachedIn viewModelScope caches paging stream in memory."),
                ("SMOOTH SCROLL", "Delivers infinite scroll with offline database cache.")
            ],
            "code": """@OptIn(ExperimentalPagingApi::class)
class ItemMediator(private val db: AppDb, private val api: Api) : RemoteMediator<Int, Item>() {
    override suspend fun load(type: LoadType, state: PagingState<Int, Item>): MediatorResult {
        val page = getPageKey(type, state) ?: return MediatorResult.Success(true)
        val res = api.fetch(page)
        db.withTransaction { dao.insert(res) }
        return MediatorResult.Success(res.isEmpty())
    }
}""",
            "metric": "Delivered buttery 60 FPS infinite scrolling with complete offline caching."
        },
        {
            "id": "q53",
            "title": "5. How do you encrypt Room Database with SQLCipher on enterprise devices?",
            "problem": "Unencrypted SQLite databases allow attackers to dump customer data and tokens.",
            "solution": [
                ("SQLCIPHER FACTORY", "SupportFactory encrypts SQLite with 256-bit passphrases."),
                ("KEYSTORE STORAGE", "Android KeyStore securely stores the master passphrase."),
                ("IN-MEMORY CLEAR", "Passphrase byte arrays are zeroed after use."),
                ("SECURE HARDWARE", "StrongBox TEE protects the master encryption keys."),
                ("LOW CPU OVERHEAD", "Adds under 3% CPU overhead during queries."),
                ("BANKING SECURITY", "Protects sensitive user data with full encryption.")
            ],
            "code": """val passphrase = KeyStoreHelper.getKey()
val factory = SupportFactory(passphrase)
val db = Room.databaseBuilder(context, AppDb::class.java, "secure.db")
    .openHelperFactory(factory)
    .build()""",
            "metric": "Achieved full HIPAA and banking-grade on-device data compliance."
        },
        {
            "id": "q54",
            "title": "6. How do you resolve Concurrent Write SQLiteDatabaseLockedException?",
            "problem": "Multiple coroutines writing to Room at once crash with DatabaseLockedException.",
            "solution": [
                ("WAL JOURNAL MODE", "setJournalMode WRITE_AHEAD_LOGGING enables concurrent database reads."),
                ("SINGLE WRITER", "Dispatchers.IO limitedParallelism 1 serializes all writes."),
                ("WITH TRANSACTION", "withTransaction groups dependent write operations cleanly."),
                ("BUSY TIMEOUT", "Pragma busy_timeout allows locks to clear safely."),
                ("SUSPEND DAOS", "DAO methods use suspend or return Flow."),
                ("ZERO DB LOCKS", "Eliminates database locked crashes in multi-threaded sync.")
            ],
            "code": """val db = Room.databaseBuilder(context, AppDb::class.java, "app.db")
    .setJournalMode(RoomDatabase.JournalMode.WRITE_AHEAD_LOGGING)
    .build()""",
            "metric": "Reduced SQLite database locked crashes from 0.38% down to 0.00%."
        },
        {
            "id": "q55",
            "title": "7. How do you implement Conflict Resolution (Last-Write-Wins vs Field Merging)?",
            "problem": "Simultaneous offline edits on different phones overwrite each other on server.",
            "solution": [
                ("UTC TIMESTAMPS", "Every record stores client UTC update timestamp."),
                ("FIELD MERGING", "Server merges non-conflicting fields independently."),
                ("LAST WRITE WINS", "Latest timestamp wins for single conflicting fields."),
                ("USER DIFF PROMPTS", "Displays visual diff screens for business documents."),
                ("REVISION VECTORS", "Version sequence numbers detect out-of-order sync packets."),
                ("PRESERVE DATA", "Preserves multi-device data during offline edits.")
            ],
            "code": """data class SyncItem(
    val id: String,
    val value: String,
    val version: Long,
    val updatedAt: Long
)""",
            "metric": "Preserved 99.99% multi-device sync data integrity during offline operations."
        },
        {
            "id": "q56",
            "title": "8. How do you optimize Room Full-Text Search with SQLite FTS4 / FTS5?",
            "problem": "LIKE queries do slow table scans, taking 800ms across 50,000 items.",
            "solution": [
                ("FTS5 TABLE", "@Fts5 creates indexed virtual full-text tables."),
                ("MATCH OPERATOR", "MATCH operator searches prefix tokens in milliseconds."),
                ("UNICODE TOKENIZER", "unicode61 tokenizer supports international search characters."),
                ("AUTO TRIGGERS", "SQLite triggers keep FTS indexes updated automatically."),
                ("FAST PREFIX LOOKUP", "Prefix queries execute without scanning entire tables."),
                ("SUB-10MS SEARCH", "Delivers instant search across 100,000 product rows.")
            ],
            "code": """@Entity(tableName = "products_fts")
@Fts5(contentEntity = ProductEntity::class)
data class ProductFts(val name: String, val desc: String)

@Query("SELECT * FROM products JOIN products_fts ON products.id = products_fts.rowid WHERE products_fts MATCH :q")
fun search(q: String): Flow<List<ProductEntity>>""",
            "metric": "Sped up product catalog search latency from 820ms to 6.4ms."
        },
        {
            "id": "q57",
            "title": "9. How do you implement Database Compaction and Pruning to prevent storage bloat?",
            "problem": "Old cached records bloat SQLite files to multiple gigabytes over time.",
            "solution": [
                ("RETENTION WORKER", "WorkManager deletes synced records older than 30d."),
                ("INCREMENTAL VACUUM", "PRAGMA incremental_vacuum reclaims freed database pages."),
                ("BACKGROUND VACUUM", "VACUUM runs periodically on background IO threads."),
                ("QUOTA CEILING", "Enforces maximum 150MB local disk cache."),
                ("STORAGE TELEMETRY", "Monitors SQLite file size health in analytics."),
                ("SAVE DISK SPACE", "Prevents uninstalls caused by full device storage.")
            ],
            "code": """class CleanupWorker(ctx: Context, p: WorkerParameters) : CoroutineWorker(ctx, p) {
    override suspend fun doWork(): Result {
        db.dao().deleteOld(System.currentTimeMillis() - 30 * 86400000L)
        db.openHelper.writableDatabase.execSQL("PRAGMA incremental_vacuum(50)")
        return Result.success()
    }
}""",
            "metric": "Reduced average app storage footprint by 64%."
        },
        {
            "id": "q58",
            "title": "10. How do you test Room DAOs deterministically with inMemoryDatabaseBuilder?",
            "problem": "Testing database code on disk is slow and pollutes test environments.",
            "solution": [
                ("IN-MEMORY DB", "inMemoryDatabaseBuilder builds test database in RAM."),
                ("ALLOW MAIN THREAD", "allowMainThreadQueries enables fast synchronous test calls."),
                ("TURBINE FLOWS", "CashApp Turbine tests reactive Flow emission streams."),
                ("TEARDOWN CLOSE", "db.close runs in After teardown methods."),
                ("ISOLATED STATE", "Every test method gets clean database state."),
                ("FAST CI RUNS", "Executes 100+ database tests in two seconds.")
            ],
            "code": """@Before
fun setup() {
    db = Room.inMemoryDatabaseBuilder(context, AppDb::class.java).allowMainThreadQueries().build()
    dao = db.productDao()
}
@After fun tearDown() = db.close()""",
            "metric": "Executed 240+ database unit tests in 3.1 seconds in CI with 0 failures."
        },
        {
            "id": "q59",
            "title": "11. How do you implement Two-Way Room TypeConverters with Kotlinx.serialization?",
            "problem": "Complex nested objects and string lists cannot be saved directly in SQLite.",
            "solution": [
                ("TYPECONVERTER", "TypeConverter converts objects to JSON strings."),
                ("KOTLINX JSON", "Json.encodeToString handles serialization to strings."),
                ("PROVIDED CONVERTERS", "ProvidedTypeConverter injects configured Json serializers into Room."),
                ("SAFE FALLBACK", "try-catch provides safe empty list fallback parsing."),
                ("DATABASE BUILDER", "Room database builder registers the custom converters."),
                ("COMPLEX OBJECTS", "Enables storing lists and custom models cleanly.")
            ],
            "code": """@ProvidedTypeConverter
class Converters(private val json: Json) {
    @TypeConverter fun fromList(l: List<String>): String = json.encodeToString(l)
    @TypeConverter fun toList(s: String): List<String> = try { json.decodeFromString(s) } catch (e: Exception) { emptyList() }
}""",
            "metric": "Serialized complex nested metadata structures with zero schema compromises."
        },
        {
            "id": "q60",
            "title": "12. How do you implement atomic multi-table bulk insertion benchmarks in Room?",
            "problem": "Inserting 10,000 records individually takes 25 seconds due to separate transactions.",
            "solution": [
                ("LIST INSERT", "DAO Insert accepts complete List of entities."),
                ("WITH TRANSACTION", "withTransaction wraps batch in single SQLite transaction."),
                ("CHUNK BATCHES", "Large datasets split into 500-item chunks safely."),
                ("PREPARED CACHE", "Room reuses compiled SQLite prepared statements automatically."),
                ("FLASH STORAGE SPEED", "Maximizes sequential write speeds on flash storage."),
                ("FAST SYNC", "Inserts 10,000 items in 360ms.")
            ],
            "code": """suspend fun insertCatalog(items: List<ProductEntity>) = db.withTransaction {
    items.chunked(500).forEach { chunk ->
        productDao.insertAll(chunk)
    }
}""",
            "metric": "Sped up catalog sync from 22.4 seconds to 360 milliseconds (62x boost)."
        }
    ]
}

m6 = {
    "id": "module-6",
    "title": "Module 6: Jetpack Compose & Modern Reactive UI",
    "badge": "Rose",
    "color": "rose",
    "summary": "@Immutable, @Stable, derivedStateOf, PersistentList, Side-Effects Lifecycle, LazyColumn Keys, Compiler Metrics.",
    "questions": [
        {
            "id": "q61",
            "title": "1. How do you eliminate redundant recompositions with @Immutable and @Stable?",
            "problem": "Passing unstable standard Kotlin List causes non-skippable composables and UI lag.",
            "solution": [
                ("IMMUTABLE TAG", "@Immutable promises the Compose compiler stability."),
                ("PERSISTENT LIST", "PersistentList replaces unstable standard Kotlin List."),
                ("COMPILER METRICS", "Compiler metrics verify functions are marked skippable."),
                ("STABLE INTERFACES", "Annotates external domain models with Stable annotations."),
                ("SKIPPABLE UI", "Compose skips rendering when inputs are unchanged."),
                ("STEADY 60 FPS", "Eliminates unnecessary recompositions during fast scrolls.")
            ],
            "code": """@Immutable
data class FeedUiState(
    val items: PersistentList<FeedItem> = persistentListOf(),
    val isLoading: Boolean = false
)""",
            "metric": "Eliminated 86% of unnecessary UI recompositions, achieving 60 FPS."
        },
        {
            "id": "q62",
            "title": "2. When and why must you use derivedStateOf in Jetpack Compose?",
            "problem": "Reading scroll offsets directly inside composables triggers 60 recompositions every second.",
            "solution": [
                ("DERIVED STATE", "derivedStateOf wraps calculations on frequent state."),
                ("FILTER EMISSIONS", "Emits updates only when output boolean changes."),
                ("REMEMBER WRAPPER", "remember caches the calculated derivedStateOf instance safely."),
                ("SCROLL BUTTON", "Controls ScrollToTop button visibility with zero lag."),
                ("NO PIXEL CHURN", "Triggers recomposition only on 0-to-1 threshold transitions."),
                ("ZERO JANK", "Reduces scrolling recompositions from 300 to two.")
            ],
            "code": """val listState = rememberLazyListState()
val showButton by remember {
    derivedStateOf { listState.firstVisibleItemIndex > 5 }
}""",
            "metric": "Reduced LazyList scrolling recomposition count from 340 down to 2 events."
        },
        {
            "id": "q63",
            "title": "3. How do you govern Side-Effects in Compose (LaunchedEffect, DisposableEffect)?",
            "problem": "Launching network or analytics calls directly in Composable bodies causes repeat bugs.",
            "solution": [
                ("LAUNCHED EFFECT", "LaunchedEffect runs coroutines tied to state keys."),
                ("DISPOSABLE EFFECT", "DisposableEffect adds listeners and cleans in onDispose."),
                ("SIDE EFFECT", "SideEffect runs safely after successful composition commits."),
                ("COROUTINE SCOPE", "rememberCoroutineScope launches coroutines from user UI callbacks."),
                ("NO NAKED COROUTINES", "Bans running coroutines directly inside composable bodies."),
                ("ZERO COROUTINE LEAKS", "Prevents duplicate analytics and coroutine leaks.")
            ],
            "code": """DisposableEffect(lifecycleOwner) {
    val obs = LifecycleEventObserver { _, e -> if (e == Lifecycle.Event.ON_RESUME) vm.load() }
    lifecycleOwner.lifecycle.addObserver(obs)
    onDispose { lifecycleOwner.lifecycle.removeObserver(obs) }
}""",
            "metric": "Eliminated 100% of coroutine leaks and duplicate analytics tracking."
        },
        {
            "id": "q64",
            "title": "4. How do you optimize LazyColumn performance with stable keys and contentType?",
            "problem": "LazyColumn without keys loses scroll position; missing contentType breaks recycling.",
            "solution": [
                ("STABLE KEYS", "items key sets unique business ID keys."),
                ("CONTENT TYPE", "contentType reuses matching layout item slots."),
                ("NO INLINE LAMBDAS", "Method references prevent breaking composable equality."),
                ("SUB-COMPOSE REUSE", "Reuses item composition slots without rebuilding layouts."),
                ("PRESERVE SCROLL", "Maintains scroll position during list dynamic insertions."),
                ("FAST FLINGS", "Maintains smooth 120Hz scrolling on feeds.")
            ],
            "code": """LazyColumn(state = listState) {
    items(
        items = feedItems,
        key = { it.id },
        contentType = { it.type }
    ) { item ->
        FeedCard(item)
    }
}""",
            "metric": "Reduced frame drop jank from 18.4% down to 0.6% on feeds."
        },
        {
            "id": "q65",
            "title": "5. How do you implement Type-Safe Navigation in Jetpack Compose 2.8+?",
            "problem": "Legacy string-based routes were error-prone and crashed on argument type mismatch.",
            "solution": [
                ("SERIALIZABLE ROUTES", "Serializable data classes define type-safe navigation destinations."),
                ("NAVHOST COMPOSABLE", "NavHost uses composable route type parameters directly."),
                ("TO ROUTE EXTRACT", "toRoute extracts typed parameters without string parsing."),
                ("DEEP LINK SUPPORT", "Parses incoming deep links into typed models."),
                ("COMPILE SAFETY", "Catches missing navigation parameters during code compilation."),
                ("ZERO ROUTE CRASHES", "Eliminates string route typo bugs for good.")
            ],
            "code": """@Serializable
data class DetailRoute(val id: String)

NavHost(navController, startDestination = HomeRoute) {
    composable<DetailRoute> { backStack ->
        val route: DetailRoute = backStack.toRoute()
        DetailScreen(route.id)
    }
}""",
            "metric": "Eliminated 100% of runtime navigation route typo crashes."
        },
        {
            "id": "q66",
            "title": "6. How do you build a Custom Layout with SubcomposeLayout and Intrinsics?",
            "problem": "Standard Row and Column cannot measure dynamic proportional multi-column headers.",
            "solution": [
                ("SUBCOMPOSE LAYOUT", "SubcomposeLayout measures dynamic dependent UI slots."),
                ("INTRINSIC SIZES", "Intrinsic measurements align multi-column heights equally."),
                ("PLACE RELATIVE", "placeRelative positions child placeables with zero allocations."),
                ("MODIFIER LAYOUT", "Custom Modifier.layout adjusts bounds without extra nesting."),
                ("ZERO FRAME DROPS", "Measurement pass completes within 16 millisecond budget."),
                ("CUSTOM UI", "Builds complex layouts without nested XML views.")
            ],
            "code": """@Composable
fun CustomLayout(modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    Layout(content = content, modifier = modifier) { measurables, constraints ->
        val placeables = measurables.map { it.measure(constraints) }
        layout(constraints.maxWidth, constraints.maxHeight) {
            var y = 0
            placeables.forEach { it.placeRelative(0, y); y += it.height }
        }
    }
}""",
            "metric": "Built complex multi-tier UI layouts with zero dropped frames."
        },
        {
            "id": "q67",
            "title": "7. How do you interpret and optimize Compose Compiler Metrics Reports?",
            "problem": "Invisible performance regressions slip in because developers cannot see unstable composables.",
            "solution": [
                ("COMPILER FLAGS", "Gradle flags export compiler metrics reports automatically."),
                ("SKIPPABLE REPORT", "Reports show which composables are marked skippable."),
                ("STABILITY CONFIG", "Stability config files declare third-party classes stable."),
                ("LAMBDA WRAPPERS", "Unstable parameters wrap in lambda function holders."),
                ("CI GATES", "CI fails PRs if skippability drops."),
                ("HIGH PERFORMANCE", "Enforces 98% skippable composable compliance across screens.")
            ],
            "code": """// gradle.properties
kotlin.composeCompiler.reportsDestination=build/metrics
kotlin.composeCompiler.metricsDestination=build/metrics""",
            "metric": "Enforced 98% skippable composable compliance across 400+ screens."
        },
        {
            "id": "q68",
            "title": "8. How do you implement robust UI State restoration with rememberSaveable?",
            "problem": "Android process death wipes in-memory remember state, losing form inputs.",
            "solution": [
                ("REMEMBER SAVEABLE", "rememberSaveable preserves values across process death."),
                ("CUSTOM SAVER", "mapSaver serializes custom multi-field state classes."),
                ("PARCELIZE SUPPORT", "Parcelize data classes work with zero boilerplate."),
                ("SAVEDSTATEHANDLE", "SavedStateHandle in ViewModels restores background state."),
                ("PROCESS TESTING", "Dont Keep Activities tests verify state recovery."),
                ("SURVIVE KILLS", "User inputs survive sudden background app terminations.")
            ],
            "code": """var query by rememberSaveable { mutableStateOf("") }
var filter by rememberSaveable(stateSaver = FilterSaver) { mutableStateOf(Filter()) }""",
            "metric": "Preserved 100% of user cart and form data across process death."
        },
        {
            "id": "q69",
            "title": "9. How do you architect Design Systems with Material 3 and CompositionLocal?",
            "problem": "Hardcoding colors and spacing in composables blocks dark mode and white-labeling.",
            "solution": [
                ("COMPOSITIONLOCAL", "staticCompositionLocalOf provides design tokens without prop drilling."),
                ("DYNAMIC COLORS", "dynamicLightColorScheme adapts colors to user wallpaper."),
                ("APP THEME", "AppTheme wrapper supplies colors, shapes, and typography."),
                ("LOCAL ACCESS", "Components access tokens using LocalColors.current anywhere."),
                ("CONTRAST RATIOS", "Theme guarantees accessibility contrast for dark mode."),
                ("EASY THEMING", "Supports light, dark, and white-label themes.")
            ],
            "code": """val LocalSpacing = staticCompositionLocalOf { Spacing() }

@Composable
fun AppTheme(content: @Composable () -> Unit) {
    CompositionLocalProvider(LocalSpacing provides Spacing()) {
        MaterialTheme(colorScheme = AppColors, content = content)
    }
}""",
            "metric": "Standardized 120+ design system tokens across 3 client apps."
        },
        {
            "id": "q70",
            "title": "10. How do you implement Complex Gestures, Dragging, and Swipe-to-Dismiss?",
            "problem": "Handling swipe and drag with manual touch listeners causes gesture conflicts.",
            "solution": [
                ("SWIPE TO DISMISS", "SwipeToDismissBox handles list item swipe deletions."),
                ("POINTER INPUT", "Modifier.pointerInput detects 2D drag touch gestures."),
                ("ANIMATABLE", "Animatable animates dragged offsets with spring physics."),
                ("CONSUME CHANGES", "change.consume prevents parent scroll containers from intercepting."),
                ("ACCESSIBILITY ACTIONS", "Custom semantics actions allow screen reader dismissals."),
                ("SMOOTH TOUCH", "Delivers 120Hz physics-based touch response.")
            ],
            "code": """val state = rememberSwipeToDismissBoxState(
    confirmValueChange = { if (it == SwipeToDismissBoxValue.EndToStart) { onDelete(); true } else false }
)
SwipeToDismissBox(state = state, backgroundContent = { DeleteBg() }) { ItemCard() }""",
            "metric": "Delivered smooth physics-based swipe actions matching 120Hz native touch."
        },
        {
            "id": "q71",
            "title": "11. How do you test Jetpack Compose UI deterministically with ComposeTestRule?",
            "problem": "Testing dynamic UI animations and async coroutines in Espresso is flaky.",
            "solution": [
                ("COMPOSE TEST RULE", "createComposeRule sets up headless Compose UI tests."),
                ("SEMANTICS FINDERS", "onNodeWithText and onNodeWithTag locate UI elements."),
                ("PERFORM ACTIONS", "performClick triggers clicks and asserts expected state."),
                ("AUTO CLOCK CONTROL", "ComposeTestRule synchronizes with asynchronous coroutines automatically."),
                ("ACCESSIBILITY CHECKS", "AccessibilityChecks find missing semantics content description labels."),
                ("FAST CI TESTS", "Automated clock control eliminates flakiness in CI.")
            ],
            "code": """@Test
fun testLoginButton() {
    rule.setContent { LoginScreen(canSubmit = false) }
    rule.onNodeWithTag("submit").assertIsNotEnabled()
}""",
            "metric": "Sped up UI tests 4x and eliminated test flakiness in CI."
        },
        {
            "id": "q72",
            "title": "12. How do you embed Legacy Android Views inside Compose and Compose in XML?",
            "problem": "Migrating large XML codebases requires mixing legacy Views and Compose screens.",
            "solution": [
                ("ANDROIDVIEW", "AndroidView embeds legacy views inside Compose."),
                ("COMPOSEVIEW", "ComposeView renders composable trees inside XML layouts."),
                ("DISPOSE STRATEGY", "DisposeOnViewTreeLifecycleDestroyed prevents memory leaks in XML."),
                ("LIFECYCLE BRIDGE", "Bridges Activity lifecycle events to legacy views."),
                ("SHARED VIEWMODELS", "Shared Hilt ViewModels supply identical state streams."),
                ("SAFE MIGRATION", "Enables gradual screen-by-screen modernization of legacy apps.")
            ],
            "code": """// Compose in XML
binding.composeView.apply {
    setViewCompositionStrategy(ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed)
    setContent { AppTheme { ModernScreen() } }
}""",
            "metric": "Migrated 120+ legacy XML screens to Jetpack Compose with zero downtime."
        }
    ]
}

print("Part 2 (6 points): Modules 4, 5, 6 compiled.")
