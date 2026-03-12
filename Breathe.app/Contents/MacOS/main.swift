import Cocoa
import WebKit

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    var webView: WKWebView!

    func applicationDidFinishLaunching(_ notification: Notification) {
        // Window size
        let screenFrame = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 800, height: 600)
        let windowWidth: CGFloat = 680
        let windowHeight: CGFloat = 720
        let windowX = screenFrame.midX - windowWidth / 2
        let windowY = screenFrame.midY - windowHeight / 2

        let windowRect = NSRect(x: windowX, y: windowY, width: windowWidth, height: windowHeight)

        window = NSWindow(
            contentRect: windowRect,
            styleMask: [.titled, .closable, .miniaturizable, .resizable, .fullSizeContentView],
            backing: .buffered,
            defer: false
        )

        window.title = "Breathe"
        window.titlebarAppearsTransparent = true
        window.titleVisibility = .hidden
        window.backgroundColor = NSColor(red: 0.04, green: 0.04, blue: 0.1, alpha: 1.0)
        window.isMovableByWindowBackground = true
        window.level = .floating  // Stay on top

        // WebView config — use persistent data store so localStorage survives app restarts
        let config = WKWebViewConfiguration()
        config.websiteDataStore = WKWebsiteDataStore.default()
        config.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")

        webView = WKWebView(frame: window.contentView!.bounds, configuration: config)
        webView.autoresizingMask = [.width, .height]
        webView.setValue(false, forKey: "drawsBackground")

        // Load the HTML from Resources
        let bundle = Bundle.main
        if let htmlPath = bundle.path(forResource: "breathe", ofType: "html") {
            let htmlURL = URL(fileURLWithPath: htmlPath)
            webView.loadFileURL(htmlURL, allowingReadAccessTo: htmlURL.deletingLastPathComponent())
        }

        window.contentView?.addSubview(webView)
        window.makeKeyAndOrderFront(nil)

        // Activate the app and bring to front
        NSApp.activate(ignoringOtherApps: true)
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()
