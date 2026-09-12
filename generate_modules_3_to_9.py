import json

def get_modules_3_to_9():
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
                "problem": "Android BLE stack crashes with Error 133 (GATT_ERROR) during rapid connect/disconnect cycles or overlapping GATT commands.",
                "solution": [
                    ("MUTEX SERIAL QUEUE", "I serialize all GATT read, write, and descriptor operations through a Mutex queue."),
                    ("MAIN THREAD GATTCALLS", "I invoke connectGatt and gatt operations strictly on the Main thread as required."),
                    ("AUTOCONNECT FALSE", "I set autoConnect=false for rapid direct connection attempts, avoiding background scan delays."),
                    ("EXPLICIT CLOSE CLEANUP", "I invoke gatt.disconnect() followed immediately by gatt.close() to free native client handles."),
                    ("EXPONENTIAL RECONNECT", "I retry failed connections using exponential backoff intervals with random jitter.")
                ],
                "code": """class BleSerialQueue {
    private val mutex = Mutex()
    suspend fun <T> execute(block: suspend () -> T): T = mutex.withLock {
        withTimeout(5000L) { block() }
    }
}""",
                "metric": "Eliminated GATT Error 133 occurrences, achieving 99.4% BLE hardware connection success rate."
            },
            {
                "id": "q26",
                "title": "2. How do you negotiate maximum BLE throughput with MTU 517 and PHY 2M?",
                "problem": "Default BLE 23-byte MTU limits payload throughput to 3KB/s, causing slow sensor data sync and lagging telemetry.",
                "solution": [
                    ("REQUEST MTU 517", "I request gatt.requestMtu(517) immediately upon onConnectionStateChange reaching STATE_CONNECTED."),
                    ("NEGOTIATE 2M PHY", "I request gatt.setPreferredPhy(PHY_LE_2M) to double physical RF raw bit rate."),
                    ("WRITE TYPE NO RESPONSE", "I use WRITE_TYPE_NO_RESPONSE for continuous data streaming to bypass packet ACKs."),
                    ("CHUNKING AND PACKING", "I pack binary telemetry into 512-byte contiguous byte arrays for maximum pipe utilization."),
                    ("FLOW CONTROL ACKS", "I implement application-layer sliding window ACKs to ensure zero packet loss.")
                ],
                "code": """override fun onConnectionStateChange(gatt: BluetoothGatt, status: Int, newState: Int) {
    if (newState == BluetoothProfile.STATE_CONNECTED) {
        gatt.requestMtu(517)
    }
}
override fun onMtuChanged(gatt: BluetoothGatt, mtu: Int, status: Int) {
    gatt.setPreferredPhy(BluetoothDevice.PHY_LE_2M_MASK, BluetoothDevice.PHY_LE_2M_MASK, BluetoothDevice.PHY_OPTION_NO_PREFERRED)
}""",
                "metric": "Increased BLE payload data throughput from 2.8 KB/s to 64.5 KB/s (23x speedup)."
            },
            {
                "id": "q27",
                "title": "3. How do you correctly enable CCCD (0x2902) Descriptor Notifications?",
                "problem": "Enabling setCharacteristicNotification without writing the CCCD 0x2902 descriptor fails to receive peripheral notifications.",
                "solution": [
                    ("LOCAL NOTIFICATION FLAG", "I enable local OS notification reception using gatt.setCharacteristicNotification(char, true)."),
                    ("CCCD DESCRIPTOR UUID", "I retrieve the Client Characteristic Configuration Descriptor with standard UUID 0x2902."),
                    ("ENABLE NOTIFICATION VALUE", "I set descriptor value to BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE bytes."),
                    ("WRITE DESCRIPTOR QUEUE", "I dispatch gatt.writeDescriptor(descriptor) through the serial Mutex command queue."),
                    ("ANDROID 13+ COMPLIANCE", "I adapt writeDescriptor for Android 13 (API 33) signature changes safely.")
                ],
                "code": """val cccdUuid = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
gatt.setCharacteristicNotification(characteristic, true)
val descriptor = characteristic.getDescriptor(cccdUuid).apply {
    value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
}
bleQueue.execute { gatt.writeDescriptor(descriptor) }""",
                "metric": "Guaranteed 100% reliable hardware sensor telemetry streaming across 10+ medical IoT devices."
            },
            {
                "id": "q28",
                "title": "4. When should you use autoConnect=true vs autoConnect=false in connectGatt?",
                "problem": "Incorrect autoConnect parameter usage causes 30-second connection timeouts or failure to reconnect in the background.",
                "solution": [
                    ("AUTOCONNECT FALSE DIRECT", "I use autoConnect=false when the user initiates an immediate foreground connection."),
                    ("30 SECOND TIMEOUT", "autoConnect=false directs controller to attempt direct connection with immediate 30s timeout."),
                    ("AUTOCONNECT TRUE BACKGROUND", "I use autoConnect=true for passive background reconnection to bonded peripheral devices."),
                    ("PASSIVE SCANNING", "autoConnect=true registers device in native BLE whitelist, connecting instantly when device advertises."),
                    ("POWER EFFICIENCY", "autoConnect=true avoids continuous active RF scanning, conserving substantial mobile battery.")
                ],
                "code": """fun connect(device: BluetoothDevice, isBackgroundReconnect: Boolean) {
    val autoConnect = isBackgroundReconnect
    val gatt = device.connectGatt(context, autoConnect, gattCallback, BluetoothDevice.TRANSPORT_LE)
}""",
                "metric": "Reduced background reconnection latency by 85% while cutting peripheral scanning battery consumption."
            },
            {
                "id": "q29",
                "title": "5. How do you implement robust Over-The-Air (OTA) Dual-Bank Firmware Flashing?",
                "problem": "Flashing firmware over BLE is prone to RF packet loss, bricking hardware peripherals if connection drops mid-flash.",
                "solution": [
                    ("DUAL BANK PARTITIONING", "Firmware writes into inactive flash bank B while active firmware executes from bank A."),
                    ("BLOCK BYTES CHUNKING", "I chunk firmware binary into MTU-sized packets with sequence numbering and CRC16."),
                    ("SLIDING WINDOW ACK", "I request verification checksum ACK every 32 packets to validate data integrity."),
                    ("RETRY RESUMPTION", "If BLE disconnects, flashing resumes from last verified block offset rather than restarting."),
                    ("ATOMIC SWAP REBOOT", "Bootloader verifies full binary SHA-256 before swapping active partitions and rebooting.")
                ],
                "code": """suspend fun flashFirmware(firmwareBytes: ByteArray) {
    val totalChunks = (firmwareBytes.size + CHUNK_SIZE - 1) / CHUNK_SIZE
    for (i in 0 until totalChunks) {
        val chunk = firmwareBytes.copyOfRange(i * CHUNK_SIZE, minOf((i + 1) * CHUNK_SIZE, firmwareBytes.size))
        bleQueue.execute { sendFirmwareChunk(i, chunk) }
        if (i % 32 == 0) bleQueue.execute { verifyOtaProgress(i) }
    }
}""",
                "metric": "Achieved 99.98% successful OTA completion rate across 250,000+ deployed connected smart devices."
            },
            {
                "id": "q30",
                "title": "6. How do you handle Android 12+ Bluetooth Runtime Permissions (BLUETOOTH_SCAN, CONNECT)?",
                "problem": "Legacy ACCESS_FINE_LOCATION permission requirement for BLE scanning confused users and broke on Android 12+.",
                "solution": [
                    ("BLUETOOTH SCAN PERMISSION", "I declare BLUETOOTH_SCAN with neverForLocation flag when physical location is unused."),
                    ("BLUETOOTH CONNECT PERMISSION", "I request BLUETOOTH_CONNECT runtime permission before interacting with any BluetoothDevice."),
                    ("RUNTIME PERMISSION CONTRACT", "I request multiple permissions simultaneously using ActivityResultContracts.RequestMultiplePermissions."),
                    ("PRECISE VERSION BRANCHING", "I branch permission logic at Build.VERSION.SDK_INT >= Build.VERSION_CODES.S."),
                    ("BLUETOOTH ADVERTISE", "I request BLUETOOTH_ADVERTISE permission when device acts as BLE peripheral beacon.")
                ],
                "code": """<uses-permission android:name="android.permission.BLUETOOTH_SCAN"
    android:usesPermissionFlags="neverForLocation" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />""",
                "metric": "Complied 100% with Android 12/13/14 runtime security rules while removing location prompt friction."
            },
            {
                "id": "q31",
                "title": "7. How do you filter noisy BLE RSSI telemetry using a 1D Kalman Filter?",
                "problem": "Raw RSSI values fluctuate wildly (+/-15 dBm) due to multipath RF interference, causing inaccurate distance estimates.",
                "solution": [
                    ("STATE ESTIMATION", "Kalman filter computes optimal estimated distance by balancing prediction and measurement variance."),
                    ("MEASUREMENT NOISE R", "I tune measurement noise covariance R based on experimental RF sensor characteristics."),
                    ("PROCESS NOISE Q", "I adjust process noise covariance Q to control filter responsiveness to user motion."),
                    ("KALMAN GAIN UPDATE", "Filter calculates Kalman Gain dynamically to weight each incoming RSSI data point."),
                    ("REALTIME DISTANCE ACCURACY", "Delivers stable distance approximation using log-distance path loss path formulas.")
                ],
                "code": """class RssiKalmanFilter(private val r: Double = 0.8, private val q: Double = 0.05) {
    private var x: Double = -65.0 // Initial estimate
    private var p: Double = 1.0   // Estimation error
    fun update(measurement: Double): Double {
        p += q
        val k = p / (p + r)
        x += k * (measurement - x)
        p *= (1 - k)
        return x
    }
}""",
                "metric": "Smoothed RSSI noise fluctuations by 82%, improving indoor proximity accuracy within 0.5 meters."
            },
            {
                "id": "q32",
                "title": "8. How do you manage BLE Peripheral GATT Server mode on Android?",
                "problem": "Creating an on-device GATT Server requires advertising, service registration, and responding to remote central requests.",
                "solution": [
                    ("BLUETOOTH LE ADVERTISER", "I broadcast service UUIDs and custom manufacturer data using BluetoothLeAdvertiser."),
                    ("GATT SERVER OPEN", "I initialize server using BluetoothManager.openGattServer() with dedicated callback handler."),
                    ("ADD SERVICE AND CHARS", "I add BluetoothGattService instances with read/write characteristics and descriptors."),
                    ("SEND RESPONSE ACKS", "I reply to central read/write requests explicitly using gattServer.sendResponse()."),
                    ("NOTIFY CONNECTED CENTRALS", "I push data updates using gattServer.notifyCharacteristicChanged() across registered devices.")
                ],
                "code": """val server = bluetoothManager.openGattServer(context, object : BluetoothGattServerCallback() {
    override fun onCharacteristicReadRequest(device: BluetoothDevice, requestId: Int, offset: Int, characteristic: BluetoothGattCharacteristic) {
        server.sendResponse(device, requestId, BluetoothGatt.GATT_SUCCESS, offset, characteristic.value)
    }
})""",
                "metric": "Enabled phone-to-phone encrypted offline mesh communications with sub-50ms peer discovery."
            },
            {
                "id": "q33",
                "title": "9. How do you implement reliable background BLE Scanning without OS throttling?",
                "problem": "Android OS aggressively throttles and blocks unconfigured background BLE scans to protect battery life.",
                "solution": [
                    ("SCAN FILTERS MANDATORY", "I configure ScanFilter with exact Service UUIDs to allow scanning in screen-off state."),
                    ("SCAN SETTINGS LOW POWER", "I set ScanSettings.SCAN_MODE_LOW_POWER to reduce radio duty cycle in background."),
                    ("PENDING INTENT SCANNING", "I pass PendingIntent to scanner.startScan() instead of callback to survive app process death."),
                    ("BATCH SCAN RESULTS", "I configure reportDelay to deliver batched BLE advertisements at 5000ms intervals."),
                    ("FOREGROUND SERVICE TYPE", "I bind BLE background sync to Foreground Service with type connectedDevice.")
                ],
                "code": """val filter = ScanFilter.Builder().setServiceUuid(ParcelUuid(SERVICE_UUID)).build()
val settings = ScanSettings.Builder()
    .setScanMode(ScanSettings.SCAN_MODE_LOW_POWER)
    .setReportDelay(5000L)
    .build()
scanner.startScan(listOf(filter), settings, scanPendingIntent)""",
                "metric": "Maintained 24/7 continuous beacon discovery in background with under 1.2% total daily battery drain."
            },
            {
                "id": "q34",
                "title": "10. How do you handle Bluetooth Hardware Adapter toggles and unexpected resets?",
                "problem": "Users toggling Bluetooth OFF in Control Center drops active GATT handles, leaving coroutines hanging indefinitely.",
                "solution": [
                    ("BLUETOOTH ADAPTER RECEIVER", "I register BroadcastReceiver for BluetoothAdapter.ACTION_STATE_CHANGED intent events."),
                    ("STATE TURNING OFF", "On STATE_TURNING_OFF, I proactively teardown all active GATT connections and clean up queues."),
                    ("CANCEL SUSPENDED JOBS", "I cancel all pending coroutine withTimeout GATT executions immediately."),
                    ("STATE ON RESUMPTION", "On STATE_ON, I re-initialize BluetoothAdapter and trigger exponential reconnect loops."),
                    ("UI ALERT SNACKBAR", "I notify UI layer of hardware availability changes via reactive StateFlow state.")
                ],
                "code": """class BleStateReceiver(private val onBluetoothState: (Boolean) -> Unit) : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == BluetoothAdapter.ACTION_STATE_CHANGED) {
            val state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BluetoothAdapter.ERROR)
            onBluetoothState(state == BluetoothAdapter.STATE_ON)
        }
    }
}""",
                "metric": "Eliminated 100% of deadlocks and coroutine leaks caused by sudden Bluetooth hardware toggles."
            },
            {
                "id": "q35",
                "title": "11. How do you implement End-to-End AES-GCM encryption over raw BLE characteristics?",
                "problem": "Standard BLE pairing encryption (Just Works) is vulnerable to Man-In-The-Middle sniffing attacks in public spaces.",
                "solution": [
                    ("APPLICATION LAYER CRYPTO", "I encrypt all binary payload bytes before transmitting over BLE GATT characteristics."),
                    ("AES GCM 128", "I use AES-GCM with authenticated tag to guarantee confidentiality and payload tampering detection."),
                    ("EPHEMERAL ECDH KEYS", "I negotiate ephemeral session keys using Elliptic Curve Diffie-Hellman (ECDH) key exchange."),
                    ("DYNAMIC IV NONCE", "I increment a 12-byte initialization vector nonce with every transmitted packet."),
                    ("REPLAY ATTACK IMMUNITY", "Receiver rejects any packet whose IV nonce does not strictly increase.")
                ],
                "code": """fun encryptBlePayload(secretKey: SecretKey, nonce: ByteArray, plaintext: ByteArray): ByteArray {
    val cipher = Cipher.getInstance("AES/GCM/NoPadding")
    cipher.init(Cipher.ENCRYPT_MODE, secretKey, GCMParameterSpec(128, nonce))
    return cipher.doFinal(plaintext)
}""",
                "metric": "Passed strict third-party enterprise hardware security penetration test with zero vulnerabilities."
            },
            {
                "id": "q36",
                "title": "12. How do you benchmark BLE Packet Loss and Connection Interval latencies?",
                "problem": "Variable peripheral connection intervals (7.5ms to 4000ms) introduce unexpected telemetry latency spikes.",
                "solution": [
                    ("CONNECTION PRIORITY HIGH", "I call gatt.requestConnectionPriority(CONNECTION_PRIORITY_HIGH) to force 11.25ms - 15ms interval."),
                    ("ROUND TRIP LATENCY PING", "I send timestamped ping packet and compute round-trip time upon peripheral response."),
                    ("PACKET LOSS TRACKING", "I track sequential packet sequence IDs to measure RF packet drop percentages."),
                    ("DYNAMIC LATENCY DOWNSHIFT", "I switch back to CONNECTION_PRIORITY_BALANCED (30-50ms) when data streaming completes."),
                    ("DIAGNOSTIC DASHBOARD", "I expose live BLE telemetry statistics in internal debug overlay for field engineers.")
                ],
                "code": """fun optimizeForStreaming(gatt: BluetoothGatt) {
    gatt.requestConnectionPriority(BluetoothGatt.CONNECTION_PRIORITY_HIGH)
}
fun optimizeForIdle(gatt: BluetoothGatt) {
    gatt.requestConnectionPriority(BluetoothGatt.CONNECTION_PRIORITY_BALANCED)
}""",
                "metric": "Decreased end-to-end sensor command round-trip latency from 180ms down to 22ms."
            }
        ]
    }
    
    return [m3]

print("Module 3 ready.")
