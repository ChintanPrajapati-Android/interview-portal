import json

def get_modules_5_to_9():
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
                "problem": "UI fetching from network directly causes blank screens offline, data tearing, and inconsistent state updates.",
                "solution": [
                    ("ROOM EXCLUSIVE SSOT", "I configure UI layer to observe Room database Flow streams exclusively as the single truth."),
                    ("NETWORK REPOSITORY BRIDGE", "Repository layer fetches remote API data and writes directly into Room database tables."),
                    ("REACTIVE FLOW UPDATES", "Room automatically emits fresh entity lists to UI collectors whenever database writes occur."),
                    ("TRANSACTION ATOMICITY", "I wrap multi-table database operations inside withTransaction blocks to prevent partial writes."),
                    ("OFFLINE ZERO LATENCY", "App renders cached database content instantly upon launch with zero network latency.")
                ],
                "code": """class ProductRepository(private val api: ApiService, private val dao: ProductDao, private val db: AppDatabase) {
    val productsFlow: Flow<List<Product>> = dao.getProductsFlow()

    suspend fun refreshProducts() = withContext(Dispatchers.IO) {
        val remoteList = api.fetchProducts()
        db.withTransaction {
            dao.clearProducts()
            dao.insertProducts(remoteList.toEntities())
        }
    }
}""",
                "metric": "Achieved sub-50ms instant cold-start screen rendering and 100% full offline browsing capability."
            },
            {
                "id": "q50",
                "title": "2. How do you implement the Outbox Pattern with pending_mutations table?",
                "problem": "Offline user actions (e.g. likes, orders, edits) are lost if app process dies before network sync completes.",
                "solution": [
                    ("OUTBOX MUTATIONS TABLE", "I record every user action as an immutable mutation record with PENDING status in Room."),
                    ("IMMEDIATE OPTIMISTIC UI", "I update local entity state optimistically so UI reflects user intent with zero lag."),
                    ("WORKMANAGER BACKGROUND SYNC", "WorkManager polls pending mutations and dispatches them sequentially to backend APIs."),
                    ("EXPONENTIAL BACKOFF RETRY", "Failed network calls retry with exponential backoff without losing pending mutation records."),
                    ("IDEMPOTENCY KEYS", "I attach client-generated UUID idempotency keys to ensure backend processes actions exactly once.")
                ],
                "code": """@Entity(tableName = "pending_mutations")
data class MutationEntity(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val actionType: String,
    val payloadJson: String,
    val timestamp: Long = System.currentTimeMillis(),
    val status: String = "PENDING"
)""",
                "metric": "Guaranteed 100% zero data loss for offline user actions across 2M+ field operations."
            },
            {
                "id": "q51",
                "title": "3. How do you safely execute Room Database Migrations with MigrationTestHelper?",
                "problem": "Unhandled Room schema migrations crash user apps on startup with IllegalStateException across millions of devices.",
                "solution": [
                    ("MANUAL MIGRATION OBJECTS", "I write explicit Migration(1, 2) SQL scripts rather than relying on destructive fallback."),
                    ("MIGRATION TEST HELPER", "I write automated instrumented tests using MigrationTestHelper to validate table schema parity."),
                    ("AUTO MIGRATIONS SPEC", "I utilize @AutoMigration with AutoMigrationSpec for simple additive column modifications."),
                    ("EXPORT SCHEMA TRUE", "I enable exportSchema = true in build.gradle to version and check schema JSON files into Git."),
                    ("ZERO PRODUCTION CRASHES", "CI pipeline runs all historical migration tests before merging any database PR.")
                ],
                "code": """val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE orders ADD COLUMN delivery_notes TEXT DEFAULT '' NOT NULL")
    }
}

@RunWith(AndroidJUnit4::class)
class MigrationTest {
    @get:Rule
    val helper = MigrationTestHelper(InstrumentationRegistry.getInstrumentation(), AppDatabase::class.java)
    
    @Test
    fun migrate1To2() {
        var db = helper.createDatabase("test-db", 1)
        db.close()
        db = helper.runMigrationsAndValidate("test-db", 2, true, MIGRATION_1_2)
    }
}""",
                "metric": "Executed 14 consecutive major database migrations across 8M users with exactly 0 migration crashes."
            },
            {
                "id": "q52",
                "title": "4. How do you implement Paging 3 RemoteMediator with Room and Retrofit?",
                "problem": "Combining local database caching with paginated network feeds creates duplicate items and jumpy scroll position.",
                "solution": [
                    ("REMOTEMEDIATOR BOUNDARY", "I implement RemoteMediator<Int, ArticleEntity> to handle network pagination triggers."),
                    ("REMOTE KEYS TABLE", "I maintain RemoteKeys table storing nextKey and prevKey tokens for each entity record."),
                    ("PAGINGSOURCE FROM ROOM", "I return PagingSource<Int, ArticleEntity> directly from Room DAO queries."),
                    ("TRANSACTION BOUNDARY WRITE", "RemoteMediator clears and inserts page items inside atomic database transaction."),
                    ("CACHED IN VIEWMODEL", "I cache paginated flow in viewModelScope using .cachedIn(viewModelScope) operator.")
                ],
                "code": """@OptIn(ExperimentalPagingApi::class)
class ArticleRemoteMediator(private val db: AppDatabase, private val api: ApiService) : RemoteMediator<Int, ArticleEntity>() {
    override suspend fun load(loadType: LoadType, state: PagingState<Int, ArticleEntity>): MediatorResult {
        val page = when (loadType) {
            LoadType.REFRESH -> 1
            LoadType.PREPEND -> return MediatorResult.Success(endOfPaginationReached = true)
            LoadType.APPEND -> {
                val remoteKeys = getRemoteKeyForLastItem(state)
                remoteKeys?.nextKey ?: return MediatorResult.Success(endOfPaginationReached = true)
            }
        }
        val response = api.fetchArticles(page, state.config.pageSize)
        db.withTransaction {
            if (loadType == LoadType.REFRESH) db.articleDao().clearAll()
            db.articleDao().insertAll(response.toEntities())
        }
        return MediatorResult.Success(endOfPaginationReached = response.isEmpty())
    }
}""",
                "metric": "Delivered infinite scrolling with 60 FPS buttery smoothness and full offline reading cache."
            },
            {
                "id": "q53",
                "title": "5. How do you encrypt Room Database with SQLCipher on enterprise devices?",
                "problem": "Unencrypted SQLite databases allow attackers to extract sensitive PII and auth tokens via ADB backups or root access.",
                "solution": [
                    ("SQLCIPHER FACTORY", "I configure SupportFactory with cryptographically strong 256-bit passphrase key bytes."),
                    ("ANDROID KEYSTORE SECRET", "I generate AES master key inside hardware-backed Android KeyStore TEE/StrongBox."),
                    ("ZERO PLAINTEXT STORAGE", "Passphrase key bytes are decrypted in memory only when building RoomDatabase instance."),
                    ("AUTOMATIC HOOKS CLEANUP", "I sanitize byte arrays in memory immediately after passing to SupportFactory."),
                    ("SUB-3 PERCENT OVERHEAD", "SQLCipher native encryption adds under 3% CPU overhead on modern 64-bit chipsets.")
                ],
                "code": """val passphrase = KeyStoreManager.getOrCreateDatabaseKey()
val factory = SupportFactory(passphrase)
val db = Room.databaseBuilder(context, SecureDatabase::class.java, "secure.db")
    .openHelperFactory(factory)
    .build()""",
                "metric": "Achieved full HIPAA and GDPR banking-grade on-device data compliance with zero plaintext leakage."
            },
            {
                "id": "q54",
                "title": "6. How do you resolve Concurrent Write SQLiteDatabaseLockedException in multi-threaded environments?",
                "problem": "Multiple background coroutines writing to Room simultaneously trigger SQLiteDatabaseLockedException crashes.",
                "solution": [
                    ("WAL MODE ENABLED", "I enable Write-Ahead Logging (WAL) mode via Room builder to allow concurrent reads during writes."),
                    ("SINGLE WRITER DISPATCHER", "I route all database writes through Dispatchers.IO.limitedParallelism(1) single-writer queue."),
                    ("WITH TRANSACTION BLOCK", "I group dependent operations inside db.withTransaction to hold transaction lock efficiently."),
                    ("BUSY TIMEOUT CONFIG", "I configure sqlite busy_timeout pragma to 5000ms to allow locks to clear gracefully."),
                    ("DAO QUERY OFF MAIN", "I ensure all DAO read/write calls are marked suspend or return Coroutine Flow.")
                ],
                "code": """val db = Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .setJournalMode(RoomDatabase.JournalMode.WRITE_AHEAD_LOGGING)
    .build()""",
                "metric": "Reduced SQLite database lock crashes from 0.38% down to 0.00% across multi-process sync jobs."
            },
            {
                "id": "q55",
                "title": "7. How do you implement Conflict Resolution (Last-Write-Wins vs Field Merging)?",
                "problem": "Simultaneous offline edits on different client devices cause server state collisions and overwritten data.",
                "solution": [
                    ("LAMPORT TIMESTAMPS", "I assign UTC timestamp and client device UUID to every updated record field."),
                    ("FIELD LEVEL MERGING", "Server merges non-conflicting fields independently rather than replacing entire entity record."),
                    ("LAST WRITE WINS FALLBACK", "For conflicting single fields, record with latest server-validated timestamp wins."),
                    ("USER PROMPT CONFLICT", "For critical business documents, app displays side-by-side diff resolution screen to user."),
                    ("VERSION REVISION VECTOR", "I maintain revision sequence number to detect out-of-order sync packet deliveries.")
                ],
                "code": """data class SyncableEntity(
    val id: String,
    val data: String,
    val version: Long,
    val clientUpdatedAt: Long,
    val isDeleted: Boolean
)""",
                "metric": "Preserved 99.99% multi-device sync data integrity during concurrent offline field operations."
            },
            {
                "id": "q56",
                "title": "8. How do you optimize Room Full-Text Search with SQLite FTS4 / FTS5?",
                "problem": "LIKE '%query%' SQL queries perform expensive table scans, taking 800ms+ across 50,000 text records.",
                "solution": [
                    ("FTS4 FTS5 ENTITY", "I annotate Room search tables with @Fts4 or @Fts5 to create virtual index tables."),
                    ("MATCH OPERATOR", "I write search queries using MATCH operator with prefix wildcards for instant lookups."),
                    ("TOKENIZER SELECTION", "I configure unicode61 tokenizer to support international character stemming and accents."),
                    ("SUB-10MS LATENCY", "FTS indexes execute prefix and full-text searches in sub-10ms across 100,000 rows."),
                    ("AUTO SYNC TRIGGERS", "Room automatically creates SQLite triggers to keep FTS table in sync with primary table.")
                ],
                "code": """@Entity(tableName = "articles_fts")
@Fts4(contentEntity = ArticleEntity::class)
data class ArticleFtsEntity(
    val title: String,
    val body: String
)

@Dao
interface ArticleDao {
    @Query("SELECT * FROM articles JOIN articles_fts ON articles.id = articles_fts.rowid WHERE articles_fts MATCH :query")
    fun searchArticles(query: String): Flow<List<ArticleEntity>>
}""",
                "metric": "Sped up catalog search query latency from 820ms to 6.4ms across 120,000 product descriptions."
            },
            {
                "id": "q57",
                "title": "9. How do you implement Database Compaction and Pruning to prevent storage bloat?",
                "problem": "Old cached records, tombstone records, and log entries bloat SQLite file size to multiple gigabytes.",
                "solution": [
                    ("TIME BASED RETENTION", "I run background WorkManager job weekly to delete synced records older than 30 days."),
                    ("VACUUM PRAGMA", "I execute db.query('VACUUM') on background thread to reclaim fragmented disk pages."),
                    ("AUTO VACUUM INCREMENTAL", "I configure auto_vacuum = INCREMENTAL pragma to reclaim freed pages progressively."),
                    ("MAX DISK QUOTA CEILING", "I enforce a 150MB maximum cache ceiling, evicting oldest LRU records when exceeded."),
                    ("ATTACHED STORAGE METRICS", "I log database file size metrics to analytics to monitor user storage health.")
                ],
                "code": """class DatabaseCleanupWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val cutoff = System.currentTimeMillis() - TimeUnit.DAYS.toMillis(30)
        appDatabase.articleDao().deleteOlderThan(cutoff)
        appDatabase.openHelper.writableDatabase.execSQL("PRAGMA incremental_vacuum(50)")
        Result.success()
    }
}""",
                "metric": "Reduced average app storage footprint by 64%, preventing user uninstalls due to low storage."
            },
            {
                "id": "q58",
                "title": "10. How do you test Room DAOs deterministically with inMemoryDatabaseBuilder?",
                "problem": "Testing database operations on physical disk is slow, causes test pollution, and leads to flaky CI builds.",
                "solution": [
                    ("IN MEMORY DB BUILDER", "I construct test database using Room.inMemoryDatabaseBuilder for each test method."),
                    ("ALLOW MAIN THREAD QUERIES", "I call allowMainThreadQueries() strictly in test suites for synchronous execution."),
                    ("TURBINE FLOW TESTING", "I test reactive Flow emissions from DAOs using CashApp Turbine test library."),
                    ("TEARDOWN CLOSE", "I invoke db.close() in @After teardown method to ensure 100% test isolation."),
                    ("SUB MILLISECOND RUNS", "In-memory database runs in RAM, executing 100+ DAO unit tests in under 2 seconds.")
                ],
                "code": """@RunWith(AndroidJUnit4::class)
class ProductDaoTest {
    private lateinit var db: AppDatabase
    private lateinit var dao: ProductDao

    @Before
    fun createDb() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java).allowMainThreadQueries().build()
        dao = db.productDao()
    }

    @After
    fun closeDb() = db.close()

    @Test
    fun insertAndGetProduct() = runTest {
        val product = ProductEntity("1", "Smart Glasses", 199.99)
        dao.insert(product)
        dao.getProductFlow("1").test {
            assertEquals(product, awaitItem())
            cancelAndIgnoreRemainingEvents()
        }
    }
}""",
                "metric": "Executed 240+ database unit tests in 3.1 seconds in CI with zero flaky failures."
            },
            {
                "id": "q59",
                "title": "11. How do you implement Two-Way Room TypeConverters with Moshi / Kotlinx.serialization?",
                "problem": "Complex nested objects, lists, and custom value types cannot be stored in primitive SQLite columns directly.",
                "solution": [
                    ("KOTLINX SERIALIZATION CONVERTER", "I write @TypeConverter methods using Kotlinx.serialization Json parser."),
                    ("TYPE TOKEN MOSHI ADAPTER", "For Moshi, I construct parameterized Type tokens for generic List<T> mappings."),
                    ("PROVIDED TYPE CONVERTERS", "I use @ProvidedTypeConverter when converter requires injected Moshi/Json instances."),
                    ("NULL SAFETY SERIALIZATION", "I handle null and empty string fallbacks safely to prevent JSON parsing crashes."),
                    ("DATABASE BUILDER REGISTRATION", "I register provided converters in Room.databaseBuilder().addTypeConverter().")
                ],
                "code": """@ProvidedTypeConverter
class Converters(private val json: Json) {
    @TypeConverter
    fun fromTagsList(tags: List<String>): String = json.encodeToString(tags)

    @TypeConverter
    fun toTagsList(jsonString: String): List<String> = try {
        json.decodeFromString(jsonString)
    } catch (e: Exception) { emptyList() }
}""",
                "metric": "Serialized complex nested metadata structures with zero schema compromises."
            },
            {
                "id": "q60",
                "title": "12. How do you implement atomic multi-table bulk insertion benchmarks in Room?",
                "problem": "Inserting 10,000 records one by one takes 25 seconds because each insert opens an individual SQLite transaction.",
                "solution": [
                    ("BULK INSERT LIST DAO", "I pass full List<Entity> to DAO @Insert method to batch inside single transaction."),
                    ("EXPLICIT WITH TRANSACTION", "I wrap multi-DAO batch operations inside db.withTransaction { } blocks."),
                    ("CHUNKED BATCH SPLITTING", "I split 50,000 items into 1,000-item chunks to avoid SQLite bind variable limit (999)."),
                    ("PREPARED STATEMENT CACHE", "Room reuses compiled SQLite prepared statements across the batch automatically."),
                    ("SUB-SECOND INSERTION", "Batched transactions insert 10,000 records in under 380ms on mobile flash storage.")
                ],
                "code": """suspend fun insertLargeCatalog(items: List<ProductEntity>) = db.withTransaction {
    items.chunked(500).forEach { chunk ->
        productDao.insertAll(chunk)
    }
}""",
                "metric": "Sped up catalog sync ingestion from 22.4 seconds to 360 milliseconds (62x speedup)."
            }
        ]
    }
    
    return [m5]

print("Module 5 ready.")
