import json
import html
import os

# We will write the full data structure for modules 1 through 9
from generate_all_modules import get_all_modules
from generate_modules_3_to_9 import get_modules_3_to_9

base_modules = get_all_modules() + get_modules_3_to_9()

m4 = {
    "id": "module-4",
    "title": "Module 4: GPS Tracking, Battery & Background Architecture",
    "badge": "Amber",
    "color": "amber",
    "summary": "Activity Recognition Transition API, 40-60% Battery Reduction, FusedLocationProviderClient, Android 14 FGS, 100k Geofences.",
    "questions": [
        {
            "id": "q37",
            "title": "1. How do you reduce GPS battery consumption by 40-60% using Activity Recognition?",
            "problem": "Continuous high-accuracy GPS polling drains 15-20% battery per hour, causing device heat and aggressive OS killing.",
            "solution": [
                ("ACTIVITY TRANSITION API", "I register ActivityTransitionRequest listeners to detect STILL, WALKING, and IN_VEHICLE user states."),
                ("DYNAMIC GPS POWER MODES", "When user is STILL, I drop GPS polling rate to PRIORITY_PASSIVE or pause entirely."),
                ("SPEED ADAPTIVE SAMPLING", "When IN_VEHICLE, I sample GPS every 5s with PRIORITY_HIGH_ACCURACY for navigation precision."),
                ("DISPLACEMENT FILTERS", "I enforce setMinUpdateDistanceMeters(25f) to prevent location updates while stationary."),
                ("BATCH LOCATION UPDATES", "I set setMaxUpdateDelayMillis(30000L) to let OS batch location deliveries efficiently.")
            ],
            "code": """val request = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 5000L)
    .setMinUpdateDistanceMeters(25f)
    .setMaxUpdateDelayMillis(30000L)
    .build()""",
            "metric": "Cut continuous tracking battery consumption by 54% while maintaining 99.2% route fidelity."
        },
        {
            "id": "q38",
            "title": "2. How do you architect Foreground Services for Android 14 (API 34) compliance?",
            "problem": "Android 14 enforces strict Foreground Service Types, throwing SecurityExceptions if types or permissions are missing.",
            "solution": [
                ("FOREGROUND SERVICE TYPES", "I declare exact foregroundServiceType='location|connectedDevice' in AndroidManifest.xml."),
                ("RUNTIME TYPE PERMISSION", "I declare FOREGROUND_SERVICE_LOCATION permission matching the declared service type."),
                ("ONSTARTCOMMAND BINDING", "I pass ServiceCompat.startForeground with matching service type bitmasks explicitly."),
                ("NOTIFICATION VISIBILITY", "I post high-priority persistent Notification with clear user-facing action buttons."),
                ("SHORT SERVICE TIMEOUTS", "I migrate short-lived background syncs to shortService type with 3-minute execution limit.")
            ],
            "code": """ServiceCompat.startForeground(
    this, NOTIFICATION_ID, notification,
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        ServiceInfo.FOREGROUND_SERVICE_TYPE_LOCATION
    } else 0
)""",
            "metric": "Achieved 100% Android 14 compatibility with zero ForegroundServiceStartNotAllowedExceptions."
        },
        {
            "id": "q39",
            "title": "3. How do you scale to 100,000+ Geofences on mobile without hitting OS limits?",
            "problem": "Android OS hard-limits active registered Geofences to 100 per app, making national store/depot geofencing impossible.",
            "solution": [
                ("SPATIAL R-TREE INDEXING", "I store 100,000 geofences in local SQLite with R-Tree spatial indexing extensions."),
                ("DYNAMIC ACTIVE SWAPPING", "As user location updates, I query nearest 50 geofences within a 10km radius."),
                ("GEOFENCING CLIENT REGISTER", "I register only the 50 closest geofences with GeofencingClient hardware provider."),
                ("EXPONENTIAL BOUNDARY BUFFER", "I calculate distance to furthest active geofence to set next spatial query trigger."),
                ("PENDING INTENT BROADCAST", "I process Geofence transition broadcasts in background WorkManager pipelines.")
            ],
            "code": """// Spatial Query for Nearest Geofences
val nearestGeofences = geofenceDao.findNearestWithinRadius(userLat, userLng, radiusMeters = 10_000, limit = 50)
geofencingClient.addGeofences(buildGeofenceRequest(nearestGeofences), geofencePendingIntent)""",
            "metric": "Supported 150,000 global merchant geofences seamlessly within the OS 100-geofence limit."
        },
        {
            "id": "q40",
            "title": "4. How do you survive Doze Mode and App Standby Buckets for time-critical alerts?",
            "problem": "Doze Mode batches network calls, suspends coroutines, and defers AlarmManager alarms when device is idle.",
            "solution": [
                ("FCM HIGH PRIORITY", "I deliver time-critical triggers using High-Priority Firebase Cloud Messaging push packets."),
                ("ALARM SET EXACT AND ALLOW", "I use alarmManager.setExactAndAllowWhileIdle() strictly for user-visible alarm events."),
                ("EXPEDITED WORKMANAGER", "I execute urgent background processing using WorkManager setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)."),
                ("STANDBY BUCKET RESPECT", "I design sync logic to tolerate RESTRICTED and RARE app standby bucket throttling."),
                ("BATTERY OPTIMIZATION PROMPT", "I guide enterprise field workers to disable battery optimization when strictly necessary.")
            ],
            "code": """val workRequest = OneTimeWorkRequestBuilder<UrgentSyncWorker>()
    .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
    .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())
    .build()
WorkManager.getInstance(context).enqueue(workRequest)""",
            "metric": "Delivered 99.8% on-time critical dispatch alerts within 3 seconds during deep overnight Doze mode."
        },
        {
            "id": "q41",
            "title": "5. How do you filter GPS Multipath and Drift in urban canyon environments?",
            "problem": "Tall buildings reflect satellite signals, creating GPS multipath errors with sudden 100-meter coordinate jumps.",
            "solution": [
                ("ACCURACY THRESHOLD FILTER", "I discard raw GPS readings with horizontal accuracy radius greater than 25 meters."),
                ("SPEED ACCURACY RATIO", "I filter out locations where delta distance exceeds physically possible vehicle velocity."),
                ("EXTENDED KALMAN FILTER", "I fuse GPS coordinates with accelerometer and gyroscope sensor data in real-time."),
                ("ROAD MAP MATCHING", "I snap filtered coordinates to OSM road vectors using hidden Markov map matching."),
                ("BEARING SMOOTHING", "I compute moving average bearing headings to prevent erratic map rotation jitter.")
            ],
            "code": """fun isValidPoint(last: Location?, current: Location): Boolean {
    if (current.accuracy > 25f) return false
    if (last == null) return true
    val distance = last.distanceTo(current)
    val timeDeltaSec = (current.time - last.time) / 1000f
    val speedKmh = (distance / timeDeltaSec) * 3.6
    return speedKmh < 180.0 // Reject supersonic teleports
}""",
            "metric": "Eliminated 94% of urban GPS phantom jumps, improving driver dispatch ETA accuracy."
        },
        {
            "id": "q42",
            "title": "6. How do you manage Offline GPS Breadcrumb Caching and Batch Uploading?",
            "problem": "Transmitting every GPS ping over cellular drains radio power; network drops cause telemetry data loss.",
            "solution": [
                ("ROOM PERSISTENT BUFFER", "I insert location coordinates into local Room database with pending_upload status flags."),
                ("RADIO DUTY BATCHING", "I buffer 50 location points before turning on cellular radio to transmit in bulk."),
                ("GZIP COMPRESSION", "I serialize and GZIP compress location batches, reducing network payload size by 80%."),
                ("EXPONENTIAL BACKOFF SYNC", "Failed uploads remain in database and retry with exponential backoff on reconnect."),
                ("TRANSACTION RETENTION PRUNING", "I delete successfully acknowledged location records inside atomic Room database transactions.")
            ],
            "code": """@Dao
interface LocationDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBatch(points: List<LocationEntity>)
    
    @Query("SELECT * FROM locations WHERE is_synced = 0 ORDER BY timestamp ASC LIMIT 50")
    suspend fun getPendingBatch(): List<LocationEntity>
}""",
            "metric": "Saved 45% cellular data bandwidth and achieved 100% zero-loss tracking during 4-hour tunnel outages."
        },
        {
            "id": "q43",
            "title": "7. How do you implement Background Location permissions on Android 10, 11, 12, 13, 14?",
            "problem": "Requesting Background Location simultaneously with Foreground Location causes immediate OS denial on Android 11+.",
            "solution": [
                ("TWO STEP PERMISSION FLOW", "I request ACCESS_FINE_LOCATION first; only after approval do I request ACCESS_BACKGROUND_LOCATION."),
                ("IN-APP FULL SCREEN DIALOG", "I explain why background tracking is required before launching system permission dialog."),
                ("SETTINGS SCREEN REDIRECT", "On Android 11+, OS directs user to App Permissions settings to select 'Allow all the time'."),
                ("PERMISSION DECLARATION", "I submit clear video proof to Google Play Console for Background Location policy compliance."),
                ("REVOCATION GRACEFUL HANDLING", "I handle runtime permission revocations gracefully without crashing background workers.")
            ],
            "code": """fun requestLocationStep1() {
    requestPermissionLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
}
fun requestLocationStep2() {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        requestPermissionLauncher.launch(Manifest.permission.ACCESS_BACKGROUND_LOCATION)
    }
}""",
            "metric": "Achieved 100% Google Play policy approval on first review for background location tracking."
        },
        {
            "id": "q44",
            "title": "8. How do you calculate high-precision Geodesic Distances (Vincenty vs Haversine)?",
            "problem": "Spherical Haversine formula assumes perfect sphere, introducing up to 0.5% error on Earth's oblate spheroid.",
            "solution": [
                ("WGS-84 ELLIPSOID", "I use Vincenty's inverse geodesic formula modeling Earth as an accurate oblate spheroid."),
                ("SUB-MILLIMETER ACCURACY", "Vincenty formula yields millimeter-accurate distances across long-range continental trajectories."),
                ("HAVERSINE FOR SHORT RANGE", "I fallback to fast Haversine for sub-100 meter micro calculations to save CPU cycles."),
                ("LOCATION DISTANCETO", "I utilize Android Location.distanceBetween() which internally uses WGS-84 geodesic algorithms."),
                ("ACCUMULATED ODOMETER", "I sum consecutive point-to-point geodesic deltas to compute total trip odometer distance.")
            ],
            "code": """fun calculateOdometer(points: List<Location>): Double {
    var totalMeters = 0.0
    val results = FloatArray(1)
    for (i in 0 until points.size - 1) {
        Location.distanceBetween(
            points[i].latitude, points[i].longitude,
            points[i+1].latitude, points[i+1].longitude,
            results
        )
        totalMeters += results[0]
    }
    return totalMeters
}""",
            "metric": "Delivered 99.9% accurate commercial mileage billing calculations matching hardware vehicle odometers."
        },
        {
            "id": "q45",
            "title": "9. How do you implement Indoor Positioning using WiFi RTT (802.11mc) and Beacons?",
            "problem": "GPS satellite signals are completely blocked indoors, dropping positioning accuracy to zero inside malls/warehouses.",
            "solution": [
                ("WIFI RTT ROUND TRIP", "I measure time-of-flight distances to 802.11mc Access Points using RttManager APIs."),
                ("SUB-METER INDOOR ACCURACY", "WiFi RTT provides 1-2 meter indoor accuracy without needing fingerprinting calibration."),
                ("BLE BEACON TRILATERATION", "I fuse WiFi RTT with BLE iBeacon/Eddystone RSSI proximity trilateration."),
                ("STEP DETECTOR PEDOMETER", "I integrate Hardware Step Counter sensor for dead-reckoning navigation between fixes."),
                ("FLOOR LEVEL DETECTION", "I read Barometer pressure sensor deltas to identify elevator and staircase floor changes.")
            ],
            "code": """val rttRequest = RangingRequest.Builder().apply {
    accessPoints.forEach { addAccessPoint(it) }
}.build()
wifiRttManager.startRanging(rttRequest, executor, object : RangingResultCallback() {
    override fun onRangingResults(results: List<RangingResult>) {
        val indoorCoordinate = trilaterate(results)
        updateIndoorMap(indoorCoordinate)
    }
})""",
            "metric": "Achieved 1.5-meter indoor warehouse forklift tracking accuracy with instant floor-level detection."
        },
        {
            "id": "q46",
            "title": "10. How do you audit and prevent WakeLock Leaks that trigger Google Play bad behavior warnings?",
            "problem": "Acquiring PowerManager.WakeLock without reliable release drains battery and triggers Google Play Vitals penalties.",
            "solution": [
                ("TIMEOUT MANDATORY WAKELOCKS", "I enforce strict timeouts on every wakeLock.acquire(10000L) invocation."),
                ("WORKMANAGER REPLACEMENT", "I replace manual WakeLocks with WorkManager which manages platform wakelocks safely."),
                ("AUTOMATED CI AUDITS", "I run static lint checks and automated LeakCanary wakelock monitors in CI."),
                ("BATTERY HISTORIAN PROFILING", "I analyze bugreports using Google Battery Historian to detect stuck wakelocks."),
                ("FINALLY BLOCK RELEASES", "I wrap wakeLock releases inside mandatory finally blocks with isHeld checks.")
            ],
            "code": """val wakeLock = powerManager.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "MyApp:SyncTag")
try {
    wakeLock.acquire(5000L) // 5s safety timeout
    doSync()
} finally {
    if (wakeLock.isHeld) wakeLock.release()
}""",
            "metric": "Zero wakeLock leak reports in Google Play Console across 5M+ active daily installations."
        },
        {
            "id": "q47",
            "title": "11. How do you build an animated vehicle Smooth Marker on Google Maps / Mapbox?",
            "problem": "Raw GPS updates cause vehicle map marker to jump abruptly, looking jerky and disorienting users.",
            "solution": [
                ("VALUEANIMATOR INTERPOLATION", "I animate marker coordinate positions using ValueAnimator with Spherical LatLngInterpolator."),
                ("LINEAR INTERPOLATOR FRACTION", "I calculate fraction elapsed over update interval (e.g., 2000ms) for fluid motion."),
                ("BEARING ROTATION ANIMATION", "I animate marker rotation angle smoothly using shortest angular distance math."),
                ("CATMULL-ROM SPLINE", "I smooth trajectory path using Catmull-Rom splines through historical GPS waypoints."),
                ("DESYNCHRONIZATION BUFFER", "I maintain a 1-point latency buffer to ensure continuous uninterrupted vehicle animation.")
            ],
            "code": """fun animateMarker(marker: Marker, toPosition: LatLng, toRotation: Float) {
    val startPosition = marker.position
    val startRotation = marker.rotation
    val valueAnimator = ValueAnimator.ofFloat(0f, 1f).apply {
        duration = 2000L
        interpolator = LinearInterpolator()
        addUpdateListener { va ->
            val v = va.animatedFraction
            marker.position = latLngInterpolator.interpolate(v, startPosition, toPosition)
            marker.rotation = computeRotation(v, startRotation, toRotation)
        }
    }
    valueAnimator.start()
}""",
            "metric": "Delivered Uber-grade 60 FPS smooth car animation with zero visual teleportation."
        },
        {
            "id": "q48",
            "title": "12. How do you manage Android 14 Exact Alarm scheduling policies?",
            "problem": "Android 14 revokes SCHEDULE_EXACT_ALARM by default for non-calendar/alarm apps, crashing setExact() calls.",
            "solution": [
                ("CAN SCHEDULE EXACT ALARMS", "I query alarmManager.canScheduleExactAlarms() before attempting any exact alarm registration."),
                ("USE_EXACT_ALARM PERMISSION", "I declare USE_EXACT_ALARM for permitted core categories (alarms, timers, reminders)."),
                ("WORKMANAGER INEXACT FALLBACK", "If exact alarm permission is missing, I gracefully fallback to WorkManager periodic tasks."),
                ("ACTION_SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED", "I register broadcast receiver to detect when user grants exact alarm permission in settings."),
                ("USER FRIENDLY PROMPT", "I show custom educational bottom sheet directing user to system settings toggle.")
            ],
            "code": """if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    if (alarmManager.canScheduleExactAlarms()) {
        alarmManager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, triggerAtMs, pendingIntent)
    } else {
        context.startActivity(Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM))
    }
}""",
            "metric": "Prevented 100% of SecurityExceptions on Android 14 while preserving precise alarm delivery."
        }
    ]
}

print("Module 4 ready.")
