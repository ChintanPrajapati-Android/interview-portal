import json

def get_modules_6_to_9():
    m6 = {
        "id": "module-6",
        "title": "Module 6: Jetpack Compose & Modern Reactive UI",
        "badge": "Rose",
        "color": "rose",
        "summary": "@Immutable, @Stable, derivedStateOf, PersistentList, Side-Effects Lifecycle, LazyColumn Keys, Compose Compiler Metrics.",
        "questions": [
            {
                "id": "q61",
                "title": "1. How do you eliminate redundant recompositions with @Immutable and @Stable?",
                "problem": "Passing unstable standard Kotlin collections (List<T>) makes composable functions non-skippable, lagging 60 FPS scrolling.",
                "solution": [
                    ("IMMUTABLE DATA MODELS", "I annotate UI state data classes with @Immutable to promise compiler stability."),
                    ("PERSISTENT COLLECTIONS", "I replace standard List<T> with kotlinx.collections.immutable.PersistentList to ensure stability."),
                    ("COMPOSE COMPILER METRICS", "I run compiler metrics to verify all composables are marked restartable and skippable."),
                    ("STABLE INTERFACES", "I annotate domain interfaces and external library models with @Stable annotations."),
                    ("PRUNED RECOMPOSITION TREE", "Compose skips execution of stable composables whose inputs have not structurally changed.")
                ],
                "code": """@Immutable
data class FeedUiState(
    val title: String,
    val items: PersistentList<FeedItem> = persistentListOf(),
    val isRefreshing: Boolean = false
)

@Composable
fun FeedScreen(state: FeedUiState, onRefresh: () -> Unit) {
    // Skippable because FeedUiState is 100% Immutable and stable
}""",
                "metric": "Eliminated 86% of unnecessary UI recompositions, achieving steady 60 FPS scrolling."
            },
            {
                "id": "q62",
                "title": "2. When and why must you use derivedStateOf in Jetpack Compose?",
                "problem": "Reading rapidly changing state (like scroll offset or text length) directly inside composable causes 60 recompositions/sec.",
                "solution": [
                    ("DERIVED STATE OF", "I wrap calculation inside derivedStateOf when input state changes more frequently than output."),
                    ("FILTER RAPID EMISSIONS", "derivedStateOf notifies composition only when calculated boolean/integer value actually transitions."),
                    ("SCROLL OFFSET BUTTON", "I compute showScrollToTopButton = derivedStateOf { listState.firstVisibleItemIndex > 5 }."),
                    ("ZERO REDUNDANT FRAMES", "Recomposition runs only on 0->1 or 1->0 boolean edge transitions rather than every pixel."),
                    ("REMEMBER DERIVED STATE", "I always remember the derivedStateOf calculation to survive standard recomposition cycles.")
                ],
                "code": """val listState = rememberLazyListState()
val showScrollToTop by remember {
    derivedStateOf { listState.firstVisibleItemIndex > 5 }
}

if (showScrollToTop) {
    ScrollToTopFab(onClick = { /* scroll */ })
}""",
                "metric": "Reduced LazyList scrolling recomposition count from 340 events down to 2 discrete events."
            },
            {
                "id": "q63",
                "title": "3. How do you govern Side-Effects in Compose (LaunchedEffect, DisposableEffect, SideEffect)?",
                "problem": "Triggering network calls, analytics, or native listeners directly inside Composable body causes repeated execution bugs.",
                "solution": [
                    ("LAUNCHED EFFECT KEYS", "I use LaunchedEffect(key1) to launch coroutines that automatically cancel on key changes."),
                    ("DISPOSABLE EFFECT CLEANUP", "I use DisposableEffect to register system listeners and clean them up in onDispose."),
                    ("SIDE EFFECT COMMITTED", "I use SideEffect to update non-Compose state objects only after successful composition commit."),
                    ("REMEMBER COROUTINE SCOPE", "I use rememberCoroutineScope strictly for launching coroutines from user UI callbacks (onClick)."),
                    ("ZERO UNSAFE LAUNCHES", "Banned launching naked coroutines or side-effects inside composable rendering execution.")
                ],
                "code": """DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, event ->
        if (event == Lifecycle.Event.ON_RESUME) viewModel.refresh()
    }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose {
        lifecycleOwner.lifecycle.removeObserver(observer)
    }
}""",
                "metric": "Eliminated 100% of coroutine leaks and duplicate analytics tracking in Jetpack Compose screens."
            },
            {
                "id": "q64",
                "title": "4. How do you optimize LazyColumn performance with stable keys and contentType?",
                "problem": "LazyColumn without keys loses scroll state during list mutations; missing contentType breaks item view recycling.",
                "solution": [
                    ("EXPLICIT ITEM KEYS", "I supply unique business ID keys in items(items, key = { it.id }) to preserve item identity."),
                    ("CONTENT TYPE SPEC", "I define contentType = { it.viewType } so Compose reuses composition slots for matching item layouts."),
                    ("AVOID INLINE LAMBDAS", "I use method references or remember lambdas to prevent breaking composable equality."),
                    ("SUB-COMPOSE OPTIMIZATION", "Compose reuses item slots with matching contentType without rebuilding semantic layout nodes."),
                    ("SMOOTH FLING SPEED", "Maintains silky smooth 120Hz flinging across lists containing 10,000+ mixed view items.")
                ],
                "code": """LazyColumn(state = listState) {
    items(
        items = feedItems,
        key = { it.id },
        contentType = { it.type }
    ) { item ->
        when (item) {
            is FeedItem.Header -> HeaderItem(item)
            is FeedItem.Card -> ProductCardItem(item)
        }
    }
}""",
                "metric": "Reduced frame drop jank from 18.4% to 0.6% on complex heterogenous feeds."
            },
            {
                "id": "q65",
                "title": "5. How do you implement Type-Safe Navigation in Jetpack Compose 2.8+?",
                "problem": "Legacy string-based route URLs ('profile/{id}?arg=val') were error-prone, untyped, and crashed on runtime type mismatch.",
                "solution": [
                    ("KOTLINX SERIALIZABLE ROUTES", "I define navigation destinations as @Serializable data classes and data objects."),
                    ("TYPE SAFE NAVHOST", "I define NavHost with composable<RouteType> lambda builders without string parsing."),
                    ("AUTOMATIC TO ROUTE EXTRACT", "I extract route arguments inside composables using backStackEntry.toRoute<RouteType>()."),
                    ("DEEP LINK PARSING", "Navigation library handles deep link URL mapping and argument decoding automatically."),
                    ("COMPILE TIME NAVIGATION", "Any missing or invalid navigation parameter is caught instantly during compilation.")
                ],
                "code": """@Serializable
data class ProductDetailRoute(val productId: String, val referralCode: String? = null)

// NavHost setup
NavHost(navController = navController, startDestination = HomeRoute) {
    composable<ProductDetailRoute> { backStackEntry ->
        val route: ProductDetailRoute = backStackEntry.toRoute()
        ProductDetailScreen(productId = route.productId)
    }
}""",
                "metric": "Eliminated 100% of runtime navigation route typo crashes and argument cast exceptions."
            },
            {
                "id": "q66",
                "title": "6. How do you build a Custom Layout with SubcomposeLayout and Intrinsic Measurements?",
                "problem": "Standard Row/Column cannot handle complex dynamic slot measuring, custom cascading headers, or aspect ratio grids.",
                "solution": [
                    ("SUBCOMPOSE LAYOUT", "I use SubcomposeLayout when composition of dependent content depends on measurement of preceding slots."),
                    ("INTRINSIC MEASUREMENTS", "I query intrinsic heights and widths (IntrinsicSize.Min/Max) for proportional multi-column alignment."),
                    ("MEASURE AND PLACE", "I measure child placeables and position them using placeRelativeWithLayer() coordinates."),
                    ("ZERO ALLOCATION MEASURE", "I reuse measurement objects to ensure layout pass executes within 16ms window."),
                    ("MODIFIER LAYOUT CUSTOM", "I build custom Modifier.layout to adjust layout bounds without extra layout tree nesting.")
                ],
                "code": """@Composable
fun CustomCascadeLayout(modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    Layout(modifier = modifier, content = content) { measurables, constraints ->
        val placeables = measurables.map { it.measure(constraints) }
        layout(constraints.maxWidth, constraints.maxHeight) {
            var yOffset = 0
            placeables.forEach { placeable ->
                placeable.placeRelative(x = 0, y = yOffset)
                yOffset += placeable.height
            }
        }
    }
}""",
                "metric": "Built complex multi-tier cascading UI layouts with 0 jank and zero additional XML layouts."
            },
            {
                "id": "q67",
                "title": "7. How do you interpret and optimize Compose Compiler Metrics Reports?",
                "problem": "Invisible performance regressions slip into production because developers cannot easily see unskippable composables.",
                "solution": [
                    ("GRADLE COMPILER FLAGS", "I pass -Pplugin:androidx.compose.compiler.plugins.kotlin:reportsDestination flags in Gradle build."),
                    ("SKIPPABLE VS RESTARTABLE", "I inspect app_composables.txt to verify all screen composables are marked skippable."),
                    ("STABILITY CONFIG FILE", "I add external third-party classes into compose_compiler_config.conf stability file."),
                    ("UNSTABLE PARAMETER FIX", "I convert unstable parameters to Immutable data wrappers or lambda function holders."),
                    ("CI AUTOMATION GATE", "CI fails the pull request if the percentage of skippable composables drops below 95%.")
                ],
                "code": """// gradle.properties
kotlin.composeCompiler.reportsDestination=build/compose_metrics
kotlin.composeCompiler.metricsDestination=build/compose_metrics

// compose_compiler_config.conf
java.time.Instant
java.time.LocalDate""",
                "metric": "Enforced 98% skippable composable compliance across 400+ production Compose screens."
            },
            {
                "id": "q68",
                "title": "8. How do you implement robust UI State restoration with rememberSaveable?",
                "problem": "Activity recreation during system process death wipes in-memory remember state, losing user inputs and form data.",
                "solution": [
                    ("REMEMBER SAVEABLE", "I use rememberSaveable instead of remember for user inputs that must survive process death."),
                    ("CUSTOM SAVER MAP", "I write custom mapSaver or listSaver for complex custom data classes and objects."),
                    ("AUTO PARCELABLE SAVER", "Data classes annotated with @Parcelize work with rememberSaveable with zero extra code."),
                    ("SAVEDSTATEHANDLE VIEWMODEL", "I persist ViewModel state inside SavedStateHandle for seamless background restoration."),
                    ("PROCESS DEATH TESTING", "I verify state recovery in tests by toggling 'Don't Keep Activities' in Developer Options.")
                ],
                "code": """var query by rememberSaveable { mutableStateOf("") }

val FilterSaver = mapSaver(
    save = { mapOf("min" to it.minPrice, "max" to it.maxPrice) },
    restore = { FilterRange(it["min"] as Double, it["max"] as Double) }
)
var filter by rememberSaveable(stateSaver = FilterSaver) { mutableStateOf(FilterRange(0.0, 1000.0)) }""",
                "metric": "Preserved 100% of user cart and multi-page form progress across sudden process terminations."
            },
            {
                "id": "q69",
                "title": "9. How do you architect Design Systems with Material 3 Theme and CompositionLocal?",
                "problem": "Hardcoding colors, typography, and spacing in composables prevents dark mode support and enterprise white-labeling.",
                "solution": [
                    ("STATIC COMPOSITION LOCAL", "I declare staticCompositionLocalOf for design tokens that rarely change (typography, spacing)."),
                    ("DYNAMIC COLOR SCHEMES", "I support Android 12+ dynamic wallpaper color schemes using dynamicLightColorScheme."),
                    ("CUSTOM THEME WRAPPER", "I wrap entire app with AppTheme providing custom colors, shapes, and elevation tokens."),
                    ("NO PROP DRILLING", "Components access theme tokens anywhere via LocalAppColors.current without parameter passing."),
                    ("LIGHT DARK ACCESSIBILITY", "Theme automatically adapts contrast ratios for light, dark, and high-contrast accessibility modes.")
                ],
                "code": """val LocalSpacing = staticCompositionLocalOf { Spacing() }

@Composable
fun AppTheme(darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    val colors = if (darkTheme) DarkColorPalette else LightColorPalette
    CompositionLocalProvider(LocalSpacing provides Spacing(), LocalAppColors provides colors) {
        MaterialTheme(colorScheme = colors, typography = AppTypography, content = content)
    }
}""",
                "metric": "Standardized 120+ design system tokens across 3 white-label enterprise client applications."
            },
            {
                "id": "q70",
                "title": "10. How do you implement Complex Gestures, Dragging, and Swipe-to-Dismiss?",
                "problem": "Handling drag, fling, and dismiss gestures using nested scroll listeners creates gesture conflicts and jank.",
                "solution": [
                    ("SWIPEABLE BOX COMPONENT", "I utilize SwipeToDismissBox with rememberSwipeToDismissBoxState() for list item dismissals."),
                    ("POINTER INPUT DETECT", "I use Modifier.pointerInput with detectDragGestures to capture raw 2D touch drag deltas."),
                    ("ANIMATABLE OFFSET", "I animate dragged UI offsets smoothly using Animatable(0f) with spring physics specs."),
                    ("CONSUME POSITION CHANGE", "I call change.consume() on pointer changes to prevent parent scroll container interception."),
                    ("ACCESSIBILITY ACTIONS", "I add custom accessibility semantics actions so screen readers can trigger dismissal.")
                ],
                "code": """val dismissState = rememberSwipeToDismissBoxState(
    confirmValueChange = { value ->
        if (value == SwipeToDismissBoxValue.EndToStart) {
            onDelete(item)
            true
        } else false
    }
)
SwipeToDismissBox(state = dismissState, backgroundContent = { DismissBackground(dismissState) }) {
    ItemCard(item)
}""",
                "metric": "Delivered smooth physics-based swipe actions matching 120Hz native touch response."
            },
            {
                "id": "q71",
                "title": "11. How do you test Jetpack Compose UI deterministically with ComposeTestRule?",
                "problem": "Testing dynamic animations, asynchronous state updates, and composables in espresso is flaky and slow.",
                "solution": [
                    ("CREATE COMPOSE RULE", "I instantiate createComposeRule() or createAndroidComposeRule<MainActivity>() in test suites."),
                    ("SEMANTICS NODE FINDERS", "I locate UI elements using onNodeWithText, onNodeWithTag, and onNodeWithContentDescription."),
                    ("ASSERTIONS AND ACTIONS", "I perform deterministic clicks with performClick() and verify with assertIsDisplayed()."),
                    ("AUTOMATIC CLOCK CONTROL", "ComposeTestRule pauses test clock automatically, synchronizing with async coroutines."),
                    ("ACCESSIBILITY TESTING", "I run AccessibilityChecks in Compose tests to catch missing semantics content descriptions.")
                ],
                "code": """@RunWith(AndroidJUnit4::class)
class LoginScreenTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun loginButtonDisabledWhenFieldsEmpty() {
        composeTestRule.setContent { LoginScreen(uiState = LoginUiState(canSubmit = false)) }
        composeTestRule.onNodeWithTag("submit_btn").assertIsNotEnabled()
    }
}""",
                "metric": "Increased UI test execution speed by 4x and eliminated 100% of timing flakiness in CI."
            },
            {
                "id": "q72",
                "title": "12. How do you embed Legacy Android Views inside Compose and Compose inside XML?",
                "problem": "Migrating large XML codebases requires bidirectional interop between legacy Views (e.g. MapView, Player) and Compose.",
                "solution": [
                    ("ANDROIDVIEW IN COMPOSE", "I use AndroidView(factory = { MapView(it) }, update = { it.render(state) }) for legacy views."),
                    ("COMPOSEVIEWTREE RELEASING", "I configure DisposeOnViewTreeLifecycleDestroyed strategy on ComposeView in XML."),
                    ("VIEW INTEROP LIFECYCLE", "I bridge Activity/Fragment lifecycle events to AndroidView instances explicitly."),
                    ("INCREMENTAL MIGRATION", "I replace individual XML RecyclerView item layouts with ComposeView progressively."),
                    ("SHARED VIEWMODELS", "Shared Hilt ViewModels provide identical reactive StateFlow streams to both XML and Compose.")
                ],
                "code": """// ComposeView in XML Fragment
binding.composeView.apply {
    setViewCompositionStrategy(ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed)
    setContent {
        AppTheme {
            ModernComposeFeatureScreen()
        }
    }
}""",
                "metric": "Successfully migrated 120+ legacy XML screens to Jetpack Compose incrementally with 0 downtime."
            }
        ]
    }
    
    return [m6]

print("Module 6 ready.")
