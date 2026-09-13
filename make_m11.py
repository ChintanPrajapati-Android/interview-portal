# -*- coding: utf-8 -*-
import json

m11_data = {
    "id": "module-11",
    "title": "Module 11: Android Architecture & Design Patterns Masterclass",
    "badge": "Architecture & Patterns",
    "color": "indigo",
    "summary": "Comprehensive architectural blueprints and design patterns: MVVM + Clean Architecture, MVI (UDF), Modularization (API/Impl), and 12 Production Android Design Patterns.",
    
    # Section 1: MVVM + CLEAN ARCHITECTURE
    "mvvm_clean": {
        "id": "arch-mvvm-clean",
        "title": "MVVM + Clean Architecture (Enterprise In-Depth)",
        "subtitle": "Separation of Concerns, Dependency Inversion & Single Source of Truth",
        "diagram": """+---------------------------------------------------------------------------------------------------+
|                                      PRESENTATION LAYER                                           |
|  +------------------------------+                +---------------------------------------------+  |
|  |   Jetpack Compose / View     |  Observe State |                 ViewModel                   |  |
|  |   (Passive UI Rendering)     |<---------------+   (State Holder, Survives Config Changes)   |  |
|  |                              |  User Actions  |   - Exposes StateFlow<UiState>              |  |
|  |                              |--------------->|   - Dispatches Coroutines / viewModelScope  |  |
|  +------------------------------+                +----------------------+----------------------+  |
+-------------------------------------------------------------------------|-------------------------+
                                                                          | Invokes Execute()
                                                                          v
+---------------------------------------------------------------------------------------------------+
|                                        DOMAIN LAYER (Pure Kotlin)                                 |
|  +----------------------------------------------------------------------+                         |
|  |                              UseCase / Interactor                    |                         |
|  |    (Encapsulates Single Business Rule, e.g., GetOrderDetailsUseCase) |                         |
|  +----------------------------------+-----------------------------------+                         |
|                                     | Calls Interface                                             |
|                                     v                                                             |
|  +----------------------------------+-----------------------------------+   +------------------+  |
|  |                   Repository Interface (Abstraction)                 |   |   Domain Model   |  |
|  |                   e.g., interface OrderRepository                    |   |   (Pure Entity)  |  |
|  +----------------------------------------------------------------------+   +------------------+  |
+-------------------------------------------------------------------------^-------------------------+
                                                                          | Implements (DIP)
                                                                          |
+-------------------------------------------------------------------------|-------------------------+
|                                         DATA LAYER                      |                         |
|  +----------------------------------------------------------------------+----------------------+  |
|  |                            Repository Implementation (OrderRepositoryImpl)                  |  |
|  |                     (Single Source of Truth, Cache Policy, Offline First)                   |  |
|  +------------------------------------+------------------------------------+------------------+  |
|                                       |                                    |                      |
|            Queries / Maps             |                 Fetches / Maps     |                      |
|                                       v                                    v                      |
|  +------------------------------------+------+   +-------------------------+-------------------+  |
|  |          LocalDataSource (Room)           |   |            RemoteDataSource (Retrofit)      |  |
|  |  - OrderDao                               |   |  - OrderApiService                          |  |
|  |  - OrderEntity (DB Schema)                |   |  - OrderDto (JSON Network Response)         |  |
|  +-------------------------------------------+   +---------------------------------------------+  |
|  +---------------------------------------------------------------------------------------------+  |
|  |                       Mappers (DTO -> Domain Model, Entity -> Domain Model)                 |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+""",
        "why_it_matters": "Clean Architecture enforces the Dependency Inversion Principle: the core business logic (Domain layer) is completely isolated from Android SDK frameworks, database engines (Room), and HTTP libraries (Retrofit). This ensures your code is 100% unit-testable without Android mocks, allows swapping out SQLite for DataStore or REST for GraphQL with zero changes to UI or business logic, and keeps large enterprise teams from stepping on each other's code.",
        "layer_breakdown": [
            {
                "layer": "Presentation Layer",
                "color": "emerald",
                "description": "Handles UI rendering, receiving user input, and displaying state. Completely passive.",
                "classes": [
                    {
                        "name": "Screen / Composable / View",
                        "why_used": "Renders pixels and captures clicks. Must contain zero business logic or decision making.",
                        "responsibility": "Collects StateFlow<UiState> with lifecycle awareness (e.g. collectAsStateWithLifecycle) and forwards user interactions as events to the ViewModel."
                    },
                    {
                        "name": "ViewModel",
                        "why_used": "Retains state across screen rotations / configuration changes and mediates between UI and Domain layers.",
                        "responsibility": "Launches coroutines in viewModelScope, invokes UseCases, handles domain errors, and reduces business responses into a single immutable UiState."
                    },
                    {
                        "name": "UiState & UiEvent",
                        "why_used": "Establishes a strict contract for what the screen displays and what actions it can trigger.",
                        "responsibility": "UiState is an immutable data class modeling loading, data, and error fields. UiEvent represents single-shot actions like navigation or snackbars."
                    }
                ]
            },
            {
                "layer": "Domain Layer (Pure Kotlin - Zero Android Dependencies)",
                "color": "indigo",
                "description": "The heart of the application containing enterprise business rules. Never imports android.* packages.",
                "classes": [
                    {
                        "name": "UseCase / Interactor",
                        "why_used": "Enforces Single Responsibility Principle (SRP). Prevents ViewModel from bloating into an unmaintainable God-object.",
                        "responsibility": "Contains one specific business action (e.g., ValidateCartItemsUseCase, CalculateTaxUseCase). Can be reused across multiple ViewModels."
                    },
                    {
                        "name": "Domain Model (Entity)",
                        "why_used": "Clean, immutable representation of business data independent of JSON keys or SQLite table columns.",
                        "responsibility": "Contains domain fields and business validation logic. Never contains @Entity or @SerializedName annotations."
                    },
                    {
                        "name": "Repository Interface",
                        "why_used": "Applies the Dependency Inversion Principle (DIP). Domain layer declares what data it needs without knowing HOW it is fetched.",
                        "responsibility": "Defines abstract suspending methods and Flow streams (e.g., fun getOrderStream(id: String): Flow<Order>)."
                    }
                ]
            },
            {
                "layer": "Data Layer",
                "color": "amber",
                "description": "Responsible for data retrieval, caching, network communication, and database persistence.",
                "classes": [
                    {
                        "name": "RepositoryImpl",
                        "why_used": "Serves as the Single Source of Truth (SSOT). Coordinates local caching and remote network syncing.",
                        "responsibility": "Implements the Domain Repository Interface. Decides whether to return cached DB data, fetch from network, or sync in the background."
                    },
                    {
                        "name": "RemoteDataSource & LocalDataSource",
                        "why_used": "Encapsulates raw framework libraries (Retrofit, Ktor, Room, DataStore) away from repository logic.",
                        "responsibility": "Directly interacts with Retrofit APIs or Room DAOs and handles raw HTTP/SQLite exceptions."
                    },
                    {
                        "name": "DTOs & DB Entities",
                        "why_used": "Models external data contracts exactly as delivered by backend APIs or stored on disk.",
                        "responsibility": "OrderDto matches backend JSON schemas; OrderEntity defines Room table schemas with indexes and foreign keys."
                    },
                    {
                        "name": "Mappers (Extension Functions)",
                        "why_used": "Acts as an Anti-Corruption Layer. Isolates backend schema changes from breaking the domain model or UI.",
                        "responsibility": "Transforms OrderDto -> Order (Domain) and OrderEntity -> Order (Domain)."
                    }
                ]
            }
        ],
        "code": """// ==========================================
// 1. DOMAIN LAYER (Pure Kotlin, Zero Android)
// ==========================================
data class Order(
    val id: String,
    val totalAmount: Double,
    val isDelivered: Boolean
)

interface OrderRepository {
    fun getOrderStream(orderId: String): Flow<Order>
    suspend fun refreshOrder(orderId: String): Result<Unit>
}

class GetOrderDetailsUseCase @Inject constructor(
    private val repository: OrderRepository
) {
    operator fun invoke(orderId: String): Flow<Order> {
        return repository.getOrderStream(orderId)
    }
}

// ==========================================
// 2. DATA LAYER (DTOs, Room, RepositoryImpl)
// ==========================================
data class OrderDto(
    @SerializedName("order_id") val id: String,
    @SerializedName("total_cents") val totalCents: Long,
    @SerializedName("status") val status: String
)

@Entity(tableName = "orders")
data class OrderEntity(
    @PrimaryKey val id: String,
    val totalAmount: Double,
    val isDelivered: Boolean
)

// Anti-Corruption Mappers
fun OrderDto.toEntity(): OrderEntity = OrderEntity(
    id = this.id,
    totalAmount = this.totalCents / 100.0,
    isDelivered = this.status.equals("DELIVERED", ignoreCase = true)
)

fun OrderEntity.toDomain(): Order = Order(
    id = this.id,
    totalAmount = this.totalAmount,
    isDelivered = this.isDelivered
)

class OrderRepositoryImpl @Inject constructor(
    private val api: OrderApiService,
    private val dao: OrderDao,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) : OrderRepository {

    override fun getOrderStream(orderId: String): Flow<Order> {
        return dao.observeOrder(orderId)
            .filterNotNull()
            .map { it.toDomain() }
            .flowOn(ioDispatcher)
    }

    override suspend fun refreshOrder(orderId: String): Result<Unit> = withContext(ioDispatcher) {
        runCatching {
            val response = api.fetchOrder(orderId)
            dao.insertOrder(response.toEntity())
        }
    }
}

// ==========================================
// 3. PRESENTATION LAYER (ViewModel & Compose)
// ==========================================
data class OrderUiState(
    val isLoading: Boolean = false,
    val order: Order? = null,
    val errorMessage: String? = null
)

@HiltViewModel
class OrderViewModel @Inject constructor(
    private val getOrderDetailsUseCase: GetOrderDetailsUseCase,
    private val repository: OrderRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val orderId: String = checkNotNull(savedStateHandle["orderId"])

    private val _uiState = MutableStateFlow(OrderUiState(isLoading = true))
    val uiState: StateFlow<OrderUiState> = _uiState.asStateFlow()

    init {
        observeOrder()
        refresh()
    }

    private fun observeOrder() {
        viewModelScope.launch {
            getOrderDetailsUseCase(orderId)
                .catch { e -> _uiState.update { it.copy(isLoading = false, errorMessage = e.message) } }
                .collect { order ->
                    _uiState.update { it.copy(isLoading = false, order = order, errorMessage = null) }
                }
        }
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            repository.refreshOrder(orderId)
                .onFailure { e -> _uiState.update { it.copy(isLoading = false, errorMessage = e.message) } }
        }
    }
}"""
    },

    # Section 2: MVI ARCHITECTURE (MODEL-VIEW-INTENT)
    "mvi_udf": {
        "id": "arch-mvi",
        "title": "MVI Architecture (Model-View-Intent & Unidirectional Data Flow)",
        "subtitle": "Deterministic State Machines, Predictable State Transitions & Single-Shot Effects",
        "diagram": """+---------------------------------------------------------------------------------------------------+
|                                 UNIDIRECTIONAL DATA FLOW (UDF)                                    |
|                                                                                                   |
|               +------------------------------------------------------------------+                |
|               |                         1. USER INTERACTION                      |                |
|               |                (User taps 'Add To Cart' / Pulls to Refresh)      |                |
|               +---------------------------------+--------------------------------+                |
|                                                 |                                                 |
|                                                 | Dispatches User Intent                          |
|                                                 v                                                 |
|               +------------------------------------------------------------------+                |
|               |                      2. INTENT / USER ACTION                     |                |
|               |       (Immutable Sealed Class: CartIntent.AddToCart(itemId))     |                |
|               +---------------------------------+--------------------------------+                |
|                                                 |                                                 |
|                                                 | Processed in ViewModel                          |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  |                                  3. VIEWMODEL / STORE                                       |  |
|  |  - Coordinates UseCases / Repositories                                                      |  |
|  |  - Emits Side Effects (Navigation, Snackbar) via Channel                                    |  |
|  |  - Calculates Mutation / Partial State Change                                               |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 | (PreviousState, Mutation) -> NewState           |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  |                                  4. PURE REDUCER FUNCTION                                   |  |
|  |          Deterministic State Machine: takes CurrentState + Mutation -> New ImmutableState   |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 | Emits via StateFlow<CartUiState>                |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  |                                    5. SINGLE IMMUTABLE STATE                                |  |
|  |            (Complete snapshot of screen: Loading, Items, Total, Discounts, DisabledButtons) |  |
|  +----------------------------------------------+----------------------------------------------+  |
|                                                 |                                                 |
|                                                 | Renders passively                               |
|                                                 v                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  |                                          6. VIEW / UI                                       |  |
|  |       (Jetpack Compose strictly renders State snapshot; zero local state divergence)        |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+""",
        "why_it_matters": "In complex mobile apps, state bugs happen when multiple async callbacks modify independent boolean flags (e.g. isLoading = false, showError = true, hasData = true) leading to impossible states (e.g. showing a loading spinner AND an error screen AND data list at the same time). MVI completely eliminates impossible states by enforcing a Single Source of Truth: the UI is a pure mathematical reflection of a single immutable state object (UI = f(State)).",
        "class_breakdown": [
            {
                "name": "Intent / UserAction (Sealed Interface)",
                "why_used": "Represents all explicit intentions from the user or system triggers.",
                "description": "Every single action (Button click, search query text change, retry button tap, screen load) is modeled as a strongly typed sealed class. Makes user analytics, logging, and crash reproduction trivial."
            },
            {
                "name": "UiState (Single Immutable Data Class)",
                "why_used": "Eliminates state fragmentation and UI race conditions.",
                "description": "Contains all data needed to render the entire screen. The View never computes state; it only renders whatever is inside this snapshot."
            },
            {
                "name": "SideEffect / SingleEvent (Channel / SharedFlow)",
                "why_used": "Handles one-shot transient events that must not survive screen rotation.",
                "description": "Used for actions that should happen exactly once: navigating to checkout, showing a Toast or Snackbar, or requesting runtime camera permissions."
            },
            {
                "name": "Reducer (State Transition Function)",
                "why_used": "Ensures state mutations are 100% deterministic, thread-safe, and pure.",
                "description": "A pure function with zero side effects: takes the previous state and a mutation/result, then returns a brand new state. Because it has no side effects, it is effortlessly unit-testable."
            },
            {
                "name": "MviViewModel (Store)",
                "why_used": "Orchestrates intent dispatching, executes async coroutines, and holds the StateFlow.",
                "description": "Receives intents from the UI, executes background use cases, passes results to the reducer, and exposes val state: StateFlow<UiState> and val effect: Flow<UiEffect>."
            }
        ],
        "code": """// ==========================================
// 1. MVI CONTRACT: STATE, INTENT, EFFECT
// ==========================================
data class CartUiState(
    val isLoading: Boolean = false,
    val items: List<CartItem> = emptyList(),
    val totalPrice: Double = 0.0,
    val error: String? = null
)

sealed interface CartIntent {
    data class LoadCart(val cartId: String) : CartIntent
    data class UpdateQuantity(val itemId: String, val newQuantity: Int) : CartIntent
    data object CheckoutClicked : CartIntent
}

sealed interface CartSideEffect {
    data class ShowToast(val message: String) : CartSideEffect
    data class NavigateToCheckout(val orderId: String) : CartSideEffect
}

// ==========================================
// 2. MVI VIEWMODEL & UDF ORCHESTRATION
// ==========================================
@HiltViewModel
class CartViewModel @Inject constructor(
    private val cartRepository: CartRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(CartUiState(isLoading = true))
    val uiState: StateFlow<CartUiState> = _uiState.asStateFlow()

    private val _sideEffect = Channel<CartSideEffect>(Channel.BUFFERED)
    val sideEffect: Flow<CartSideEffect> = _sideEffect.receiveAsFlow()

    fun processIntent(intent: CartIntent) {
        when (intent) {
            is CartIntent.LoadCart -> loadCart(intent.cartId)
            is CartIntent.UpdateQuantity -> updateItemQuantity(intent.itemId, intent.newQuantity)
            is CartIntent.CheckoutClicked -> startCheckout()
        }
    }

    private fun loadCart(cartId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            cartRepository.getCart(cartId)
                .onSuccess { cart ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            items = cart.items,
                            totalPrice = cart.items.sumOf { item -> item.price * item.quantity }
                        )
                    }
                }
                .onFailure { error ->
                    _uiState.update { it.copy(isLoading = false, error = error.message) }
                }
        }
    }

    private fun startCheckout() {
        viewModelScope.launch {
            if (_uiState.value.items.isEmpty()) {
                _sideEffect.send(CartSideEffect.ShowToast("Your cart is empty!"))
                return@launch
            }
            _sideEffect.send(CartSideEffect.NavigateToCheckout(orderId = "ORD-9921"))
        }
    }
}

// ==========================================
// 3. COMPOSE UI CONSUMING MVI
// ==========================================
@Composable
fun CartScreen(
    viewModel: CartViewModel,
    onNavigateToCheckout: (String) -> Unit
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current

    // Collect single-shot side effects safely
    LaunchedEffect(Unit) {
        viewModel.sideEffect.collect { effect ->
            when (effect) {
                is CartSideEffect.ShowToast -> Toast.makeText(context, effect.message, Toast.LENGTH_SHORT).show()
                is CartSideEffect.NavigateToCheckout -> onNavigateToCheckout(effect.orderId)
            }
        }
    }

    // Pure UI rendering from state snapshot
    Box(modifier = Modifier.fillMaxSize()) {
        when {
            state.isLoading -> CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
            state.error != null -> ErrorBanner(message = state.error!!)
            else -> CartContent(
                items = state.items,
                total = state.totalPrice,
                onItemCountChanged = { id, qty -> viewModel.processIntent(CartIntent.UpdateQuantity(id, qty)) },
                onCheckout = { viewModel.processIntent(CartIntent.CheckoutClicked) }
            )
        }
    }
}"""
    },

    # Section 3: MODULAR ARCHITECTURE (MULTI-MODULE ANDROID)
    "modular_architecture": {
        "id": "arch-modularization",
        "title": "Modular Architecture (Enterprise Multi-Module App Architecture)",
        "subtitle": "Feature Modularization, API/Impl Separation, Build Cache Optimization & Navigation",
        "diagram": """+---------------------------------------------------------------------------------------------------+
|                                       MULTI-MODULE DEPENDENCY GRAPH                               |
|                                                                                                   |
|                                                +----------+                                       |
|                                                |   :app   | (Root Container & Hilt Assembly)       |
|                                                +----+-----+                                       |
|                                                     |                                             |
|                     +-------------------------------+-------------------------------+             |
|                     |                                                               |             |
|                     v                                                               v             |
|        +-------------------------+                                     +------------------------+ |
|        |   :feature:feed:impl    |                                     | :feature:detail:impl   | |
|        | (Internal UI & Screens) |                                     | (Internal UI & Screens)| |
|        +------------+------------+                                     +------------+-----------+ |
|                     |                                                               |             |
|       Depends on    | Implements                                      Depends on    | Implements  |
|       API contract  |                                                 API contract  |             |
|                     v                                                               v             |
|        +-------------------------+                                     +------------------------+ |
|        |   :feature:feed:api     | <---------------------------------- | :feature:detail:api    | |
|        | (Nav Route / EntryPoint)|   Navigation Contract (Zero Impl)   | (Nav Route / EntryPoint)| |
|        +------------+------------+                                     +------------+-----------+ |
|                     |                                                               |             |
|                     +-------------------------------+-------------------------------+             |
|                                                     |                                             |
|                                                     v                                             |
|                           +---------------------------------------------------+                   |
|                           |                   :core:* MODULES                 |                   |
|                           +---------------------------------------------------+                   |
|                           |  :core:model         (Shared Pure Kotlin Models)  |                   |
|                           |  :core:network       (Retrofit / OkHttp / Ktor)   |                   |
|                           |  :core:database      (Room Database & DAOs)       |                   |
|                           |  :core:designsystem  (Compose Theme, Components)  |                   |
|                           |  :core:common        (Dispatchers, Extensions)    |                   |
|                           |  :core:testing       (Mock Engines, Test Rules)   |                   |
|                           +---------------------------------------------------+                   |
+---------------------------------------------------------------------------------------------------+""",
        "why_it_matters": "A monolithic single-module app forces Gradle to recompile the entire project whenever a single line changes, causing 5-10 minute build times. Proper modularization enables Gradle's parallel build execution, incremental compilation cache hits, strict code ownership boundaries across teams, and dynamic feature delivery on Google Play.",
        "module_taxonomy": [
            {
                "module_type": "App Module (:app)",
                "why_used": "Serves as the root orchestrator and application launcher.",
                "description": "Contains Application class, root NavHost, and assembles the top-level Hilt dependency injection graph by aggregating all feature and core modules."
            },
            {
                "module_type": "Feature API (:feature:xxx:api)",
                "why_used": "Prevents circular dependencies and enables instant compilation for sibling modules.",
                "description": "Exports strictly the public navigation route interface or feature contract. Contains ZERO UI code or ViewModels. Sibling feature modules can navigate to this feature without depending on its heavy implementation."
            },
            {
                "module_type": "Feature IMPL (:feature:xxx:impl)",
                "why_used": "Encapsulates private UI, ViewModels, and internal business logic.",
                "description": "Contains Compose screens, ViewModels, feature UseCases, and internal mappers. Marked with internal visibility so no outside module can access internal classes."
            },
            {
                "module_type": "Core Modules (:core:*)",
                "why_used": "Provides shared utilities, infrastructure, and design systems across all features.",
                "description": ":core:model (shared data structures), :core:network (network client), :core:database (Room tables), :core:designsystem (Color palette, typography, design tokens)."
            }
        ],
        "golden_rules": [
            "Rule 1: Feature modules MUST NEVER directly depend on other Feature implementation modules (:feature:A:impl -> :feature:B:impl is STRICTLY FORBIDDEN).",
            "Rule 2: Features communicate ONLY through Feature APIs (:feature:A:impl -> :feature:B:api).",
            "Rule 3: Core modules MUST NEVER depend on any Feature modules.",
            "Rule 4: Use Gradle convention plugins (build-logic) to share common build configurations without copy-pasting build.gradle files."
        ],
        "code": """// =========================================================================
// 1. GRADLE CONVENTION: :feature:feed:api/build.gradle.kts
// =========================================================================
plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
}

dependencies {
    implementation(projects.core.model) // Shared Domain Models
}

// Public Contract in :feature:feed:api
package com.app.feature.feed.api

interface FeedFeatureNavEntry {
    fun route(): String
    fun createRouteWithQuery(query: String): String
}

// =========================================================================
// 2. GRADLE CONVENTION: :feature:feed:impl/build.gradle.kts
// =========================================================================
plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.hilt.android)
}

dependencies {
    implementation(projects.feature.feed.api)     // Implements API Contract
    implementation(projects.feature.detail.api)   // Can navigate to Detail API
    implementation(projects.core.designsystem)    // UI Components & Theme
    implementation(projects.core.network)         // API Clients
    implementation(projects.core.database)        // Room Cache
}

// Implementation in :feature:feed:impl
package com.app.feature.feed.impl

@Singleton
class FeedFeatureNavEntryImpl @Inject constructor() : FeedFeatureNavEntry {
    override fun route(): String = "feed_route"
    override fun createRouteWithQuery(query: String): String = "feed_route?q=$query"
}

@Composable
internal fun FeedScreen(
    onNavigateToDetail: (String) -> Unit
) {
    // Internal Compose UI implementation
}"""
    },

    # Section 4: 12 ANDROID DESIGN PATTERNS WITH REAL EXAMPLES
    "design_patterns": [
        {
            "id": "dp-singleton",
            "number": 1,
            "category": "Creational",
            "name": "Singleton Pattern",
            "when_to_use": "When exactly one instance of a class must coordinate actions across the entire application (e.g. Database client, Analytics tracker, Encrypted SharedPreferences).",
            "why_used": "Prevents redundant object allocation, eliminates resource contention (e.g., multiple open SQLite database connections causing file lock corruption), and centralizes global application state.",
            "how_in_android": "In Kotlin, use object for thread-safe lazy singletons. For parameterized singletons (e.g. requiring Context), use Double-Checked Locking with @Volatile or Dagger/Hilt @Singleton.",
            "code": """// 1. Standard Thread-Safe Kotlin Singleton
object AnalyticsManager {
    fun trackEvent(name: String, params: Map<String, Any>) {
        // Global tracking logic
    }
}

// 2. Parameterized Double-Checked Locking Singleton
class AppDatabase private constructor(context: Context) {
    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: AppDatabase(context.applicationContext).also { INSTANCE = it }
            }
        }
    }
}"""
        },
        {
            "id": "dp-factory",
            "number": 2,
            "category": "Creational",
            "name": "Factory Method & Abstract Factory",
            "when_to_use": "When object creation logic is complex, requires dynamic parameter resolution, or should be decoupled from the caller (e.g., ViewModelProvider.Factory, FragmentFactory, WorkerFactory).",
            "why_used": "Android components (Activities, Fragments, ViewModels, Workers) are instantiated by the OS runtime. The Factory pattern lets developers pass custom dependencies via constructor injection.",
            "how_in_android": "Used by ViewModelProvider.Factory to construct ViewModels with custom arguments, and HiltWorkerFactory for background WorkManager tasks.",
            "code": """// Real Android Factory: Custom ViewModel Factory
class ProfileViewModelFactory(
    private val userId: String,
    private val repository: UserRepository
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(ProfileViewModel::class.java)) {
            return ProfileViewModel(userId, repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}"""
        },
        {
            "id": "dp-builder",
            "number": 3,
            "category": "Creational",
            "name": "Builder Pattern",
            "when_to_use": "When constructing complex objects with numerous optional parameters without exploding constructor overloads (Telescoping Constructor Anti-pattern).",
            "why_used": "Improves readability, enforces immutability, and validates parameters step-by-step before finalizing object creation.",
            "how_in_android": "Everywhere in Android Framework & Jetpack: AlertDialog.Builder, NotificationCompat.Builder, OkHttpClient.Builder, Room.databaseBuilder(), WorkRequest.Builder.",
            "code": """// Real Android Usage: OkHttpClient & Notification Builder
val okHttpClient = OkHttpClient.Builder()
    .connectTimeout(30, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS)
    .addInterceptor(HttpLoggingInterceptor().apply { level = Level.BODY })
    .build()

val notification = NotificationCompat.Builder(context, CHANNEL_ID)
    .setSmallIcon(R.drawable.ic_alert)
    .setContentTitle("Order Shipped")
    .setContentText("Your parcel is on the way!")
    .setPriority(NotificationCompat.PRIORITY_HIGH)
    .setAutoCancel(true)
    .build()"""
        },
        {
            "id": "dp-di",
            "number": 4,
            "category": "Creational",
            "name": "Dependency Injection (Inversion of Control)",
            "when_to_use": "When classes require collaborators (Services, Repositories, Network clients) and should not instantiate dependencies themselves.",
            "why_used": "Eliminates hardcoded dependencies, makes 100% unit-testing possible by swapping real dependencies with mocks, and manages object lifecycles cleanly.",
            "how_in_android": "Implemented via Google Hilt / Dagger at compile-time to generate dependency graphs without slow runtime reflection.",
            "code": """// Real Android Usage: Hilt Constructor Injection & Scope
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl("https://api.example.com/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
}

@HiltViewModel
class FeedViewModel @Inject constructor(
    private val feedRepository: FeedRepository // Injected automatically
) : ViewModel()"""
        },
        {
            "id": "dp-adapter",
            "number": 5,
            "category": "Structural",
            "name": "Adapter Pattern",
            "when_to_use": "When two incompatible interfaces need to work together without altering their existing codebases.",
            "why_used": "Converts arbitrary business data structures into UI items that Android views (RecyclerView, ViewPager) or serialization engines (Moshi JsonAdapter, Retrofit CallAdapter) can consume.",
            "how_in_android": "RecyclerView.Adapter converts arbitrary List<T> domain models into ViewHolder view hierarchies. CallAdapter.Factory in Retrofit converts Call<T> to Flow<T> or Result<T>.",
            "code": """// Real Android Usage: ListAdapter (RecyclerView Adapter)
class UserListAdapter : ListAdapter<User, UserListAdapter.UserViewHolder>(UserDiffCallback()) {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): UserViewHolder {
        val binding = ItemUserBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return UserViewHolder(binding)
    }

    override fun onBindViewHolder(holder: UserViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    class UserViewHolder(private val binding: ItemUserBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(user: User) { binding.userName.text = user.name }
    }
}"""
        },
        {
            "id": "dp-decorator",
            "number": 6,
            "category": "Structural",
            "name": "Decorator Pattern (Wrapper)",
            "when_to_use": "When you need to attach additional responsibilities or behaviors to an object dynamically without modifying the original class or using inheritance.",
            "why_used": "Adheres to Open/Closed Principle (open for extension, closed for modification) and avoids deep class inheritance hierarchies.",
            "how_in_android": "ContextWrapper in Android Framework (wraps Context to override themes or locales) and OkHttp Interceptor (wraps network requests to add Auth tokens or gzip encoding).",
            "code": """// Real Android Usage: OkHttp Auth Interceptor (Decorator)
class AuthInterceptor(private val tokenProvider: () -> String) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        
        // Decorate request dynamically with Authorization header
        val authenticatedRequest = originalRequest.newBuilder()
            .header("Authorization", "Bearer ${tokenProvider()}")
            .build()
            
        return chain.proceed(authenticatedRequest)
    }
}"""
        },
        {
            "id": "dp-facade",
            "number": 7,
            "category": "Structural",
            "name": "Facade Pattern",
            "when_to_use": "When you need to provide a simplified, unified high-level interface to a complex subsystem composed of multiple underlying classes.",
            "why_used": "Hides subsystem complexity from client code, prevents tight coupling, and centralizes multi-step operations.",
            "how_in_android": "The Clean Architecture Repository is the canonical Facade in Android: it hides Room DB caching, Retrofit API calls, In-Memory Memory Caches, and DataStore preferences behind simple functions like fun getUser(id: String): Flow<User>.",
            "code": """// Real Android Usage: Repository as a Facade Subsystem
class UserRepositoryImpl(
    private val remoteApi: UserApiService,
    private val localDao: UserDao,
    private val memoryCache: LruCache<String, User>
) : UserRepository {

    // Simplified Facade method hiding complex cache-network choreography
    override fun getUser(userId: String): Flow<User> = flow {
        // 1. Check RAM Cache
        memoryCache.get(userId)?.let { emit(it) }

        // 2. Check SQLite DB
        val cached = localDao.getUserById(userId)
        if (cached != null) emit(cached.toDomain())

        // 3. Fetch Remote API & Sync
        val remote = remoteApi.fetchUser(userId)
        localDao.insertUser(remote.toEntity())
        memoryCache.put(userId, remote.toDomain())
        emit(remote.toDomain())
    }
}"""
        },
        {
            "id": "dp-proxy",
            "number": 8,
            "category": "Structural",
            "name": "Proxy Pattern",
            "when_to_use": "When you want to provide a surrogate or placeholder for another object to control access to it, lazy-load it, or generate remote calls dynamically.",
            "why_used": "Decouples callers from execution mechanics, enables remote IPC communication, and allows dynamic method interception.",
            "how_in_android": "Retrofit.create(ApiService::class.java) uses Java's dynamic Proxy.newProxyInstance() to intercept Kotlin interface method calls and turn them into HTTP requests. Android IPC Binder/AIDL uses Stub and Proxy classes.",
            "code": """// Conceptual Android Retrofit Dynamic Proxy Mechanics
interface WeatherApi {
    @GET("weather")
    suspend fun getWeather(): WeatherResponse
}

// Retrofit uses java.lang.reflect.Proxy under the hood:
val proxyInstance = Proxy.newProxyInstance(
    WeatherApi::class.java.classLoader,
    arrayOf(WeatherApi::class.java)
) { proxy, method, args ->
    // Intercepts call, inspects annotations (@GET, @Query), and executes HTTP request
    println("Intercepted call to method: ${method.name}")
    executeHttpRequest(method, args)
} as WeatherApi"""
        },
        {
            "id": "dp-observer",
            "number": 9,
            "category": "Behavioral",
            "name": "Observer Pattern (Pub/Sub)",
            "when_to_use": "When a change in one object requires automatically updating other objects without tightly coupling them together.",
            "why_used": "Enables reactive programming, asynchronous data streams, and safe event multicasting across architectural boundaries.",
            "how_in_android": "Kotlin StateFlow / SharedFlow, Android LiveData, and BroadcastReceiver.",
            "code": """// Real Android Usage: StateFlow Observer with Lifecycle in Compose
class TimerViewModel : ViewModel() {
    private val _seconds = MutableStateFlow(0)
    val seconds: StateFlow<Int> = _seconds.asStateFlow()

    init {
        viewModelScope.launch {
            while (isActive) {
                delay(1000)
                _seconds.update { it + 1 }
            }
        }
    }
}

@Composable
fun TimerDisplay(viewModel: TimerViewModel) {
    // Observer: Automatically recomposes whenever _seconds changes
    val time by viewModel.seconds.collectAsStateWithLifecycle()
    Text(text = "Elapsed Time: $time s", style = MaterialTheme.typography.headlineMedium)
}"""
        },
        {
            "id": "dp-strategy",
            "number": 10,
            "category": "Behavioral",
            "name": "Strategy Pattern",
            "when_to_use": "When you have a family of interchangeable algorithms or business policies and want to select one at runtime based on context.",
            "why_used": "Eliminates ugly, bloated if/else or when statements, and allows adding new policies without modifying existing classes.",
            "how_in_android": "Network Caching Strategies (CacheFirstStrategy, NetworkFirstStrategy), Payment Gateways (GooglePayStrategy, CreditCardStrategy), Image Loading Transformations.",
            "code": """// Real Android Usage: Interchangeable Caching Strategy
interface CacheStrategy<T> {
    suspend fun fetch(key: String, remote: suspend () -> T, local: suspend () -> T?): T
}

class CacheFirstStrategy<T> : CacheStrategy<T> {
    override suspend fun fetch(key: String, remote: suspend () -> T, local: suspend () -> T?): T {
        return local() ?: remote()
    }
}

class NetworkFirstStrategy<T> : CacheStrategy<T> {
    override suspend fun fetch(key: String, remote: suspend () -> T, local: suspend () -> T?): T {
        return try { remote() } catch (e: Exception) { local() ?: throw e }
    }
}"""
        },
        {
            "id": "dp-chain-of-responsibility",
            "number": 11,
            "category": "Behavioral",
            "name": "Chain of Responsibility Pattern",
            "when_to_use": "When more than one object can handle a request, and you want to pass the request along a sequential pipeline of handlers until it is processed.",
            "why_used": "Decouples sender from receivers and allows adding, removing, or reordering processing steps dynamically.",
            "how_in_android": "OkHttp Interceptors (LoggingInterceptor -> AuthInterceptor -> RetryInterceptor -> NetworkInterceptor) and Android View Touch Event Dispatching (dispatchTouchEvent -> onInterceptTouchEvent -> onTouchEvent).",
            "code": """// Real Android Usage: OkHttp Interceptor Chain Execution
class MetricsInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        val startTime = System.nanoTime()

        // Passes request to the next handler in the chain
        val response = chain.proceed(request)

        val durationMs = (System.nanoTime() - startTime) / 1e6
        println("Request ${request.url} completed in ${durationMs}ms with status ${response.code}")
        
        return response
    }
}"""
        },
        {
            "id": "dp-command-state",
            "number": 12,
            "category": "Behavioral",
            "name": "Command & State Patterns",
            "when_to_use": "When you need to encapsulate a request as an object to parameterize clients with queues, logs, and undoable operations (Command) or alter object behavior when its internal state changes (State).",
            "why_used": "Enforces deterministic state transitions and decouples task execution from scheduling.",
            "how_in_android": "WorkManager OneTimeWorkRequest (Command Pattern: encapsulating background jobs) and Media Player / Audio Playback State Machines (IdleState, PreparingState, PlayingState, PausedState).",
            "code": """// Real Android Usage: Command Pattern with WorkManager
val syncCommand = OneTimeWorkRequestBuilder<SyncDatabaseWorker>()
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build()
    )
    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 10, TimeUnit.SECONDS)
    .setInputData(workDataOf("SYNC_MODE" to "FULL"))
    .build()

// Schedules and enqueues command for reliable execution by OS
WorkManager.getInstance(context).enqueue(syncCommand)"""
        }
    ]
}

if __name__ == "__main__":
    import pprint
    print(f"Module 11 loaded successfully with {len(m11_data['design_patterns'])} design patterns and 3 deep arch architectures!")
